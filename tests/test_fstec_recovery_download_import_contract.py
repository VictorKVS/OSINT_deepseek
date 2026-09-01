from pathlib import Path


def test_one_click_fstec_recovery_download_import_launcher_exists():
    cmd = Path("DOWNLOAD_AND_IMPORT_FSTEC_RECOVERY.cmd").read_text(encoding="utf-8")
    assert "download_and_import_fstec_recovery.ps1" in cmd
    assert "LATEST_FSTEC_RECOVERY_IMPORT.json" in cmd


def test_download_script_prefers_latest_non_expired_actions_artifact_and_imports():
    text = Path("scripts/download_and_import_fstec_recovery.ps1").read_text(encoding="utf-8")
    assert "actions/artifacts?per_page=100" in text
    assert "expired" in text
    assert "ArtifactNamePrefix" in text
    assert "GH_TOKEN" in text
    assert "GITHUB_TOKEN" in text
    assert "Get-Command gh" in text
    assert "IMPORT_FSTEC_RECOVERY_BUNDLE.cmd" in text
