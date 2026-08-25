from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "security_current_only" / "LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json"
META_DIR = ROOT / "data" / "security_current_only" / "metadata"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    if not REPORT.is_file():
        raise SystemExit(f"master report missing: {REPORT}")

    environment_id = os.environ.get("FATHER_EXECUTION_ENVIRONMENT_ID", "GITHUB_ACTIONS_UBUNTU_LATEST")
    run_id = os.environ.get("GITHUB_RUN_ID")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
    head_sha = os.environ.get("GITHUB_SHA")

    report = load_json(REPORT)
    report["execution_environment_id"] = environment_id
    report["execution_environment_class"] = "CLOUD_CI"
    report["github_run_id"] = run_id
    report["github_run_attempt"] = run_attempt
    report["github_head_sha"] = head_sha
    report["environment_stamped_at"] = utc_now()

    for row in report.get("results", []) or []:
        if not isinstance(row, dict):
            continue
        row["execution_environment_id"] = environment_id
        row["github_run_id"] = run_id
        row["github_head_sha"] = head_sha

        did = str(row.get("document_id") or "").strip()
        status = str(row.get("status") or "")
        if not did or status not in {"DOWNLOADED", "REUSED_EXACT"}:
            continue
        meta_path = META_DIR / f"{did}.json"
        if not meta_path.is_file():
            continue
        try:
            meta = load_json(meta_path)
        except Exception:
            continue
        meta["execution_environment_id"] = environment_id
        meta["execution_environment_class"] = "CLOUD_CI"
        meta["github_run_id"] = run_id
        meta["github_head_sha"] = head_sha
        meta["environment_stamped_at"] = utc_now()
        meta["legal_truth_eligible"] = False
        meta["kb_auto_promotion"] = False
        write_json(meta_path, meta)

    write_json(REPORT, report)
    print(json.dumps({
        "status": report.get("status"),
        "execution_environment_id": environment_id,
        "github_run_id": run_id,
        "documents_unique_total": report.get("documents_unique_total"),
        "downloaded_total": report.get("downloaded_total"),
        "reused_exact_total": report.get("reused_exact_total"),
        "reused_declared_local_a0_total": report.get("reused_declared_local_a0_total"),
        "failed_total": report.get("failed_total"),
        "need_official_source_total": report.get("need_official_source_total"),
        "bytes_downloaded": report.get("bytes_downloaded"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
