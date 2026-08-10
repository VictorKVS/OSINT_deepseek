from poc.tdlib.mapping import map_tdlib_message
from poc.tdlib.tdjson_bridge import redact


def test_tdlib_text_message_maps_to_transport_neutral_contract():
    raw = {
        "@type": "message",
        "id": 12345,
        "chat_id": -100987654321,
        "date": 1_700_000_000,
        "is_channel_post": True,
        "sender_id": {"@type": "messageSenderChat", "chat_id": -100987654321},
        "content": {
            "@type": "messageText",
            "text": {"@type": "formattedText", "text": "Привет, TDLib", "entities": []},
        },
    }

    message = map_tdlib_message(
        raw,
        chat_title="PoC Channel",
        public_username="father_test_channel",
    )

    assert message.chat_id == "-100987654321"
    assert message.message_id == "12345"
    assert message.text == "Привет, TDLib"
    assert message.chat_title == "PoC Channel"
    assert message.url == "https://t.me/father_test_channel/12345"
    assert message.published_at is not None
    assert message.metadata["tdlib_content_type"] == "messageText"
    assert message.metadata["is_channel_post"] is True


def test_tdlib_media_caption_is_preserved_without_media_download():
    raw = {
        "id": 77,
        "chat_id": 55,
        "date": 1_700_000_001,
        "content": {
            "@type": "messagePhoto",
            "caption": {"@type": "formattedText", "text": "caption text", "entities": []},
            "photo": {"id": 999},
        },
    }

    message = map_tdlib_message(raw)

    assert message.text == "caption text"
    assert message.metadata["tdlib_content_type"] == "messagePhoto"
    assert message.url is None


def test_tdlib_mapping_requires_stable_message_identity():
    try:
        map_tdlib_message({"content": {"@type": "messageText"}})
    except ValueError as exc:
        assert "chat_id and id" in str(exc)
    else:
        raise AssertionError("mapping must reject TDLib messages without stable identifiers")


def test_tdlib_sensitive_values_are_redacted_recursively():
    payload = {
        "api_hash": "secret-hash",
        "nested": {
            "phone_number": "+10000000000",
            "password": "secret-password",
            "safe": "visible",
        },
        "items": [{"authentication_code": "12345"}],
    }

    safe = redact(payload)

    assert safe["api_hash"] == "<redacted>"
    assert safe["nested"]["phone_number"] == "<redacted>"
    assert safe["nested"]["password"] == "<redacted>"
    assert safe["nested"]["safe"] == "visible"
    assert safe["items"][0]["authentication_code"] == "<redacted>"
