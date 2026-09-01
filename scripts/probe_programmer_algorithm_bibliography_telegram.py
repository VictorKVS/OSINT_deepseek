from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import probe_programmer_bibliography_telegram as base  # noqa: E402

TARGETS_PATH = ROOT / "config" / "programmer_algorithm_bibliography_targets.json"
PROFILE_PATH = ROOT / "config" / "architect_telegram_acquisition_profile.json"
REPORT_PATH = ROOT / "reports" / "team_role_telegram" / "LATEST_PROGRAMMER_ALGORITHM_BIBLIOGRAPHY_PROBE.json"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


async def _run(priority: str) -> dict[str, Any]:
    started = time.perf_counter()
    registry = _load_json(TARGETS_PATH)
    profile = _load_json(PROFILE_PATH)
    policy = registry["policy"]
    api_id, api_hash, session = base._load_credentials(profile)

    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for algorithm bibliography probe") from exc

    all_targets = [row for row in registry.get("targets", []) if isinstance(row, dict)]
    selected = all_targets if priority == "ALL" else [row for row in all_targets if row.get("priority") == priority]

    client = TelegramClient(str(session), api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("shared Telethon session is not authorized")
        semaphore = asyncio.Semaphore(min(5, max(1, int(policy.get("max_parallel_streams", 5)))))
        allowed_exts = {str(value).casefold() for value in policy.get("allowed_extensions", [])}
        tasks = [
            asyncio.create_task(
                base._probe_target(
                    client,
                    target,
                    semaphore=semaphore,
                    limit=max(1, int(policy.get("max_results_per_query", 20))),
                    max_candidates=max(1, int(policy.get("max_candidates_per_target", 5))),
                    allowed_exts=allowed_exts,
                )
            )
            for target in selected
        ]
        rows = [await task for task in asyncio.as_completed(tasks)]
    finally:
        await client.disconnect()

    rows.sort(key=lambda row: row["id"])
    found = sum(1 for row in rows if row["status"] == "FOUND_CANDIDATE")
    ambiguous = sum(1 for row in rows if row["status"] == "AMBIGUOUS")
    not_found = sum(1 for row in rows if row["status"] == "NOT_FOUND")
    errors_total = sum(len(row.get("errors") or []) for row in rows)
    elapsed = time.perf_counter() - started

    track_counts: dict[str, int] = {}
    source_by_id = {str(row.get("id")): row for row in selected}
    for row in rows:
        track = str(source_by_id.get(str(row.get("id")), {}).get("track") or "UNKNOWN")
        track_counts[track] = track_counts.get(track, 0) + 1

    report = {
        "record_type": "PROGRAMMER_ALGORITHM_BIBLIOGRAPHY_TELEGRAM_PROBE",
        "schema_version": "1.0",
        "status": "PASS" if errors_total == 0 else "PASS_WITH_ERRORS",
        "probe_only": True,
        "downloaded_total": 0,
        "priority_filter": priority,
        "targets_total": len(rows),
        "found_candidate_total": found,
        "ambiguous_total": ambiguous,
        "not_found_total": not_found,
        "errors_total": errors_total,
        "availability_ratio": (found / len(rows)) if rows else None,
        "elapsed_seconds": elapsed,
        "max_parallel_streams": min(5, max(1, int(policy.get("max_parallel_streams", 5)))),
        "speedup_vs_1_stream_pct": None,
        "track_counts": dict(sorted(track_counts.items())),
        "targets": rows,
        "rights_note": "Telegram match is discovery evidence only. No payload is downloaded by this probe.",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Telegram for the PROGRAMMER algorithms/data-structures bibliography wave.")
    parser.add_argument("--priority", choices=("ALL", "P0", "P1"), default="ALL")
    args = parser.parse_args()
    try:
        report = asyncio.run(_run(args.priority))
    except Exception as exc:
        report = {
            "record_type": "PROGRAMMER_ALGORITHM_BIBLIOGRAPHY_TELEGRAM_PROBE",
            "status": "FATAL",
            "probe_only": True,
            "downloaded_total": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }
    compact_keys = (
        "status",
        "probe_only",
        "priority_filter",
        "targets_total",
        "found_candidate_total",
        "ambiguous_total",
        "not_found_total",
        "errors_total",
        "availability_ratio",
        "elapsed_seconds",
        "max_parallel_streams",
        "speedup_vs_1_stream_pct",
        "error",
    )
    print(json.dumps({key: report.get(key) for key in compact_keys if key in report}, ensure_ascii=False, indent=2))
    print(f"Report: {REPORT_PATH.relative_to(ROOT).as_posix()}")
    return 0 if report.get("status") in {"PASS", "PASS_WITH_ERRORS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
