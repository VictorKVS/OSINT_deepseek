from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROLE_REGISTRY = ROOT / "config" / "team_role_material_registry.json"
PROFILE = ROOT / "config" / "architect_telegram_acquisition_profile.json"
OUTPUT_ROOT = ROOT / "data" / "team_role_telegram"
RECEIPT_ROOT = ROOT / "reports" / "osint_control_center" / "download_receipts"

from scripts.download_progress_registry import DownloadProgressRegistry  # noqa: E402
from scripts.run_architect_telegram_acquisition import (  # noqa: E402
    _load_credentials,
    _local_display_path,
    _safe_name,
    _sha256_file,
)
from scripts.run_team_role_acquisition import _scan_existing_hashes  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_context(role_id: str, target_id: str) -> tuple[dict[str, Any], str, int]:
    registry = load_json(ROLE_REGISTRY)
    normalized = role_id.strip().upper().replace("-", "_")
    for role in registry.get("roles", []):
        if str(role.get("role_id", "")).upper() != normalized:
            continue
        for index, topic in enumerate(role.get("topics", []), start=1):
            expected = f"{normalized}-TOPIC-{index:02d}"
            if expected == target_id:
                return role, str(topic), index
        raise RuntimeError(f"target {target_id!r} does not belong to role {normalized}")
    raise RuntimeError(f"unknown role {role_id!r}")


def trace_context() -> dict[str, Any]:
    return {
        "trace_id": os.getenv("FATHER_TRACE_ID"),
        "correlation_id": os.getenv("FATHER_CORRELATION_ID"),
        "task_id": os.getenv("FATHER_TASK_ID"),
        "command_id": os.getenv("FATHER_COMMAND_ID"),
        "parent_command_id": os.getenv("FATHER_PARENT_COMMAND_ID"),
    }


