from __future__ import annotations

import asyncio
import getpass
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SESSION = REPO_ROOT / "legacy" / "telegram" / "reader_session"


def _load_api_credentials() -> tuple[int, str]:
    api_id_raw = os.getenv("TELEGRAM_API_ID", "").strip()
    api_hash = os.getenv("TELEGRAM_API_HASH", "").strip()
    if not api_id_raw or not api_hash:
        raise RuntimeError("TELEGRAM_API_ID/TELEGRAM_API_HASH are required in the local process environment")
    try:
        api_id = int(api_id_raw)
    except ValueError as exc:
        raise RuntimeError("TELEGRAM_API_ID must be an integer") from exc
    if api_id <= 0:
        raise RuntimeError("TELEGRAM_API_ID must be positive")
    return api_id, api_hash


def _session_path() -> Path:
    raw = os.getenv("TELEGRAM_SESSION_PATH", "").strip()
    path = Path(raw) if raw else DEFAULT_SESSION
    if not path.is_absolute():
        path = REPO_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


async def _authorize() -> dict[str, object]:
    try:
        from telethon import TelegramClient  # type: ignore
        from telethon.errors import (  # type: ignore
            PhoneCodeExpiredError,
            PhoneCodeInvalidError,
            SessionPasswordNeededError,
        )
    except ImportError as exc:
        raise RuntimeError("Telethon is required in the selected Python environment") from exc

    api_id, api_hash = _load_api_credentials()
    session = _session_path()
    client = TelegramClient(str(session), api_id, api_hash)

    await client.connect()
    try:
        if await client.is_user_authorized():
            return {
                "status": "ALREADY_AUTHORIZED",
                "session": str(session),
                "session_file_expected": str(session) + ".session",
            }

        print("============================================================")
        print("FATHER Telegram - one-time local Telethon authorization")
        print("============================================================")
        print("Phone, Telegram code and 2FA password are entered only in this local console.")
        print("They are not written to Git or to the authorization report.")
        print("do not paste them into chat")
        print("")

        phone = os.getenv("TELEGRAM_PHONE_NUMBER", "").strip()
        if not phone:
            phone = getpass.getpass("Telegram phone number (international format, e.g. +...): ").strip()
        if not phone:
            raise RuntimeError("Telegram phone number is required")

        await client.send_code_request(phone)
        code = getpass.getpass("Telegram login code: ").strip().replace(" ", "")
        if not code:
            raise RuntimeError("Telegram login code is required")

        try:
            await client.sign_in(phone=phone, code=code)
        except SessionPasswordNeededError:
            password = getpass.getpass("Telegram 2FA password: ")
            if not password:
                raise RuntimeError("Telegram 2FA password is required")
            await client.sign_in(password=password)
        except PhoneCodeInvalidError as exc:
            raise RuntimeError("Telegram login code is invalid") from exc
        except PhoneCodeExpiredError as exc:
            raise RuntimeError("Telegram login code expired; rerun authorization to request a fresh code") from exc

        if not await client.is_user_authorized():
            raise RuntimeError("Telethon session did not become authorized")

        return {
            "status": "AUTHORIZED",
            "session": str(session),
            "session_file_expected": str(session) + ".session",
        }
    finally:
        await client.disconnect()


def main() -> int:
    try:
        result = asyncio.run(_authorize())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({
            "status": "AUTHORIZATION_FAILED",
            "error": f"{type(exc).__name__}: {exc}",
        }, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
