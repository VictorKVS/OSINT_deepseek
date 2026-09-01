from pathlib import Path


def test_telegram_network_preflight_is_read_only_and_fail_closed():
    text = Path("scripts/test_telegram_network_path.ps1").read_text(encoding="utf-8")
    assert "Test-TcpEndpoint" in text
    assert "telegram.org" in text
    assert "web.telegram.org" in text
    assert "Get-NetTCPConnection -State Listen" in text
    assert "Get-NetAdapter" in text
    assert "Get-InstalledTransportClients" in text
    assert "WINDOWS_UNINSTALL_REGISTRY" in text
    assert "COMMAND_ON_PATH" in text
    assert "installed_transport_clients" in text
    assert "TRANSPORT_CLIENT_INSTALLED_NOT_ACTIVE" in text
    assert "auto_use_unknown_proxy = $false" in text
    assert "auto_change_windows_routes = $false" in text
    assert "auto_enable_vpn = $false" in text
    assert "auto_launch_transport_client = $false" in text
    assert "DIRECT_BLOCKED_NO_APPROVED_ALTERNATE_ROUTE" in text
    assert "LOCAL_PROXY_CANDIDATE_REQUIRES_EXPLICIT_CONFIG" in text
    assert "Set-NetRoute" not in text
    assert "New-NetRoute" not in text
    assert "Remove-NetRoute" not in text
    assert "Set-NetFirewall" not in text
    assert "Start-Process" not in text


def test_architect_launcher_runs_network_gate_before_telethon():
    text = Path("scripts/run_architect_telegram_acquisition.ps1").read_text(encoding="utf-8")
    preflight = text.index("test_telegram_network_path.ps1")
    python_runner = text.index("run_architect_telegram_acquisition.py")
    assert preflight < python_runner
    assert "acquisition will not start blindly" in text
    assert "network path is not proven reachable" in text


def test_one_click_network_diagnostic_exists_and_is_secret_independent():
    text = Path("RUN_TELEGRAM_NETWORK_DIAGNOSTIC.cmd").read_text(encoding="utf-8")
    assert "test_telegram_network_path.ps1" in text
    assert "No Telegram credentials are read" in text
    assert "TELEGRAM_API_ID" not in text
    assert "TELEGRAM_API_HASH" not in text
