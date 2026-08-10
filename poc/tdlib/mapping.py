from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from father_osint.collectors.telegram import TelegramMessage


def _formatted_text_text(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    text = value.get("text")
    return text if isinstance(text, str) else None


def extract_message_text(content: dict[str, Any] | None) -> str:
    """Extract text/caption without interpreting Telegram content semantically."""
    if not isinstance(content, dict):
        return ""

    content_type = content.get("@type")
    if content_type == "messageText":
        return _formatted_text_text(content.get("text")) or ""

    caption = _formatted_text_text(content.get("caption"))
    return caption or ""


def unix_to_iso(value: Any) -> str | None:
    if not isinstance(value, int) or value <= 0:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()


def map_tdlib_message(
    raw: dict[str, Any],
    *,
    chat_title: str | None = None,
    public_username: str | None = None,
    author: str | None = None,
) -> TelegramMessage:
    """Map one TDLib message JSON object to the frozen transport-neutral contract.

    TDLib-specific fields remain in metadata; no TDLib object escapes upward.
    """
    chat_id = raw.get("chat_id")
    message_id = raw.get("id")
    if chat_id is None or message_id is None:
        raise ValueError("TDLib message must contain chat_id and id")

    username = public_username.lstrip("@") if public_username else None
    url = f"https://t.me/{username}/{message_id}" if username else None

    metadata: dict[str, Any] = {
        "tdlib_content_type": (raw.get("content") or {}).get("@type")
        if isinstance(raw.get("content"), dict)
        else None,
        "is_channel_post": raw.get("is_channel_post"),
        "sender_id": raw.get("sender_id"),
        "reply_to": raw.get("reply_to"),
        "forward_info": raw.get("forward_info"),
        "media_album_id": raw.get("media_album_id"),
        "edit_date": raw.get("edit_date"),
    }
    metadata = {key: value for key, value in metadata.items() if value is not None}

    return TelegramMessage(
        chat_id=str(chat_id),
        message_id=str(message_id),
        text=extract_message_text(raw.get("content")),
        chat_title=chat_title,
        author=author,
        published_at=unix_to_iso(raw.get("date")),
        url=url,
        metadata=metadata,
    )
