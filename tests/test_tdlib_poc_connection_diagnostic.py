from __future__ import annotations

from collections import deque

import pytest

import poc.tdlib.run_local as run_local


class FakeBridge:
    def __init__(self, _library_path: str, _expected_sha256: str, responses):
        self.responses = deque(responses)
        self.sent: list[dict[str, object]] = []
        self.library_sha256 = "fake-approved-sha256"

    def execute(self, _request):
        return None

    def send(self, request):
        self.sent.append(dict(request))

    def receive(self, _timeout_seconds=1.0):
        if self.responses:
            response = self.responses.popleft()
            if response.get("@type") == "ok" and self.sent:
                response = dict(response)
                response["@extra"] = self.sent[-1].get("@extra")
            return response
        return None


def auth_update(state_type: str):
    return {
        "@type": "updateAuthorizationState",
        "authorization_state": {"@type": state_type},
    }


def connection_update(state_type: str):
    return {
        "@type": "updateConnectionState",
        "state": {"@type": state_type},
    }


def configure_env(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_API_ID", "123456")
    monkeypatch.setenv("TELEGRAM_API_HASH", "synthetic-hash")
    monkeypatch.setenv("FATHER_TDLIB_DB_KEY", "synthetic-db-key")
    monkeypatch.setenv("TDJSON_LIBRARY", str(tmp_path / "tdjson.dll"))
    monkeypatch.setenv("TDJSON_SHA256", "0" * 64)
    monkeypatch.setenv("FATHER_TDLIB_RUNTIME", str(tmp_path / "runtime"))
    monkeypatch.setenv("TELEGRAM_PHONE_NUMBER", "+10000000000")
    monkeypatch.setenv("FATHER_TDLIB_AUTH_TRANSITION_TIMEOUT", "1")


def test_auth_net_01_connection_state_is_surfaced(monkeypatch, tmp_path, capsys):
    configure_env(monkeypatch, tmp_path)
    bridge = FakeBridge(
        "unused",
        "unused",
        [
            auth_update("authorizationStateWaitTdlibParameters"),
            {"@type": "ok"},
            auth_update("authorizationStateWaitPhoneNumber"),
            connection_update("connectionStateConnecting"),
        ],
    )
    monkeypatch.setattr(run_local, "TdJsonBridge", lambda *_args: bridge)

    with pytest.raises(SystemExit, match="timed out waiting for response"):
        run_local.main()

    output = capsys.readouterr().out
    assert '"connection_state": "connectionStateConnecting"' in output


def test_auth_net_02_connection_diagnostic_is_secret_safe(monkeypatch, tmp_path, capsys):
    configure_env(monkeypatch, tmp_path)
    bridge = FakeBridge(
        "unused",
        "unused",
        [
            auth_update("authorizationStateWaitTdlibParameters"),
            {"@type": "ok"},
            auth_update("authorizationStateWaitPhoneNumber"),
            connection_update("connectionStateWaitingForNetwork"),
        ],
    )
    monkeypatch.setattr(run_local, "TdJsonBridge", lambda *_args: bridge)

    with pytest.raises(SystemExit):
        run_local.main()

    output = capsys.readouterr().out
    assert "synthetic-hash" not in output
    assert "synthetic-db-key" not in output
    assert "+10000000000" not in output
    assert '"connection_state": "connectionStateWaitingForNetwork"' in output
