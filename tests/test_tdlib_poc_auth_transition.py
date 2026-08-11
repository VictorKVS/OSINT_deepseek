from __future__ import annotations

from collections import deque

import pytest

import poc.tdlib.run_local as run_local


class FakeBridge:
    def __init__(self, _library_path: str, _expected_sha256: str, responses):
        self.responses = deque(responses)
        self.sent: list[dict[str, object]] = []
        self.library_sha256 = "fake-approved-sha256"
        self.receive_calls = 0

    def execute(self, _request):
        return None

    def send(self, request):
        self.sent.append(dict(request))
        correlation = request.get("@extra")
        if correlation is not None:
            for response in self.responses:
                if response.get("@extra") == "AUTO":
                    response["@extra"] = correlation
                    break

    def receive(self, _timeout_seconds=1.0):
        self.receive_calls += 1
        if self.responses:
            return self.responses.popleft()
        if self.receive_calls > 12:
            raise RuntimeError("TEST_GUARD_UNBOUNDED_RECEIVE")
        return None


def auth_update(state_type: str):
    return {
        "@type": "updateAuthorizationState",
        "authorization_state": {"@type": state_type},
    }


def configure_env(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_API_ID", "123456")
    monkeypatch.setenv("TELEGRAM_API_HASH", "fake-hash")
    monkeypatch.setenv("FATHER_TDLIB_DB_KEY", "fake-db-key")
    monkeypatch.setenv("TDJSON_LIBRARY", str(tmp_path / "tdjson.dll"))
    monkeypatch.setenv("TDJSON_SHA256", "0" * 64)
    monkeypatch.setenv("FATHER_TDLIB_RUNTIME", str(tmp_path / "runtime"))
    monkeypatch.setenv("TELEGRAM_PHONE_NUMBER", "test-phone")


def test_auth_01_post_phone_transition_is_bounded(monkeypatch, tmp_path):
    configure_env(monkeypatch, tmp_path)
    bridge = FakeBridge(
        "unused",
        "unused",
        [
            auth_update("authorizationStateWaitTdlibParameters"),
            {"@type": "ok", "@extra": "AUTO"},
            auth_update("authorizationStateWaitPhoneNumber"),
            {"@type": "ok", "@extra": "AUTO"},
        ],
    )
    monkeypatch.setattr(run_local, "TdJsonBridge", lambda *_args: bridge)

    with pytest.raises(SystemExit, match="timed out.*authorization transition"):
        run_local.main()

    assert any(item.get("@type") == "setAuthenticationPhoneNumber" for item in bridge.sent)


def test_auth_02_post_phone_tdlib_error_is_explicit(monkeypatch, tmp_path):
    configure_env(monkeypatch, tmp_path)
    bridge = FakeBridge(
        "unused",
        "unused",
        [
            auth_update("authorizationStateWaitTdlibParameters"),
            {"@type": "ok", "@extra": "AUTO"},
            auth_update("authorizationStateWaitPhoneNumber"),
            {"@type": "error", "code": 400, "message": "TEST_INPUT_REJECTED", "@extra": "AUTO"},
        ],
    )
    monkeypatch.setattr(run_local, "TdJsonBridge", lambda *_args: bridge)

    with pytest.raises(SystemExit, match="TDLib returned an error for authorization request"):
        run_local.main()


def test_auth_03_successful_transition_remains_processable(monkeypatch, tmp_path):
    configure_env(monkeypatch, tmp_path)
    bridge = FakeBridge(
        "unused",
        "unused",
        [
            auth_update("authorizationStateWaitTdlibParameters"),
            {"@type": "ok", "@extra": "AUTO"},
            auth_update("authorizationStateWaitPhoneNumber"),
            {"@type": "ok", "@extra": "AUTO"},
            auth_update("authorizationStateReady"),
        ],
    )
    monkeypatch.setattr(run_local, "TdJsonBridge", lambda *_args: bridge)

    run_local.main()

    assert any(item.get("@type") == "setAuthenticationPhoneNumber" for item in bridge.sent)
