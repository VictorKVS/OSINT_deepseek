from pathlib import Path


def test_fstec_recovery_import_verifies_environment_sha_and_pdf_magic():
    text = Path("scripts/import_fstec_recovery_bundle.py").read_text(encoding="utf-8")
    assert 'GITHUB_ACTIONS_UBUNTU_LATEST' in text
    assert 'sha256_bytes' in text
    assert 'data.startswith(b"%PDF-")' in text
    assert 'document_identity_confirmed' in text
    assert 'VISUAL_FIRST_PAGE_REVIEW_REQUIRED' in text
    assert '"legal_truth_eligible": False' in text
    assert '"kb_auto_promotion": False' in text


def test_fstec_recovery_import_launcher_exists():
    text = Path("IMPORT_FSTEC_RECOVERY_BUNDLE.cmd").read_text(encoding="utf-8")
    assert "import_fstec_recovery_bundle.py" in text
    assert "LATEST_FSTEC_RECOVERY_IMPORT.json" in text
