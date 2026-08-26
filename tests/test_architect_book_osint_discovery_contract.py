import json
from pathlib import Path


def test_architect_book_registry_has_original_16_targets():
    payload = json.loads(Path("config/architect_book_acquisition_registry.json").read_text(encoding="utf-8"))
    targets = payload["targets"]
    assert len(targets) == 16
    assert {row["book_id"] for row in targets} == {f"ARCH-BOOK-{i:03d}" for i in range(1, 17)}
    assert payload["policy"]["commercial_fulltext_auto_download"] is False


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
