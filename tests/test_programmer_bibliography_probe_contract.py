import json
from pathlib import Path


def test_programmer_bibliography_first_wave_is_bounded_and_explicit():
    registry = json.loads(Path("config/programmer_bibliography_targets.json").read_text(encoding="utf-8"))
    policy = registry["policy"]
    assert registry["role_id"] == "PROGRAMMER"
    assert len(registry["targets"]) == 20
    assert policy["probe_only"] is True
    assert policy["download"] is False
    assert policy["auto_join_channels"] is False
    assert policy["access_control_bypass"] is False
    assert policy["paywall_bypass"] is False
    assert int(policy["max_parallel_streams"]) == 5
    ids = [row["id"] for row in registry["targets"]]
    assert len(ids) == len(set(ids))
    for row in registry["targets"]:
        assert row["title"]
        assert row["author"]
        assert row["query_variants"]


def test_programmer_bibliography_probe_never_downloads_payloads():
    text = Path("scripts/probe_programmer_bibliography_telegram.py").read_text(encoding="utf-8")
    assert "client.iter_messages(None, search=query" in text
    assert "FOUND_CANDIDATE" in text
    assert "AMBIGUOUS" in text
    assert "NOT_FOUND" in text
    assert '"probe_only": True' in text
    assert '"downloaded_total": 0' in text
    assert "download_media" not in text
    assert "join_channel" not in text.casefold()


def test_programmer_bibliography_probe_uses_shared_proven_gates():
    ps1 = Path("scripts/run_team_role_acquisition.ps1").read_text(encoding="utf-8")
    cmd = Path("RUN_PROGRAMMER_BIBLIOGRAPHY_PROBE.cmd").read_text(encoding="utf-8")
    assert "[switch] $BibliographyProbe" in ps1
    assert "test_telegram_network_path.ps1" in ps1
    assert "authorize_telethon_session.py" in ps1
    assert "probe_programmer_bibliography_telegram.py" in ps1
    assert "-Role PROGRAMMER -BibliographyProbe" in cmd
    assert "PROBE ONLY - no downloads" in cmd
