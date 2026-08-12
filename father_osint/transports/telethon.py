from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from pathlib import Path
from typing import Any

from ..collectors.telegram import TelegramMessage
from ..models import ResearchTask


class TelethonTransport:
    """Reference Telethon adapter for the M5 integration path.

    The adapter requires an already-authorized local session. Channel failures
    are isolated, FloodWait retries are explicitly bounded, and all optional
    Telethon imports remain outside the frozen core dependency surface.
    """

    def __init__(
        self,
        *,
        api_id: int,
        api_hash: str,
        session_path: str | Path,
        channels: Sequence[str],
        per_channel_limit: int = 100,
        max_flood_wait_retries: int = 1,
        max_flood_wait_seconds: int = 30,
        client_factory: Callable[..., Any] | None = None,
        sleep_func: Callable[[float], Awaitable[Any]] | None = None,
    ) -> None:
        if api_id <= 0:
            raise ValueError("api_id must be > 0")
        if not api_hash.strip():
            raise ValueError("api_hash must not be empty")
        if per_channel_limit <= 0:
            raise ValueError("per_channel_limit must be > 0")
        if max_flood_wait_retries < 0:
            raise ValueError("max_flood_wait_retries must be >= 0")
        if max_flood_wait_seconds < 0:
            raise ValueError("max_flood_wait_seconds must be >= 0")

        normalized_channels = [str(channel).strip() for channel in channels if str(channel).strip()]
        if not normalized_channels:
            raise ValueError("at least one Telegram channel is required")

        self.api_id = api_id
        self.api_hash = api_hash
        self.session_path = Path(session_path)
        self.channels = tuple(normalized_channels)
        self.per_channel_limit = per_channel_limit
        self.max_flood_wait_retries = max_flood_wait_retries
        self.max_flood_wait_seconds = max_flood_wait_seconds
        self._client_factory = client_factory
        self._sleep_func = sleep_func or asyncio.sleep
        self.last_errors: list[str] = []

    def search(self, task: ResearchTask) -> list[TelegramMessage]:
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
        self.last_errors = []

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

                try:
                    entity = await client.get_entity(channel)
                    messages = await self._get_messages_with_bounded_flood_wait(
                        client=client,
                        entity=entity,
                        limit=request_limit,
                        channel=str(channel),
                    )
                except Exception as exc:  # channel-level isolation boundary
                    self.last_errors.append(
                        f"{channel}: {exc.__class__.__name__}: {exc}"
                    )
                    continue

                for message in messages:
                    text = getattr(message, "message", None) or getattr(message, "text", None)
                    if not text:
                        continue

                    results.append(self._map_message(entity, message, str(text)))
                    if len(results) >= task.max_items:
                        break
        finally:
            await client.disconnect()

        return results

    async def _get_messages_with_bounded_flood_wait(
        self,
        *,
        client: Any,
        entity: Any,
        limit: int,
        channel: str,
    ) -> Any:
        attempts = 0
        while True:
            try:
                return await client.get_messages(entity, limit=limit)
            except Exception as exc:
                if exc.__class__.__name__ != "FloodWaitError":
                    raise

                wait_seconds = int(getattr(exc, "seconds", 0) or 0)
                if wait_seconds > self.max_flood_wait_seconds:
                    raise RuntimeError(
                        f"FloodWait for {channel} is {wait_seconds}s, above bound "
                        f"{self.max_flood_wait_seconds}s"
                    ) from exc
                if attempts >= self.max_flood_wait_retries:
                    raise RuntimeError(
                        f"FloodWait retry budget exhausted for {channel}"
                    ) from exc

                attempts += 1
                await self._sleep_func(wait_seconds)

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
