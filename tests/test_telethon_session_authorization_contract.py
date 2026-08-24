from pathlib import Path


def test_telethon_authorization_is_local_interactive_and_session_backed():
    text = Path("scripts/authorize_telethon_session.py").read_text(encoding="utf-8")
    assert "client.is_user_authorized()" in text
    assert "client.send_code_request(phone)" in text
    assert "client.sign_in(phone=phone, code=code)" in text
    assert "SessionPasswordNeededError" in text
    assert 'getpass.getpass("Telegram phone number' in text
    assert 'getpass.getpass("Telegram login code' in text
    assert 'getpass.getpass("Telegram 2FA password' in text
    assert "TELEGRAM_PHONE_NUMBER" in text
    assert "legacy" in text and "reader_session" in text
    assert "AUTHORIZED" in text
    assert "ALREADY_AUTHORIZED" in text
    assert "do not paste them into chat" in text


def test_telethon_authorization_does_not_report_sensitive_values():
    text = Path("scripts/authorize_telethon_session.py").read_text(encoding="utf-8")
    assert '"phone": phone' not in text
    assert '"code": code' not in text
    assert '"password": password' not in text
    assert "print(phone)" not in text
    assert "print(code)" not in text
    assert "print(password)" not in text


def test_architect_launcher_orders_network_auth_then_acquisition():
    text = Path("scripts/run_architect_telegram_acquisition.ps1").read_text(encoding="utf-8")
    network_index = text.index("test_telegram_network_path.ps1")
    auth_index = text.index("authorize_telethon_session.py")
    acquire_index = text.index("run_architect_telegram_acquisition.py")
    assert network_index < auth_index < acquire_index
    assert "Telethon session authorization did not complete; acquisition was not started." in text
    assert "[ACQUIRE] Telethon session is authorized. Starting Architect acquisition." in text
