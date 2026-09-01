from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "_LOCAL_DOWNLOADS_KB_INTAKE"
INVENTORY = LOCAL_ROOT / "INVENTORY.json"
CATALOGS = LOCAL_ROOT / "CATALOG_REFERENCES.json"
OUT_JSON = LOCAL_ROOT / "COVERAGE_GAPS.json"
OUT_TSV = LOCAL_ROOT / "COVERAGE_GAPS.tsv"
REPORT = ROOT / "reports" / "downloads_intake" / "LATEST_DOWNLOADS_COVERAGE_GAPS.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: str) -> str:
    s = value.upper().replace("Ё", "Е")
    s = re.sub(r"[«»\"'()]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace(" № ", " №")
    return s


def ref_kind(value: str) -> str:
    v = canonical(value)
    if v.startswith("ГОСТ"):
        return "STANDARD"
    if "-ФЗ" in v:
        return "FEDERAL_LAW"
    if v.startswith("№"):
        return "NUMBER_ONLY_NEEDS_CONTEXT"
    return "OTHER_REFERENCE"


def main() -> int:
    if not INVENTORY.is_file() or not CATALOGS.is_file():
        print(json.dumps({"status": "INPUT_MISSING", "inventory": str(INVENTORY), "catalogs": str(CATALOGS)}, ensure_ascii=False, indent=2))
        return 2

    inventory = load_json(INVENTORY)
    catalogs = load_json(CATALOGS)

    observed: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in inventory.get("items", []) or []:
        if not isinstance(item, dict) or item.get("status") == "DUPLICATE_SHA":
            continue
        for ident in item.get("identifiers") or []:
            observed[canonical(str(ident))].append({
                "item_id": item.get("item_id"),
                "source_file_name": item.get("source_file_name"),
                "sha256": item.get("sha256"),
                "document_type": item.get("document_type"),
                "authority": item.get("authority"),
            })

    references: defaultdict[str, set[str]] = defaultdict(set)
    original_forms: defaultdict[str, set[str]] = defaultdict(set)
    for catalog in catalogs.get("catalogs", []) or []:
        if not isinstance(catalog, dict):
            continue
        catalog_sha = str(catalog.get("source_sha256") or "")
        for ref in catalog.get("references") or []:
            ref_s = str(ref)
            key = canonical(ref_s)
            if not key:
                continue
            references[key].add(catalog_sha)
            original_forms[key].add(ref_s)

    rows: list[dict[str, Any]] = []
    for key in sorted(references):
        matches = observed.get(key, [])
        kind = ref_kind(key)
        if matches:
            status = "FOUND" if len(matches) == 1 else "DUPLICATE_OBSERVED"
        elif kind == "NUMBER_ONLY_NEEDS_CONTEXT":
            status = "NEEDS_CANONICALIZATION"
        else:
            status = "MISSING"
        rows.append({
            "reference": sorted(original_forms[key], key=len)[0],
            "canonical_reference": key,
            "reference_kind": kind,
            "status": status,
            "catalog_source_sha256": sorted(references[key]),
            "observed_matches": matches,
        })

    counts = Counter(str(row["status"]) for row in rows)
    payload = {
        "schema_version": "1.0",
        "record_type": "DOWNLOADS_KB_COVERAGE_GAPS",
        "references_total": len(rows),
        "status_counts": dict(sorted(counts.items())),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = ["status\treference_kind\treference\tcatalogs_total\tobserved_total"]
    for row in rows:
        lines.append(
            f"{row['status']}\t{row['reference_kind']}\t{row['reference']}\t"
            f"{len(row['catalog_source_sha256'])}\t{len(row['observed_matches'])}"
        )
    OUT_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = {
        "schema_version": "1.0",
        "record_type": "DOWNLOADS_KB_COVERAGE_GAPS_RUN",
        "status": "PASS",
        "references_total": len(rows),
        "found_total": counts.get("FOUND", 0),
        "missing_total": counts.get("MISSING", 0),
        "duplicate_observed_total": counts.get("DUPLICATE_OBSERVED", 0),
        "needs_canonicalization_total": counts.get("NEEDS_CANONICALIZATION", 0),
        "coverage_json": OUT_JSON.relative_to(ROOT).as_posix(),
        "coverage_tsv": OUT_TSV.relative_to(ROOT).as_posix(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
