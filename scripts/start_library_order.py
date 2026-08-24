from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_GLOBAL = ROOT / "scripts" / "build_global_document_registry.py"
CREATE = ROOT / "scripts" / "create_library_order.py"
RUN = ROOT / "scripts" / "run_library_order.py"
ORDER_ROOT = ROOT / "reports" / "library_orders"
GLOBAL_REGISTRY = ROOT / "reports" / "global_document_registry" / "GLOBAL_DOCUMENT_REGISTRY.json"
GLOBAL_BINDINGS = ROOT / "reports" / "global_document_registry" / "APPLICABILITY_BINDINGS.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def latest_path(role_id: str) -> Path:
    return ORDER_ROOT / f"LATEST_{role_id.upper().replace('-', '_')}.json"


def load_latest(role_id: str) -> dict:
    path = latest_path(role_id)
    if not path.is_file():
        raise RuntimeError(f"latest order was not created: {path}")
    return load_json(path)


def build_global_registry() -> int:
    cmd = [sys.executable, str(BUILD_GLOBAL)]
    rc = int(subprocess.run(cmd, cwd=str(ROOT), env=os.environ.copy(), check=False).returncode)
    if rc != 0:
        return rc
    if not GLOBAL_REGISTRY.is_file() or not GLOBAL_BINDINGS.is_file():
        raise RuntimeError("global document registry build returned success without canonical outputs")
    registry = load_json(GLOBAL_REGISTRY)
    if not (registry.get("acceptance") or {}).get("ready_for_shared_use"):
        raise RuntimeError("global document registry has blocking canonical status conflicts")
    return 0


def attach_global_registry(order: dict) -> dict:
    registry = load_json(GLOBAL_REGISTRY)
    binding_payload = load_json(GLOBAL_BINDINGS)
    role_id = str(order["role_id"])
    kb_id = str(order.get("knowledge_base_id") or "")
    relevant = [
        row for row in binding_payload.get("bindings", [])
        if (row.get("subject_type") == "ROLE" and row.get("subject_id") == role_id)
        or (kb_id and row.get("subject_type") == "KNOWLEDGE_BASE" and row.get("subject_id") == kb_id)
    ]
    document_ids = sorted({str(row["document_id"]) for row in relevant if row.get("document_id")})
    known_ids = {str(row["document_id"]) for row in registry.get("documents", [])}
    missing = sorted(set(document_ids) - known_ids)
    if missing:
        raise RuntimeError(f"role bindings reference missing canonical document(s): {', '.join(missing)}")

    order["global_document_registry"] = {
        "registry_id": registry.get("registry_id"),
        "registry_ref": str(GLOBAL_REGISTRY.relative_to(ROOT)).replace("\\", "/"),
        "bindings_ref": str(GLOBAL_BINDINGS.relative_to(ROOT)).replace("\\", "/"),
        "documents_total_global": registry.get("documents_total"),
        "resolved_document_refs": document_ids,
        "resolved_document_refs_total": len(document_ids),
        "bindings": relevant,
        "resolution_state": "PASS" if document_ids else "GAP_NO_ROLE_BINDINGS",
        "resolved_at_epoch": time.time(),
    }
    stages = order.setdefault("stages", {})
    stages["STAGE_0_GLOBAL_DOCUMENT_REGISTRY_RESOLUTION"] = {
        "state": "PASS" if document_ids else "RESEARCH_REQUIRED",
        "evidence_refs": [
            str(GLOBAL_REGISTRY.relative_to(ROOT)).replace("\\", "/"),
            str(GLOBAL_BINDINGS.relative_to(ROOT)).replace("\\", "/"),
        ],
        "documents_total": len(document_ids),
    }
    if not document_ids:
        order.setdefault("gaps", []).append({
            "type": "GLOBAL_DOCUMENT_BINDING_GAP",
            "role_id": role_id,
            "knowledge_base_id": kb_id or None,
            "blocking_for_maturity_claim": True,
        })
    order["updated_at_epoch"] = time.time()
    return order


def persist_order(order: dict) -> None:
    order_path = ORDER_ROOT / f"{order['order_id']}.json"
    write_json(order_path, order)
    write_json(latest_path(str(order["role_id"])), order)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and run one FATHER role library order")
    parser.add_argument("--role", required=True)
    parser.add_argument("--maturity", default="MIN", choices=("MIN", "MEDIUM", "MAX"))
    parser.add_argument("--mode", default="AUTO_BOUNDED", choices=("AUTO_BOUNDED", "REVIEW_EACH_STAGE"))
    parser.add_argument("--sources", default=None)
    parser.add_argument("--create-only", action="store_true")
    args = parser.parse_args()

    registry_rc = build_global_registry()
    if registry_rc != 0:
        return registry_rc

    create_cmd = [
        sys.executable,
        str(CREATE),
        "--role", args.role,
        "--maturity", args.maturity,
        "--mode", args.mode,
    ]
    if args.sources:
        create_cmd.extend(["--sources", args.sources])
    rc = subprocess.run(create_cmd, cwd=str(ROOT), env=os.environ.copy(), check=False).returncode
    if rc != 0:
        return int(rc)

    order = attach_global_registry(load_latest(args.role))
    persist_order(order)
    order_id = str(order["order_id"])
    if args.create_only:
        print(json.dumps({
            "status": "CREATED",
            "order_id": order_id,
            "role_id": order["role_id"],
            "maturity_target": order["maturity_target"],
            "current_stage": order["current_stage"],
            "global_document_refs_total": order["global_document_registry"]["resolved_document_refs_total"],
            "global_document_registry": str(GLOBAL_REGISTRY.relative_to(ROOT)).replace("\\", "/"),
            "global_applicability_bindings": str(GLOBAL_BINDINGS.relative_to(ROOT)).replace("\\", "/"),
        }, ensure_ascii=False, indent=2))
        return 0

    run_cmd = [sys.executable, str(RUN), "--order", order_id]
    return int(subprocess.run(run_cmd, cwd=str(ROOT), env=os.environ.copy(), check=False).returncode)


if __name__ == "__main__":
    raise SystemExit(main())
