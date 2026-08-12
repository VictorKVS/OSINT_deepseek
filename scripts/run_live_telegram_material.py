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
from father_osint.storage import MaterialStore
from father_osint.transports.telethon import TelethonTransport


DEFAULT_CONFIG = REPO_ROOT / "legacy/telegram/config.yaml"
DEFAULT_SESSION = REPO_ROOT / "legacy/telegram/reader_session"
DEFAULT_OUTPUT = REPO_ROOT / "data/m5_live_telegram"


def load_local_config(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError(
            "PyYAML is required only for this live operator runner"
        ) from exc

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="M5 live proof: Telethon -> TelegramMessage -> Material -> MaterialStore"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--session", type=Path, default=DEFAULT_SESSION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-items", type=int, default=10)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_items <= 0:
        raise SystemExit("--max-items must be > 0")

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

    store.save_task(task)

    materials = []
    payloads_reused = 0
    for material in collector.collect(task):
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

    summary = {
        "status": "PASS" if materials else "NO_MATERIAL",
        "task_id": task.task_id,
        "package_id": package.package_id,
        "materials": len(materials),
        "payloads_reused": payloads_reused,
        "output": str(args.output),
        "first_material": None,
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

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if materials else 2


if __name__ == "__main__":
    raise SystemExit(main())
