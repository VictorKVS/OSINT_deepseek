from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class AuthActionRequired(RuntimeError):
    """Raised when the local operator must supply an authentication step."""


@dataclass(slots=True)
class AuthStep:
    state: str
    request: dict[str, Any] | None = None
    operator_prompt: str | None = None


def next_auth_step(
    update: dict[str, Any],
    *,
    parameters_request: dict[str, Any] | None = None,
    phone_number: str | None = None,
    email_address: str | None = None,
    email_code: str | None = None,
    code: str | None = None,
    password: str | None = None,
) -> AuthStep | None:
    """Translate current TDLib authorization updates into explicit local actions.

    The function is deterministic: credentials are never invented, persisted, or
    read from Git-tracked configuration. New/unknown auth states fail closed at the
    local harness instead of being silently bypassed.
    """
    if update.get("@type") != "updateAuthorizationState":
        return None

    state = update.get("authorization_state")
    if not isinstance(state, dict):
        raise ValueError("authorization_state must be an object")

    state_type = state.get("@type")

    if state_type == "authorizationStateWaitTdlibParameters":
        if parameters_request is None:
            raise AuthActionRequired("TDLib parameters are required")
        return AuthStep(state=state_type, request=parameters_request)

    if state_type == "authorizationStateWaitPhoneNumber":
        if not phone_number:
            return AuthStep(state=state_type, operator_prompt="Enter Telegram phone number locally")
        return AuthStep(
            state=state_type,
            request={"@type": "setAuthenticationPhoneNumber", "phone_number": phone_number},
        )

    if state_type == "authorizationStateWaitEmailAddress":
        if not email_address:
            return AuthStep(state=state_type, operator_prompt="Enter Telegram email address locally")
        return AuthStep(
            state=state_type,
            request={"@type": "setAuthenticationEmailAddress", "email_address": email_address},
        )

    if state_type == "authorizationStateWaitEmailCode":
        if not email_code:
            return AuthStep(state=state_type, operator_prompt="Enter Telegram email code locally")
        return AuthStep(
            state=state_type,
            request={
                "@type": "checkAuthenticationEmailCode",
                "code": {"@type": "emailAddressAuthenticationCode", "code": email_code},
            },
        )

    if state_type == "authorizationStateWaitCode":
        if not code:
            return AuthStep(state=state_type, operator_prompt="Enter Telegram authentication code locally")
        return AuthStep(
            state=state_type,
            request={"@type": "checkAuthenticationCode", "code": code},
        )

    if state_type == "authorizationStateWaitPassword":
        if not password:
            return AuthStep(state=state_type, operator_prompt="Enter Telegram 2FA password locally")
        return AuthStep(
            state=state_type,
            request={"@type": "checkAuthenticationPassword", "password": password},
        )

    if state_type == "authorizationStateWaitRegistration":
        raise AuthActionRequired("PoC does not register new Telegram accounts; use an existing account")

    if state_type in {
        "authorizationStateReady",
        "authorizationStateLoggingOut",
        "authorizationStateClosing",
        "authorizationStateClosed",
    }:
        return AuthStep(state=state_type)

    return AuthStep(state=str(state_type or "unknown"), operator_prompt="Unsupported TDLib authorization state")
