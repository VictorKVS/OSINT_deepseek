from __future__ import annotations

from father_osint.evidence_quality import (
    EvidenceQualityAssessment,
    EvidenceQualityResult,
    QualityDimension,
)
from father_osint.protocol import DecisionRecord, EvidencePackage, ResearchGap
from father_osint.sufficiency import DeterministicResearchSufficiencyAssessor


def _quality(package_id: str, material_id: str) -> EvidenceQualityResult:
    assessment = EvidenceQualityAssessment(
        material_id=material_id,
        package_id=package_id,
        reliability=QualityDimension("reliability", "UNKNOWN", "no history", "m", [material_id]),
        relevance=QualityDimension("relevance", "HIGH", "matches question", "m", [material_id]),
        independence=QualityDimension("independence", "MEDIUM", "no derivative signal", "m", [material_id]),
        recency=QualityDimension("recency", "HIGH", "recent", "m", [material_id]),
        directness=QualityDimension("directness", "HIGH", "primary", "m", [material_id]),
        corroboration=QualityDimension("corroboration", "MEDIUM", "distinct support", "m", [material_id]),
        provenance_quality=QualityDimension("provenance_quality", "HIGH", "canonical provenance", "m", [material_id]),
    )
    decision = DecisionRecord(case_id="case", role_id="OSINT_EXPERT", decision="QUALITY")
    return EvidenceQualityResult([assessment], decision)


def test_g8_supports_explicit_insufficient_without_evidence() -> None:
    package = EvidencePackage(
        case_id="case",
        request_id="req",
        search_plan_id="plan",
        requested_sufficiency="GOOD",
        achieved_sufficiency="INSUFFICIENT",
        coverage={"successful_source_classes": 0, "distinct_source_ids": 0},
    )

    result = DeterministicResearchSufficiencyAssessor().assess(package)

    assert result.assessment.achieved_sufficiency == "INSUFFICIENT"
    assert result.assessment.recommended_next_search
    assert result.decision_record.reason_codes == ["SUFFICIENCY_INSUFFICIENT"]


def test_g8_raw_material_count_does_not_create_good_sufficiency() -> None:
    refs = [f"m-{i}" for i in range(100)]
    package = EvidencePackage(
        case_id="case",
        request_id="req",
        search_plan_id="plan",
        requested_sufficiency="GOOD",
        achieved_sufficiency="MINIMUM",
        material_refs=refs,
        evidence_refs=refs,
        coverage={"successful_source_classes": 1, "distinct_source_ids": 1},
    )

    result = DeterministicResearchSufficiencyAssessor().assess(package)

    assert result.assessment.achieved_sufficiency == "MINIMUM"
    assert any("independence" in item for item in result.assessment.recommended_next_search)


def test_g8_good_requires_diversity_independence_primary_counterevidence_and_quality() -> None:
    package = EvidencePackage(
        case_id="case",
        request_id="req",
        search_plan_id="plan",
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

    result = DeterministicResearchSufficiencyAssessor().assess(
        package,
        quality=_quality(package.package_id, "m1"),
    )

    assert result.assessment.achieved_sufficiency == "GOOD"


def test_g8_desirable_requires_broader_depth_and_temporal_target_coverage() -> None:
    package = EvidencePackage(
        case_id="case",
        request_id="req",
        search_plan_id="plan",
        requested_sufficiency="DESIRABLE",
        achieved_sufficiency="MINIMUM",
        material_refs=["m1"],
        evidence_refs=["m1"],
        coverage={
            "successful_source_classes": 3,
            "distinct_source_ids": 3,
            "independent_evidence_refs": 3,
            "primary_evidence_refs": 1,
            "counter_evidence_searched": True,
            "temporal_coverage_complete": True,
            "target_coverage_complete": True,
        },
    )

    result = DeterministicResearchSufficiencyAssessor().assess(
        package,
        quality=_quality(package.package_id, "m1"),
    )

    assert result.assessment.achieved_sufficiency == "DESIRABLE"


def test_g8_blocking_gap_forces_insufficient() -> None:
    package = EvidencePackage(
        case_id="case",
        request_id="req",
        search_plan_id="plan",
        requested_sufficiency="GOOD",
        achieved_sufficiency="MINIMUM",
        material_refs=["m1"],
        evidence_refs=["m1"],
        critical_gaps=["blocking: primary source unavailable"],
        coverage={"successful_source_classes": 2, "distinct_source_ids": 2},
    )

    result = DeterministicResearchSufficiencyAssessor().assess(package)

    assert result.assessment.achieved_sufficiency == "INSUFFICIENT"


def test_protocol_allows_insufficient_current_state_but_not_requested_target() -> None:
    package = EvidencePackage(
        case_id="case",
        request_id="req",
        search_plan_id="plan",
        requested_sufficiency="GOOD",
        achieved_sufficiency="INSUFFICIENT",
    )
    gap = ResearchGap(
        case_id="case",
        parent_request_id="req",
        question="What is missing?",
        why_needed="Need sufficient evidence",
        missing_evidence_type="independent primary evidence",
        current_sufficiency="INSUFFICIENT",
        required_sufficiency="GOOD",
    )

    assert package.achieved_sufficiency == "INSUFFICIENT"
    assert gap.current_sufficiency == "INSUFFICIENT"
