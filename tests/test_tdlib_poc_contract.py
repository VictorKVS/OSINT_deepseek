from __future__ import annotations

import pytest

from poc.tdlib.auth import AuthActionRequired, AuthStep, next_auth_step
from poc.tdlib.requests import (
    get_chat_history_request,
    search_public_chat_request,
    set_tdlib_parameters_request,
)
from poc.tdlib.tdjson_bridge import redact


def auth_update(state_type: str):
    return {
        "@type": "updateAuthorizationState",
        "authorization_state": {"@type": state_type},
    }


def test_tdlib_parameters_require_encrypted_runtime_state():
    request = set_tdlib_parameters_request(
        api_id=123,
        api_hash="secret-hash",
        database_directory="runtime/tdlib/db",
        files_directory="runtime/tdlib/files",
        database_encryption_key="local-db-key",
    )
    assert request["@type"] == "setTdlibParameters"
    assert request["api_id"] == 123
    assert request["api_hash"] == "secret-hash"
    assert request["database_encryption_key"] == "local-db-key"
    assert request["use_secret_chats"] is False
    assert request["database_directory"].endswith("runtime/tdlib/db")
    assert redact(request)["database_encryption_key"] == "<redacted>"


def test_tdlib_parameters_reject_empty_database_key():
    with pytest.raises(ValueError):
        set_tdlib_parameters_request(
            api_id=123,
            api_hash="secret-hash",
            database_directory="runtime/tdlib/db",
            files_directory="runtime/tdlib/files",
            database_encryption_key="",
        )


def test_public_locator_is_normalized_without_business_logic():
    assert search_public_chat_request("@example") == {
        "@type": "searchPublicChat",
        "username": "example",
    }
    assert search_public_chat_request("https://t.me/example/12")["username"] == "example"


def test_history_request_is_hard_bounded_per_call():
    request = get_chat_history_request(chat_id=42, limit=50)
    assert request["limit"] == 50
    with pytest.raises(ValueError):
        get_chat_history_request(chat_id=42, limit=101)


def test_auth_state_machine_requires_local_operator_for_code():
    step = next_auth_step(auth_update("authorizationStateWaitCode"))
    assert isinstance(step, AuthStep)
    assert step.request is None
    assert "locally" in (step.operator_prompt or "")


def test_auth_state_machine_builds_code_request_only_when_supplied():
    step = next_auth_step(auth_update("authorizationStateWaitCode"), code="12345")
    assert step is not None
    assert step.request == {"@type": "checkAuthenticationCode", "code": "12345"}
    assert redact(step.request)["code"] == "<redacted>"


def test_auth_state_machine_supports_current_email_code_state():
    step = next_auth_step(auth_update("authorizationStateWaitEmailCode"), email_code="6789")
    assert step is not None
    assert step.request == {
        "@type": "checkAuthenticationEmailCode",
        "code": {"@type": "emailAddressAuthenticationCode", "code": "6789"},
    }
    assert redact(step.request)["code"] == "<redacted>"


def test_registration_fails_closed_for_poc():
    with pytest.raises(AuthActionRequired):
        next_auth_step(auth_update("authorizationStateWaitRegistration"))


def test_ready_state_has_no_follow_up_request():
    step = next_auth_step(auth_update("authorizationStateReady"))
    assert step == AuthStep(state="authorizationStateReady")
