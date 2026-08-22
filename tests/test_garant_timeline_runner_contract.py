from pathlib import Path


def test_garant_timeline_runner_is_local_metadata_only_contract():
    script = Path("scripts/run_pdn_garant_timeline.py").read_text(encoding="utf-8")

    assert "data\" / \"operator_import\" / \"garant_timeline" in script
    assert "semantic_text_mirrored" in script
    assert "official_evidence_requests" in script
    assert "GARANT_NAVIGATES_A0_A1_PROVES" in script
    assert "source_capture_sha256" in script
    assert "hashlib.sha256" in script
    assert "requests.get" not in script
    assert "urllib" not in script


def test_garant_timeline_one_click_runner_exists():
    cmd = Path("RUN_PDN_GARANT_TIMELINE.cmd")
    assert cmd.is_file()
    content = cmd.read_text(encoding="utf-8")
    assert "scripts\\run_pdn_garant_timeline.py" in content
    assert "data\\operator_import\\garant_timeline" in content