async def run(args: argparse.Namespace) -> dict[str, Any]:
    role, topic, _ = resolve_context(args.role, args.target_id)
    role_id = str(role["role_id"])
    profile = load_json(PROFILE)
    allowed_exts = {str(value).casefold() for value in profile["inventory"]["downloadable_extensions"]}
    max_bytes = int(args.max_file_size_mb) * 1024 * 1024
    api_id, api_hash, session = _load_credentials(profile)

    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for targeted Telegram download") from exc

    trace = trace_context()
    registry_key = f"UI_{trace.get('command_id') or int(time.time())}_{role_id}_{args.message_id}"
    progress = DownloadProgressRegistry(role_id, registry_key=registry_key, context={
        **trace,
        "target_id": args.target_id,
        "topic": topic,
        "source": "TELEGRAM",
        "mode": "USER_SELECTED_ITEM",
    })

    output_dir = OUTPUT_ROOT / role_id.casefold() / _safe_name(args.target_id.casefold())
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_hashes, existing_locations = _scan_existing_hashes(
        [ROOT / "data" / "architect_telegram_downloads", OUTPUT_ROOT],
        max_bytes=max_bytes,
    )

    client = TelegramClient(str(session), api_id, api_hash)
    started = time.perf_counter()
    item_id = f"{args.chat_id}:{args.message_id}"
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized")

        entity_ref: Any
        if args.chat_username:
            entity_ref = args.chat_username.lstrip("@")
        else:
            try:
                entity_ref = int(args.chat_id)
            except ValueError as exc:
                raise RuntimeError("chat_id is not numeric and chat_username was not provided") from exc
        entity = await client.get_entity(entity_ref)
        message = await client.get_messages(entity, ids=int(args.message_id))
        if message is None:
            raise RuntimeError("Telegram message was not found in the accessible account scope")
        file_obj = getattr(message, "file", None)
        if file_obj is None:
            raise RuntimeError("selected Telegram message has no downloadable file")

        file_name = str(getattr(file_obj, "name", None) or args.expected_file_name or "").strip()
        ext = str(getattr(file_obj, "ext", None) or "").strip().casefold()
        if not ext and file_name:
            ext = Path(file_name).suffix.casefold()
        mime = str(getattr(file_obj, "mime_type", None) or "").strip() or None
        size_raw = getattr(file_obj, "size", None)
        size = int(size_raw) if isinstance(size_raw, int) else 0
        if ext not in allowed_exts:
            raise RuntimeError(f"file extension {ext or '<none>'} is outside the acquisition allowlist")
        if mime and mime.casefold().startswith(("video/", "audio/", "image/")):
            raise RuntimeError(f"media type {mime} is outside the document acquisition profile")
        if size and size > max_bytes:
            raise RuntimeError(f"file is larger than the configured {args.max_file_size_mb} MB limit")

        original = _safe_name(file_name, fallback=f"telegram_{args.message_id}{ext or '.bin'}")
        destination = output_dir / f"{_safe_name(args.chat_id)}_{args.message_id}_{original}"
        source_url = f"https://t.me/{args.chat_username.lstrip('@')}/{args.message_id}" if args.chat_username else None
        progress.start([{
            "item_id": item_id,
            "role_id": role_id,
            "knowledge_base_id": role.get("knowledge_base_id"),
            "target_id": args.target_id,
            "topic": topic,
            "chat_id": args.chat_id,
            "chat_username": args.chat_username,
            "message_id": int(args.message_id),
            "source_url": source_url,
            "file_name": original,
            "file_size": size,
            "total_bytes": size,
            "status": "QUEUED",
        }])

        if destination.exists():
            digest = _sha256_file(destination)
            progress.update(
                item_id,
                status="REUSED",
                bytes_received=destination.stat().st_size,
                total_bytes=destination.stat().st_size,
                sha256=digest,
                local_path=_local_display_path(destination),
                force=True,
            )
            progress.finish()
            return {
                "status": "REUSED",
                "role_id": role_id,
                "knowledge_base_id": role.get("knowledge_base_id"),
                "target_id": args.target_id,
                "topic": topic,
                "file_name": original,
                "local_path": _local_display_path(destination),
                "sha256": digest,
                "source_url": source_url,
                "reason": "destination already exists",
                **trace,
            }

        progress.update(item_id, status="DOWNLOADING", bytes_received=0, total_bytes=size, force=True)

        def on_progress(received: int, total: int) -> None:
            progress.update(item_id, status="DOWNLOADING", bytes_received=received, total_bytes=total or size)

        downloaded = await client.download_media(message, file=str(destination), progress_callback=on_progress)
        if not downloaded:
            raise RuntimeError("download_media returned no path")
        path = Path(str(downloaded))
        if not path.is_file():
            raise RuntimeError(f"downloaded path is not a file: {path}")

        actual_size = path.stat().st_size
        progress.update(item_id, status="HASHING", bytes_received=actual_size, total_bytes=actual_size, force=True)
        digest = _sha256_file(path)
        if digest in existing_hashes:
            existing = existing_locations.get(digest)
            try:
                path.unlink()
            except OSError:
                pass
            progress.update(
                item_id,
                status="REUSED",
                bytes_received=actual_size,
                total_bytes=actual_size,
                sha256=digest,
                local_path=existing,
                force=True,
            )
            final_status = "REUSED"
            local_path = existing
            reason = "SHA-256 already exists in the local acquisition corpus"
        else:
            progress.update(
                item_id,
                status="DOWNLOADED",
                bytes_received=actual_size,
                total_bytes=actual_size,
                sha256=digest,
                local_path=_local_display_path(path),
                force=True,
            )
            final_status = "DOWNLOADED"
            local_path = _local_display_path(path)
            reason = None
        progress.finish()

        return {
            "status": final_status,
            "role_id": role_id,
            "knowledge_base_id": role.get("knowledge_base_id"),
            "target_id": args.target_id,
            "topic": topic,
            "chat_id": args.chat_id,
            "chat_username": args.chat_username,
            "message_id": int(args.message_id),
            "source_url": source_url,
            "file_name": original,
            "file_size": actual_size,
            "mime_type": mime,
            "local_path": local_path,
            "sha256": digest,
            "elapsed_seconds": time.perf_counter() - started,
            "kb_auto_promotion": False,
            "reason": reason,
            **trace,
        }
    except Exception as exc:
        progress.ensure_item(
            item_id,
            role_id=role_id,
            target_id=args.target_id,
            topic=topic,
            chat_id=args.chat_id,
            message_id=int(args.message_id),
            file_name=args.expected_file_name or f"message_{args.message_id}",
        )
        progress.update(item_id, status="FAILED", error=f"{type(exc).__name__}: {exc}", force=True)
        progress.finish()
        raise
    finally:
        await client.disconnect()


def main() -> int:
    parser = argparse.ArgumentParser(description="Download one user-selected Telegram document into the role/topic acquisition folder")
    parser.add_argument("--role", required=True)
    parser.add_argument("--target-id", required=True)
    parser.add_argument("--chat-id", required=True)
    parser.add_argument("--message-id", type=int, required=True)
    parser.add_argument("--chat-username", default=None)
    parser.add_argument("--expected-file-name", default=None)
    parser.add_argument("--max-file-size-mb", type=int, default=100)
    args = parser.parse_args()

    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    receipt = RECEIPT_ROOT / f"{stamp}_{_safe_name(args.role)}_{args.message_id}.json"
    try:
        report = asyncio.run(run(args))
        code = 0
    except Exception as exc:
        report = {
            "status": "FAILED",
            "role_id": args.role.upper(),
            "target_id": args.target_id,
            "chat_id": args.chat_id,
            "message_id": args.message_id,
            "error": f"{type(exc).__name__}: {exc}",
            "kb_auto_promotion": False,
            **trace_context(),
        }
        code = 1
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: report.get(key) for key in ("status", "role_id", "target_id", "topic", "file_name", "file_size", "local_path", "sha256", "elapsed_seconds", "error") if key in report}
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    print(f"Receipt: {receipt.relative_to(ROOT)}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
