from pathlib import Path


def test_departmental_shadow_runner_boundary():
    text = Path("scripts/run_security_departmental_candidate_d4_d9.py").read_text(encoding="utf-8")
    assert "SHADOW_CANDIDATE_D4_D9_ONLY" in text
    assert '"official_pipeline_advanced": False' in text
    assert '"currentness_verified": False' in text
    assert '"legal_truth_eligible": False' in text
    assert '"kb_promotion_allowed": False' in text
    assert "KnowledgeFactoryStore" not in text
    assert "set_stage_state" not in text


def test_departmental_shadow_runner_reuses_existing_algorithms():
    text = Path("scripts/run_security_departmental_candidate_d4_d9.py").read_text(encoding="utf-8")
    assert "parse_legal_structure" in text
    assert "build_chunks" in text
    assert "extract_candidates" in text
    assert "ThreadPoolExecutor(max_workers=WORKERS" in text
    assert "WORKERS = 5" in text


def test_departmental_shadow_cmd_bootstraps_repo_root():
    text = Path("RUN_SECURITY_DEPARTMENTAL_D4_D9_CANDIDATE.cmd").read_text(encoding="utf-8")
    assert 'set "PYTHONPATH=%CD%;%PYTHONPATH%"' in text
    assert "%PY% scripts\\run_security_departmental_candidate_d4_d9.py" in text
