import json
from pathlib import Path


def test_active_architect_registry_tracks_current_15_gaps():
    payload = json.loads(Path("config/architect_book_acquisition_registry.json").read_text(encoding="utf-8"))
    targets = payload["targets"]
    assert len(targets) == 15
    assert {row["book_id"] for row in targets} == {f"ARCH-GAP-{i:03d}" for i in range(1, 16)}
    assert payload["policy"]["commercial_fulltext_auto_download"] is False
    assert "G:/1/OTUS/Библиотека" in payload["basis"]


def test_legacy_python_engineering_subset_is_preserved():
    payload = json.loads(Path("config/architect_python_engineering_book_registry.json").read_text(encoding="utf-8"))
    assert len(payload["targets"]) == 16


def test_discovery_scans_local_before_telegram_and_never_downloads():
    text = Path("scripts/run_architect_book_osint_discovery.py").read_text(encoding="utf-8")
    assert "FOUND_LOCAL" in text
    assert "MISSING_LOCAL" in text
    assert "iter_messages" in text
    assert "download_media" not in text
    assert '"DISCOVERY_ONLY"' in text
    assert '"kb_auto_promotion": False' in text


def test_launcher_uses_credential_aware_wrapper():
    text = Path("RUN_ARCHITECT_BOOK_OSINT_DISCOVERY.cmd").read_text(encoding="utf-8")
    assert "run_architect_book_osint_discovery.ps1" in text
    assert "Commercial titles: discovery metadata only" in text
