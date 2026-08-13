from __future__ import annotations

"""Transparent acquisition reporting contract for Analyst handoff."""

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from father_osint.counter_evidence import CounterEvidenceAssessmentResult
from father_osint.evidence_quality import EvidenceQualityResult
from father_osint.models import utc_now_iso
from father_osint.protocol import DecisionRecord, EvidencePackage, ResearchRequest, SearchPlan
from father_osint.reconnaissance import ReconnaissanceResult
from father_osint.sufficiency import ResearchSufficiencyResult


@dataclass(slots=True)
class AcquisitionReport:
    case_id: str
    request_id: str
    search_plan_id: str
    evidence_package_id: str
    objective: str
    research_questions: list[str]
    searched_scope: list[str]
    source_attempts: list[dict[str, Any]]
    collection_bounds: dict[str, Any]
    source_failures: list[dict[str, Any]]
    provenance_refs: list[str]
    evidence_refs: list[str]
    lead_refs: list[str]
    contradictions: list[str]
    counter_evidence_status: str
    counter_evidence_refs: list[str]
    evidence_quality_summary: dict[str, Any]
    coverage: dict[str, Any]
    requested_sufficiency: str
    achieved_sufficiency: str
    sufficiency_reasons: list[str]
    unresolved_gaps: list[str]
    limitations: list[str]
    recommended_follow_up: list[str]
    lineage_refs: list[str]
    report_id: str = field(default_factory=lambda: str(uuid4()))
    schema_version: str = "1.0"
    algorithm_version: str = "acquisition-report-v1"
    knowledge_version: str = "information-evidence-standard-v1"
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.request_id.strip() or not self.search_plan_id.strip():
            raise ValueError("acquisition report requires case/request/search-plan lineage")
        if not self.objective.strip() or not self.research_questions:
            raise ValueError("acquisition report requires objective and research questions")
        if not self.requested_sufficiency.strip() or not self.achieved_sufficiency.strip():
            raise ValueError("acquisition report requires requested and achieved sufficiency")
        if not self.lineage_refs:
            raise ValueError("acquisition report requires explicit lineage refs")


@dataclass(slots=True)
class AcquisitionReportResult:
    report: AcquisitionReport
    decision_record: DecisionRecord


