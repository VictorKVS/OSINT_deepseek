from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.acquire_programming_kb_open_sources import acquire_one  # noqa: E402

LAYERS = ROOT / "config" / "programming_kb_source_layers.json"
KNOWLEDGE_SOURCES = ROOT / "config" / "knowledge_source_registry.json"
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
REPORT = REPORT_ROOT / "LATEST_AUTHORITATIVE_ACQUISITION.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _layer(payload: dict[str, Any], layer_id: str) -> dict[str, Any]:
    for row in payload.get("layers", []):
        if isinstance(row, dict) and row.get("layer_id") == layer_id:
            return row
    raise RuntimeError(f"source layer not found: {layer_id}")


def build_targets() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    layer_payload = load_json(LAYERS)
    source_registry = load_json(KNOWLEDGE_SOURCES)
    source_by_id = {
        str(row.get("source_id")): row
        for row in source_registry.get("sources", [])
        if isinstance(row, dict) and row.get("source_id")
    }
    rows: list[dict[str, Any]] = []
    gated: list[dict[str, Any]] = []

    l2 = _layer(layer_payload, "L2_LANGUAGE_PRIMARY_AUTHORITY")
    for target in l2.get("targets", []):
        if not isinstance(target, dict):
            continue
        acquisition = str(target.get("acquisition") or "")
        if not acquisition.startswith("OFFICIAL_OPEN_WEB"):
            gated.append({
                "source_id": target.get("source_id"),
                "language": target.get("language"),
                "name": target.get("name"),
                "acquisition": acquisition,
                "rights_gate": target.get("rights_gate"),
                "state": "AUTHORIZED_COPY_OR_PRIMARY_METADATA_REQUIRED",
            })
            continue
        rows.append({
            "id": target["source_id"],
            "source_id": target["source_id"],
            "source_layer": "L2_LANGUAGE_PRIMARY_AUTHORITY",
            "authority_class": "PRIMARY_TECHNICAL_AUTHORITY",
            "language": target.get("language"),
            "kind": "PRIMARY_LANGUAGE_SOURCE",
            "author": target.get("language") or "Official language authority",
            "title": target.get("name"),
            "official_url": target.get("url"),
            "route": "OFFICIAL_OPEN_WEB",
            "rights_class": "OFFICIAL_OPEN_DOCUMENTATION",
            "rights_basis": "PRIMARY_AUTHORITY_OPEN_WEB",
            "source_language": "en",
            "topics": ["language semantics", "official usage", str(target.get("language") or "")],
        })

    for layer_id, authority in (
        ("L3_SCIENTIFIC_PROFESSIONAL_CONSENSUS", "SCIENTIFIC_AND_PROFESSIONAL_CONSENSUS"),
        ("L5_WORLD_PRODUCTION_EVIDENCE", "WORLD_PRODUCTION_EVIDENCE"),
    ):
        layer = _layer(layer_payload, layer_id)
        for source_ref in layer.get("source_refs", []):
            source = source_by_id.get(str(source_ref))
            if not source:
                gated.append({
                    "source_id": source_ref,
                    "source_layer": layer_id,
                    "state": "SOURCE_REGISTRY_GAP",
                })
                continue
            url = str(source.get("canonical_url") or "").strip()
            if not url.startswith("https://"):
                gated.append({
                    "source_id": source_ref,
                    "source_layer": layer_id,
                    "state": "CANONICAL_HTTPS_URL_GAP",
                })
                continue
            rows.append({
                "id": str(source_ref),
                "source_id": str(source_ref),
                "source_layer": layer_id,
                "authority_class": authority,
                "kind": source.get("source_class"),
                "author": source.get("owner"),
                "title": source.get("name"),
                "official_url": url,
                "route": "OFFICIAL_OPEN_WEB",
                "rights_class": "OFFICIAL_OR_INSTITUTIONAL_OPEN_REFERENCE",
                "rights_basis": "CANONICAL_PRIMARY_OR_CONSENSUS_WEB",
                "source_language": "en",
                "topics": [],
            })

    unique: dict[str, dict[str, Any]] = {}
    for row in rows:
        unique[str(row["id"])] = row
    return [unique[key] for key in sorted(unique)], gated


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire PROGRAMMING_KB primary language, consensus and world-practice sources.")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-file-size-mb", type=int, default=100)
    args = parser.parse_args()

    started = time.perf_counter()
    rows, gated = build_targets()
    errors: list[str] = []
    layer_ids = {str(row.get("source_layer")) for row in rows}
    if "L2_LANGUAGE_PRIMARY_AUTHORITY" not in layer_ids:
        errors.append("no automatically acquirable primary language sources")
    if "L3_SCIENTIFIC_PROFESSIONAL_CONSENSUS" not in layer_ids:
        errors.append("no automatically acquirable scientific/consensus sources")
    if "L5_WORLD_PRODUCTION_EVIDENCE" not in layer_ids:
        errors.append("no automatically acquirable world-production sources")
    if len(rows) > 30:
        errors.append("authoritative seed is unexpectedly unbounded")

    if args.validate_only:
        payload = {
            "record_type": "PROGRAMMING_KB_AUTHORITATIVE_ACQUISITION_VALIDATION",
            "status": "PASS" if not errors else "FAIL",
            "targets_total": len(rows),
            "gated_total": len(gated),
            "layer_counts": {
                layer: sum(row.get("source_layer") == layer for row in rows)
                for layer in sorted(layer_ids)
            },
            "validation_errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 2

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    workers = max(1, min(5, int(args.workers)))
    max_bytes = max(1, int(args.max_file_size_mb)) * 1024 * 1024
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(acquire_one, row, timeout=max(1, int(args.timeout)), max_bytes=max_bytes)
            for row in rows
        ]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda row: str(row.get("target_id")))

    downloaded = sum(row.get("acquisition_status") == "DOWNLOADED" for row in results)
    reused = sum(row.get("acquisition_status") == "REUSED_EXACT" for row in results)
    failed = sum(row.get("acquisition_status") == "FAILED" for row in results)
    elapsed = time.perf_counter() - started
    layer_counts = {
        layer: {
            "targets": sum(row.get("source_layer") == layer for row in results),
            "available": sum(
                row.get("source_layer") == layer and row.get("acquisition_status") in {"DOWNLOADED", "REUSED_EXACT"}
                for row in results
            ),
            "failed": sum(row.get("source_layer") == layer and row.get("acquisition_status") == "FAILED" for row in results),
        }
        for layer in sorted({str(row.get("source_layer")) for row in results})
    }
    summary = {
        "record_type": "PROGRAMMING_KB_AUTHORITATIVE_ACQUISITION",
        "schema_version": "1.0",
        "status": "PASS" if failed == 0 else "PASS_WITH_GAPS" if downloaded + reused > 0 else "FAIL",
        "targets_total": len(results),
        "downloaded_total": downloaded,
        "reused_total": reused,
        "failed_total": failed,
        "gated_total": len(gated),
        "gated_sources": gated,
        "layer_counts": layer_counts,
        "workers": workers,
        "elapsed_seconds": elapsed,
        "throughput_sources_per_second": (downloaded + reused) / elapsed if elapsed > 0 else None,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "kb_auto_promotion": False,
        "results": results,
    }
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key not in {"results", "gated_sources"}}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if summary["status"] in {"PASS", "PASS_WITH_GAPS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
