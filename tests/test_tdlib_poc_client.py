from __future__ import annotations

from collections import deque

import pytest

from poc.tdlib.client import TdJsonClient, TdLibResponseError, TdLibTimeoutError


class FakeBridge:
    def __init__(self, responses):
        self.responses = deque(responses)
        self.sent = []

    def send(self, request):
        self.sent.append(dict(request))
        correlation = request.get("@extra")
        for response in self.responses:
            if response.get("@extra") == "AUTO":
                response["@extra"] = correlation

    def receive(self, _timeout_seconds=1.0):
        return self.responses.popleft() if self.responses else None


def test_call_correlates_response_and_keeps_unrelated_update():
    bridge = FakeBridge([
        {"@type": "updateNewMessage", "message": {"id": 1}},
        {"@type": "chat", "id": 42, "@extra": "AUTO"},
    ])
    client = TdJsonClient(bridge)

    response = client.call({"@type": "getChat", "chat_id": 42}, timeout_seconds=0.5)

    assert response["id"] == 42
    assert len(client.pending_updates) == 1
    assert client.pending_updates[0]["@type"] == "updateNewMessage"
    assert bridge.sent[0]["@type"] == "getChat"
    assert "@extra" in bridge.sent[0]


def test_call_surfaces_tdlib_error_structurally():
    bridge = FakeBridge([
        {"@type": "error", "code": 400, "message": "CHAT_NOT_FOUND", "@extra": "AUTO"}
    ])
    client = TdJsonClient(bridge)

    with pytest.raises(TdLibResponseError) as exc:
        client.call({"@type": "getChat", "chat_id": 999}, timeout_seconds=0.5)

    assert exc.value.response["code"] == 400


def test_call_has_hard_timeout():
    client = TdJsonClient(FakeBridge([]))
    with pytest.raises(TdLibTimeoutError):
        client.call({"@type": "getMe"}, timeout_seconds=0.01)
