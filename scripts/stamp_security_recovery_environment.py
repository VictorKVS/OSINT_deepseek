from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "security_current_only" / "LATEST_FSTEC_OFFICIAL_RECOVERY_RUN.json"


def main() -> int:
    environment_id = os.environ.get("FATHER_EXECUTION_ENVIRONMENT_ID", "UNSPECIFIED_EXECUTION_ENVIRONMENT")
    if not REPORT.is_file():
        print(f"report missing: {REPORT}")
        return 2

    payload = json.loads(REPORT.read_text(encoding="utf-8"))
    payload["execution_environment_id"] = environment_id
    for row in payload.get("results", []) or []:
        if isinstance(row, dict):
            row["execution_environment_id"] = environment_id
            for attempt in row.get("route_attempts", []) or []:
                if isinstance(attempt, dict):
                    attempt["execution_environment_id"] = environment_id

    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "execution_environment_id": environment_id,
        "report": REPORT.relative_to(ROOT).as_posix(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
