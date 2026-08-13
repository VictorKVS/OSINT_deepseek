from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from father_osint.models import utc_now_iso
from father_osint.protocol import DecisionRecord, ResearchRequest

DIRECTIVE_STATUSES = {"REQUIRED", "NOT_APPLICABLE"}
ASSESSMENT_STATUSES = {"SEARCHED", "INCOMPLETE", "NOT_APPLICABLE"}
ATTEMPT_STATUSES = {"SEARCHED", "FAILED", "SKIPPED"}


@dataclass(slots=True)
class CounterEvidenceDirective:
    case_id: str
    request_id: str
    status: str
    rationale: str
    hypotheses: list[str] = field(default_factory=list)
    challenge_questions: list[str] = field(default_factory=list)
    alternative_searches: list[str] = field(default_factory=list)
    required_methods: list[str] = field(default_factory=list)
    directive_id: str = field(default_factory=lambda: str(uuid4()))
    algorithm_version: str = "counter-evidence-plan-v1"
    knowledge_version: str = "information-evidence-standard-v1"
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.status = self.status.upper()
        if self.status not in DIRECTIVE_STATUSES:
            raise ValueError("invalid counter-evidence directive status")
        if not self.rationale.strip():
            raise ValueError("counter-evidence directive requires rationale")
        if self.status == "REQUIRED":
            if not self.hypotheses or not self.challenge_questions or not self.required_methods:
                raise ValueError("REQUIRED counter-evidence directive needs hypotheses, challenge questions and methods")


@dataclass(slots=True)
class CounterEvidenceAttempt:
    query_or_strategy: str
    source_class: str
    status: str
    evidence_refs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    attempt_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.status = self.status.upper()
        if self.status not in ATTEMPT_STATUSES:
            raise ValueError("invalid counter-evidence attempt status")
        if not self.query_or_strategy.strip() or not self.source_class.strip():
            raise ValueError("counter-evidence attempt requires strategy and source_class")


@dataclass(slots=True)
class CounterEvidenceAssessment:
    case_id: str
    request_id: str
    directive_id: str
    status: str
    attempts: list[CounterEvidenceAttempt] = field(default_factory=list)
    contradictory_evidence_refs: list[str] = field(default_factory=list)
    alternative_explanation_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    assessment_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.status = self.status.upper()
        if self.status not in ASSESSMENT_STATUSES:
            raise ValueError("invalid counter-evidence assessment status")
        if self.status == "SEARCHED" and not any(item.status == "SEARCHED" for item in self.attempts):
            raise ValueError("SEARCHED requires at least one completed search attempt")
        if self.status == "NOT_APPLICABLE" and self.attempts:
            raise ValueError("NOT_APPLICABLE must not contain search attempts")

    @property
    def counter_evidence_searched(self) -> bool:
        return self.status == "SEARCHED"


@dataclass(slots=True)
class CounterEvidencePlanResult:
    directive: CounterEvidenceDirective
    decision_record: DecisionRecord


@dataclass(slots=True)
class CounterEvidenceAssessmentResult:
    assessment: CounterEvidenceAssessment
    decision_record: DecisionRecord


