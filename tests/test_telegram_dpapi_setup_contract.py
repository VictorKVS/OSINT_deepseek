from pathlib import Path


def test_windows_dpapi_setup_reads_id_as_numeric_text_and_hash_as_hidden_secret():
    text = Path("scripts/setup_telegram_credentials.ps1").read_text(encoding="utf-8")
    assert "$apiIdPlain = (Read-Host 'Telegram API ID').Trim()" in text
    assert "Read-Host 'Telegram API ID' -AsSecureString" not in text
    assert "[long]::TryParse($apiIdPlain, [ref]$parsedApiId)" in text
    assert "$parsedApiId -le 0" in text
    assert "$apiHashSecure = Read-Host 'Telegram API HASH' -AsSecureString" in text
    assert "ConvertTo-SecureString $apiIdPlain -AsPlainText -Force" in text
    assert "ConvertFrom-SecureString $apiIdSecure" in text
    assert "ConvertFrom-SecureString $apiHashSecure" in text
    assert "No plaintext credential file was created." in text
    assert "do not paste them into chat." in text
