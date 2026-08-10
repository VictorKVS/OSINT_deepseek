from __future__ import annotations

import getpass
import json
import os
from pathlib import Path

from poc.tdlib.auth import next_auth_step
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
    runtime_root = Path(os.getenv("FATHER_TDLIB_RUNTIME", ".runtime/tdlib")).resolve()
    db_dir = runtime_root / "db"
    files_dir = runtime_root / "files"
    db_dir.mkdir(parents=True, exist_ok=True)
    files_dir.mkdir(parents=True, exist_ok=True)

    bridge = TdJsonBridge()
    parameters = set_tdlib_parameters_request(
        api_id=api_id,
        api_hash=api_hash,
        database_directory=str(db_dir),
        files_directory=str(files_dir),
    )

    phone_number: str | None = os.getenv("TELEGRAM_PHONE_NUMBER")
    print("TDLib PoC local bootstrap started. Secrets are not printed.")

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
        }

        if state == "authorizationStateWaitPhoneNumber" and not phone_number:
            phone_number = getpass.getpass("Telegram phone number (local input): ")
            kwargs["phone_number"] = phone_number
        elif state == "authorizationStateWaitCode":
            kwargs["code"] = getpass.getpass("Telegram authentication code (local input): ")
        elif state == "authorizationStateWaitPassword":
            kwargs["password"] = getpass.getpass("Telegram 2FA password (local input): ")

        step = next_auth_step(update, **kwargs)
        print(json.dumps(redact({"authorization_state": step.state if step else state}), ensure_ascii=False))

        if step and step.request:
            bridge.send(step.request)

        if step and step.state == "authorizationStateReady":
            print("TDLib authorization ready. Local PoC session initialized.")
            return

        if step and step.state in {"authorizationStateClosing", "authorizationStateClosed"}:
            raise SystemExit("TDLib closed before authorization became ready")


if __name__ == "__main__":
    main()
