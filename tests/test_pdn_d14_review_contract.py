from pathlib import Path


def test_d14_prep_is_rule_class_plus_each_conflict_candidate_and_never_auto_approves():
    script = Path("scripts/prepare_pdn_d14_review.py").read_text(encoding="utf-8")
    auto = Path("RUN_PDN_KNOWLEDGE_FACTORY_AUTO.cmd").read_text(encoding="utf-8")

    assert "RULE_CLASS_PLUS_EACH_D12_CANDIDATE" in script
    assert "D14_REVIEW_PACKET.md" in script
    assert "D14_DECISIONS.jsonl" in script
    assert '"decision": "PENDING"' in script
    assert "autonomous_kb_promotion" in script
    assert "prepare_pdn_d14_review.py" in auto
    assert "D14 remains NEEDS_REVIEW" in auto


def test_d14_apply_requires_complete_human_decisions_and_keeps_d15_unpromoted():
    script = Path("scripts/apply_pdn_d14_decisions.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_D14_APPLY_DECISIONS.cmd").read_text(encoding="utf-8")

    assert "D14_DECISION_SET_MISMATCH" in script
    assert "REVIEWER_OR_REASON_MISSING" in script
    assert "ESCALATE" in script
    assert "PipelineStage.D14_EXPERT_REVIEWED" in script
    assert "StageState.VERIFIED" in script
    assert "D15_PROMOTION_REQUEST" in script
    assert "AWAITING_EXPLICIT_D15_APPROVAL" in script
    assert "autonomous_kb_promotion" in script
    assert "apply_pdn_d14_decisions.py" in cmd
    assert "D15 remains NOT_DONE" in cmd
