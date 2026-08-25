from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
LATEST = REPORT_ROOT / "LATEST_PROGRAMMING_KB_SOURCE_FACTORY.json"

STEPS = [
    ("TELEGRAM_BIBLIOGRAPHY_PROBE", [sys.executable, "scripts/probe_programmer_bibliography_telegram.py"], False),
    ("BIBLIOGRAPHY_ACQUISITION_PLAN", [sys.executable, "scripts/build_programmer_bibliography_acquisition_plan.py"], False),
    ("OFFICIAL_OPEN_ACQUISITION", [sys.executable, "scripts/acquire_programming_kb_open_sources.py"], True),
    ("OWNED_TELEGRAM_ACQUISITION", [sys.executable, "scripts/download_programming_kb_owned_telegram_books.py"], False),
    ("KNOWLEDGE_DECOMPOSITION", [sys.executable, "scripts/process_programming_kb_sources.py"], True),
]


def run_step(name: str, command: list[str], required: bool) -> dict[str, Any]:
    started = time.perf_counter()
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "name": name,
        "required": required,
        "returncode": int(proc.returncode),
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "elapsed_seconds": time.perf_counter() - started,
        "stdout_tail": proc.stdout[-5000:],
        "stderr_tail": proc.stderr[-3000:],
    }


def main() -> int:
    started = time.perf_counter()
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for name, command, required in STEPS:
        # Acquisition-plan step needs the probe report; if probe failed, keep the gap explicit.
        if name == "BIBLIOGRAPHY_ACQUISITION_PLAN" and rows and rows[-1]["name"] == "TELEGRAM_BIBLIOGRAPHY_PROBE" and rows[-1]["returncode"] != 0:
            rows.append({
                "name": name,
                "required": required,
                "returncode": None,
                "status": "SKIPPED_DEPENDENCY_GAP",
                "elapsed_seconds": 0.0,
                "stdout_tail": "",
                "stderr_tail": "Telegram probe did not produce a usable report.",
            })
            continue
        rows.append(run_step(name, command, required))

    required_failures = [row["name"] for row in rows if row.get("required") and row.get("returncode") not in {0}]
    optional_failures = [row["name"] for row in rows if not row.get("required") and row.get("status") not in {"PASS", "SKIPPED_DEPENDENCY_GAP"}]
    process_report = REPORT_ROOT / "LATEST_SOURCE_PROCESSING.json"
    process_summary: dict[str, Any] = {}
    if process_report.exists():
        try:
            process_summary = json.loads(process_report.read_text(encoding="utf-8"))
        except Exception:
            process_summary = {}

    elapsed = time.perf_counter() - started
    summary = {
        "record_type": "PROGRAMMING_KB_SOURCE_FACTORY_RUN",
        "schema_version": "1.0",
        "status": "PASS" if not required_failures else "FAIL",
        "knowledge_base_id": "PROGRAMMING_KB",
        "region_profile": "RU",
        "required_failures": required_failures,
        "optional_failures": optional_failures,
        "steps": rows,
        "processed_sources_total": int(process_summary.get("processed_total") or 0),
        "parser_gap_total": int(process_summary.get("parser_gap_total") or 0),
        "knowledge_nodes_total": int(process_summary.get("knowledge_nodes_total") or 0),
        "relation_edges_total": int(process_summary.get("relation_edges_total") or 0),
        "definitions_total": int(process_summary.get("definitions_total") or 0),
        "requirements_total": int(process_summary.get("requirements_total") or 0),
        "claims_total": int(process_summary.get("claims_total") or 0),
        "chunks_total": int(process_summary.get("chunks_total") or 0),
        "kb_auto_promotion": False,
        "training_state": "HOLD_UNTIL_PROGRAMMING_KB_MIN_READY",
        "elapsed_seconds": elapsed,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "note": "This run builds reviewable PROGRAMMING_KB candidates. It does not train a model or promote unreviewed knowledge.",
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key != "steps"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {LATEST.relative_to(ROOT).as_posix()}")
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
