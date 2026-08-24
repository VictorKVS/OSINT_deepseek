from __future__ import annotations

import asyncio
import inspect
import json
from pathlib import Path
from typing import Any

from scripts.download_progress_registry import DownloadProgressRegistry
from scripts import run_team_role_acquisition as base


def _item_id_from_message(message: Any) -> str:
    return f"{getattr(message, 'chat_id', 'unknown')}:{int(getattr(message, 'id', 0) or 0)}"


def _message_fields(message: Any, file_arg: Any) -> dict[str, Any]:
    file_obj = getattr(message, "file", None)
    file_name = str(getattr(file_obj, "name", None) or "").strip()
    if not file_name and isinstance(file_arg, (str, Path)):
        file_name = Path(str(file_arg)).name
    size = getattr(file_obj, "size", None)
    return {
        "chat_id": str(getattr(message, "chat_id", None) or "unknown"),
        "message_id": int(getattr(message, "id", 0) or 0),
        "file_name": file_name or None,
        "file_size": int(size) if isinstance(size, int) else None,
        "total_bytes": int(size) if isinstance(size, int) else 0,
        "destination": str(file_arg) if isinstance(file_arg, (str, Path)) else None,
        "status": "QUEUED",
    }


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "status", "role_id", "knowledge_base_id", "role_priority", "stream_id", "search_streams",
        "download_streams", "queries_total", "topics_total", "search_hits_total", "media_candidates_total",
        "downloaded_total", "payload_reused_total", "skipped_type_total", "skipped_size_total", "errors_total",
        "bytes_downloaded", "elapsed_seconds", "throughput_files_per_second", "throughput_megabytes_per_second",
        "useful_candidate_ratio", "speedup_vs_1_stream_pct", "report_path", "error",
    )
    return {key: report.get(key) for key in keys if key in report}


def _reconcile(registry: DownloadProgressRegistry, report: dict[str, Any]) -> None:
    for row in report.get("downloads", []) or []:
        item_id = f"{row.get('chat_id')}:{int(row.get('message_id') or 0)}"
        size = int(row.get("file_size") or 0)
        registry.ensure_item(item_id, chat_id=row.get("chat_id"), message_id=row.get("message_id"), file_name=row.get("file_name"), source_url=row.get("source_url"), total_bytes=size)
        registry.update(item_id, status="DOWNLOADED", bytes_received=size, total_bytes=size, sha256=row.get("sha256"), local_path=row.get("local_path"), force=True)
    for row in report.get("reused", []) or []:
        item_id = f"{row.get('chat_id')}:{int(row.get('message_id') or 0)}"
        size = int(row.get("file_size") or 0)
        registry.ensure_item(item_id, chat_id=row.get("chat_id"), message_id=row.get("message_id"), file_name=row.get("file_name"), source_url=row.get("source_url"), total_bytes=size)
        registry.update(item_id, status="REUSED", bytes_received=size, total_bytes=size, sha256=row.get("sha256"), local_path=row.get("local_path"), force=True)


async def _run_with_live_progress(args) -> dict[str, Any]:
    role_id = str(args.role).upper().replace("-", "_")
    registry = DownloadProgressRegistry(role_id)
    registry.start()

    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for live acquisition telemetry") from exc

    original = TelegramClient.download_media

    async def instrumented_download_media(self, message, file=None, *call_args, **call_kwargs):
        item_id = _item_id_from_message(message)
        fields = _message_fields(message, file)
        registry.ensure_item(item_id, **fields)
        original_callback = call_kwargs.get("progress_callback")

        def progress(received, total):
            registry.update(item_id, status="DOWNLOADING", bytes_received=int(received or 0), total_bytes=int(total or fields.get("total_bytes") or 0))
            if original_callback is not None:
                result = original_callback(received, total)
                if inspect.isawaitable(result):
                    return result
            return None

        call_kwargs["progress_callback"] = progress
        try:
            result = await original(self, message, file, *call_args, **call_kwargs)
            total = int(fields.get("total_bytes") or 0)
            registry.update(item_id, status="HASHING", bytes_received=total or None, total_bytes=total or None, force=True)
            return result
        except Exception as exc:
            registry.update(item_id, status="FAILED", error=f"{type(exc).__name__}: {exc}", force=True)
            raise

    TelegramClient.download_media = instrumented_download_media
    try:
        report = await base._run(args)
        _reconcile(registry, report)
        registry.finish()
        return report
    finally:
        TelegramClient.download_media = original


def main() -> int:
    args = base.build_parser().parse_args()
    try:
        report = asyncio.run(_run_with_live_progress(args))
    except Exception as exc:
        report = {
            "record_type": "TEAM_ROLE_TELEGRAM_ACQUISITION_RUN",
            "schema_version": "1.0",
            "status": "FATAL",
            "role_id": str(args.role).upper(),
            "error": f"{type(exc).__name__}: {exc}",
            "kb_auto_promotion": False,
        }
    print(json.dumps(_compact(report), ensure_ascii=False, indent=2))
    return 0 if report.get("status") in {"PASS", "PASS_WITH_ERRORS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