class DeterministicAcquisitionReportBuilder:
    """G10 baseline for transparent OSINT → Analyst handoff.

    The builder does not invent facts, quality or coverage. It only projects
    already-recorded protocol objects into one auditable Analyst-facing report.
    """

    algorithm_version = "acquisition-report-v1"
    knowledge_version = "information-evidence-standard-v1"

    def build(
        self,
        request: ResearchRequest,
        plan: SearchPlan,
        package: EvidencePackage,
        *,
        reconnaissance: ReconnaissanceResult | None = None,
        quality: EvidenceQualityResult | None = None,
        sufficiency: ResearchSufficiencyResult | None = None,
        counter_evidence: CounterEvidenceAssessmentResult | None = None,
        collection_bounds: dict[str, Any] | None = None,
    ) -> AcquisitionReportResult:
        self._validate_lineage(request, plan, package)

        attempts = list(package.source_attempts)
        failures = [
            dict(item) for item in attempts
            if str(item.get("status", "")).upper() in {"FAILED", "ERROR", "BLOCKED", "UNAVAILABLE"}
        ]

        searched_scope = list(plan.source_classes)
        if reconnaissance is not None:
            for item in reconnaissance.report.source_landscape:
                source = str(item.get("source", "")).strip()
                if source and source not in searched_scope:
                    searched_scope.append(source)

        counter_status = "NOT_RECORDED"
        counter_refs: list[str] = []
        counter_limitations: list[str] = []
        counter_decision_ref: str | None = None
        if counter_evidence is not None:
            counter_status = counter_evidence.assessment.status
            counter_refs = list(counter_evidence.assessment.contradictory_evidence_refs)
            counter_refs.extend(counter_evidence.assessment.alternative_explanation_refs)
            counter_limitations = list(counter_evidence.assessment.limitations)
            counter_decision_ref = counter_evidence.decision_record.decision_id

        quality_summary: dict[str, Any] = {
            "assessments": 0,
            "states_by_dimension": {},
            "truth_probability": "NOT_CALCULATED",
        }
        quality_decision_ref: str | None = None
        if quality is not None:
            dimensions: dict[str, dict[str, int]] = {}
            for assessment in quality.assessments:
                for dimension in assessment.dimensions:
                    states = dimensions.setdefault(dimension.name, {})
                    states[dimension.state] = states.get(dimension.state, 0) + 1
            quality_summary = {
                "assessments": len(quality.assessments),
                "states_by_dimension": dimensions,
                "truth_probability": "NOT_CALCULATED",
            }
            quality_decision_ref = quality.decision_record.decision_id

        achieved = package.achieved_sufficiency
        sufficiency_reasons: list[str] = []
        follow_up = list(package.recommended_follow_up)
        unresolved_gaps = list(package.critical_gaps)
        sufficiency_decision_ref: str | None = None
        if sufficiency is not None:
            achieved = sufficiency.assessment.achieved_sufficiency
            sufficiency_reasons = list(sufficiency.assessment.reasons)
            unresolved_gaps = list(dict.fromkeys(unresolved_gaps + sufficiency.assessment.critical_gaps))
            follow_up = list(dict.fromkeys(follow_up + sufficiency.assessment.recommended_next_search))
            sufficiency_decision_ref = sufficiency.decision_record.decision_id

        limitations = list(package.limitations)
        limitations.extend(counter_limitations)
        if reconnaissance is not None:
            limitations.extend(reconnaissance.report.gaps)
        limitations = list(dict.fromkeys(limitations))

        lineage_refs = [
            request.request_id,
            plan.search_plan_id,
            package.package_id,
            *package.decision_record_refs,
        ]
        if reconnaissance is not None:
            lineage_refs.extend([
                reconnaissance.report.report_id,
                reconnaissance.decision_record.decision_id,
            ])
        for ref in (quality_decision_ref, sufficiency_decision_ref, counter_decision_ref):
            if ref:
                lineage_refs.append(ref)
        lineage_refs = list(dict.fromkeys(ref for ref in lineage_refs if ref))

        report = AcquisitionReport(
            case_id=request.case_id,
            request_id=request.request_id,
            search_plan_id=plan.search_plan_id,
            evidence_package_id=package.package_id,
            objective=request.objective,
            research_questions=list(request.research_questions),
            searched_scope=searched_scope,
            source_attempts=attempts,
            collection_bounds=dict(collection_bounds or {}),
            source_failures=failures,
            provenance_refs=list(package.provenance_refs),
            evidence_refs=list(package.evidence_refs),
            lead_refs=list(package.lead_refs),
            contradictions=list(package.contradictions),
            counter_evidence_status=counter_status,
            counter_evidence_refs=list(dict.fromkeys(counter_refs)),
            evidence_quality_summary=quality_summary,
            coverage=dict(package.coverage),
            requested_sufficiency=package.requested_sufficiency,
            achieved_sufficiency=achieved,
            sufficiency_reasons=sufficiency_reasons,
            unresolved_gaps=unresolved_gaps,
            limitations=limitations,
            recommended_follow_up=follow_up,
            lineage_refs=lineage_refs,
        )

        decision = DecisionRecord(
            case_id=request.case_id,
            role_id="OSINT_EXPERT",
            decision="BUILD_TRANSPARENT_ACQUISITION_REPORT",
            input_refs=lineage_refs,
            knowledge_refs=[
                "information-evidence-standard.v1",
                "EC-005.information-evidence-standard",
                "analyst-osint-interaction-protocol.v1",
            ],
            method_refs=[
                "g10.transparent-handoff-v1",
                "g10.no-hidden-failures-v1",
                "g10.lineage-preservation-v1",
            ],
            reason_codes=[
                "ANALYST_HANDOFF_REQUIRED",
                f"ACHIEVED_SUFFICIENCY_{achieved}",
                f"COUNTER_EVIDENCE_{counter_status}",
            ],
            limitations=list(report.limitations),
            output_refs=[report.report_id],
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )
        return AcquisitionReportResult(report=report, decision_record=decision)

    @staticmethod
    def _validate_lineage(request: ResearchRequest, plan: SearchPlan, package: EvidencePackage) -> None:
        if plan.case_id != request.case_id or package.case_id != request.case_id:
            raise ValueError("case lineage mismatch in acquisition report inputs")
        if plan.request_id != request.request_id or package.request_id != request.request_id:
            raise ValueError("request lineage mismatch in acquisition report inputs")
        if package.search_plan_id != plan.search_plan_id:
            raise ValueError("search-plan lineage mismatch in acquisition report inputs")
