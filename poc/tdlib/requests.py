from __future__ import annotations

from pathlib import Path
from typing import Any


def set_tdlib_parameters_request(
    *,
    api_id: int,
    api_hash: str,
    database_directory: str,
    files_directory: str,
    system_language_code: str = "en",
    device_model: str = "FATHER-OSINT-PoC",
    application_version: str = "0.1",
) -> dict[str, Any]:
    if api_id <= 0:
        raise ValueError("api_id must be > 0")
    if not api_hash.strip():
        raise ValueError("api_hash must not be empty")

    db_dir = str(Path(database_directory).expanduser())
    files_dir = str(Path(files_directory).expanduser())

    return {
        "@type": "setTdlibParameters",
        "use_test_dc": False,
        "database_directory": db_dir,
        "files_directory": files_dir,
        "use_file_database": True,
        "use_chat_info_database": True,
        "use_message_database": True,
        "use_secret_chats": False,
        "api_id": int(api_id),
        "api_hash": api_hash,
        "system_language_code": system_language_code,
        "device_model": device_model,
        "system_version": "Python",
        "application_version": application_version,
        "enable_storage_optimizer": True,
        "ignore_file_names": False,
    }


def search_public_chat_request(locator: str) -> dict[str, Any]:
    value = locator.strip()
    if not value:
        raise ValueError("locator must not be empty")
    if value.startswith("https://t.me/"):
        value = value.removeprefix("https://t.me/").split("/", 1)[0]
    value = value.lstrip("@")
    return {"@type": "searchPublicChat", "username": value}


def get_chat_history_request(
    *,
    chat_id: int,
    limit: int,
    from_message_id: int = 0,
    offset: int = 0,
    only_local: bool = False,
) -> dict[str, Any]:
    if limit <= 0:
        raise ValueError("limit must be > 0")
    if limit > 100:
        raise ValueError("TDLib getChatHistory limit must be <= 100 per request")
    return {
        "@type": "getChatHistory",
        "chat_id": int(chat_id),
        "from_message_id": int(from_message_id),
        "offset": int(offset),
        "limit": int(limit),
        "only_local": bool(only_local),
    }
