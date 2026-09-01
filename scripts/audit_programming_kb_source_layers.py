from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAYERS = ROOT / "config" / "programming_kb_source_layers.json"
NORMATIVE = ROOT / "config" / "programmer_ru_normative_scope.json"
ESPD = ROOT / "config" / "programmer_ru_espd_inventory.json"
GOST34 = ROOT / "config" / "programmer_ru_automated_systems_conditional.json"
DATA_ROOT = ROOT / "data" / "programming_kb_sources"
PROCESS_REPORT = ROOT / "reports" / "programming_kb_factory" / "LATEST_SOURCE_PROCESSING.json"
REPORT = ROOT / "reports" / "programming_kb_factory" / "LATEST_PROGRAMMING_KB_LAYER_READINESS.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def processed_ids() -> set[str]:
    if not PROCESS_REPORT.exists():
        return set()
    payload = load_json(PROCESS_REPORT)
    return {
        str(row.get("target_id"))
        for row in payload.get("results", [])
        if isinstance(row, dict) and row.get("status") == "PROCESSED_REVIEW_REQUIRED"
    }


def acquired_metadata() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not DATA_ROOT.exists():
        return rows
    for path in DATA_ROOT.glob("*/source.json"):
        try:
            payload = load_json(path)
        except Exception:
            continue
        target_id = str(payload.get("target_id") or path.parent.name)
        rows[target_id] = payload
    return rows


def main() -> int:
    layers = load_json(LAYERS)
    normative = load_json(NORMATIVE)
    espd = load_json(ESPD)
    gost34 = load_json(GOST34)
    processed = processed_ids()
    acquired = acquired_metadata()

    layer_rows: list[dict[str, Any]] = []

    normative_sectors = [row for row in normative.get("sectors", []) if isinstance(row, dict)]
    unresolved_normative = [
        str(row.get("sector_id"))
        for row in normative_sectors
        if str(row.get("state") or "") not in {
            "COMPLETE_CURRENT_CATALOG_STATUS",
            "CONDITIONAL_CORE_VERIFIED",
        }
    ]
    l1_gaps = []
    if int((espd.get("counts") or {}).get("active") or 0) < 28:
        l1_gaps.append("ESPD_GOST19_CURRENT_CATALOG_INCOMPLETE")
    if len(gost34.get("current_documents", [])) < 5:
        l1_gaps.append("GOST34_CURRENT_CORE_INCOMPLETE")
    if unresolved_normative:
        l1_gaps.append("EXACT_TEXT_APPLICABILITY_OR_SECTOR_GAPS_REMAIN")
    layer_rows.append({
        "layer_id": "L1_RU_LAW_GOST_REGULATORS",
        "state": "BUILDING" if l1_gaps else "MIN_EVIDENCE_READY",
        "catalog_or_seed_evidence": {
            "normative_sectors_total": len(normative_sectors),
            "espd_active_total": int((espd.get("counts") or {}).get("active") or 0),
            "gost34_current_core_total": len(gost34.get("current_documents", [])),
        },
        "unresolved_sector_ids": unresolved_normative,
        "gaps": l1_gaps,
        "min_ready": not l1_gaps,
        "note": "Catalog/currentness seeds do not prove exact normative text or legal applicability. Global Document Registry evidence remains authoritative.",
    })

    l2 = next(row for row in layers["layers"] if row.get("layer_id") == "L2_LANGUAGE_PRIMARY_AUTHORITY")
    language_targets = [row for row in l2.get("targets", []) if isinstance(row, dict)]
    open_language_ids = {
        str(row.get("source_id"))
        for row in language_targets
        if str(row.get("acquisition") or "").startswith("OFFICIAL_OPEN_WEB")
    }
    gated_language_ids = {
        str(row.get("source_id"))
        for row in language_targets
        if not str(row.get("acquisition") or "").startswith("OFFICIAL_OPEN_WEB")
    }
    l2_processed = open_language_ids & processed
    l2_gaps = []
    missing_open = sorted(open_language_ids - l2_processed)
    if missing_open:
        l2_gaps.append("PRIMARY_LANGUAGE_OPEN_SOURCES_NOT_ALL_PROCESSED")
    if gated_language_ids:
        l2_gaps.append("C_OR_CPP_PRIMARY_STANDARD_AUTHORIZED_COPY_OR_EQUIVALENT_PRIMARY_EVIDENCE_PENDING")
    layer_rows.append({
        "layer_id": "L2_LANGUAGE_PRIMARY_AUTHORITY",
        "targets_total": len(language_targets),
        "open_targets_total": len(open_language_ids),
        "processed_open_total": len(l2_processed),
        "missing_open_ids": missing_open,
        "gated_primary_ids": sorted(gated_language_ids),
        "gaps": l2_gaps,
        "min_ready": not l2_gaps,
        "state": "MIN_EVIDENCE_READY" if not l2_gaps else "BUILDING",
    })

    for layer_id in (
        "L3_SCIENTIFIC_PROFESSIONAL_CONSENSUS",
        "L5_WORLD_PRODUCTION_EVIDENCE",
    ):
        layer = next(row for row in layers["layers"] if row.get("layer_id") == layer_id)
        expected = {str(value) for value in layer.get("source_refs", [])}
        done = expected & processed
        missing = sorted(expected - done)
        layer_rows.append({
            "layer_id": layer_id,
            "targets_total": len(expected),
            "processed_total": len(done),
            "missing_ids": missing,
            "gaps": ["REQUIRED_SOURCES_NOT_ALL_PROCESSED"] if missing else [],
            "min_ready": not missing,
            "state": "MIN_EVIDENCE_READY" if not missing else "BUILDING",
        })

    book_ids = {
        target_id
        for target_id, meta in acquired.items()
        if str(meta.get("source_layer") or "") == "L4_BOOKS_EDUCATIONAL_PRACTICE"
        or target_id.startswith(("BOOK-", "WORK-", "ALG-", "PYALG-", "JAVAALG-", "CPPALG-", "GOALG-", "RUSTALG-", "KNUTH-", "ILLUM-"))
    }
    processed_books = book_ids & processed
    l4_gaps = [] if len(processed_books) >= 2 else ["MINIMUM_TWO_REVIEWABLE_BOOK_OR_EDUCATIONAL_SOURCES_NOT_PROCESSED"]
    layer_rows.append({
        "layer_id": "L4_BOOKS_EDUCATIONAL_PRACTICE",
        "acquired_or_registered_total": len(book_ids),
        "processed_total": len(processed_books),
        "processed_ids": sorted(processed_books),
        "gaps": l4_gaps,
        "min_ready": not l4_gaps,
        "state": "MIN_EVIDENCE_READY" if not l4_gaps else "BUILDING",
        "note": "Book coverage is explanatory/practical and never substitutes for L1-L3 authority.",
    })

    ready = all(bool(row.get("min_ready")) for row in layer_rows)
    payload = {
        "record_type": "PROGRAMMING_KB_LAYER_READINESS",
        "schema_version": "1.0",
        "knowledge_base_id": "PROGRAMMING_KB",
        "region_profile": "RU",
        "technical_pipeline_state": "PASS_OR_PARTIAL_RUN_EVIDENCE_ONLY",
        "programming_kb_min_ready": ready,
        "training_state": "READY_FOR_TASK_MAPPING" if ready else "HOLD_UNTIL_PROGRAMMING_KB_MIN_READY",
        "layers": layer_rows,
        "processed_source_ids_total": len(processed),
        "acquired_source_metadata_total": len(acquired),
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in payload.items() if key != "layers"}
    compact["layer_states"] = {row["layer_id"]: row["state"] for row in layer_rows}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
