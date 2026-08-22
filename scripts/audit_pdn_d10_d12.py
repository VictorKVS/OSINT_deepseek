from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REL_ROOT = STORE_ROOT / "relations"
SUMMARY = REPO_ROOT / "reports" / "pdn_live" / "D10_D12_SUMMARY.json"
D6_SUMMARY = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_EXTRACTION_SUMMARY.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D10_D12_QUALITY.json"
TARGETS = {
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
}


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    required = {
        "summary": SUMMARY,
        "d6_summary": D6_SUMMARY,
        "internal": REL_ROOT / "internal.jsonl",
        "cross": REL_ROOT / "cross_document.jsonl",
        "conflicts": REL_ROOT / "conflicts_overlaps.jsonl",
        "manifest": REL_ROOT / "manifest.json",
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    if missing:
        print("D10_D12_QUALITY_INPUT_MISSING: " + ", ".join(missing))
        return 2

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    manifest = json.loads(required["manifest"].read_text(encoding="utf-8"))
    d6 = json.loads(D6_SUMMARY.read_text(encoding="utf-8"))
    internal = _read_jsonl(required["internal"])
    cross = _read_jsonl(required["cross"])
    conflicts = _read_jsonl(required["conflicts"])

    failures: list[str] = []
    if summary.get("autonomous_kb_promotion") is not False or manifest.get("autonomous_kb_promotion") is not False:
        failures.append("AUTONOMOUS_PROMOTION_NOT_BLOCKED")
    if int(summary.get("confirmed_conflicts", -1)) != 0:
        failures.append("CONFIRMED_CONFLICTS_MUST_BE_ZERO_AT_CANDIDATE_STAGE")

    relation_ids = [str(row.get("relation_id", "")) for row in internal + cross]
    duplicate_relation_ids = sum(count - 1 for count in Counter(relation_ids).values() if count > 1)
    candidate_ids = [str(row.get("candidate_id", "")) for row in conflicts]
    duplicate_candidate_ids = sum(count - 1 for count in Counter(candidate_ids).values() if count > 1)
    if duplicate_relation_ids:
        failures.append("DUPLICATE_RELATION_IDS")
    if duplicate_candidate_ids:
        failures.append("DUPLICATE_CONFLICT_CANDIDATE_IDS")

    d6_docs = {str(item.get("document_id")): item for item in d6.get("documents", [])}
    if set(d6_docs) != TARGETS:
        failures.append("D6_DOCUMENT_SET_MISMATCH")

    known_definition_ids: set[str] = set()
    known_requirement_ids: set[str] = set()
    known_entity_ids: set[str] = set()
    for document_id, item in d6_docs.items():
        version_id = str(item.get("version_id", ""))
        base = STORE_ROOT / "knowledge" / document_id / version_id
        for row in _read_jsonl(base / "definitions.jsonl"):
            known_definition_ids.add(str(row["definition_id"]))
        for row in _read_jsonl(base / "requirements.jsonl"):
            known_requirement_ids.add(str(row["requirement_id"]))
        for row in _read_jsonl(base / "entities.jsonl"):
            known_entity_ids.add(str(row["entity_mention_id"]))

    broken_internal_refs = 0
    invalid_review_states = 0
    for row in internal:
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED":
            invalid_review_states += 1
        if row.get("relation_type") == "TERM_DEFINED_BY":
            if str(row.get("to_definition_id")) not in known_definition_ids:
                broken_internal_refs += 1
        elif row.get("relation_type") == "REQUIREMENT_MENTIONS_ENTITY":
            if str(row.get("from_requirement_id")) not in known_requirement_ids:
                broken_internal_refs += 1
            if str(row.get("to_entity_mention_id")) not in known_entity_ids:
                broken_internal_refs += 1
        else:
            broken_internal_refs += 1
    if broken_internal_refs:
        failures.append("BROKEN_INTERNAL_RELATION_REFERENCE")

    invalid_cross = 0
    for row in cross:
        docs = set(str(value) for value in row.get("document_ids", []))
        if len(docs) < 2 or not docs.issubset(TARGETS):
            invalid_cross += 1
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED":
            invalid_review_states += 1
    if invalid_cross:
        failures.append("INVALID_CROSS_DOCUMENT_RELATION")

    confirmed_conflict_candidates = 0
    for row in conflicts:
        if row.get("confirmed_conflict") is not False:
            confirmed_conflict_candidates += 1
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED":
            invalid_review_states += 1
    if confirmed_conflict_candidates:
        failures.append("CONFLICT_CANDIDATE_PREMATURELY_CONFIRMED")
    if invalid_review_states:
        failures.append("REVIEW_OR_PROMOTION_STATE_INVALID")

    payload = {
        "summary": {
            "record_type": "D10_D12_QUALITY",
            "quality_pass": not failures,
            "promotion_to_d13_allowed": not failures,
            "internal_relations": len(internal),
            "cross_document_relations": len(cross),
            "conflict_overlap_candidates": len(conflicts),
            "duplicate_relation_ids": duplicate_relation_ids,
            "duplicate_conflict_candidate_ids": duplicate_candidate_ids,
            "broken_internal_refs": broken_internal_refs,
            "invalid_cross_relations": invalid_cross,
            "premature_confirmed_conflicts": confirmed_conflict_candidates,
            "invalid_review_states": invalid_review_states,
            "failures": failures,
            "autonomous_kb_promotion": False,
        }
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
