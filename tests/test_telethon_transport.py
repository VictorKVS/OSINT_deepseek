from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from father_osint.models import ResearchTask
from father_osint.transports.telethon import TelethonTransport


@dataclass
class FakeEntity:
    id: int
    username: str | None
    title: str


@dataclass
class FakeSender:
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class FakeMessage:
    id: int
    message: str | None
    date: datetime
    sender: FakeSender | None = None
    views: int | None = None
    forwards: int | None = None
    edit_date: datetime | None = None
    grouped_id: int | None = None
    reply_to_msg_id: int | None = None
    text: str | None = None


class FakeClient:
    def __init__(self, _session: str, _api_id: int, _api_hash: str, *, authorized=True):
        self.authorized = authorized
        self.connected = False
        self.disconnected = False
        self.requests: list[tuple[str, int]] = []

    async def connect(self):
        self.connected = True

    async def disconnect(self):
        self.disconnected = True

    async def is_user_authorized(self):
        return self.authorized

    async def get_entity(self, channel):
        username = str(channel).replace("https://t.me/", "").lstrip("@")
        return FakeEntity(id=1001, username=username, title=f"Channel {username}")

    async def get_messages(self, entity, limit):
        self.requests.append((entity.username, limit))
        return [
            FakeMessage(
                id=index + 1,
                message=f"message {index + 1}",
                date=datetime(2026, 8, 12, 18, index, tzinfo=timezone.utc),
                sender=FakeSender(username="author"),
                views=100 + index,
            )
            for index in range(limit)
        ]


def test_telethon_transport_maps_messages_and_respects_global_task_bound(tmp_path):
    created: list[FakeClient] = []

    def factory(session, api_id, api_hash):
        client = FakeClient(session, api_id, api_hash)
        created.append(client)
        return client

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "reader_session",
        channels=["@durov", "@telegram"],
        per_channel_limit=100,
        client_factory=factory,
    )
    task = ResearchTask(question="collect", max_items=3)

    messages = transport.search(task)

    assert len(messages) == 3
    assert len(created) == 1
    assert created[0].connected is True
    assert created[0].disconnected is True
    assert created[0].requests == [("durov", 3)]

    first = messages[0]
    assert first.chat_id == "durov"
    assert first.message_id == "1"
    assert first.url == "https://t.me/durov/1"
    assert first.chat_title == "Channel durov"
    assert first.author == "author"
    assert first.metadata["transport"] == "telethon"
    assert first.metadata["views"] == 100


def test_telethon_transport_requires_pre_authorized_session(tmp_path):
    created: list[FakeClient] = []

    def factory(session, api_id, api_hash):
        client = FakeClient(session, api_id, api_hash, authorized=False)
        created.append(client)
        return client

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "reader_session",
        channels=["@durov"],
        client_factory=factory,
    )

    with pytest.raises(RuntimeError, match="not authorized"):
        transport.search(ResearchTask(question="collect", max_items=1))

    assert created[0].disconnected is True


def test_telethon_transport_skips_non_text_objects_without_overclaiming_count(tmp_path):
    class MixedClient(FakeClient):
        async def get_messages(self, entity, limit):
            self.requests.append((entity.username, limit))
            return [
                FakeMessage(
                    id=1,
                    message=None,
                    text=None,
                    date=datetime(2026, 8, 12, 18, 0, tzinfo=timezone.utc),
                ),
                FakeMessage(
                    id=2,
                    message="usable text",
                    date=datetime(2026, 8, 12, 18, 1, tzinfo=timezone.utc),
                ),
            ]

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "reader_session",
        channels=["@durov"],
        per_channel_limit=2,
        client_factory=MixedClient,
    )

    messages = transport.search(ResearchTask(question="collect", max_items=2))
    assert [message.message_id for message in messages] == ["2"]


def test_channel_failure_is_isolated_and_next_channel_is_collected(tmp_path):
    class PartialFailureClient(FakeClient):
        async def get_entity(self, channel):
            username = str(channel).lstrip("@")
            if username == "broken":
                raise RuntimeError("synthetic channel failure")
            return FakeEntity(id=1002, username=username, title=f"Channel {username}")

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "reader_session",
        channels=["@broken", "@working"],
        per_channel_limit=1,
        client_factory=PartialFailureClient,
    )

    messages = transport.search(ResearchTask(question="collect", max_items=1))

    assert len(messages) == 1
    assert messages[0].chat_id == "working"
    assert len(transport.last_errors) == 1
    assert "broken" in transport.last_errors[0]


def test_bounded_flood_wait_retries_once_then_succeeds(tmp_path):
    class FloodWaitError(Exception):
        def __init__(self, seconds):
            super().__init__(f"wait {seconds}")
            self.seconds = seconds

    class FloodOnceClient(FakeClient):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.calls = 0

        async def get_messages(self, entity, limit):
            self.calls += 1
            if self.calls == 1:
                raise FloodWaitError(2)
            return await super().get_messages(entity, limit)

    sleeps = []

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "reader_session",
        channels=["@durov"],
        per_channel_limit=1,
        max_flood_wait_retries=1,
        max_flood_wait_seconds=5,
        client_factory=FloodOnceClient,
        sleep_func=fake_sleep,
    )

    messages = transport.search(ResearchTask(question="collect", max_items=1))

    assert len(messages) == 1
    assert sleeps == [2]
    assert transport.last_errors == []


def test_flood_wait_above_bound_is_recorded_and_channel_skipped(tmp_path):
    class FloodWaitError(Exception):
        def __init__(self, seconds):
            super().__init__(f"wait {seconds}")
            self.seconds = seconds

    class LongFloodClient(FakeClient):
        async def get_messages(self, entity, limit):
            raise FloodWaitError(120)

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "reader_session",
        channels=["@durov"],
        per_channel_limit=1,
        max_flood_wait_retries=1,
        max_flood_wait_seconds=5,
        client_factory=LongFloodClient,
    )

    messages = transport.search(ResearchTask(question="collect", max_items=1))

    assert messages == []
    assert len(transport.last_errors) == 1
    assert "above bound" in transport.last_errors[0]
