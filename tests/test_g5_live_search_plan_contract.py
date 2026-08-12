from pathlib import Path


def test_live_runner_uses_formal_role_protocol():
    source = Path("scripts/run_live_telegram_material.py").read_text(encoding="utf-8")

    for token in (
        "ResearchRequest(",
        "DeterministicTelegramSearchPlanner",
        "PlanDecision(",
        'status="ACCEPT"',
        'workflow.transition("COLLECTING"',
        "EvidencePackage(",
    ):
        assert token in source


def test_live_runner_reports_search_plan_lineage():
    source = Path("scripts/run_live_telegram_material.py").read_text(encoding="utf-8")

    for field in (
        '"case_id"',
        '"research_request_id"',
        '"search_plan_id"',
        '"search_plan_algorithm"',
        '"search_plan_knowledge_refs"',
        '"plan_decision"',
        '"workflow_state"',
        '"protocol_passed"',
        '"evidence_package_id"',
        '"evidence_achieved_sufficiency"',
        '"evidence_critical_gaps"',
    ):
        assert field in source
