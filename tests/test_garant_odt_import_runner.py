from pathlib import Path


def test_garant_152_odt_import_runner_prefers_downloaded_odt_and_identity_gate():
    script = Path("scripts/import_latest_garant_152_odt.py").read_text(encoding="utf-8")
    cmd = Path("RUN_IMPORT_GARANT_152_ODT.cmd").read_text(encoding="utf-8")

    assert 'REPO_ROOT = Path(__file__).resolve().parents[1]' in script
    assert 'sys.path.insert(0, str(REPO_ROOT))' in script
    assert 'Path.home() / "Downloads"' in script
    assert 'MARKERS = ("152-ФЗ", "О персональных данных")' in script
    assert "extract_odt_text" in script
    assert "sha256" in script
    assert "GARANT_ODT_IMPORTED" in script
    assert "scripts\\import_latest_garant_152_odt.py" in cmd
    assert "scripts\\run_pdn_garant_timeline.py" in cmd
