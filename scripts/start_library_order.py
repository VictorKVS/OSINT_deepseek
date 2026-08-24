from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREATE = ROOT / "scripts" / "create_library_order.py"
RUN = ROOT / "scripts" / "run_library_order.py"
ORDER_ROOT = ROOT / "reports" / "library_orders"


def load_latest(role_id: str) -> dict:
    path = ORDER_ROOT / f"LATEST_{role_id.upper().replace('-', '_')}.json"
    if not path.is_file():
        raise RuntimeError(f"latest order was not created: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and run one FATHER role library order")
    parser.add_argument("--role", required=True)
    parser.add_argument("--maturity", default="MIN", choices=("MIN", "MEDIUM", "MAX"))
    parser.add_argument("--mode", default="AUTO_BOUNDED", choices=("AUTO_BOUNDED", "REVIEW_EACH_STAGE"))
    parser.add_argument("--sources", default=None)
    parser.add_argument("--create-only", action="store_true")
    args = parser.parse_args()

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

    order = load_latest(args.role)
    order_id = str(order["order_id"])
    if args.create_only:
        print(json.dumps({
            "status": "CREATED",
            "order_id": order_id,
            "role_id": order["role_id"],
            "maturity_target": order["maturity_target"],
            "current_stage": order["current_stage"],
        }, ensure_ascii=False, indent=2))
        return 0

    run_cmd = [sys.executable, str(RUN), "--order", order_id]
    return int(subprocess.run(run_cmd, cwd=str(ROOT), env=os.environ.copy(), check=False).returncode)


if __name__ == "__main__":
    raise SystemExit(main())
