from __future__ import annotations

import getpass
import json
import os
import time
from pathlib import Path

from poc.tdlib.auth import AuthActionRequired, next_auth_step
from poc.tdlib.requests import set_tdlib_parameters_request
from poc.tdlib.tdjson_bridge import TdJsonBridge, redact


DEFAULT_AUTH_TRANSITION_TIMEOUT_SECONDS = 5.0
RECEIVE_SLICE_SECONDS = 1.0


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required local environment variable: {name}")
    return value


def _positive_float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise SystemExit(f"{name} must be a positive number") from exc
    if value <= 0:
        raise SystemExit(f"{name} must be a positive number")
    return value


def _as_auth_update(message: dict[str, object]) -> dict[str, object] | None:
    """Normalize both auth updates and getAuthorizationState responses."""
    message_type = message.get("@type")
    if message_type == "updateAuthorizationState":
        return message
    if isinstance(message_type, str) and message_type.startswith("authorizationState"):
        return {
            "@type": "updateAuthorizationState",
            "authorization_state": message,
        }
    return None


def main() -> None:
    try:
        api_id = int(require_env("TELEGRAM_API_ID").strip())
    except ValueError as exc:
        raise SystemExit("TELEGRAM_API_ID must be an integer") from exc

    api_hash = require_env("TELEGRAM_API_HASH").strip()
    db_key = require_env("FATHER_TDLIB_DB_KEY")
    tdjson_path = require_env("TDJSON_LIBRARY")
    tdjson_sha256 = require_env("TDJSON_SHA256")
    auth_transition_timeout = _positive_float_env(
        "FATHER_TDLIB_AUTH_TRANSITION_TIMEOUT",
        DEFAULT_AUTH_TRANSITION_TIMEOUT_SECONDS,
    )

    runtime_root = Path(os.getenv("FATHER_TDLIB_RUNTIME", ".runtime/tdlib")).resolve()
    db_dir = runtime_root / "db"
    files_dir = runtime_root / "files"
    db_dir.mkdir(parents=True, exist_ok=True)
    files_dir.mkdir(parents=True, exist_ok=True)

    bridge = TdJsonBridge(tdjson_path, tdjson_sha256)

    # Native TDLib verbosity 3 logs request bodies, including api_hash and the
    # database encryption key. Reduce verbosity before sending any secret-bearing
    # authorization request. Python-side output is separately redacted below.
    bridge.execute({"@type": "setLogVerbosityLevel", "new_verbosity_level": 1})

    parameters = set_tdlib_parameters_request(
        api_id=api_id,
        api_hash=api_hash,
        database_directory=str(db_dir),
        files_directory=str(files_dir),
        database_encryption_key=db_key,
    )

    phone_number: str | None = os.getenv("TELEGRAM_PHONE_NUMBER")
    email_address: str | None = None
    print("TDLib PoC local bootstrap started. Secret-bearing native logs are suppressed.")
    print(f"Verified tdjson SHA-256: {bridge.library_sha256}")

    # Managed JSON clients created with td_create_client_id() do not emit updates
    # until the first request is sent. Explicitly ask for the current auth state
    # before entering the receive loop.
    bridge.send({"@type": "getAuthorizationState"})
    first_auth_deadline = time.monotonic() + 15.0
    saw_auth_state = False
    parameters_sent = False

    # TDLib auth calls are asynchronous. Once we send an auth request, require
    # explicit progress (a new authorization state or a TDLib error) within a
    # bounded receive budget. Each empty td_receive(RECEIVE_SLICE_SECONDS) consumes
    # that much budget; the real bridge blocks for up to the requested slice, while
    # tests can exercise the same contract deterministically without sleeping.
    transition_waiting_for: str | None = None
    transition_budget_seconds = 0.0

    while True:
        receive_slice = RECEIVE_SLICE_SECONDS
        if transition_waiting_for is not None:
            receive_slice = min(RECEIVE_SLICE_SECONDS, transition_budget_seconds)

        message = bridge.receive(receive_slice)
        if message is None:
            if not saw_auth_state and time.monotonic() >= first_auth_deadline:
                raise SystemExit(
                    "TDLib bootstrap timed out before the first authorization state; "
                    "the managed client produced no response/update after getAuthorizationState"
                )
            if transition_waiting_for is not None:
                transition_budget_seconds -= receive_slice
                if transition_budget_seconds <= 0:
                    raise SystemExit(
                        "TDLib timed out waiting for authorization transition after "
                        f"{transition_waiting_for}"
                    )
            continue

        if message.get("@type") == "error":
            safe_error = redact(message)
            raise SystemExit(f"TDLib returned an error during authorization: {safe_error}")

        update = _as_auth_update(message)
        if update is None:
            continue
        saw_auth_state = True
        transition_waiting_for = None
        transition_budget_seconds = 0.0

        state = (update.get("authorization_state") or {}).get("@type")

        # getAuthorizationState can race with updateAuthorizationState and expose
        # the same WaitTdlibParameters state twice. setTdlibParameters is one-shot;
        # sending it twice produces "Unexpected setTdlibParameters".
        if state == "authorizationStateWaitTdlibParameters" and parameters_sent:
            continue

        kwargs = {
            "parameters_request": parameters,
            "phone_number": phone_number,
            "email_address": email_address,
        }

        if state == "authorizationStateWaitPhoneNumber" and not phone_number:
            phone_number = getpass.getpass("Telegram phone number (local input): ")
            kwargs["phone_number"] = phone_number
        elif state == "authorizationStateWaitEmailAddress":
            email_address = getpass.getpass("Telegram email address (local input): ")
            kwargs["email_address"] = email_address
        elif state == "authorizationStateWaitEmailCode":
            kwargs["email_code"] = getpass.getpass("Telegram email code (local input): ")
        elif state == "authorizationStateWaitCode":
            kwargs["code"] = getpass.getpass("Telegram authentication code (local input): ")
        elif state == "authorizationStateWaitPassword":
            kwargs["password"] = getpass.getpass("Telegram 2FA password (local input): ")

        try:
            step = next_auth_step(update, **kwargs)
        except AuthActionRequired as exc:
            raise SystemExit(f"Authorization stopped safely: {exc}") from exc

        print(json.dumps(redact({"authorization_state": step.state if step else state}), ensure_ascii=False))

        if step and step.operator_prompt and not step.request:
            raise SystemExit(f"Authorization stopped safely: {step.operator_prompt}")
        if step and step.request:
            bridge.send(step.request)
            transition_waiting_for = str(step.request.get("@type") or step.state)
            transition_budget_seconds = auth_transition_timeout
            if step.state == "authorizationStateWaitTdlibParameters":
                parameters_sent = True
        if step and step.state == "authorizationStateReady":
            print("TDLib authorization ready. Local PoC session initialized.")
            return
        if step and step.state in {"authorizationStateClosing", "authorizationStateClosed"}:
            raise SystemExit("TDLib closed before authorization became ready")


if __name__ == "__main__":
    main()
