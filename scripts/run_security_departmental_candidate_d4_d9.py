from __future__ import annotations

import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.document_compiler import PARSER_VERSION, build_chunks, parse_legal_structure
from father_osint.knowledge_extraction import EXTRACTOR_VERSION, extract_candidates
from father_osint.knowledge_factory import DocumentVersion

INPUT_REPORT = REPO_ROOT / "reports" / "security_current_only" / "LATEST_DEPARTMENTAL_5STREAM_RUN.json"
OUT_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "security_departmental_candidate"
REPORT = REPO_ROOT / "reports" / "security_current_only" / "LATEST_DEPARTMENTAL_D4_D9_CANDIDATE.json"
WORKERS = 5
MAX_CHUNK_CHARS = 2400

CONTENT_BLOCK_MARKERS = (
    "документ в некоммерческой версии консультантплюс доступен по расписанию",
    "этот документ в некоммерческой версии консультантплюс доступен по расписанию",
    "тексты документов всегда доступны в коммерческой версии консультантплюс",
    "вы можете заказать документ на e-mail",
    "откройте документ в системе консультантплюс",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _dedupe(rows: list[dict[str, object]], key: str) -> list[dict[str, object]]:
    seen: set[str] = set()
    out: list[dict[str, object]] = []
    for row in rows:
        value = str(row.get(key) or "")
        if value and value not in seen:
            seen.add(value)
            out.append(row)
    return out


def _content_quality(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    folded = stripped.casefold().replace("ё", "е")
    if any(marker in folded for marker in CONTENT_BLOCK_MARKERS):
        return False, "REFERENCE_ACCESS_WINDOW_BLOCKED"
    if len(stripped) < 600:
        return False, "TEXT_TOO_SHORT_FOR_LEGAL_BODY"
    legal_anchor = any(marker in folded for marker in ("приказ", "постановление", "федеральный закон", "распоряжение"))
    operative_anchor = any(marker in folded for marker in ("приказываю", "постановляет", "утвердить", "определить", "в соответствии", "настоящ"))
    if not (legal_anchor and operative_anchor):
        return False, "LEGAL_BODY_MARKERS_NOT_CONFIRMED"
    return True, "PASS"


def _blocked_result(row: dict[str, object], document_id: str, reason: str, text_bytes: bytes, started: float) -> dict[str, object]:
    return {
        "schema_version": "1.1",
        "record_type": "SECURITY_DEPARTMENTAL_SHADOW_D4_D9",
        "document_id": document_id,
        "title": row.get("title"),
        "source_sha256": row.get("sha256"),
        "normalized_sha256": _sha_bytes(text_bytes),
        "source_url": row.get("source_url"),
        "source_status": row.get("status"),
        "trust_tier": row.get("trust_tier"),
        "queue_legal_status": row.get("queue_legal_status", "VERIFY_CURRENTNESS"),
        "status": "CONTENT_INSUFFICIENT",
        "content_quality_pass": False,
        "content_quality_reason": reason,
        "reacquisition_required": True,
        "stage_scope": "SHADOW_CANDIDATE_D4_D9_ONLY",
        "official_pipeline_advanced": False,
        "exact_official_evidence_acquired": bool(row.get("exact_official_evidence_acquired")),
        "currentness_verified": False,
        "legal_truth_eligible": False,
        "kb_promotion_allowed": False,
        "review_state": "BLOCKED_NEEDS_FULL_TEXT",
        "structure_nodes": 0,
        "chunks": 0,
        "terms": 0,
        "definitions": 0,
        "requirements": 0,
        "entities": 0,
        "seconds": time.perf_counter() - started,
    }


def _process(row: dict[str, object]) -> dict[str, object]:
    started = time.perf_counter()
    document_id = str(row.get("document_id") or "").strip()
    normalized_path_raw = str(row.get("normalized_path") or "").strip()
    if not document_id or not normalized_path_raw:
        return {
            "document_id": document_id or None,
            "status": "INPUT_NOT_NORMALIZED",
            "error": "document_id and normalized_path are required",
            "seconds": time.perf_counter() - started,
        }

    normalized_path = REPO_ROOT / normalized_path_raw
    if not normalized_path.is_file():
        return {
            "document_id": document_id,
            "status": "INPUT_FILE_MISSING",
            "normalized_path": normalized_path_raw,
            "seconds": time.perf_counter() - started,
        }

    text_bytes = normalized_path.read_bytes()
    text = text_bytes.decode("utf-8")
    normalized_sha256 = _sha_bytes(text_bytes)
    source_sha256 = str(row.get("sha256") or "").strip().lower()
    if len(source_sha256) != 64:
        return {
            "document_id": document_id,
            "status": "INPUT_SHA256_INVALID",
            "seconds": time.perf_counter() - started,
        }

    content_quality_pass, content_quality_reason = _content_quality(text)
    if not content_quality_pass:
        return _blocked_result(row, document_id, content_quality_reason, text_bytes, started)

    version_id = f"CAND-{source_sha256[:24]}"
    version = DocumentVersion(
        source_id=str(row.get("trust_tier") or "A2_REFERENCE_WORKING_COPY"),
        source_url=str(row.get("source_url") or "candidate://local-working-copy"),
        sha256=source_sha256,
        local_path=normalized_path_raw,
        file_name=normalized_path.name,
        mime_type="text/plain",
        file_size=len(text_bytes),
        version_id=version_id,
    )

    nodes, warnings = parse_legal_structure(document_id, version_id, text)
    chunks = build_chunks(document_id, version, nodes, max_chunk_chars=MAX_CHUNK_CHARS)

    doc_root = OUT_ROOT / document_id / version_id
    structure_path = doc_root / "structure.jsonl"
    chunks_path = doc_root / "chunks.jsonl"
    extracted_path = doc_root / "extracted.txt"
    extracted_path.parent.mkdir(parents=True, exist_ok=True)
    extracted_path.write_text(text, encoding="utf-8", newline="\n")
    _write_jsonl(structure_path, [node.to_dict() for node in nodes])
    _write_jsonl(chunks_path, [chunk.to_dict() for chunk in chunks])

    terms: list[dict[str, object]] = []
    definitions: list[dict[str, object]] = []
    requirements: list[dict[str, object]] = []
    entities: list[dict[str, object]] = []
    for chunk in chunks:
        t, d, r, e = extract_candidates(chunk.to_dict())
        terms.extend(item.to_dict() for item in t)
        definitions.extend(item.to_dict() for item in d)
        requirements.extend(item.to_dict() for item in r)
        entities.extend(item.to_dict() for item in e)

    terms = _dedupe(terms, "term_id")
    definitions = _dedupe(definitions, "definition_id")
    requirements = _dedupe(requirements, "requirement_id")
    entities = _dedupe(entities, "entity_mention_id")

    knowledge_root = doc_root / "knowledge"
    _write_jsonl(knowledge_root / "terms.jsonl", terms)
    _write_jsonl(knowledge_root / "definitions.jsonl", definitions)
    _write_jsonl(knowledge_root / "requirements.jsonl", requirements)
    _write_jsonl(knowledge_root / "entities.jsonl", entities)

    exact_official = bool(row.get("exact_official_evidence_acquired"))
    manifest = {
        "schema_version": "1.1",
        "record_type": "SECURITY_DEPARTMENTAL_SHADOW_D4_D9",
        "document_id": document_id,
        "title": row.get("title"),
        "version_id": version_id,
        "source_sha256": source_sha256,
        "normalized_sha256": normalized_sha256,
        "source_url": row.get("source_url"),
        "source_status": row.get("status"),
        "trust_tier": row.get("trust_tier"),
        "queue_legal_status": row.get("queue_legal_status", "VERIFY_CURRENTNESS"),
        "parser_version": PARSER_VERSION,
        "extractor_version": EXTRACTOR_VERSION,
        "content_quality_pass": True,
        "content_quality_reason": "PASS",
        "structure_nodes": len(nodes),
        "chunks": len(chunks),
        "terms": len(terms),
        "definitions": len(definitions),
        "requirements": len(requirements),
        "entities": len(entities),
        "warnings": warnings,
        "stage_scope": "SHADOW_CANDIDATE_D4_D9_ONLY",
        "official_pipeline_advanced": False,
        "exact_official_evidence_acquired": exact_official,
        "currentness_verified": False,
        "legal_truth_eligible": False,
        "kb_promotion_allowed": False,
        "review_state": "CANDIDATE_NEEDS_REVIEW",
    }
    manifest_path = doc_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        **manifest,
        "status": "READY_D9_SHADOW_CANDIDATE",
        "manifest_path": manifest_path.relative_to(REPO_ROOT).as_posix(),
        "structure_path": structure_path.relative_to(REPO_ROOT).as_posix(),
        "chunks_path": chunks_path.relative_to(REPO_ROOT).as_posix(),
        "seconds": time.perf_counter() - started,
    }


def main() -> int:
    if not INPUT_REPORT.is_file():
        print("INPUT_REPORT_MISSING")
        return 2

    payload = json.loads(INPUT_REPORT.read_text(encoding="utf-8"))
    source_rows = [row for row in payload.get("results", []) if isinstance(row, dict)]
    targets = [
        row for row in source_rows
        if str(row.get("status") or "") in {"WORKING_COPY_NORMALIZED", "NORMALIZED", "WORKING_COPY_CONTENT_BLOCKED"}
        and str(row.get("normalized_path") or "").strip()
    ]

    started = time.perf_counter()
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="dept-d4-d9") as executor:
        futures = {executor.submit(_process, row): row for row in targets}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"[{result.get('status')}] {result.get('document_id')} "
                f"chunks={result.get('chunks', 0)} requirements={result.get('requirements', 0)}"
            )

    results.sort(key=lambda item: str(item.get("document_id") or ""))
    total_seconds = time.perf_counter() - started
    ready = sum(item.get("status") == "READY_D9_SHADOW_CANDIDATE" for item in results)
    content_insufficient = sum(item.get("status") == "CONTENT_INSUFFICIENT" for item in results)
    failed = len(results) - ready - content_insufficient

    summary = {
        "record_type": "SECURITY_DEPARTMENTAL_D4_D9_CANDIDATE_SUMMARY",
        "schema_version": "1.1",
        "observed_at": _utc_now(),
        "workers": WORKERS,
        "input_report": INPUT_REPORT.relative_to(REPO_ROOT).as_posix(),
        "input_results_total": len(source_rows),
        "targets_total": len(targets),
        "ready_d9_shadow_candidates": ready,
        "content_insufficient_total": content_insufficient,
        "failed_total": failed,
        "structure_nodes": sum(int(item.get("structure_nodes") or 0) for item in results),
        "chunks": sum(int(item.get("chunks") or 0) for item in results),
        "terms": sum(int(item.get("terms") or 0) for item in results),
        "definitions": sum(int(item.get("definitions") or 0) for item in results),
        "requirements": sum(int(item.get("requirements") or 0) for item in results),
        "entities": sum(int(item.get("entities") or 0) for item in results),
        "official_pipeline_advanced": False,
        "currentness_verified": False,
        "legal_truth_promoted": False,
        "kb_promotion_allowed": False,
        "review_required": True,
        "total_seconds": total_seconds,
        "results": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if failed == 0 and content_insufficient == 0 and ready == len(targets) else 1


if __name__ == "__main__":
    raise SystemExit(main())
