from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ORDER_ROOT = ROOT / "reports" / "library_orders"
TEAM_REPORT_ROOT = ROOT / "reports" / "team_role_telegram"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    payload["updated_at_epoch"] = time.time()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    latest = ORDER_ROOT / f"LATEST_{payload['role_id']}.json"
    latest.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_order(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_file():
        return candidate.resolve()
    if not candidate.is_absolute():
        candidate = ORDER_ROOT / (value if value.endswith(".json") else f"{value}.json")
    if not candidate.is_file():
        raise RuntimeError(f"library order not found: {value}")
    return candidate.resolve()


def run_cmd(command: list[str], env: dict[str, str]) -> int:
    proc = subprocess.run(command, cwd=str(ROOT), env=env, check=False)
    return int(proc.returncode)


def stage_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def update_stage(order: dict[str, Any], stage: str, state: str, *, evidence: str | None = None, note: str | None = None) -> None:
    row = order["stages"][stage]
    row["state"] = state
    row["updated_at_epoch"] = time.time()
    if evidence:
        row.setdefault("evidence_refs", []).append(evidence)
    if note:
        row["note"] = note


def handoff_manifest(order: dict[str, Any], acquisition: dict[str, Any], coverage: dict[str, Any]) -> Path:
    path = ORDER_ROOT / f"{order['order_id']}_STAGE2_HANDOFF.json"
    materials: list[dict[str, Any]] = []
    for status_key, status in (("downloads", "DOWNLOADED"), ("reused", "REUSED")):
        for row in acquisition.get(status_key, []) or []:
            materials.append({
                "status": status,
                "file_name": row.get("file_name"),
                "local_path": row.get("local_path"),
                "sha256": row.get("sha256"),
                "source_url": row.get("source_url"),
                "matched_target_ids": row.get("matched_target_ids") or [],
                "material_profile": "ROLE_LIBRARY_MATERIAL",
                "next_stage": "STAGE_2_DOCUMENT_COMPILER",
            })
    payload = {
        "schema_version": "1.0",
        "record_type": "LIBRARY_ORDER_STAGE2_HANDOFF",
        "order_id": order["order_id"],
        "role_id": order["role_id"],
        "knowledge_base_id": order["knowledge_base_id"],
        "maturity_target": order["maturity_target"],
        "materials_total": len(materials),
        "materials": materials,
        "coverage_ref": stage_ref(TEAM_REPORT_ROOT / f"LATEST_{order['role_id']}_COVERAGE.json"),
        "overall_min_gate": coverage.get("overall_min_gate"),
        "telegram_gate": coverage.get("telegram_gate"),
        "kb_auto_promotion": False,
        "trace": order.get("trace", {}),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the implemented stages of a FATHER library order")
    parser.add_argument("--order", required=True, help="Order id or JSON path")
    parser.add_argument("--stage1-only", action="store_true", help="Stop after acquisition and coverage")
    args = parser.parse_args()

    order_path = resolve_order(args.order)
    order = load_json(order_path)
    role_id = str(order["role_id"])
    env = os.environ.copy()
    trace = order.get("trace") or {}
    for key, env_name in (
        ("trace_id", "FATHER_TRACE_ID"),
        ("correlation_id", "FATHER_CORRELATION_ID"),
        ("task_id", "FATHER_TASK_ID"),
        ("command_id", "FATHER_PARENT_COMMAND_ID"),
    ):
        if trace.get(key):
            env[env_name] = str(trace[key])

    order["state"] = "RUNNING"
    order["current_stage"] = "STAGE_1_ACQUISITION"
    update_stage(order, "STAGE_1_ACQUISITION", "RUNNING")
    write_json(order_path, order)

    requested_sources = set(order.get("requested_sources") or [])
    if "TELEGRAM" in requested_sources:
        rc = run_cmd([
            sys.executable,
            str(ROOT / "scripts" / "run_team_role_acquisition_live.py"),
            "--role", role_id,
        ], env)
        report_path = TEAM_REPORT_ROOT / f"LATEST_{role_id}_TELEGRAM_RUN.json"
        if rc != 0 or not report_path.is_file():
            update_stage(order, "STAGE_1_ACQUISITION", "FAILED", note="Telegram acquisition failed or produced no report")
            order["state"] = "BLOCKED"
            order["gaps"].append({"type": "ACQUISITION_FAILURE", "source": "TELEGRAM"})
            write_json(order_path, order)
            return 1
        acquisition = load_json(report_path)
        update_stage(order, "STAGE_1_ACQUISITION", "PASS", evidence=stage_ref(report_path))
    else:
        acquisition = {"downloads": [], "reused": [], "search_hits_total": 0, "downloaded_total": 0, "payload_reused_total": 0, "bytes_downloaded": 0, "errors_total": 0}
        update_stage(order, "STAGE_1_ACQUISITION", "PASS_WITHOUT_TELEGRAM", note="Telegram was not requested")

    for source in sorted(requested_sources - {"TELEGRAM"}):
        state = (order.get("source_states") or {}).get(source)
        if state in {"CONNECTOR_PENDING", "MANUAL_OR_USER_AUTHORIZED_IMPORT_PENDING"}:
            order["gaps"].append({
                "type": "SOURCE_CHANNEL_PENDING",
                "source": source,
                "state": state,
                "blocking_for_requested_multisource_order": True,
            })

    order["current_stage"] = "STAGE_1_COVERAGE"
    update_stage(order, "STAGE_1_COVERAGE", "RUNNING")
    write_json(order_path, order)

    coverage_path = TEAM_REPORT_ROOT / f"LATEST_{role_id}_COVERAGE.json"
    if "TELEGRAM" in requested_sources:
        rc = run_cmd([
            sys.executable,
            str(ROOT / "scripts" / "analyze_team_role_telegram_coverage.py"),
            "--role", role_id,
        ], env)
        if rc != 0 or not coverage_path.is_file():
            update_stage(order, "STAGE_1_COVERAGE", "FAILED", note="Coverage assessment failed")
            order["state"] = "BLOCKED"
            write_json(order_path, order)
            return 1
        coverage = load_json(coverage_path)
        update_stage(order, "STAGE_1_COVERAGE", "PASS", evidence=stage_ref(coverage_path))
    else:
        coverage = {"topics_total": order.get("topics_total", 0), "topics_covered": 0, "topics_gap": order.get("topics_total", 0), "overall_min_gate": "NOT_PROVEN", "telegram_gate": "NOT_REQUESTED"}
        update_stage(order, "STAGE_1_COVERAGE", "PASS_WITHOUT_TELEGRAM")

    metrics = order["metrics"]
    metrics["search_hits_total"] = int(acquisition.get("search_hits_total") or 0)
    metrics["downloaded_total"] = int(acquisition.get("downloaded_total") or 0)
    metrics["reused_total"] = int(acquisition.get("payload_reused_total") or 0)
    metrics["failed_total"] = int(acquisition.get("errors_total") or 0)
    metrics["bytes_downloaded"] = int(acquisition.get("bytes_downloaded") or 0)
    metrics["topics_covered"] = int(coverage.get("topics_covered") or 0)
    metrics["topics_gap"] = int(coverage.get("topics_gap") or 0)

    handoff = handoff_manifest(order, acquisition, coverage)
    update_stage(order, "STAGE_2_DOCUMENT_COMPILER", "READY_FOR_HANDOFF", evidence=stage_ref(handoff), note="Adapter-driven Stage 2 handoff prepared; unsupported file/profile adapters must remain explicit gaps")

    blocking_source_gaps = [gap for gap in order.get("gaps", []) if gap.get("blocking_for_requested_multisource_order")]
    if blocking_source_gaps:
        order["state"] = "WAITING_SOURCE_CHANNELS"
        order["current_stage"] = "STAGE_1_ACQUISITION"
        order["next_actions"] = ["CONNECT_MISSING_SOURCE_CHANNELS", "REASSESS_COVERAGE", "RUN_STAGE_2_HANDOFF"]
    else:
        order["state"] = "STAGE_1_COMPLETE"
        order["current_stage"] = "STAGE_2_DOCUMENT_COMPILER"
        order["next_actions"] = ["RUN_STAGE_2_HANDOFF"]

    # Do not claim full maturity or KB readiness from Stage 1 alone.
    if coverage.get("overall_min_gate") != "PROVEN":
        order["gaps"].append({
            "type": "MATURITY_NOT_YET_PROVEN",
            "maturity_target": order["maturity_target"],
            "coverage_gate": coverage.get("overall_min_gate"),
            "note": "Downloaded file counts do not prove the requested role maturity.",
        })

    write_json(order_path, order)
    print(json.dumps({
        "status": order["state"],
        "order_id": order["order_id"],
        "role_id": role_id,
        "maturity_target": order["maturity_target"],
        "current_stage": order["current_stage"],
        "topics_total": order["topics_total"],
        "topics_covered": metrics["topics_covered"],
        "topics_gap": metrics["topics_gap"],
        "downloaded_total": metrics["downloaded_total"],
        "reused_total": metrics["reused_total"],
        "source_gaps_total": len(blocking_source_gaps),
        "handoff_path": stage_ref(handoff),
        "kb_auto_promotion": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
