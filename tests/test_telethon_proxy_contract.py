from __future__ import annotations

from father_osint.transports.telethon import TelethonTransport


def test_proxy_passed_to_factory_when_configured(tmp_path):
    received = {}

    def fake_factory(session, api_id, api_hash, **kwargs):
        received.update(kwargs)
        return object()

    proxy = (2, "127.0.0.1", 1080, True)
    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "test",
        channels=["@test"],
        proxy=proxy,
        client_factory=fake_factory,
    )
    transport._build_client()
    assert received == {"proxy": proxy}


def test_no_proxy_preserves_legacy_factory_signature(tmp_path):
    invoked = []

    def legacy_factory(session, api_id, api_hash):
        invoked.append((session, api_id, api_hash))
        return object()

    transport = TelethonTransport(
        api_id=123,
        api_hash="synthetic",
        session_path=tmp_path / "test",
        channels=["@test"],
        client_factory=legacy_factory,
    )
    transport._build_client()
    assert len(invoked) == 1
