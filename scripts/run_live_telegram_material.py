from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.collectors.telegram import TelegramCollector
from father_osint.models import MaterialPackage, ResearchTask
from father_osint.reasoning import DeterministicEvidenceAnalyst, DeterministicSocrates
from father_osint.reliability import DurableObservationWriter, JsonCheckpointStore
from father_osint.storage import MaterialStore
from father_osint.transports.telethon import TelethonTransport


DEFAULT_CONFIG = REPO_ROOT / "legacy/telegram/config.yaml"
DEFAULT_SESSION = REPO_ROOT / "legacy/telegram/reader_session"
DEFAULT_OUTPUT = REPO_ROOT / "data/m5_live_telegram"


def load_local_config(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required only for this live operator runner") from exc
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def count_jsonl_records(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def count_raw_payload_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.iterdir() if item.is_file())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M5 live Telegram evidence/restart proof")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--session", type=Path, default=DEFAULT_SESSION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-items", type=int, default=10)
    parser.add_argument("--expect-reuse-min", type=int, default=0)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=None,
        help="JSON checkpoint path; defaults to <output>/checkpoints.json when --resume is used",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Enable save-before-checkpoint and prove restart/reconciliation semantics",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_items <= 0:
        raise SystemExit("--max-items must be > 0")
    if args.expect_reuse_min < 0:
        raise SystemExit("--expect-reuse-min must be >= 0")

    config = load_local_config(args.config)
    telegram = config["telegram"]
    channels = telegram.get("channels", [])
    per_channel_limit = telegram.get("collection", {}).get("limit_per_channel", 100)

    task = ResearchTask(
        question="M5 live Telegram canonical Material proof",
        source_types=["telegram"],
        max_items=args.max_items,
        requested_by="m5-live-proof",
    )
    transport = TelethonTransport(
        api_id=int(telegram["api_id"]),
        api_hash=str(telegram["api_hash"]),
        session_path=args.session,
        channels=channels,
        per_channel_limit=int(per_channel_limit),
    )
    collector = TelegramCollector(transport)
    store = MaterialStore(args.output)

    checkpoint_path = args.checkpoint or (args.output / "checkpoints.json")
    checkpoint_store = JsonCheckpointStore(checkpoint_path) if args.resume else None
    durable_writer = DurableObservationWriter(store, checkpoint_store) if checkpoint_store else None

    material_records_before = count_jsonl_records(store.materials_file)
    raw_payload_files_before = count_raw_payload_files(store.raw_dir)
    store.save_task(task)

    materials = []
    payloads_reused = 0
    resumed_sources = 0
    checkpoint_commits = 0
    seen_source_keys: set[str] = set()

    for material in collector.collect(task):
        source_key = str(material.metadata.get("chat_id") or material.source_locator)
        cursor = str(material.metadata.get("message_id") or material.content_hash)

        if checkpoint_store and source_key not in seen_source_keys:
            if checkpoint_store.load(material.source_type, source_key) is not None:
                resumed_sources += 1
            seen_source_keys.add(source_key)

        if durable_writer:
            payloads_reused += int(
                durable_writer.save_then_checkpoint(
                    material=material,
                    source_key=source_key,
                    cursor=cursor,
                )
            )
            checkpoint_commits += 1
        else:
            payloads_reused += int(store.save_material(material))
        materials.append(material)

    package = MaterialPackage(
        task_id=task.task_id,
        materials=materials,
        payloads_reused=payloads_reused,
        stop_reason="completed",
        notes="M5 live Telethon reference adapter proof",
    )
    store.save_package(package)

    analysis = DeterministicEvidenceAnalyst().analyze(package)
    critique = DeterministicSocrates().critique(package, analysis)

    material_records_after = count_jsonl_records(store.materials_file)
    raw_payload_files_after = count_raw_payload_files(store.raw_dir)
    observations_appended = material_records_after - material_records_before
    new_raw_payload_files = raw_payload_files_after - raw_payload_files_before

    reuse_expectation_met = payloads_reused >= args.expect_reuse_min
    observations_preserved = observations_appended == len(materials)
    reasoning_passed = critique.verdict == "PASS"
    restart_reconciliation_passed = (
        not args.resume
        or (
            checkpoint_commits == len(materials)
            and observations_preserved
            and all(
                checkpoint_store.load(
                    material.source_type,
                    str(material.metadata.get("chat_id") or material.source_locator),
                ) is not None
                for material in materials
            )
        )
    )

    if not materials:
        status, exit_code = "NO_MATERIAL", 2
    elif not reuse_expectation_met:
        status, exit_code = "REUSE_EXPECTATION_FAILED", 3
    elif not observations_preserved:
        status, exit_code = "OBSERVATION_APPEND_FAILED", 4
    elif not reasoning_passed:
        status, exit_code = "REASONING_REVIEW_FAILED", 5
    elif not restart_reconciliation_passed:
        status, exit_code = "RESTART_RECONCILIATION_FAILED", 6
    else:
        status, exit_code = "PASS", 0

    summary = {
        "status": status,
        "task_id": task.task_id,
        "package_id": package.package_id,
        "materials": len(materials),
        "payloads_reused": payloads_reused,
        "expect_reuse_min": args.expect_reuse_min,
        "reuse_expectation_met": reuse_expectation_met,
        "material_records_before": material_records_before,
        "material_records_after": material_records_after,
        "observations_appended": observations_appended,
        "observations_preserved": observations_preserved,
        "raw_payload_files_before": raw_payload_files_before,
        "raw_payload_files_after": raw_payload_files_after,
        "new_raw_payload_files": new_raw_payload_files,
        "analysis_claims": len(analysis.claims),
        "analysis_limitations": analysis.limitations,
        "socrates_verdict": critique.verdict,
        "socrates_challenged_claims": len(critique.challenged_claim_ids),
        "reasoning_passed": reasoning_passed,
        "checkpoint_enabled": checkpoint_store is not None,
        "resume_requested": args.resume,
        "resumed_sources": resumed_sources,
        "checkpoint_commits": checkpoint_commits,
        "restart_reconciliation_passed": restart_reconciliation_passed,
        "checkpoint_path": str(checkpoint_path) if checkpoint_store else None,
        "output": str(args.output),
        "first_material": None,
        "first_claim": None,
    }

    if materials:
        first = materials[0]
        summary["first_material"] = {
            "material_id": first.material_id,
            "source_type": first.source_type,
            "source_locator": first.source_locator,
            "title": first.title,
            "published_at": first.published_at,
            "content_hash": first.content_hash,
            "chat_id": first.metadata.get("chat_id"),
            "message_id": first.metadata.get("message_id"),
            "transport": first.metadata.get("transport"),
        }

    if analysis.claims:
        first_claim = analysis.claims[0]
        summary["first_claim"] = {
            "claim_id": first_claim.claim_id,
            "statement": first_claim.statement,
            "evidence_ids": first_claim.evidence_ids,
            "confidence": first_claim.confidence,
        }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
