from __future__ import annotations

import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "config" / "security_legal_analytics_5stream.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip()).strip("._") or "document"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_domains(value: Any) -> set[str]:
    if isinstance(value, list):
        rows = [str(x) for x in value]
    else:
        rows = re.split(r"[,;]", str(value or ""))
    return {row.strip().upper() for row in rows if row.strip()}


def load_master_documents(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    plan = load_json(ROOT / profile["inputs"]["master_plan"])
    merged: dict[str, dict[str, Any]] = {}
    for source in plan.get("source_registries", []) or []:
        if not isinstance(source, dict):
            continue
        path = ROOT / str(source.get("path") or "")
        field = str(source.get("documents_field") or "documents")
        if not path.is_file():
            continue
        try:
            payload = load_json(path)
        except Exception:
            continue
        for row in payload.get(field, []) or []:
            if not isinstance(row, dict):
                continue
            did = str(row.get("document_id") or "").strip()
            if not did:
                continue
            merged[did] = {**merged.get(did, {}), **row, "registry_source": path.relative_to(ROOT).as_posix()}
    for row in plan.get("extra_documents", []) or []:
        if not isinstance(row, dict):
            continue
        did = str(row.get("document_id") or "").strip()
        if did:
            merged[did] = {**merged.get(did, {}), **row, "registry_source": profile["inputs"]["master_plan"]}
    return merged


def load_metadata(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    root = ROOT / profile["inputs"]["metadata_root"]
    rows: dict[str, dict[str, Any]] = {}
    if not root.is_dir():
        return rows
    for path in sorted(root.glob("*.json")):
        try:
            payload = load_json(path)
        except Exception:
            continue
        did = str(payload.get("document_id") or "").strip()
        if not did:
            continue
        payload = dict(payload)
        payload["metadata_file"] = path.relative_to(ROOT).as_posix()
        rows[did] = payload
    return rows


def resolve_normalized_path(document_id: str, meta: dict[str, Any], normalized_root: Path) -> Path | None:
    raw = str(meta.get("normalized_path") or "").strip()
    if raw:
        path = Path(raw)
        path = path if path.is_absolute() else ROOT / path
        if path.is_file():
            return path
    candidates = sorted(
        normalized_root.glob(f"{safe_name(document_id)}__*.txt"),
        key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
        reverse=True,
    )
    return candidates[0] if candidates else None


def build_corpus(profile: dict[str, Any]) -> list[dict[str, Any]]:
    master = load_master_documents(profile)
    metadata = load_metadata(profile)
    normalized_root = ROOT / profile["inputs"]["normalized_root"]
    all_ids = sorted(set(master) | set(metadata))
    rows: list[dict[str, Any]] = []
    known_detail_ids = set(profile["legal_gate"].get("known_detail_page_only_ids") or [])
    hold_statuses = set(profile["legal_gate"].get("hold_statuses") or [])

    for did in all_ids:
        registry = master.get(did, {})
        meta = metadata.get(did, {})
        normalized = resolve_normalized_path(did, meta, normalized_root)
        text = ""
        text_sha = None
        if normalized:
            try:
                text = normalized.read_text(encoding="utf-8", errors="replace")
                text_sha = sha256_text(text)
            except OSError:
                text = ""

        legal_status = str(meta.get("legal_status") or registry.get("legal_status") or "UNKNOWN").upper()
        source_url = str(meta.get("source_url") or meta.get("final_url") or registry.get("official_source_url") or "").strip() or None
        mime = str(meta.get("mime_type") or "").casefold()
        identity_confirmed = meta.get("document_identity_confirmed") is True
        currentness_verified = meta.get("currentness_verified") is True
        detail_page_risk = bool(
            did in known_detail_ids
            and source_url
            and "protect.gost.ru/gost/details/" in source_url
            and ("html" in mime or str(meta.get("normalization") or "").upper().startswith("HTML"))
        )
        gate_reasons: list[str] = []
        if legal_status != "CURRENT":
            gate_reasons.append(f"LEGAL_STATUS_{legal_status}")
        if legal_status in hold_statuses:
            gate_reasons.append("CURRENTNESS_HOLD_STATUS")
        if not identity_confirmed:
            gate_reasons.append("IDENTITY_NOT_CONFIRMED")
        if not currentness_verified:
            gate_reasons.append("CURRENTNESS_NOT_VERIFIED")
        if detail_page_risk:
            gate_reasons.append("GOST_DETAIL_PAGE_NOT_CONFIRMED_FULL_TEXT")
        if not text.strip():
            gate_reasons.append("NORMALIZED_TEXT_MISSING")

        rows.append(
            {
                "document_id": did,
                "title": meta.get("title") or registry.get("title"),
                "domain": meta.get("domain") or registry.get("domain"),
                "domains": sorted(split_domains(meta.get("domain") or registry.get("domain"))),
                "legal_status": legal_status,
                "importance_class": registry.get("importance_class"),
                "maturity_level": registry.get("maturity_level"),
                "source_url": source_url,
                "metadata_file": meta.get("metadata_file"),
                "normalized_path": normalized.relative_to(ROOT).as_posix() if normalized else None,
                "source_sha256": meta.get("sha256"),
                "normalized_sha256": text_sha,
                "text": text,
                "text_chars": len(text),
                "document_identity_confirmed": identity_confirmed,
                "currentness_verified": currentness_verified,
                "legal_truth_eligible": meta.get("legal_truth_eligible") is True,
                "detail_page_only_risk": detail_page_risk,
                "legal_promotion_gate": "PASS" if not gate_reasons else "HOLD",
                "legal_gate_reasons": sorted(set(gate_reasons)),
            }
        )
    return rows


def evidence_lines(doc: dict[str, Any], *, min_chars: int = 18) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(str(doc.get("text") or "").splitlines(), start=1):
        text = " ".join(raw.split())
        if len(text) < min_chars:
            continue
        rows.append(
            {
                "evidence_id": f"{doc['document_id']}#L{number}",
                "line": number,
                "text": text,
                "source_sha256": doc.get("source_sha256"),
                "normalized_sha256": doc.get("normalized_sha256"),
            }
        )
    return rows


def candidate(doc: dict[str, Any], ev: dict[str, Any], kind: str, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "candidate_type": kind,
        "document_id": doc["document_id"],
        "evidence_id": ev["evidence_id"],
        "exact_text": ev["text"],
        "source_sha256": doc.get("source_sha256"),
        "normalized_sha256": doc.get("normalized_sha256"),
        "legal_promotion_gate": doc.get("legal_promotion_gate"),
        "review_status": "MAIN_ANALYST_REVIEW_REQUIRED",
        "kb_auto_promotion": False,
    }
    if extra:
        payload.update(extra)
    return payload


def run_s1(docs: list[dict[str, Any]]) -> dict[str, Any]:
    started = time.perf_counter()
    records = []
    for doc in docs:
        records.append({k: v for k, v in doc.items() if k != "text"})
    return {
        "stream_id": "S1_IDENTITY_CURRENTNESS",
        "semantic": False,
        "records_total": len(records),
        "hold_total": sum(row.get("legal_promotion_gate") == "HOLD" for row in records),
        "text_available_total": sum(bool(row.get("normalized_path")) and int(row.get("text_chars") or 0) > 0 for row in records),
        "records": records,
        "elapsed_seconds": time.perf_counter() - started,
    }


def run_s2(docs: list[dict[str, Any]]) -> dict[str, Any]:
    started = time.perf_counter()
    patterns: list[tuple[str, re.Pattern[str]]] = [
        ("DEFINITION_CANDIDATE", re.compile(r"(?i)(понимается|означает|определяется как|следующие понятия|используются следующие термины|термин[ыа]?)")),
        ("SCOPE_CANDIDATE", re.compile(r"(?i)(настоящ(?:ий|ая|ее).*?(регулирует|устанавливает|определяет)|предмет регулирования|область применения)")),
        ("APPLICABILITY_CANDIDATE", re.compile(r"(?i)(распространяется на|не распространяется на|применяется к|не применяется к|в отношении|для целей настоящ)")),
    ]
    results: list[dict[str, Any]] = []
    per_doc = Counter()
    for doc in docs:
        if not str(doc.get("text") or "").strip():
            continue
        for ev in evidence_lines(doc):
            for kind, pattern in patterns:
                if pattern.search(ev["text"]):
                    results.append(candidate(doc, ev, kind, extra={"model_stage": "M5_TERMINOLOGY"}))
                    per_doc[doc["document_id"]] += 1
                    break
            if per_doc[doc["document_id"]] >= 250:
                break
    return {
        "stream_id": "S2_TERMS_SCOPE",
        "semantic": True,
        "candidate_objects_total": len(results),
        "candidates": results,
        "elapsed_seconds": time.perf_counter() - started,
    }


def requirement_kind(text: str) -> str | None:
    lowered = text.casefold()
    if re.search(r"\b(запрещается|не допускается|не вправе)\b", lowered):
        return "PROHIBITION_CANDIDATE"
    if re.search(r"\b(обязан|обязана|обязаны|должен|должна|должны|необходимо|требуется|подлежит)\b", lowered):
        return "OBLIGATION_CANDIDATE"
    if re.search(r"\b(вправе|может|могут|допускается)\b", lowered):
        return "PERMISSION_CANDIDATE"
    if re.search(r"\b(не позднее|в течение|срок|рабочих дней|календарных дней|до \d{1,2})\b", lowered):
        return "DEADLINE_CANDIDATE"
    return None


def run_s3(docs: list[dict[str, Any]]) -> dict[str, Any]:
    started = time.perf_counter()
    results: list[dict[str, Any]] = []
    kinds = Counter()
    per_doc = Counter()
    for doc in docs:
        if not str(doc.get("text") or "").strip():
            continue
        for ev in evidence_lines(doc):
            kind = requirement_kind(ev["text"])
            if not kind:
                continue
            row = candidate(doc, ev, kind, extra={"model_stage": "M6_KNOWLEDGE_EXTRACTION"})
            results.append(row)
            kinds[kind] += 1
            per_doc[doc["document_id"]] += 1
            if per_doc[doc["document_id"]] >= 600:
                break
    return {
        "stream_id": "S3_REQUIREMENTS_OBLIGATIONS",
        "semantic": True,
        "candidate_objects_total": len(results),
        "candidate_type_counts": dict(sorted(kinds.items())),
        "candidates": results,
        "elapsed_seconds": time.perf_counter() - started,
    }


def identity_tokens(doc: dict[str, Any]) -> set[str]:
    text = f"{doc.get('document_id','')} {doc.get('title','')}"
    tokens: set[str] = set()
    for pattern in (
        r"\b\d{1,4}-ФЗ\b",
        r"№\s*\d{1,5}\b",
        r"\bГОСТ\s+Р\s+\d{4,6}-\d{4}\b",
        r"\b\d{4,6}-\d{4}\b",
    ):
        tokens.update(match.group(0).casefold().replace(" ", "") for match in re.finditer(pattern, text, flags=re.IGNORECASE))
    return tokens


def run_s4(docs: list[dict[str, Any]]) -> dict[str, Any]:
    started = time.perf_counter()
    token_map: dict[str, set[str]] = {doc["document_id"]: identity_tokens(doc) for doc in docs}
    reference_candidates: list[dict[str, Any]] = []
    ref_pattern = re.compile(
        r"(?i)(?:федеральн\w*\s+закон\w*|постановлен\w*\s+правительств\w*|приказ\w*|ГОСТ(?:\s+Р)?)[^\n.;]{0,140}(?:№\s*\d{1,5}|\d{1,4}-ФЗ|\d{4,6}-\d{4})"
    )
    for doc in docs:
        if not str(doc.get("text") or "").strip():
            continue
        per_doc = 0
        for ev in evidence_lines(doc):
            match = ref_pattern.search(ev["text"])
            if not match:
                continue
            ref_text = match.group(0)
            compact = ref_text.casefold().replace(" ", "")
            targets = []
            for target_id, tokens in token_map.items():
                if target_id == doc["document_id"]:
                    continue
                if any(token and token in compact for token in tokens):
                    targets.append(target_id)
            reference_candidates.append(
                candidate(
                    doc,
                    ev,
                    "REFERENCE_CANDIDATE",
                    extra={
                        "reference_text": ref_text,
                        "target_document_ids": sorted(set(targets)),
                        "model_stage": "M7_RELATION_DISCOVERY",
                    },
                )
            )
            per_doc += 1
            if per_doc >= 250:
                break

    review_pairs: list[dict[str, Any]] = []
    text_docs = [doc for doc in docs if str(doc.get("text") or "").strip()]
    for i, left in enumerate(text_docs):
        left_domains = set(left.get("domains") or [])
        if not left_domains:
            continue
        for right in text_docs[i + 1 :]:
            shared = sorted(left_domains & set(right.get("domains") or []))
            if not shared:
                continue
            review_pairs.append(
                {
                    "candidate_type": "CONTRADICTION_REVIEW_PAIR",
                    "document_a": left["document_id"],
                    "document_b": right["document_id"],
                    "shared_domains": shared,
                    "verdict": "NOT_ASSERTED",
                    "required_model_stage": "M8_CONTRADICTION_VERIFICATION",
                    "review_status": "MODEL_OR_MAIN_ANALYST_REVIEW_REQUIRED",
                    "kb_auto_promotion": False,
                }
            )
            if len(review_pairs) >= 1000:
                break
        if len(review_pairs) >= 1000:
            break
    return {
        "stream_id": "S4_RELATIONS_CONTRADICTIONS",
        "semantic": True,
        "reference_candidates_total": len(reference_candidates),
        "cross_document_pairs_total": len(review_pairs),
        "reference_candidates": reference_candidates,
        "contradiction_review_pairs": review_pairs,
        "elapsed_seconds": time.perf_counter() - started,
    }


def control_family(text: str) -> list[str]:
    low = text.casefold()
    mapping = {
        "ACCESS_CONTROL": ("доступ", "идентификац", "аутентификац", "учетн"),
        "LOGGING_MONITORING": ("журнал", "регистрац", "мониторинг", "событи"),
        "INCIDENT_RESPONSE": ("инцидент", "компьютерн атак", "госсопка"),
        "CRYPTOGRAPHY": ("криптограф", "шифрован", "скзи"),
        "VULNERABILITY_MANAGEMENT": ("уязвим", "обновлен", "устранен"),
        "BACKUP_RECOVERY": ("резервн", "восстановлен"),
        "SECURE_DEVELOPMENT": ("разработк", "исходн код", "статическ анализ", "тестирован"),
        "DATA_PROTECTION": ("персональн данн", "защит информации", "конфиденциаль"),
    }
    return [family for family, needles in mapping.items() if any(needle in low for needle in needles)]


def run_s5(docs: list[dict[str, Any]]) -> dict[str, Any]:
    started = time.perf_counter()
    mappings: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []
    for doc in docs:
        mapped = 0
        for ev in evidence_lines(doc):
            kind = requirement_kind(ev["text"])
            if not kind:
                continue
            families = control_family(ev["text"])
            if not families:
                continue
            mappings.append(
                candidate(
                    doc,
                    ev,
                    "CONTROL_MAPPING_CANDIDATE",
                    extra={"control_families": families, "source_requirement_kind": kind, "model_stage": "M9_PROFESSOR_SYNTHESIS"},
                )
            )
            mapped += 1
            if mapped >= 300:
                break
        queue.append(
            {
                "work_item_id": f"LEGAL-{doc['document_id']}",
                "document_id": doc["document_id"],
                "title": doc.get("title"),
                "domains": doc.get("domains") or [],
                "legal_status": doc.get("legal_status"),
                "legal_promotion_gate": doc.get("legal_promotion_gate"),
                "legal_gate_reasons": doc.get("legal_gate_reasons") or [],
                "normalized_path": doc.get("normalized_path"),
                "source_sha256": doc.get("source_sha256"),
                "priority": "P0" if doc.get("importance_class") == "NECESSARY" else "P1" if doc.get("importance_class") == "DESIRABLE" else "P2",
                "required_stages": ["M5_TERMINOLOGY", "M6_KNOWLEDGE_EXTRACTION", "M7_RELATION_DISCOVERY", "M8_CONTRADICTION_VERIFICATION", "M9_PROFESSOR_SYNTHESIS", "M10_INDEPENDENT_JUDGE"],
                "state": "READY_FOR_ANALYSIS" if doc.get("normalized_path") else "HOLD_NO_TEXT",
                "promotion_state": "BLOCKED_PENDING_LEGAL_GATE" if doc.get("legal_promotion_gate") != "PASS" else "REVIEW_REQUIRED",
                "kb_auto_promotion": False,
            }
        )
    queue.sort(key=lambda row: (row["priority"], row["document_id"]))
    return {
        "stream_id": "S5_APPLICABILITY_CONTROL_MAPPING",
        "semantic": True,
        "control_mapping_candidates_total": len(mappings),
        "main_analyst_queue_total": len(queue),
        "control_mapping_candidates": mappings,
        "main_analyst_queue": queue,
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> int:
    started = time.perf_counter()
    profile = load_json(PROFILE_PATH)
    docs = build_corpus(profile)
    out_root = ROOT / profile["outputs"]["root"]
    out_root.mkdir(parents=True, exist_ok=True)

    streams: list[tuple[str, Callable[[list[dict[str, Any]]], dict[str, Any]]]] = [
        ("S1_IDENTITY_CURRENTNESS", run_s1),
        ("S2_TERMS_SCOPE", run_s2),
        ("S3_REQUIREMENTS_OBLIGATIONS", run_s3),
        ("S4_RELATIONS_CONTRADICTIONS", run_s4),
        ("S5_APPLICABILITY_CONTROL_MAPPING", run_s5),
    ]
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=5, thread_name_prefix="legal-analytics") as executor:
        futures = {executor.submit(func, docs): stream_id for stream_id, func in streams}
        for future in as_completed(futures):
            stream_id = futures[future]
            try:
                payload = future.result()
                payload["status"] = "PASS"
            except Exception as exc:
                payload = {
                    "stream_id": stream_id,
                    "status": "FAILED",
                    "error": f"{type(exc).__name__}: {exc}",
                    "elapsed_seconds": None,
                }
            results[stream_id] = payload
            path = out_root / f"{stream_id}.json"
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"[{payload['status']}] {stream_id}")

    s1 = results.get("S1_IDENTITY_CURRENTNESS", {})
    s2 = results.get("S2_TERMS_SCOPE", {})
    s3 = results.get("S3_REQUIREMENTS_OBLIGATIONS", {})
    s4 = results.get("S4_RELATIONS_CONTRADICTIONS", {})
    s5 = results.get("S5_APPLICABILITY_CONTROL_MAPPING", {})
    analyst_queue = list(s5.get("main_analyst_queue") or [])
    queue_path = ROOT / profile["outputs"]["main_analyst_queue"]
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(
        json.dumps(
            {
                "record_type": "SECURITY_LEGAL_MAIN_ANALYST_QUEUE",
                "schema_version": "1.0",
                "state": "MAIN_ANALYST_REVIEW_REQUIRED",
                "items_total": len(analyst_queue),
                "items": analyst_queue,
                "kb_auto_promotion": False,
                "observed_at": utc_now(),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    total_candidates = (
        int(s2.get("candidate_objects_total") or 0)
        + int(s3.get("candidate_objects_total") or 0)
        + int(s4.get("reference_candidates_total") or 0)
        + int(s5.get("control_mapping_candidates_total") or 0)
    )
    failed_streams = [stream_id for stream_id, payload in results.items() if payload.get("status") != "PASS"]
    summary = {
        "record_type": "SECURITY_LEGAL_ANALYTICS_5STREAM_RUN",
        "schema_version": "1.0",
        "status": "PASS" if not failed_streams else "PASS_WITH_GAPS" if len(failed_streams) < 5 else "FAILED",
        "mode": "EXISTING_CORPUS_ONLY",
        "workers": 5,
        "network_acquisition": False,
        "documents_seen_total": len(docs),
        "documents_with_text_total": sum(bool(doc.get("normalized_path")) and int(doc.get("text_chars") or 0) > 0 for doc in docs),
        "documents_hold_total": int(s1.get("hold_total") or 0),
        "candidate_objects_total": total_candidates,
        "requirements_candidates_total": int(s3.get("candidate_objects_total") or 0),
        "cross_document_pairs_total": int(s4.get("cross_document_pairs_total") or 0),
        "main_analyst_queue_total": len(analyst_queue),
        "failed_streams": failed_streams,
        "stream_elapsed_seconds": {stream_id: payload.get("elapsed_seconds") for stream_id, payload in sorted(results.items())},
        "elapsed_seconds": time.perf_counter() - started,
        "speedup_vs_1_stream_pct": None,
        "speedup_note": "No 1-stream speedup is claimed until the same corpus and analysis contract are measured serially on the same workstation.",
        "rework_rate": None,
        "rework_note": "Rework telemetry is not available on the first analytics run.",
        "contradiction_policy": "REVIEW_PAIRS_ONLY_NO_CONFLICT_ASSERTION_WITHOUT_M8",
        "legal_truth_policy": "MODEL_AND_HEURISTIC_OUTPUTS_ARE_CANDIDATES_ONLY",
        "kb_auto_promotion": False,
        "profile": PROFILE_PATH.relative_to(ROOT).as_posix(),
        "main_analyst_queue": queue_path.relative_to(ROOT).as_posix(),
        "observed_at": utc_now(),
    }
    aggregate = ROOT / profile["outputs"]["aggregate"]
    aggregate.parent.mkdir(parents=True, exist_ok=True)
    aggregate.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] in {"PASS", "PASS_WITH_GAPS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
