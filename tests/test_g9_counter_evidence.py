from __future__ import annotations

from father_osint.counter_evidence import (
    CounterEvidenceAttempt,
    DeterministicCounterEvidenceAssessor,
    DeterministicCounterEvidencePlanner,
)
from father_osint.evidence_quality import EvidenceQualityAssessment, EvidenceQualityResult, QualityDimension
from father_osint.protocol import DecisionRecord, EvidencePackage, ResearchRequest
from father_osint.sufficiency_g9 import LineageBoundResearchSufficiencyAssessor


def _request(*, hypotheses: list[str]) -> ResearchRequest:
    return ResearchRequest(
        objective="Establish what the available evidence supports",
        research_questions=["What evidence supports or contradicts the proposed explanation?"],
        hypotheses=hypotheses,
        required_sufficiency="GOOD",
        case_id="case-g9",
        request_id="request-g9",
    )


def _quality(package_id: str) -> EvidenceQualityResult:
    assessment = EvidenceQualityAssessment(
        material_id="m1",
        package_id=package_id,
        reliability=QualityDimension("reliability", "UNKNOWN", "no history", "m", ["m1"]),
        relevance=QualityDimension("relevance", "HIGH", "matches question", "m", ["m1"]),
        independence=QualityDimension("independence", "MEDIUM", "distinct source", "m", ["m1"]),
        recency=QualityDimension("recency", "HIGH", "recent", "m", ["m1"]),
        directness=QualityDimension("directness", "HIGH", "primary", "m", ["m1"]),
        corroboration=QualityDimension("corroboration", "MEDIUM", "distinct support", "m", ["m1"]),
        provenance_quality=QualityDimension("provenance_quality", "HIGH", "canonical provenance", "m", ["m1"]),
    )
    return EvidenceQualityResult(
        [assessment],
        DecisionRecord(case_id="case-g9", role_id="OSINT_EXPERT", decision="QUALITY"),
    )


def _package() -> EvidencePackage:
    return EvidencePackage(
        case_id="case-g9",
        request_id="request-g9",
        search_plan_id="plan-g9",
        requested_sufficiency="GOOD",
        achieved_sufficiency="MINIMUM",
        material_refs=["m1"],
        evidence_refs=["m1"],
        coverage={
            "successful_source_classes": 2,
            "distinct_source_ids": 2,
            "independent_evidence_refs": 2,
            "primary_evidence_refs": 1,
            "counter_evidence_searched": True,
        },
    )


def test_g9_hypothesis_requires_deliberate_challenge_search() -> None:
    result = DeterministicCounterEvidencePlanner().plan(
        _request(hypotheses=["Organization X initiated event Y"])
    )

    assert result.directive.status == "REQUIRED"
    assert result.directive.challenge_questions
    assert result.directive.alternative_searches
    assert "COUNTER_EVIDENCE_REQUIRED" in result.decision_record.reason_codes


def test_g9_without_leading_hypothesis_records_not_applicable() -> None:
    result = DeterministicCounterEvidencePlanner().plan(_request(hypotheses=[]))

    assert result.directive.status == "NOT_APPLICABLE"
    assert "NO_LEADING_HYPOTHESIS" in result.decision_record.reason_codes
    assert result.directive.rationale


def test_g9_required_search_is_incomplete_without_completed_attempt() -> None:
    directive = DeterministicCounterEvidencePlanner().plan(
        _request(hypotheses=["Hypothesis A"])
    ).directive
    result = DeterministicCounterEvidenceAssessor().assess(
        directive,
        attempts=[CounterEvidenceAttempt("search contradiction", "telegram", "FAILED")],
    )

    assert result.assessment.status == "INCOMPLETE"
    assert not result.assessment.counter_evidence_searched


def test_g9_completed_attempt_records_searched_without_claiming_absence() -> None:
    directive = DeterministicCounterEvidencePlanner().plan(
        _request(hypotheses=["Hypothesis A"])
    ).directive
    result = DeterministicCounterEvidenceAssessor().assess(
        directive,
        attempts=[CounterEvidenceAttempt("search contradiction", "telegram", "SEARCHED")],
    )

    assert result.assessment.status == "SEARCHED"
    assert result.assessment.counter_evidence_searched
    assert any("absence" in item for item in result.assessment.limitations)


def test_g9_sufficiency_ignores_naked_counter_evidence_boolean() -> None:
    package = _package()
    result = LineageBoundResearchSufficiencyAssessor().assess(
        package,
        quality=_quality(package.package_id),
    )

    assert result.assessment.achieved_sufficiency == "MINIMUM"
    assert any("counter evidence" in item for item in result.assessment.recommended_next_search)


def test_g9_audited_counter_evidence_lineage_can_satisfy_good_gate() -> None:
    package = _package()
    directive = DeterministicCounterEvidencePlanner().plan(
        _request(hypotheses=["Hypothesis A"])
    ).directive
    counter = DeterministicCounterEvidenceAssessor().assess(
        directive,
        attempts=[CounterEvidenceAttempt("search contradiction", "telegram", "SEARCHED")],
        contradictory_evidence_refs=["m2"],
        alternative_explanation_refs=["m3"],
    )

    result = LineageBoundResearchSufficiencyAssessor().assess(
        package,
        quality=_quality(package.package_id),
        counter_evidence=counter,
    )

    assert result.assessment.achieved_sufficiency == "GOOD"
    assert counter.decision_record.decision_id in result.decision_record.input_refs
    assert "g9.counter-evidence-lineage-required-v1" in result.decision_record.method_refs
