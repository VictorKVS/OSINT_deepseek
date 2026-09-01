from pathlib import Path


def test_timeline_evidence_runner_is_local_fail_closed_and_non_promoting():
    script = Path("scripts/resolve_pdn_timeline_evidence.py").read_text(encoding="utf-8")

    assert "OFFICIAL_EVIDENCE_REQUEST" in script
    assert "VERIFIED_OFFICIAL_EVIDENCE" in script
    assert "timeline_official_evidence" in script
    assert "timeline_evidence_resolution.jsonl" in script
    assert '"timeline_source_remains_non_evidentiary": True' in script
    assert '"legal_truth_promoted": False' in script
    assert "return 0 if pending == 0 else 2" in script


def test_timeline_evidence_one_click_runner_exists():
    runner = Path("RUN_RESOLVE_PDN_TIMELINE_EVIDENCE.cmd")
    text = runner.read_text(encoding="utf-8")

    assert runner.is_file()
    assert "resolve_pdn_timeline_evidence.py" in text
    assert "verified A0/A1" in text
    assert "no legal date was invented" in text
