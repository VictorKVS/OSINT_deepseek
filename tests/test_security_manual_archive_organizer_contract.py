from pathlib import Path


def test_manual_archive_organizer_preserves_review_gates_and_groups_files():
    text = Path("scripts/organize_security_manual_archive.py").read_text(encoding="utf-8")
    assert "_MANUAL_OFFICIAL_ARCHIVE" in text
    assert "authority_for" in text
    assert "domain_for" in text
    assert "legal_truth_eligible" in text
    assert "INDEX.json" in text
    assert "INDEX.md" in text
    for marker in (
        "FEDERAL_LAWS",
        "GOVERNMENT",
        "FSTEC",
        "FSB",
        "ROSKOMNADZOR",
        "ROSSTANDART_GOST",
    ):
        assert marker in text


def test_one_click_manual_import_and_organize_launcher_exists():
    text = Path("IMPORT_AND_ORGANIZE_SECURITY_OFFICIAL.cmd").read_text(encoding="utf-8")
    assert "import_security_official_manual_inbox.py" in text
    assert "organize_security_manual_archive.py" in text
    assert "_MANUAL_OFFICIAL_INBOX" in text
    assert "_MANUAL_OFFICIAL_ARCHIVE" in text
