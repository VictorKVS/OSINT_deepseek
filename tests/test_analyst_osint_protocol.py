import pytest

from father_osint.protocol import (
    DecisionRecord,
    EvidencePackage,
    PlanDecision,
    ResearchGap,
    ResearchRequest,
    ResearchWorkflow,
    SearchPlan,
)


def test_research_request_normalizes_sufficiency_and_requires_questions():
    request = ResearchRequest(
        objective="Establish what happened",
        research_questions=["What happened?"],
        required_sufficiency="good",
    )
    assert request.required_sufficiency == "GOOD"

    with pytest.raises(ValueError):
        ResearchRequest(objective="x", research_questions=[])


def test_search_plan_requires_knowledge_reference_or_explicit_gap():
    request = ResearchRequest(
        objective="Test Telegram search planning",
        research_questions=["Which relevant messages exist?"],
    )

    with pytest.raises(ValueError):
        SearchPlan(
            case_id=request.case_id,
            request_id=request.request_id,
            information_gaps=["Relevant Telegram evidence"],
            source_classes=["telegram"],
            methods=["historical channel collection"],
            search_sequence=["collect selected channels"],
        )

    plan = SearchPlan(
        case_id=request.case_id,
        request_id=request.request_id,
        information_gaps=["Relevant Telegram evidence"],
        source_classes=["telegram"],
        methods=["historical channel collection"],
        search_sequence=["collect selected channels"],
        knowledge_refs=["SIKB.telegram.history.v1"],
    )
    assert plan.knowledge_refs == ["SIKB.telegram.history.v1"]


def test_plan_amendment_requires_reasons_and_changes():
    with pytest.raises(ValueError):
        PlanDecision(case_id="c", search_plan_id="p", status="AMEND")

    decision = PlanDecision(
        case_id="c",
        search_plan_id="p",
        status="amend",
        reason_codes=["COVERAGE_TOO_NARROW"],
        requested_changes=["add second independent channel"],
    )
    assert decision.status == "AMEND"


def test_workflow_blocks_collection_before_plan_approval():
    workflow = ResearchWorkflow("case-1")
    workflow.transition("ISSUED", actor_role="ANALYST", reason="request issued")
    workflow.transition("PLANNING", actor_role="OSINT_EXPERT", reason="planning started")

    with pytest.raises(ValueError, match="invalid transition"):
        workflow.transition("COLLECTING", actor_role="OSINT_EXPERT", reason="too early")


def test_workflow_accept_path_to_closed():
    workflow = ResearchWorkflow("case-1")
    workflow.transition("ISSUED", actor_role="ANALYST", reason="issued")
    workflow.transition("PLANNING", actor_role="OSINT_EXPERT", reason="planning")
    workflow.transition("PLAN_REVIEW", actor_role="OSINT_EXPERT", reason="proposal ready")
    workflow.apply_plan_decision(
        PlanDecision(case_id="case-1", search_plan_id="plan-1", status="ACCEPT")
    )
    workflow.transition("COLLECTING", actor_role="OSINT_EXPERT", reason="approved")
    workflow.transition("EVIDENCE_DELIVERED", actor_role="OSINT_EXPERT", reason="package delivered")
    workflow.transition("ANALYSIS", actor_role="ANALYST", reason="analysis started")
    workflow.transition("CLOSED", actor_role="ANALYST", reason="answer sufficient")

    assert workflow.state == "CLOSED"
    assert [item["to"] for item in workflow.history] == [
        "ISSUED",
        "PLANNING",
        "PLAN_REVIEW",
        "APPROVED",
        "COLLECTING",
        "EVIDENCE_DELIVERED",
        "ANALYSIS",
        "CLOSED",
    ]


def test_workflow_amend_returns_to_planning():
    workflow = ResearchWorkflow("case-1", state="PLAN_REVIEW")
    workflow.apply_plan_decision(
        PlanDecision(
            case_id="case-1",
            search_plan_id="plan-1",
            status="AMEND",
            reason_codes=["NEED_COUNTER_EVIDENCE"],
            requested_changes=["add counter-evidence branch"],
        )
    )
    assert workflow.state == "PLANNING"


def test_evidence_package_and_research_gap_are_explicit_about_sufficiency():
    package = EvidencePackage(
        case_id="case-1",
        request_id="req-1",
        search_plan_id="plan-1",
        requested_sufficiency="GOOD",
        achieved_sufficiency="MINIMUM",
        material_refs=["m1"],
        critical_gaps=["independent confirmation missing"],
    )
    assert package.achieved_sufficiency == "MINIMUM"

    gap = ResearchGap(
        case_id="case-1",
        parent_request_id="req-1",
        question="Can the claim be independently corroborated?",
        why_needed="GOOD sufficiency has not been reached",
        missing_evidence_type="independent source",
        current_sufficiency="MINIMUM",
        required_sufficiency="GOOD",
    )
    assert gap.required_sufficiency == "GOOD"


def test_decision_record_carries_algorithm_and_knowledge_lineage():
    record = DecisionRecord(
        case_id="case-1",
        role_id="OSINT_EXPERT",
        decision="Use Telegram historical collection",
        knowledge_refs=["SIKB.telegram.history.v1"],
        method_refs=["telegram_history_collection.v1"],
        reason_codes=["HISTORY_REQUIRED"],
        algorithm_version="search-plan-v1",
        knowledge_version="sikb-v1",
    )
    data = record.to_dict()

    assert data["role_id"] == "OSINT_EXPERT"
    assert data["algorithm_version"] == "search-plan-v1"
    assert data["knowledge_version"] == "sikb-v1"
