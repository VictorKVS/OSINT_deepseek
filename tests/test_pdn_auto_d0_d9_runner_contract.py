from pathlib import Path


def test_one_click_pdn_auto_runner_is_bounded_and_fail_closed():
    cmd = Path("RUN_PDN_KNOWLEDGE_FACTORY_AUTO.cmd").read_text(encoding="utf-8")

    assert "scripts\\run_pdn_operator_import.py" in cmd
    assert "scripts\\normalize_pdn_d4_d5_article_points.py" in cmd
    assert "scripts\\audit_pdn_d4_d5_structure.py" in cmd
    assert "scripts\\run_pdn_d6_d9.py" in cmd
    assert "scripts\\audit_pdn_d6_d9.py" in cmd
    assert "scripts\\run_pdn_d10_d12.py" in cmd
    assert "scripts\\audit_pdn_d10_d12.py" in cmd
    assert "scripts\\run_pdn_d13_review_queue.py" in cmd
    assert cmd.count("--document-id") == 4
    assert "if errorlevel 1 goto :fail" in cmd
    assert "D14 remains NEEDS_REVIEW" in cmd
    assert "D15 autonomous promotion is blocked" in cmd
    assert "exit /b 2" in cmd


def test_d6_d9_runner_requires_quality_gate_and_keeps_review_candidates_unpromoted():
    script = Path("scripts/run_pdn_d6_d9.py").read_text(encoding="utf-8")

    assert "promotion_to_d6_allowed" in script
    assert "D6_BLOCKED_BY_D4_D5_QUALITY_GATE" in script
    assert "CANDIDATE_NEEDS_REVIEW" in script
    assert "autonomous_kb_promotion" in script
    assert "PipelineStage.D6_TERMS_EXTRACTED" in script
    assert "PipelineStage.D9_ENTITIES_EXTRACTED" in script
    assert "quality_gate_sha256" in script


def test_d6_d9_quality_gate_checks_lineage_ids_and_promotion_state():
    script = Path("scripts/audit_pdn_d6_d9.py").read_text(encoding="utf-8")

    assert "D6_D9_QUALITY" in script
    assert "LINEAGE_INCOMPLETE" in script
    assert "DUPLICATE_CANDIDATE_IDS" in script
    assert "PROMOTION_STATE_INVALID" in script
    assert "ZERO_EXPLICIT_DEFINITIONS_IN_152" in script
    assert "promotion_to_d10_allowed" in script
    assert "autonomous_kb_promotion" in script
