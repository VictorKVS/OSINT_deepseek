from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "osint_control_center" / "searches"
PROFILE = ROOT / "config" / "architect_telegram_acquisition_profile.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
    value = re.sub(r"[^0-9A-Za-zА-Яа-яЁё]+", "-", text.strip().casefold()).strip("-")
    return (value[:80] or "query")


def credentials() -> tuple[int, str, Path]:
    profile = load_json(PROFILE)["telegram"]
    api_id = os.getenv(str(profile.get("api_id_env", "TELEGRAM_API_ID")), "").strip()
    api_hash = os.getenv(str(profile.get("api_hash_env", "TELEGRAM_API_HASH")), "").strip()
    session_raw = os.getenv(str(profile.get("session_env", "TELEGRAM_SESSION_PATH")), "").strip()
    if not api_id or not api_hash:
        raise RuntimeError("Telegram credentials are not present in the Control Center process")
    session = Path(session_raw) if session_raw else ROOT / str(profile["default_session_path"])
    if not session.is_absolute():
        session = ROOT / session
    return int(api_id), api_hash, session


async def run(query: str, limit: int) -> dict[str, Any]:
    from telethon import TelegramClient  # type: ignore

    api_id, api_hash, session = credentials()
    client = TelegramClient(str(session), api_id, api_hash)
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("shared Telethon session is not authorized")
        async for message in client.iter_messages(None, search=query, limit=limit):
            file_obj = getattr(message, "file", None)
            chat_id = str(getattr(message, "chat_id", None) or "unknown")
            message_id = int(getattr(message, "id", 0) or 0)
            username = None
            title = None
            try:
                chat = await message.get_chat()
                username = str(getattr(chat, "username", None) or "").strip() or None
                title = str(getattr(chat, "title", None) or getattr(chat, "first_name", None) or "").strip() or None
            except Exception:
                pass
            rows.append({
                "chat_id": chat_id,
                "chat_title": title,
                "chat_username": username,
                "message_id": message_id,
                "source_url": f"https://t.me/{username}/{message_id}" if username and message_id else None,
                "date": getattr(getattr(message, "date", None), "isoformat", lambda: None)(),
                "text": str(getattr(message, "message", None) or "")[:700],
                "has_file": file_obj is not None,
                "file_name": str(getattr(file_obj, "name", None) or "") if file_obj else None,
                "mime_type": str(getattr(file_obj, "mime_type", None) or "") if file_obj else None,
                "file_size": getattr(file_obj, "size", None) if file_obj else None,
            })
    finally:
        await client.disconnect()
    elapsed = time.perf_counter() - started
    return {
        "record_type": "OSINT_CONTROL_CENTER_QUERY_PROBE",
        "status": "PASS",
        "query": query,
        "source": "TELEGRAM",
        "probe_only": True,
        "results_total": len(rows),
        "files_total": sum(1 for row in rows if row["has_file"]),
        "elapsed_seconds": elapsed,
        "results": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    query = " ".join(args.query.split()).strip()
    if not query or len(query) > 240:
        raise SystemExit("query must contain 1..240 characters")
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = REPORT_ROOT / f"{stamp}_{slug(query)}.json"
    try:
        report = asyncio.run(run(query, max(1, min(args.limit, 100))))
    except Exception as exc:
        report = {"record_type": "OSINT_CONTROL_CENTER_QUERY_PROBE", "status": "FATAL", "query": query, "error": f"{type(exc).__name__}: {exc}", "probe_only": True}
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report.get(k) for k in ("status", "query", "results_total", "files_total", "elapsed_seconds", "error") if k in report}, ensure_ascii=False, indent=2))
    print(f"Report: {path.relative_to(ROOT)}")
    return 0 if report.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
