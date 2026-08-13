from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from father_osint.evidence_quality import EvidenceQualityResult
from father_osint.models import utc_now_iso
from father_osint.protocol import DecisionRecord, EvidencePackage

SUFFICIENCY_OUTCOMES = {"INSUFFICIENT", "MINIMUM", "GOOD", "DESIRABLE"}


@dataclass(slots=True)
class ResearchSufficiencyAssessment:
    case_id: str
    package_id: str
    requested_sufficiency: str
    achieved_sufficiency: str
    reasons: list[str]
    critical_gaps: list[str] = field(default_factory=list)
    recommended_next_search: list[str] = field(default_factory=list)
    assessment_id: str = field(default_factory=lambda: str(uuid4()))
    algorithm_version: str = "research-sufficiency-v1"
    knowledge_version: str = "information-evidence-standard-v1"
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.achieved_sufficiency = self.achieved_sufficiency.upper()
        if self.achieved_sufficiency not in SUFFICIENCY_OUTCOMES:
            raise ValueError("invalid achieved_sufficiency")
        if not self.reasons:
            raise ValueError("sufficiency assessment requires explicit reasons")


@dataclass(slots=True)
class ResearchSufficiencyResult:
    assessment: ResearchSufficiencyAssessment
    decision_record: DecisionRecord


class DeterministicResearchSufficiencyAssessor:
    """Policy baseline for G8.

    The assessor deliberately ignores raw post/material count as a sufficiency
    criterion. It uses explicit coverage, independence, primary-source,
    counter-evidence and quality signals. Missing signals fail conservatively.
    """

    algorithm_version = "research-sufficiency-v1"
    knowledge_version = "information-evidence-standard-v1"

    def assess(
        self,
        package: EvidencePackage,
        *,
        quality: EvidenceQualityResult | None = None,
    ) -> ResearchSufficiencyResult:
        coverage = package.coverage or {}
        successful_source_classes = int(coverage.get("successful_source_classes", 0) or 0)
        distinct_source_ids = int(coverage.get("distinct_source_ids", 0) or 0)
        independent_evidence_refs = int(coverage.get("independent_evidence_refs", 0) or 0)
        primary_evidence_refs = int(coverage.get("primary_evidence_refs", 0) or 0)
        counter_evidence_searched = bool(coverage.get("counter_evidence_searched", False))
        temporal_coverage_complete = bool(coverage.get("temporal_coverage_complete", False))
        target_coverage_complete = bool(coverage.get("target_coverage_complete", False))

        evidence_present = bool(package.evidence_refs or package.material_refs)
        fatal_gaps = [
            gap for gap in package.critical_gaps
            if str(gap).lower().startswith(("fatal:", "blocking:"))
        ]

        high_or_medium_provenance = 0
        high_or_medium_relevance = 0
        if quality is not None:
            for item in quality.assessments:
                if item.provenance_quality.state in {"HIGH", "MEDIUM"}:
                    high_or_medium_provenance += 1
                if item.relevance.state in {"HIGH", "MEDIUM"}:
                    high_or_medium_relevance += 1

        reasons: list[str] = []
        recommendations: list[str] = []

        if not evidence_present:
            achieved = "INSUFFICIENT"
            reasons.append("no evidence/material references are available for analysis")
            recommendations.append("collect at least one provenance-preserved evidence item")
        elif fatal_gaps:
            achieved = "INSUFFICIENT"
            reasons.append("blocking critical gaps remain unresolved")
            recommendations.extend(fatal_gaps)
        elif successful_source_classes <= 0 or distinct_source_ids <= 0:
            achieved = "INSUFFICIENT"
            reasons.append("search coverage does not establish any successfully covered source class/source identity")
            recommendations.append("record successful source coverage before analytical use")
        else:
            achieved = "MINIMUM"
            reasons.append("at least one covered source and provenance-preserved evidence item are available")

            good_conditions = {
                "source_diversity": successful_source_classes >= 2 or distinct_source_ids >= 2,
                "independence": independent_evidence_refs >= 2,
                "primary_evidence": primary_evidence_refs >= 1,
                "counter_evidence": counter_evidence_searched,
                "no_critical_gaps": not package.critical_gaps,
                "quality_context": quality is not None and high_or_medium_provenance >= 1 and high_or_medium_relevance >= 1,
            }
            if all(good_conditions.values()):
                achieved = "GOOD"
                reasons.append("diversity, independence, primary evidence, counter-evidence search and quality context satisfy GOOD policy")

                desirable_conditions = {
                    "broader_source_diversity": successful_source_classes >= 3 or distinct_source_ids >= 3,
                    "independent_depth": independent_evidence_refs >= 3,
                    "temporal_coverage": temporal_coverage_complete,
                    "target_coverage": target_coverage_complete,
                }
                if all(desirable_conditions.values()):
                    achieved = "DESIRABLE"
                    reasons.append("broader independent source depth and target/temporal coverage satisfy DESIRABLE policy")
                else:
                    for name, ok in desirable_conditions.items():
                        if not ok:
                            recommendations.append(f"improve {name.replace('_', ' ')} for DESIRABLE sufficiency")
            else:
                for name, ok in good_conditions.items():
                    if not ok:
                        recommendations.append(f"resolve {name.replace('_', ' ')} for GOOD sufficiency")

        assessment = ResearchSufficiencyAssessment(
            case_id=package.case_id,
            package_id=package.package_id,
            requested_sufficiency=package.requested_sufficiency,
            achieved_sufficiency=achieved,
            reasons=reasons,
            critical_gaps=list(package.critical_gaps),
            recommended_next_search=recommendations,
        )
        decision = DecisionRecord(
            case_id=package.case_id,
            role_id="OSINT_EXPERT",
            decision="ASSESS_RESEARCH_SUFFICIENCY",
            input_refs=[package.package_id] + ([quality.decision_record.decision_id] if quality else []),
            knowledge_refs=["information-evidence-standard.v1", "EC-005.information-evidence-standard"],
            method_refs=[
                "g8.coverage-not-count-v1",
                "g8.independence-primary-counterevidence-v1",
                "g8.explicit-insufficient-v1",
            ],
            reason_codes=[f"SUFFICIENCY_{achieved}"],
            limitations=[
                "v1 is a deterministic policy gate, not a calibrated probability model",
                "coverage signals must be produced by the acquisition/reconnaissance layer",
            ],
            output_refs=[assessment.assessment_id],
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )
        return ResearchSufficiencyResult(assessment=assessment, decision_record=decision)
