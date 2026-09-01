from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.knowledge_extraction import EXTRACTOR_VERSION, extract_candidates
from father_osint.knowledge_factory import AuditEvent, DocumentRecord, DocumentVersion, PipelineStage, Role, StageState
from father_osint.knowledge_factory_store import KnowledgeFactoryStore

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REVIEW = STORE_ROOT / "review" / "batch_review_manifest.json"
QUALITY = REPO_ROOT / "reports" / "pdn_live" / "D4_D5_STRUCTURE_QUALITY.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_EXTRACTION_SUMMARY.json"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _document(payload: dict[str, object]) -> DocumentRecord:
    return DocumentRecord(
        title=str(payload["title"]),
        document_type=str(payload["document_type"]),
        workspace_id=str(payload.get("workspace_id", "default")),
        owner=str(payload.get("owner", "system")),
        jurisdiction=payload.get("jurisdiction"),
        language=str(payload.get("language", "ru")),
        topic_tags=list(payload.get("topic_tags", [])),
        versions=[DocumentVersion(**item) for item in payload.get("versions", [])],
        current_version_id=payload.get("current_version_id"),
        stage_states=dict(payload.get("stage_states", {})),
        document_id=str(payload["document_id"]),
        created_at=str(payload["created_at"]),
        updated_at=str(payload["updated_at"]),
    )


def _dedupe(rows: list[dict[str, object]], key: str) -> list[dict[str, object]]:
    seen: set[str] = set()
    out: list[dict[str, object]] = []
    for row in rows:
        value = str(row[key])
        if value not in seen:
            seen.add(value)
            out.append(row)
    return out


def main() -> int:
    if not QUALITY.is_file():
        print("QUALITY_GATE_MISSING")
        return 2
    quality = json.loads(QUALITY.read_text(encoding="utf-8"))
    if quality.get("summary", {}).get("promotion_to_d6_allowed") is not True:
        print("D6_BLOCKED_BY_D4_D5_QUALITY_GATE")
        return 2
    if not REVIEW.is_file():
        print("REVIEW_MISSING")
        return 2

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    by_id = {str(item.get("document_id")): item for item in review.get("documents", [])}
    if any(document_id not in by_id for document_id in TARGETS):
        print("D6_D9_INPUT_INCOMPLETE")
        return 2

    store = KnowledgeFactoryStore(STORE_ROOT)
    quality_sha = _sha(QUALITY)
    results: list[dict[str, object]] = []

    for document_id in TARGETS:
        item = by_id[document_id]
        if item.get("status") != "READY_D5":
            print(f"INPUT_NOT_READY_D5: {document_id}")
            return 2
        chunks_path = STORE_ROOT / str(item["chunks_path"])
        version_id = str(item["version_id"])
        artifact_sha = str(item["artifact_sha256"])
        chunks = _read_jsonl(chunks_path)

        terms: list[dict[str, object]] = []
        definitions: list[dict[str, object]] = []
        requirements: list[dict[str, object]] = []
        entities: list[dict[str, object]] = []
        for chunk in chunks:
            if str(chunk.get("artifact_sha256")) != artifact_sha:
                raise RuntimeError(f"artifact lineage mismatch: {document_id}")
            t, d, r, e = extract_candidates(chunk)
            terms.extend(value.to_dict() for value in t)
            definitions.extend(value.to_dict() for value in d)
            requirements.extend(value.to_dict() for value in r)
            entities.extend(value.to_dict() for value in e)

        terms = _dedupe(terms, "term_id")
        definitions = _dedupe(definitions, "definition_id")
        requirements = _dedupe(requirements, "requirement_id")
        entities = _dedupe(entities, "entity_mention_id")

        out = STORE_ROOT / "knowledge" / document_id / version_id
        paths = {
            "terms": out / "terms.jsonl",
            "definitions": out / "definitions.jsonl",
            "requirements": out / "requirements.jsonl",
            "entities": out / "entities.jsonl",
        }
        _write_jsonl(paths["terms"], terms)
        _write_jsonl(paths["definitions"], definitions)
        _write_jsonl(paths["requirements"], requirements)
        _write_jsonl(paths["entities"], entities)

        manifest = {
            "schema_version": "1.0",
            "document_id": document_id,
            "version_id": version_id,
            "artifact_sha256": artifact_sha,
            "chunks_sha256": _sha(chunks_path),
            "quality_gate_sha256": quality_sha,
            "extractor_version": EXTRACTOR_VERSION,
            "terms": len(terms),
            "definitions": len(definitions),
            "requirements": len(requirements),
            "entities": len(entities),
            "all_objects_review_state": "CANDIDATE_NEEDS_REVIEW",
            "autonomous_kb_promotion": False,
        }
        manifest_path = out / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        payload = store.get_document(document_id)
        if not payload:
            raise RuntimeError(f"document registry missing: {document_id}")
        doc = _document(payload)
        for stage in (
            PipelineStage.D6_TERMS_EXTRACTED,
            PipelineStage.D7_DEFINITIONS_EXTRACTED,
            PipelineStage.D8_REQUIREMENTS_EXTRACTED,
            PipelineStage.D9_ENTITIES_EXTRACTED,
        ):
            doc.set_stage_state(stage, StageState.DONE)
        store.save_document(doc)
        store.append_audit(AuditEvent(
            actor_id="pdn-d6-d9-deterministic",
            actor_role=Role.KNOWLEDGE_CURATOR.value,
            action="EXTRACT_KNOWLEDGE_D6_D9",
            object_type="DOCUMENT",
            object_id=document_id,
            result="SUCCESS",
            metadata={**manifest, "manifest_path": manifest_path.relative_to(STORE_ROOT).as_posix()},
        ))

        results.append({
            "document_id": document_id,
            "status": "READY_D9_CANDIDATES",
            "version_id": version_id,
            "chunks": len(chunks),
            "terms": len(terms),
            "definitions": len(definitions),
            "requirements": len(requirements),
            "entities": len(entities),
            "review_state": "CANDIDATE_NEEDS_REVIEW",
            "autonomous_kb_promotion": False,
        })

    summary = {
        "record_type": "D6_D9_EXTRACTION_SUMMARY",
        "targets": len(TARGETS),
        "ready_d9_candidates": len(results),
        "terms": sum(int(item["terms"]) for item in results),
        "definitions": sum(int(item["definitions"]) for item in results),
        "requirements": sum(int(item["requirements"]) for item in results),
        "entities": sum(int(item["entities"]) for item in results),
        "extractor_version": EXTRACTOR_VERSION,
        "quality_gate_sha256": quality_sha,
        "review_required_before_promotion": True,
        "autonomous_kb_promotion": False,
    }
    output = {"summary": summary, "documents": results}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
