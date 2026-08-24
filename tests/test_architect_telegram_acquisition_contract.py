import json
from pathlib import Path


def test_architect_telegram_profile_is_bounded_and_local_only():
    profile = json.loads(Path("config/architect_telegram_acquisition_profile.json").read_text(encoding="utf-8"))
    policy = profile["policy"]
    assert profile["role_id"] == "ARCHITECT"
    assert policy["access_scope"] == "ALREADY_ACCESSIBLE_TO_AUTHORIZED_TELEGRAM_SESSION_ONLY"
    assert policy["auto_join_channels"] is False
    assert policy["access_control_bypass"] is False
    assert policy["paywall_bypass"] is False
    assert policy["download_video_by_default"] is False
    assert policy["auto_extract_archives"] is False
    assert policy["commit_downloaded_payloads_to_git"] is False
    assert policy["kb_auto_promotion"] is False
    assert policy["provenance_required"] is True
    assert policy["sha256_required"] is True
    assert int(profile["telegram"]["max_search_streams"]) == 5
    assert int(profile["telegram"]["max_download_streams"]) == 5


def test_architect_telegram_runner_builds_gaps_and_preserves_lineage():
    text = Path("scripts/run_architect_telegram_acquisition.py").read_text(encoding="utf-8")
    assert "has_primary_source" in text
    assert "LESSON_GAP" in text
    assert "ROLE_TOPIC" in text
    assert "client.iter_messages(None, search=target.query" in text
    assert "client.download_media" in text
    assert "_sha256_file" in text
    assert '"chat_id"' in text
    assert '"message_id"' in text
    assert '"source_url"' in text
    assert '"matched_target_ids"' in text
    assert '"speedup_vs_1_stream_pct": None' in text
    assert '"kb_auto_promotion": False' in text
    assert "join_channel" not in text.casefold()
    assert "extractall" not in text.casefold()


def test_architect_telegram_cmd_routes_through_safe_powershell_bootstrap():
    cmd = Path("RUN_ARCHITECT_TELEGRAM_ACQUISITION.cmd").read_text(encoding="utf-8")
    assert 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\\run_architect_telegram_acquisition.ps1" %*' in cmd
    assert "TELEGRAM_API_HASH" not in cmd
    assert "TELEGRAM_API_ID" not in cmd


def test_architect_telegram_bootstrap_reads_local_secret_sources_without_printing_values():
    text = Path("scripts/run_architect_telegram_acquisition.ps1").read_text(encoding="utf-8")
    assert "WINDOWS_$($scope.ToUpperInvariant())_ENV" in text
    assert "Read-DotEnvValue" in text
    assert "TELEGRAM_API_ID" in text
    assert "TELEGRAM_API_HASH" in text
    assert "[Environment]::SetEnvironmentVariable('TELEGRAM_API_ID'" in text
    assert "[Environment]::SetEnvironmentVariable('TELEGRAM_API_HASH'" in text
    assert "Secret values are not printed or persisted by this bootstrap." in text
    assert "do not paste them into chat" in text
    assert "Write-Host $apiId.Value" not in text
    assert "Write-Host $apiHash.Value" not in text
