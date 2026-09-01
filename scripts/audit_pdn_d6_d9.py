from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
SUMMARY = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_EXTRACTION_SUMMARY.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_QUALITY.json"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    if not SUMMARY.is_file():
        print("D6_D9_SUMMARY_MISSING")
        return 2
    summary_payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    by_id = {str(item.get("document_id")): item for item in summary_payload.get("documents", [])}
    if any(document_id not in by_id for document_id in TARGETS):
        print("D6_D9_QUALITY_INPUT_INCOMPLETE")
        return 2

    results: list[dict[str, object]] = []
    hard_failures = 0
    for document_id in TARGETS:
        item = by_id[document_id]
        version_id = str(item.get("version_id", ""))
        base = STORE_ROOT / "knowledge" / document_id / version_id
        paths = {
            "terms": base / "terms.jsonl",
            "definitions": base / "definitions.jsonl",
            "requirements": base / "requirements.jsonl",
            "entities": base / "entities.jsonl",
            "manifest": base / "manifest.json",
        }
        missing = [name for name, path in paths.items() if not path.is_file()]
        if missing:
            results.append({"document_id": document_id, "status": "QUALITY_INPUT_MISSING", "missing": missing})
            hard_failures += 1
            continue

        terms = _read_jsonl(paths["terms"])
        definitions = _read_jsonl(paths["definitions"])
        requirements = _read_jsonl(paths["requirements"])
        entities = _read_jsonl(paths["entities"])
        manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
        failures: list[str] = []

        if manifest.get("autonomous_kb_promotion") is not False:
            failures.append("AUTONOMOUS_PROMOTION_NOT_BLOCKED")
        if manifest.get("all_objects_review_state") != "CANDIDATE_NEEDS_REVIEW":
            failures.append("REVIEW_STATE_INVALID")
        if not terms:
            failures.append("ZERO_TERMS")
        if not entities:
            failures.append("ZERO_ENTITIES")
        if not requirements:
            failures.append("ZERO_REQUIREMENTS")
        if document_id == "DOC-RU-FZ-152-2006" and not definitions:
            failures.append("ZERO_EXPLICIT_DEFINITIONS_IN_152")

        collections = (
            (terms, "term_id"),
            (definitions, "definition_id"),
            (requirements, "requirement_id"),
            (entities, "entity_mention_id"),
        )
        duplicate_ids = 0
        lineage_failures = 0
        promotion_failures = 0
        for rows, id_key in collections:
            ids = [str(row.get(id_key, "")) for row in rows]
            duplicate_ids += sum(count - 1 for count in Counter(ids).values() if count > 1)
            for row in rows:
                lineage = row.get("lineage") or {}
                if (
                    lineage.get("document_id") != document_id
                    or lineage.get("version_id") != version_id
                    or len(str(lineage.get("artifact_sha256", ""))) != 64
                    or len(str(lineage.get("source_text_sha256", ""))) != 64
                    or not lineage.get("chunk_id")
                ):
                    lineage_failures += 1
                if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED":
                    promotion_failures += 1

        if duplicate_ids:
            failures.append("DUPLICATE_CANDIDATE_IDS")
        if lineage_failures:
            failures.append("LINEAGE_INCOMPLETE")
        if promotion_failures:
            failures.append("PROMOTION_STATE_INVALID")
        for row in requirements:
            trigger = str(row.get("trigger", "")).casefold().replace("ё", "е")
            statement = str(row.get("statement", "")).casefold().replace("ё", "е")
            if not trigger or trigger not in statement:
                failures.append("REQUIREMENT_TRIGGER_NOT_IN_STATEMENT")
                break

        status = "QUALITY_PASS" if not failures else "QUALITY_FAIL"
        if failures:
            hard_failures += 1
        results.append({
            "document_id": document_id,
            "status": status,
            "terms": len(terms),
            "definitions": len(definitions),
            "requirements": len(requirements),
            "entities": len(entities),
            "duplicate_candidate_ids": duplicate_ids,
            "lineage_failures": lineage_failures,
            "promotion_state_failures": promotion_failures,
            "failures": failures,
        })

    summary = {
        "record_type": "D6_D9_QUALITY",
        "targets": len(TARGETS),
        "quality_pass": sum(item.get("status") == "QUALITY_PASS" for item in results),
        "quality_fail": sum(item.get("status") == "QUALITY_FAIL" for item in results),
        "quality_input_missing": sum(item.get("status") == "QUALITY_INPUT_MISSING" for item in results),
        "promotion_to_d10_allowed": hard_failures == 0,
        "autonomous_kb_promotion": False,
    }
    payload = {"summary": summary, "documents": results}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if hard_failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
