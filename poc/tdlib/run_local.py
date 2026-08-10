from __future__ import annotations

import getpass
import json
import os
from pathlib import Path

from poc.tdlib.auth import AuthActionRequired, next_auth_step
from poc.tdlib.requests import set_tdlib_parameters_request
from poc.tdlib.tdjson_bridge import TdJsonBridge, redact


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required local environment variable: {name}")
    return value


def main() -> None:
    api_id = int(require_env("TELEGRAM_API_ID"))
    api_hash = require_env("TELEGRAM_API_HASH")
    db_key = require_env("FATHER_TDLIB_DB_KEY")
    tdjson_path = require_env("TDJSON_LIBRARY")
    tdjson_sha256 = require_env("TDJSON_SHA256")

    runtime_root = Path(os.getenv("FATHER_TDLIB_RUNTIME", ".runtime/tdlib")).resolve()
    db_dir = runtime_root / "db"
    files_dir = runtime_root / "files"
    db_dir.mkdir(parents=True, exist_ok=True)
    files_dir.mkdir(parents=True, exist_ok=True)

    bridge = TdJsonBridge(tdjson_path, tdjson_sha256)
    parameters = set_tdlib_parameters_request(
        api_id=api_id,
        api_hash=api_hash,
        database_directory=str(db_dir),
        files_directory=str(files_dir),
        database_encryption_key=db_key,
    )

    phone_number: str | None = os.getenv("TELEGRAM_PHONE_NUMBER")
    email_address: str | None = None
    print("TDLib PoC local bootstrap started. Secrets are not printed.")
    print(f"Verified tdjson SHA-256: {bridge.library_sha256}")

    while True:
        update = bridge.receive(1.0)
        if update is None:
            continue
        if update.get("@type") != "updateAuthorizationState":
            continue

        state = (update.get("authorization_state") or {}).get("@type")
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
        if step and step.state == "authorizationStateReady":
            print("TDLib authorization ready. Local PoC session initialized.")
            return
        if step and step.state in {"authorizationStateClosing", "authorizationStateClosed"}:
            raise SystemExit("TDLib closed before authorization became ready")


if __name__ == "__main__":
    main()
