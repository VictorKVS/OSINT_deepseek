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
    ("RU_NORMATIVE_SCOPE_GATE", [sys.executable, "scripts/validate_programming_kb_ru_normative_scope.py"], True),
    ("AUTHORITATIVE_L2_L3_L5_ACQUISITION", [sys.executable, "scripts/acquire_programming_kb_authoritative_sources.py"], True),
    ("TELEGRAM_BIBLIOGRAPHY_PROBE", [sys.executable, "scripts/probe_programmer_bibliography_telegram.py"], False),
    ("BIBLIOGRAPHY_ACQUISITION_PLAN", [sys.executable, "scripts/build_programmer_bibliography_acquisition_plan.py"], False),
    ("BOOKS_AND_OPEN_PAPERS_ACQUISITION", [sys.executable, "scripts/acquire_programming_kb_open_sources.py"], True),
    ("OWNED_TELEGRAM_ACQUISITION", [sys.executable, "scripts/download_programming_kb_owned_telegram_books.py"], False),
    ("KNOWLEDGE_DECOMPOSITION", [sys.executable, "scripts/process_programming_kb_sources.py"], True),
    ("LAYER_READINESS_AUDIT", [sys.executable, "scripts/audit_programming_kb_source_layers.py"], True),
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


def find_step(rows: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("name") == name:
            return row
    return None


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    started = time.perf_counter()
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for name, command, required in STEPS:
        if name == "BIBLIOGRAPHY_ACQUISITION_PLAN":
            probe = find_step(rows, "TELEGRAM_BIBLIOGRAPHY_PROBE")
            if probe and probe.get("returncode") != 0:
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

    process_summary = read_json_if_exists(REPORT_ROOT / "LATEST_SOURCE_PROCESSING.json")
    readiness = read_json_if_exists(REPORT_ROOT / "LATEST_PROGRAMMING_KB_LAYER_READINESS.json")
    normative_gate = read_json_if_exists(REPORT_ROOT / "LATEST_RU_NORMATIVE_SCOPE_GATE.json")
    authoritative = read_json_if_exists(REPORT_ROOT / "LATEST_AUTHORITATIVE_ACQUISITION.json")

    kb_min_ready = bool(readiness.get("programming_kb_min_ready"))
    technical_pass = not required_failures
    if not technical_pass:
        status = "FAIL"
    elif kb_min_ready:
        status = "PASS_KB_MIN_READY"
    else:
        status = "PASS_BUILDING_KB"

    elapsed = time.perf_counter() - started
    summary = {
        "record_type": "PROGRAMMING_KB_SOURCE_FACTORY_RUN",
        "schema_version": "1.1",
        "status": status,
        "technical_pipeline_pass": technical_pass,
        "programming_kb_min_ready": kb_min_ready,
        "knowledge_base_id": "PROGRAMMING_KB",
        "region_profile": "RU",
        "source_layer_order": [
            "L1_RU_LAW_GOST_REGULATORS",
            "L2_LANGUAGE_PRIMARY_AUTHORITY",
            "L3_SCIENTIFIC_PROFESSIONAL_CONSENSUS",
            "L4_BOOKS_EDUCATIONAL_PRACTICE",
            "L5_WORLD_PRODUCTION_EVIDENCE",
        ],
        "required_failures": required_failures,
        "optional_failures": optional_failures,
        "steps": rows,
        "ru_normative_scope_status": normative_gate.get("status"),
        "ru_normative_exact_text_or_applicability_gaps_total": int(normative_gate.get("exact_text_or_applicability_gaps_total") or 0),
        "authoritative_targets_total": int(authoritative.get("targets_total") or 0),
        "authoritative_downloaded_total": int(authoritative.get("downloaded_total") or 0),
        "authoritative_reused_total": int(authoritative.get("reused_total") or 0),
        "processed_sources_total": int(process_summary.get("processed_total") or 0),
        "parser_gap_total": int(process_summary.get("parser_gap_total") or 0),
        "knowledge_nodes_total": int(process_summary.get("knowledge_nodes_total") or 0),
        "relation_edges_total": int(process_summary.get("relation_edges_total") or 0),
        "definitions_total": int(process_summary.get("definitions_total") or 0),
        "requirements_total": int(process_summary.get("requirements_total") or 0),
        "claims_total": int(process_summary.get("claims_total") or 0),
        "chunks_total": int(process_summary.get("chunks_total") or 0),
        "layer_readiness_report": "reports/programming_kb_factory/LATEST_PROGRAMMING_KB_LAYER_READINESS.json",
        "kb_auto_promotion": False,
        "training_state": readiness.get("training_state") or "HOLD_UNTIL_PROGRAMMING_KB_MIN_READY",
        "elapsed_seconds": elapsed,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "note": "Technical PASS means the factory ran. PROGRAMMING_KB MIN readiness is a separate layered gate and remains false until required RU normative, language-primary, scientific, book/practice and world-production evidence is reviewable.",
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key != "steps"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {LATEST.relative_to(ROOT).as_posix()}")
    return 0 if technical_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
