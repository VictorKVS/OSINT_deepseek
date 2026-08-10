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
    code: str | None = None,
    password: str | None = None,
    database_encryption_key: str = "",
) -> AuthStep | None:
    """Translate TDLib authorization-state updates into explicit local actions.

    This is intentionally deterministic. It never invents credentials and never
    reads secrets from Git-tracked configuration.
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

    if state_type == "authorizationStateWaitEncryptionKey":
        return AuthStep(
            state=state_type,
            request={"@type": "checkDatabaseEncryptionKey", "encryption_key": database_encryption_key},
        )

    if state_type == "authorizationStateWaitPhoneNumber":
        if not phone_number:
            return AuthStep(state=state_type, operator_prompt="Enter Telegram phone number locally")
        return AuthStep(
            state=state_type,
            request={"@type": "setAuthenticationPhoneNumber", "phone_number": phone_number},
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

    if state_type in {"authorizationStateReady", "authorizationStateLoggingOut", "authorizationStateClosing", "authorizationStateClosed"}:
        return AuthStep(state=state_type)

    return AuthStep(state=str(state_type or "unknown"))
