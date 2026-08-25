from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NORMATIVE = ROOT / "config" / "programmer_ru_normative_scope.json"
ESPD = ROOT / "config" / "programmer_ru_espd_inventory.json"
GOST34 = ROOT / "config" / "programmer_ru_automated_systems_conditional.json"
REPORT = ROOT / "reports" / "programming_kb_factory" / "LATEST_RU_NORMATIVE_SCOPE_GATE.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    normative = load_json(NORMATIVE)
    espd = load_json(ESPD)
    gost34 = load_json(GOST34)
    sectors = [row for row in normative.get("sectors", []) if isinstance(row, dict)]
    active_espd = int((espd.get("counts") or {}).get("active") or 0)
    current_gost34 = len(gost34.get("current_documents", []))
    errors: list[str] = []
    if normative.get("role_id") != "PROGRAMMER" or normative.get("knowledge_base_id") != "PROGRAMMING_KB":
        errors.append("normative scope is not bound to PROGRAMMER/PROGRAMMING_KB")
    if active_espd != 28:
        errors.append(f"expected 28 active ESPD catalog records, got {active_espd}")
    if current_gost34 < 5:
        errors.append(f"expected at least 5 current GOST34 core records, got {current_gost34}")
    if not sectors:
        errors.append("programmer RU normative sectors are empty")

    exact_or_applicability_gaps = [
        {
            "sector_id": row.get("sector_id"),
            "state": row.get("state"),
            "next": row.get("next"),
        }
        for row in sectors
        if str(row.get("state") or "") not in {"COMPLETE_CURRENT_CATALOG_STATUS", "CONDITIONAL_CORE_VERIFIED"}
    ]
    payload = {
        "record_type": "PROGRAMMING_KB_RU_NORMATIVE_SCOPE_GATE",
        "schema_version": "1.0",
        "status": "PASS_CATALOG_AND_SCOPE" if not errors else "FAIL",
        "region_profile": "RU",
        "knowledge_base_id": "PROGRAMMING_KB",
        "sectors_total": len(sectors),
        "espd_active_catalog_total": active_espd,
        "gost34_current_core_total": current_gost34,
        "exact_text_or_applicability_gaps_total": len(exact_or_applicability_gaps),
        "exact_text_or_applicability_gaps": exact_or_applicability_gaps,
        "programming_kb_l1_ready": False if exact_or_applicability_gaps else not errors,
        "note": "PASS_CATALOG_AND_SCOPE proves the bounded RU inventory/scope contract only. It does not prove exact current normative text or applicability for a concrete project.",
        "validation_errors": errors,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in payload.items() if key not in {"exact_text_or_applicability_gaps", "validation_errors"}}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