class DeterministicCounterEvidencePlanner:
    """G9 baseline: never silently skips challenge search.

    If ANALYST supplied one or more leading hypotheses, OSINT_EXPERT must plan a
    deliberate falsification/alternative search. If no leading hypothesis exists,
    the planner records NOT_APPLICABLE explicitly instead of fabricating one.
    """

    algorithm_version = "counter-evidence-plan-v1"
    knowledge_version = "information-evidence-standard-v1"

    def plan(self, request: ResearchRequest) -> CounterEvidencePlanResult:
        hypotheses = [item.strip() for item in request.hypotheses if item.strip()]
        if hypotheses:
            questions = [f"What observable evidence would be inconsistent with: {item}" for item in hypotheses]
            alternatives = [f"Search for a materially different explanation for evidence supporting: {item}" for item in hypotheses]
            directive = CounterEvidenceDirective(
                case_id=request.case_id,
                request_id=request.request_id,
                status="REQUIRED",
                rationale="leading analytical hypotheses exist and require deliberate challenge search",
                hypotheses=hypotheses,
                challenge_questions=questions,
                alternative_searches=alternatives,
                required_methods=[
                    "contradictory_statement_search",
                    "alternative_explanation_search",
                    "source_independence_check",
                ],
            )
            reason_codes = ["LEADING_HYPOTHESIS_PRESENT", "COUNTER_EVIDENCE_REQUIRED"]
        else:
            directive = CounterEvidenceDirective(
                case_id=request.case_id,
                request_id=request.request_id,
                status="NOT_APPLICABLE",
                rationale="no leading hypothesis was supplied; research is currently exploratory/descriptive",
            )
            reason_codes = ["NO_LEADING_HYPOTHESIS", "COUNTER_EVIDENCE_NOT_APPLICABLE"]

        decision = DecisionRecord(
            case_id=request.case_id,
            role_id="OSINT_EXPERT",
            decision="PLAN_COUNTER_EVIDENCE_SEARCH",
            input_refs=[request.request_id],
            knowledge_refs=["information-evidence-standard.v1", "EC-005.information-evidence-standard"],
            method_refs=["g9.counter-evidence-protocol-v1"],
            reason_codes=reason_codes,
            limitations=["v1 uses explicit ANALYST hypotheses as the trigger and does not infer hidden hypotheses from prose"],
            output_refs=[directive.directive_id],
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )
        return CounterEvidencePlanResult(directive=directive, decision_record=decision)


class DeterministicCounterEvidenceAssessor:
    """Turns execution records into an auditable G9 completion state."""

    algorithm_version = "counter-evidence-assessment-v1"
    knowledge_version = "information-evidence-standard-v1"

    def assess(
        self,
        directive: CounterEvidenceDirective,
        *,
        attempts: list[CounterEvidenceAttempt] | None = None,
        contradictory_evidence_refs: list[str] | None = None,
        alternative_explanation_refs: list[str] | None = None,
    ) -> CounterEvidenceAssessmentResult:
        attempts = list(attempts or [])
        contradictory_evidence_refs = list(contradictory_evidence_refs or [])
        alternative_explanation_refs = list(alternative_explanation_refs or [])

        if directive.status == "NOT_APPLICABLE":
            status = "NOT_APPLICABLE"
            limitations = [directive.rationale]
        elif any(item.status == "SEARCHED" for item in attempts):
            status = "SEARCHED"
            limitations = []
            if not contradictory_evidence_refs:
                limitations.append("no contradictory evidence was found; absence of a finding is not proof that none exists")
            if not alternative_explanation_refs:
                limitations.append("no alternative explanation evidence was retained in this bounded search")
        else:
            status = "INCOMPLETE"
            limitations = ["required counter-evidence search has no completed SEARCHED attempt"]

        assessment = CounterEvidenceAssessment(
            case_id=directive.case_id,
            request_id=directive.request_id,
            directive_id=directive.directive_id,
            status=status,
            attempts=attempts if status != "NOT_APPLICABLE" else [],
            contradictory_evidence_refs=contradictory_evidence_refs,
            alternative_explanation_refs=alternative_explanation_refs,
            limitations=limitations,
        )
        decision = DecisionRecord(
            case_id=directive.case_id,
            role_id="OSINT_EXPERT",
            decision="ASSESS_COUNTER_EVIDENCE_SEARCH",
            input_refs=[directive.directive_id] + [item.attempt_id for item in attempts],
            knowledge_refs=["information-evidence-standard.v1", "EC-005.information-evidence-standard"],
            method_refs=["g9.counter-evidence-assessment-v1"],
            reason_codes=[f"COUNTER_EVIDENCE_{status}"],
            limitations=list(assessment.limitations),
            output_refs=[assessment.assessment_id],
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )
        return CounterEvidenceAssessmentResult(assessment=assessment, decision_record=decision)
