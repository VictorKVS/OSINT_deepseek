from __future__ import annotations

import asyncio
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from ..collectors.telegram import TelegramMessage
from ..models import ResearchTask


class TelethonTransport:
    """Reference Telethon adapter for the M5 integration path.

    This adapter deliberately requires an already-authorized local Telethon
    session. Interactive authorization, credential enrollment, VPN management,
    persistence/checkpointing, and analysis are outside this transport.

    Telethon is imported lazily so the frozen core test/dependency surface does
    not depend on the optional runtime library.
    """

    def __init__(
        self,
        *,
        api_id: int,
        api_hash: str,
        session_path: str | Path,
        channels: Sequence[str],
        per_channel_limit: int = 100,
        client_factory: Callable[..., Any] | None = None,
    ) -> None:
        if api_id <= 0:
            raise ValueError("api_id must be > 0")
        if not api_hash.strip():
            raise ValueError("api_hash must not be empty")
        if per_channel_limit <= 0:
            raise ValueError("per_channel_limit must be > 0")

        normalized_channels = [str(channel).strip() for channel in channels if str(channel).strip()]
        if not normalized_channels:
            raise ValueError("at least one Telegram channel is required")

        self.api_id = api_id
        self.api_hash = api_hash
        self.session_path = Path(session_path)
        self.channels = tuple(normalized_channels)
        self.per_channel_limit = per_channel_limit
        self._client_factory = client_factory

    def search(self, task: ResearchTask) -> list[TelegramMessage]:
        """Return at most task.max_items text-bearing messages.

        The current canonical TelegramTransport protocol is synchronous. The
        Telethon backend is asynchronous, so this reference adapter owns a
        bounded event loop at the adapter boundary. It intentionally refuses to
        nest inside an already-running loop; an async transport contract can be
        introduced later only through an explicit architecture change.
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            raise RuntimeError(
                "TelethonTransport.search() cannot run inside an active asyncio loop"
            )

        return asyncio.run(self._search_async(task))

    async def _search_async(self, task: ResearchTask) -> list[TelegramMessage]:
        client = self._build_client()
        results: list[TelegramMessage] = []

        await client.connect()
        try:
            if not await client.is_user_authorized():
                raise RuntimeError(
                    "Telethon session is not authorized; authorize the local session outside the collector"
                )

            for channel in self.channels:
                if len(results) >= task.max_items:
                    break

                remaining = task.max_items - len(results)
                request_limit = min(self.per_channel_limit, remaining)
                entity = await client.get_entity(channel)
                messages = await client.get_messages(entity, limit=request_limit)

                for message in messages:
                    text = getattr(message, "message", None) or getattr(message, "text", None)
                    if not text:
                        continue

                    mapped = self._map_message(entity, message, str(text))
                    results.append(mapped)
                    if len(results) >= task.max_items:
                        break
        finally:
            await client.disconnect()

        return results

    def _build_client(self):
        factory = self._client_factory
        if factory is None:
            try:
                from telethon import TelegramClient
            except ImportError as exc:
                raise RuntimeError(
                    "Telethon runtime dependency is missing; install Telethon only for the live adapter environment"
                ) from exc
            factory = TelegramClient

        return factory(str(self.session_path), self.api_id, self.api_hash)

    @staticmethod
    def _map_message(entity: Any, message: Any, text: str) -> TelegramMessage:
        entity_id = str(getattr(entity, "id", "unknown"))
        username = getattr(entity, "username", None)
        chat_id = str(username or entity_id)
        message_id = str(getattr(message, "id"))
        title = getattr(entity, "title", None) or username

        sender = getattr(message, "sender", None)
        author = None
        if sender is not None:
            author = (
                getattr(sender, "username", None)
                or " ".join(
                    part
                    for part in (
                        getattr(sender, "first_name", None),
                        getattr(sender, "last_name", None),
                    )
                    if part
                )
                or None
            )

        date = getattr(message, "date", None)
        published_at = date.isoformat() if date is not None else None
        url = f"https://t.me/{username}/{message_id}" if username else None

        metadata: dict[str, Any] = {
            "transport": "telethon",
            "entity_id": entity_id,
        }

        for field_name in ("views", "forwards", "edit_date", "grouped_id"):
            value = getattr(message, field_name, None)
            if value is not None:
                metadata[field_name] = (
                    value.isoformat() if hasattr(value, "isoformat") else value
                )

        reply_to = getattr(message, "reply_to_msg_id", None)
        if reply_to is not None:
            metadata["reply_to_msg_id"] = str(reply_to)

        return TelegramMessage(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            chat_title=title,
            author=author,
            published_at=published_at,
            url=url,
            metadata=metadata,
        )
