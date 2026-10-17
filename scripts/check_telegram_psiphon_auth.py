"""Check existing Telethon session authorization over the Psiphon SOCKS5 proxy.

No sign-in, no channel reads, no API secrets in reports. Does not modify original
session: --session must identify an operator-provided disposable compatible copy.
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.transports.telethon import TelethonTransport


def load_credentials(path: Path) -> tuple[int, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        if key in {"TELEGRAM_API_ID", "TELEGRAM_API_HASH"}:
            values[key] = value.strip().strip('"').strip("'")
    identifier = values.get("TELEGRAM_API_ID", "")
    secret = values.get("TELEGRAM_API_HASH", "")
    if not identifier.isdecimal() or not secret:
        raise ValueError("Telegram credentials missing or invalid")
    return int(identifier), secret


async def verify(transport: TelethonTransport) -> bool:
    client = transport._build_client()
    try:
        await asyncio.wait_for(client.connect(), timeout=40)
        connected = client.is_connected()
        authorized = await asyncio.wait_for(client.is_user_authorized(), timeout=20)
        print(f"FATHER_TRANSPORT_CONNECTED: {connected}")
        print(f"SESSION_AUTHORIZED: {authorized}")
        print("MESSAGES_READ: 0")
        return connected and authorized
    finally:
        await client.disconnect()


def main() -> int:
    parser = argparse.ArgumentParser(description="FATHER safe Telegram auth verification")
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--proxy-host", default="127.0.0.1")
    parser.add_argument("--proxy-port", type=int, default=1080)
    args = parser.parse_args()

    import socks

    session_file = args.session
    if session_file.suffix != ".session":
        session_file = Path(str(session_file) + ".session")
    if not session_file.is_file():
        raise SystemExit("SESSION_MISSING")
    api_id, api_hash = load_credentials(args.env_file)
    transport = TelethonTransport(
        api_id=api_id,
        api_hash=api_hash,
        session_path=Path(str(session_file)[:-len(".session")]),
        channels=["@telegram"],
        proxy=(socks.SOCKS5, args.proxy_host, args.proxy_port, True),
    )
    try:
        return 0 if asyncio.run(verify(transport)) else 2
    except (OSError, asyncio.TimeoutError, RuntimeError) as exc:
        print(f"CONNECTION_ERROR: {type(exc).__name__}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
