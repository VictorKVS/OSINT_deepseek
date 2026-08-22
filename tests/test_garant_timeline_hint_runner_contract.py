from pathlib import Path


def test_runner_distinguishes_compact_hints_from_empty_or_verified_timeline():
    script = Path("scripts/run_pdn_garant_timeline.py").read_text(encoding="utf-8")

    assert "TIMELINE_HINTS_READY" in script
    assert "amendment_date_hints" in script
    assert "A2_NAVIGATION_HINT_ONLY" in script
    assert "official_evidence_requests" in script
    assert "hard_failures" in script
