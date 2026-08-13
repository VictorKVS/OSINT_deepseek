import pytest

from father_osint.acquisition_report import DeterministicAcquisitionReportBuilder
from father_osint.protocol import EvidencePackage, ResearchRequest, SearchPlan
from father_osint.sufficiency import ResearchSufficiencyAssessment, ResearchSufficiencyResult
from father_osint.protocol import DecisionRecord


def _request() -> ResearchRequest:
    return ResearchRequest(
        objective="Establish what the selected Telegram sources support",
        research_questions=["What is observed and what remains unverified?"],
        required_sufficiency="GOOD",
        hypotheses=["A leading explanation exists"],
    )


def _plan(request: ResearchRequest) -> SearchPlan:
    return SearchPlan(
        case_id=request.case_id,
        request_id=request.request_id,
        information_gaps=list(request.research_questions),
        source_classes=["telegram"],
        methods=["bounded_telegram_collection"],
        search_sequence=["sample", "refine", "collect"],
        knowledge_refs=["SIKB.telegram.source-playbook.v0.1"],
        expected_sufficiency="GOOD",
    )


def _package(request: ResearchRequest, plan: SearchPlan) -> EvidencePackage:
    return EvidencePackage(
        case_id=request.case_id,
        request_id=request.request_id,
        search_plan_id=plan.search_plan_id,
        requested_sufficiency="GOOD",
        achieved_sufficiency="MINIMUM",
        material_refs=["m1"],
        evidence_refs=["e1"],
        lead_refs=["l1"],
        source_attempts=[
            {"source": "telegram://channel/a", "status": "SEARCHED"},
            {"source": "telegram://channel/b", "status": "FAILED", "reason": "unavailable"},
        ],
        provenance_refs=["raw:sha256:abc"],
        contradictions=["c1"],
        coverage={"successful_source_classes": 1, "distinct_source_ids": 1},
        limitations=["Telegram-only proof"],
        critical_gaps=["Need independent non-Telegram corroboration"],
        recommended_follow_up=["Check an independent primary source"],
        decision_record_refs=["decision-1"],
    )


def test_report_preserves_failures_gaps_sufficiency_and_lineage():
    request = _request()
    plan = _plan(request)
    package = _package(request, plan)

    result = DeterministicAcquisitionReportBuilder().build(
        request,
        plan,
        package,
        collection_bounds={"max_items": 10, "source_class": "telegram"},
    )

    report = result.report
    assert report.requested_sufficiency == "GOOD"
    assert report.achieved_sufficiency == "MINIMUM"
    assert report.source_failures[0]["source"] == "telegram://channel/b"
    assert "Need independent non-Telegram corroboration" in report.unresolved_gaps
    assert request.request_id in report.lineage_refs
    assert plan.search_plan_id in report.lineage_refs
    assert package.package_id in report.lineage_refs
    assert report.evidence_quality_summary["truth_probability"] == "NOT_CALCULATED"
    assert result.decision_record.role_id == "OSINT_EXPERT"
    assert result.decision_record.decision == "BUILD_TRANSPARENT_ACQUISITION_REPORT"


def test_report_uses_explicit_sufficiency_assessment_without_inventing_score():
    request = _request()
    plan = _plan(request)
    package = _package(request, plan)
    assessment = ResearchSufficiencyAssessment(
        case_id=request.case_id,
        package_id=package.package_id,
        requested_sufficiency="GOOD",
        achieved_sufficiency="INSUFFICIENT",
        reasons=["independent corroboration is missing"],
        critical_gaps=["blocking: independent source missing"],
        recommended_next_search=["search an independent primary source"],
    )
    sufficiency = ResearchSufficiencyResult(
        assessment=assessment,
        decision_record=DecisionRecord(
            case_id=request.case_id,
            role_id="OSINT_EXPERT",
            decision="ASSESS_RESEARCH_SUFFICIENCY",
        ),
    )

    report = DeterministicAcquisitionReportBuilder().build(
        request,
        plan,
        package,
        sufficiency=sufficiency,
    ).report

    assert report.achieved_sufficiency == "INSUFFICIENT"
    assert report.sufficiency_reasons == ["independent corroboration is missing"]
    assert "search an independent primary source" in report.recommended_follow_up
    assert report.evidence_quality_summary["truth_probability"] == "NOT_CALCULATED"


def test_report_rejects_cross_case_lineage():
    request = _request()
    plan = _plan(request)
    package = _package(request, plan)
    package.case_id = "different-case"

    with pytest.raises(ValueError, match="case lineage mismatch"):
        DeterministicAcquisitionReportBuilder().build(request, plan, package)


def test_report_does_not_hide_failed_source_attempts():
    request = _request()
    plan = _plan(request)
    package = _package(request, plan)

    report = DeterministicAcquisitionReportBuilder().build(request, plan, package).report

    assert len(report.source_attempts) == 2
    assert len(report.source_failures) == 1
    assert report.source_failures[0]["status"] == "FAILED"
