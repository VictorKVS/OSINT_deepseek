from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import run_security_current_only_5stream_v2 as bulk

QUEUE_FILE = REPO_ROOT / "config" / "security_departmental_acquisition_map.json"
REPORT_DIR = REPO_ROOT / "reports" / "security_current_only"
REPORT = REPORT_DIR / "LATEST_DEPARTMENTAL_5STREAM_RUN.json"
WORKERS = 5


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    started = time.perf_counter()
    payload = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    documents = [row for row in payload.get("documents", []) if isinstance(row, dict)]

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="security-dept") as executor:
        futures = {executor.submit(bulk._process, doc): doc for doc in documents}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"[{result.get('status')}] {result.get('document_id')} {result.get('sha256') or ''}")

    results.sort(key=lambda row: str(row.get("document_id") or ""))
    total_seconds = time.perf_counter() - started
    official_acquired = sum(row.get("status") in {"NORMALIZED", "ACQUIRED_RAW"} for row in results)
    official_normalized = sum(row.get("status") == "NORMALIZED" for row in results)
    working_acquired = sum(row.get("status") in {"WORKING_COPY_NORMALIZED", "WORKING_COPY_RAW"} for row in results)
    working_normalized = sum(row.get("status") == "WORKING_COPY_NORMALIZED" for row in results)
    unresolved = sum(row.get("status") == "UNRESOLVED" for row in results)
    operational = official_acquired + working_acquired

    summary = {
        "record_type": "SECURITY_DEPARTMENTAL_5STREAM_RUN",
        "schema_version": "1.0",
        "observed_at": _utc_now(),
        "workers": WORKERS,
        "queue": QUEUE_FILE.relative_to(REPO_ROOT).as_posix(),
        "queue_total": len(documents),
        "official_acquired_total": official_acquired,
        "official_normalized_total": official_normalized,
        "working_copy_acquired_total": working_acquired,
        "working_copy_normalized_total": working_normalized,
        "operationally_available_total": operational,
        "unresolved_total": unresolved,
        "official_coverage_ratio": official_acquired / len(documents) if documents else 1.0,
        "operational_coverage_ratio": operational / len(documents) if documents else 1.0,
        "throughput_operational_docs_per_second": operational / total_seconds if total_seconds > 0 else 0.0,
        "speedup_vs_1_stream_pct": None,
        "speedup_note": "No 1-stream baseline is claimed until measured on the same queue and workstation.",
        "legal_truth_policy": "Every queue item begins VERIFY_CURRENTNESS. Only proof-grade exact official acquisition is legal-truth eligible; A2 working copies remain blocked from KB promotion.",
        "total_seconds": total_seconds,
        "results": results,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
