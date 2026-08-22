from pathlib import Path


def test_d10_d12_runner_is_quality_gated_and_candidate_only():
    script = Path("scripts/run_pdn_d10_d12.py").read_text(encoding="utf-8")

    assert "promotion_to_d10_allowed" in script
    assert "D10_BLOCKED_BY_D6_D9_QUALITY_GATE" in script
    assert "TERM_DEFINED_BY" in script
    assert "REQUIREMENT_MENTIONS_ENTITY" in script
    assert "SHARED_TERM_ACROSS_DOCUMENTS" in script
    assert "DEFINITION_VARIANCE_CANDIDATE" in script
    assert "REQUIREMENT_OVERLAP_CANDIDATE" in script
    assert '"confirmed_conflict": False' in script
    assert "PipelineStage.D10_INTERNAL_RELATIONS" in script
    assert "PipelineStage.D12_CONFLICTS_OVERLAPS" in script
    assert "autonomous_kb_promotion" in script


def test_d10_d12_quality_gate_blocks_bad_refs_and_premature_conflicts():
    script = Path("scripts/audit_pdn_d10_d12.py").read_text(encoding="utf-8")

    assert "BROKEN_INTERNAL_RELATION_REFERENCE" in script
    assert "INVALID_CROSS_DOCUMENT_RELATION" in script
    assert "CONFLICT_CANDIDATE_PREMATURELY_CONFIRMED" in script
    assert "promotion_to_d13_allowed" in script
    assert "autonomous_kb_promotion" in script


def test_d13_builder_prepares_review_queue_but_does_not_complete_d14_or_d15():
    script = Path("scripts/run_pdn_d13_review_queue.py").read_text(encoding="utf-8")

    assert "promotion_to_d13_allowed" in script
    assert "D13_BLOCKED_BY_D10_D12_QUALITY_GATE" in script
    assert "PipelineStage.D13_KNOWLEDGE_GRAPH_READY" in script
    assert "PipelineStage.D14_EXPERT_REVIEWED" in script
    assert "StageState.NEEDS_REVIEW" in script
    assert "D14_REVIEW_QUEUE.md" in script
    assert "autonomous_kb_promotion" in script
    assert "D15" in script


def test_one_click_runner_reaches_d13_in_order_and_stops_before_autonomous_review():
    cmd = Path("RUN_PDN_KNOWLEDGE_FACTORY_AUTO.cmd").read_text(encoding="utf-8")

    expected = [
        "scripts\\run_pdn_operator_import.py",
        "scripts\\normalize_pdn_d4_d5_article_points.py",
        "scripts\\audit_pdn_d4_d5_structure.py",
        "scripts\\run_pdn_d6_d9.py",
        "scripts\\audit_pdn_d6_d9.py",
        "scripts\\run_pdn_d10_d12.py",
        "scripts\\audit_pdn_d10_d12.py",
        "scripts\\run_pdn_d13_review_queue.py",
    ]
    positions = [cmd.index(value) for value in expected]
    assert positions == sorted(positions)
    assert "D14 remains NEEDS_REVIEW" in cmd
    assert "D15 autonomous promotion is blocked" in cmd
