from __future__ import annotations

from father_osint.collectors.telegram import TelegramCollector, TelegramMessage
from father_osint.models import ResearchTask


class FakeTelegramTransport:
    def search(self, task: ResearchTask) -> list[TelegramMessage]:
        assert task.max_items == 10
        return [
            TelegramMessage(
                chat_id="durov",
                message_id="123",
                text="Telegram message body",
                chat_title="Pavel Durov",
                author="Pavel Durov",
                published_at="2026-08-12T18:00:00+00:00",
                url="https://t.me/durov/123",
                metadata={"views": 42, "transport": "fixture"},
            )
        ]


def test_telegram_collector_maps_transport_message_to_canonical_material():
    task = ResearchTask(question="Telegram evidence", max_items=10)
    collector = TelegramCollector(FakeTelegramTransport())

    materials = list(collector.collect(task))

    assert len(materials) == 1
    material = materials[0]
    assert material.source_type == "telegram"
    assert material.source_locator == "https://t.me/durov/123"
    assert material.title == "Pavel Durov"
    assert material.raw_text == "Telegram message body"
    assert material.author == "Pavel Durov"
    assert material.published_at == "2026-08-12T18:00:00+00:00"
    assert material.metadata["chat_id"] == "durov"
    assert material.metadata["message_id"] == "123"
    assert material.metadata["views"] == 42


def test_telegram_collector_has_stable_fallback_locator():
    task = ResearchTask(question="Telegram evidence", max_items=10)

    class NoUrlTransport:
        def search(self, task: ResearchTask) -> list[TelegramMessage]:
            return [
                TelegramMessage(
                    chat_id="-10042",
                    message_id="7",
                    text="Evidence",
                )
            ]

    material = next(TelegramCollector(NoUrlTransport()).collect(task))
    assert material.source_locator == "telegram://-10042/7"
    assert material.metadata["chat_id"] == "-10042"
    assert material.metadata["message_id"] == "7"
