from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from ..models import Material, ResearchTask


@dataclass(slots=True)
class TelegramMessage:
    """Transport-neutral Telegram message returned by a Telegram backend."""

    chat_id: str
    message_id: str
    text: str
    chat_title: str | None = None
    author: str | None = None
    published_at: str | None = None
    url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class TelegramTransport(Protocol):
    """Minimal boundary around TDLib, GramJS, or another MTProto implementation."""

    def search(self, task: ResearchTask) -> list[TelegramMessage]:
        ...


class TelegramCollector:
    """Collect Telegram material without performing analysis.

    Transport choice is deliberately outside this collector. A TDLib or GramJS
    adapter only needs to implement TelegramTransport.search().
    """

    name = "telegram"
    source_types = {"telegram"}

    def __init__(self, transport: TelegramTransport) -> None:
        self.transport = transport

    def collect(self, task: ResearchTask):
        for message in self.transport.search(task):
            locator = message.url or f"telegram://{message.chat_id}/{message.message_id}"
            title = message.chat_title or f"Telegram {message.chat_id}"
            metadata = {
                "chat_id": message.chat_id,
                "message_id": message.message_id,
                **message.metadata,
            }
            yield Material(
                source_type="telegram",
                source_locator=locator,
                title=title,
                raw_text=message.text,
                published_at=message.published_at,
                author=message.author,
                metadata=metadata,
            )
