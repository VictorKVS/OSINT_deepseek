from pathlib import Path


def test_departmental_acquisition_runner_reuses_v2_contract():
    text = Path("scripts/run_security_departmental_5stream.py").read_text(encoding="utf-8")
    assert "import run_security_current_only_5stream_v2 as bulk" in text
    assert "ThreadPoolExecutor(max_workers=WORKERS" in text
    assert "WORKERS = 5" in text
    assert "bulk._process" in text
    assert '"speedup_vs_1_stream_pct": None' in text
    assert 'result["currentness_verified"] = False' in text
    assert 'result["legal_truth_eligible"] = False' in text
    assert "CURRENTNESS_AND_AMENDMENT_CHAIN_NOT_VERIFIED" in text
    assert "WORKING_COPY_CONTENT_BLOCKED" in text
    assert "A2_CONTENT_NOT_FULL_LEGAL_TEXT" in text
    assert '"working_copy_content_blocked_total"' in text
    assert "Exact official bytes prove provenance/identity only" in text


def test_departmental_acquisition_source_map_keeps_a2_separate():
    text = Path("config/security_departmental_acquisition_map.json").read_text(encoding="utf-8")
    assert '"legal_status": "VERIFY_CURRENTNESS"' in text
    assert '"official_source_url"' in text
    assert '"status_reference_url"' in text
    assert "A2 working-copy fallbacks only" in text


def test_departmental_acquisition_cmd_bootstraps_repo_root():
    text = Path("RUN_SECURITY_DEPARTMENTAL_5STREAM.cmd").read_text(encoding="utf-8")
    assert 'set "PYTHONPATH=%CD%;%PYTHONPATH%"' in text
    assert "%PY% scripts\\run_security_departmental_5stream.py" in text
