from father_osint.collectors.telegram import TelegramCollector, TelegramMessage
from father_osint.models import ResearchTask


class FakeTelegramTransport:
    def search(self, task: ResearchTask):
        assert task.question
        return [
            TelegramMessage(
                chat_id="test_channel",
                message_id="42",
                chat_title="Test Technology Channel",
                text="New inference runtime released",
                author="channel",
                published_at="2026-08-09T00:00:00+00:00",
                url="https://t.me/test_channel/42",
                metadata={"views": 100},
            )
        ]


def test_telegram_collector_maps_transport_message_to_material():
    task = ResearchTask(
        question="Find new AI infrastructure technologies",
        source_types=["telegram"],
    )
    collector = TelegramCollector(FakeTelegramTransport())

    materials = list(collector.collect(task))

    assert len(materials) == 1
    material = materials[0]
    assert material.source_type == "telegram"
    assert material.source_locator == "https://t.me/test_channel/42"
    assert material.raw_text == "New inference runtime released"
    assert material.metadata["chat_id"] == "test_channel"
    assert material.metadata["message_id"] == "42"
    assert material.metadata["views"] == 100


def test_telegram_collector_builds_locator_when_public_url_missing():
    task = ResearchTask(question="test", source_types=["telegram"])

    class NoUrlTransport:
        def search(self, task):
            return [TelegramMessage(chat_id="-100123", message_id="7", text="signal")]

    material = next(iter(TelegramCollector(NoUrlTransport()).collect(task)))
    assert material.source_locator == "telegram://-100123/7"
