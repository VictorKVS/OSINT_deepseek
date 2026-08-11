from __future__ import annotations

from collections import deque

import pytest

from poc.tdlib.client import TdJsonClient, TdLibResponseError, TdLibTimeoutError


class FakeBridge:
    def __init__(self, responses):
        self.responses = deque(responses)
        self.sent: list[dict[str, object]] = []

    def send(self, request):
        payload = dict(request)
        self.sent.append(payload)
        correlation = payload.get("@extra")
        for response in self.responses:
            if response.get("@extra") == "AUTO":
                response["@extra"] = correlation

    def receive(self, _timeout_seconds=1.0):
        return self.responses.popleft() if self.responses else None


def test_auth_rsp_01_phone_request_ok_is_correlated():
    bridge = FakeBridge([
        {"@type": "updateAuthorizationState", "authorization_state": {"@type": "authorizationStateWaitCode"}},
        {"@type": "ok", "@extra": "AUTO"},
    ])
    client = TdJsonClient(bridge)

    response = client.call(
        {"@type": "setAuthenticationPhoneNumber", "phone_number": "+10000000000"},
        timeout_seconds=0.5,
    )

    assert response["@type"] == "ok"
    assert bridge.sent[0]["@type"] == "setAuthenticationPhoneNumber"
    assert "@extra" in bridge.sent[0]
    assert len(client.pending_updates) == 1
    assert client.pending_updates[0]["authorization_state"]["@type"] == "authorizationStateWaitCode"


def test_auth_rsp_02_phone_request_error_is_structured():
    bridge = FakeBridge([
        {"@type": "error", "code": 400, "message": "PHONE_NUMBER_INVALID", "@extra": "AUTO"},
    ])
    client = TdJsonClient(bridge)

    with pytest.raises(TdLibResponseError) as exc:
        client.call(
            {"@type": "setAuthenticationPhoneNumber", "phone_number": "+10000000000"},
            timeout_seconds=0.5,
        )

    assert exc.value.response["code"] == 400
    assert exc.value.response["message"] == "PHONE_NUMBER_INVALID"


def test_auth_rsp_03_phone_request_timeout_is_bounded():
    client = TdJsonClient(FakeBridge([]))

    with pytest.raises(TdLibTimeoutError, match="setAuthenticationPhoneNumber"):
        client.call(
            {"@type": "setAuthenticationPhoneNumber", "phone_number": "+10000000000"},
            timeout_seconds=0.01,
        )
