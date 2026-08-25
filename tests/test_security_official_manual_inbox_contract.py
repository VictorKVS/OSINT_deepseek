from pathlib import Path


def test_manual_official_inbox_importer_preserves_traceability_and_blocks_promotion():
    text = Path("scripts/import_security_official_manual_inbox.py").read_text(encoding="utf-8")
    assert "_MANUAL_OFFICIAL_INBOX" in text
    assert "MANUAL_DOWNLOAD_CHECKLIST.tsv" in text
    assert "MANUAL_BROWSER_DOWNLOAD" in text
    assert "sha256" in text.casefold()
    assert '"SOURCE_URL_MISSING"' in text
    assert '"document_identity_confirmed": False' in text
    assert '"legal_truth_eligible": False' in text
    assert '"kb_auto_promotion": False' in text


def test_manual_inbox_launchers_exist():
    importer = Path("IMPORT_SECURITY_OFFICIAL_MANUAL_INBOX.cmd").read_text(encoding="utf-8")
    opener = Path("OPEN_SECURITY_OFFICIAL_MANUAL_INBOX.cmd").read_text(encoding="utf-8")
    assert "import_security_official_manual_inbox.py" in importer
    assert "MANUAL_DOWNLOAD_CHECKLIST.tsv" in importer
    assert "_MANUAL_OFFICIAL_INBOX" in opener
    assert "start \"\"" in opener
