from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from father_osint.models import utc_now_iso


SUFFICIENCY_LEVELS = {"MINIMUM", "GOOD", "DESIRABLE"}
PLAN_DECISIONS = {"ACCEPT", "AMEND", "REJECT"}
WORKFLOW_STATES = {
    "DRAFT",
    "ISSUED",
    "PLANNING",
    "PLAN_REVIEW",
    "APPROVED",
    "COLLECTING",
    "EVIDENCE_DELIVERED",
    "ANALYSIS",
    "RESEARCH_MORE",
    "CLOSED",
}


@dataclass(slots=True)
class DecisionRecord:
    case_id: str
    role_id: str
    decision: str
    input_refs: list[str] = field(default_factory=list)
    knowledge_refs: list[str] = field(default_factory=list)
    method_refs: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    alternatives_considered: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    algorithm_version: str = "1.0"
    knowledge_version: str = "unknown"
    policy_version: str | None = None
    decision_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.role_id.strip() or not self.decision.strip():
            raise ValueError("case_id, role_id and decision must not be empty")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ResearchRequest:
    objective: str
    research_questions: list[str]
    required_sufficiency: str = "GOOD"
    hypotheses: list[str] = field(default_factory=list)
    entities_of_interest: list[str] = field(default_factory=list)
    time_window: dict[str, str | None] = field(default_factory=dict)
    geography: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    known_context: list[str] = field(default_factory=list)
    known_evidence_refs: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    created_by: str = "ANALYST"
    case_id: str = field(default_factory=lambda: str(uuid4()))
    request_id: str = field(default_factory=lambda: str(uuid4()))
    schema_version: str = "1.0"
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.required_sufficiency = self.required_sufficiency.upper()
        if not self.objective.strip():
            raise ValueError("objective must not be empty")
        if not self.research_questions:
            raise ValueError("research_questions must not be empty")
        if self.required_sufficiency not in SUFFICIENCY_LEVELS:
            raise ValueError(f"required_sufficiency must be one of {sorted(SUFFICIENCY_LEVELS)}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SearchPlan:
    case_id: str
    request_id: str
    information_gaps: list[str]
    source_classes: list[str]
    methods: list[str]
    search_sequence: list[str]
    expected_coverage: list[str] = field(default_factory=list)
    verification_approach: list[str] = field(default_factory=list)
    alternatives_considered: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    knowledge_refs: list[str] = field(default_factory=list)
    tool_capabilities: list[str] = field(default_factory=list)
    expected_sufficiency: str = "GOOD"
    knowledge_gap: bool = False
    algorithm_version: str = "1.0"
    knowledge_version: str = "unknown"
    search_plan_id: str = field(default_factory=lambda: str(uuid4()))
    version: int = 1
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.expected_sufficiency = self.expected_sufficiency.upper()
        if not self.case_id.strip() or not self.request_id.strip():
            raise ValueError("case_id and request_id must not be empty")
        if not self.source_classes or not self.methods or not self.search_sequence:
            raise ValueError("source_classes, methods and search_sequence must not be empty")
        if self.expected_sufficiency not in SUFFICIENCY_LEVELS:
            raise ValueError(f"expected_sufficiency must be one of {sorted(SUFFICIENCY_LEVELS)}")
        if self.version <= 0:
            raise ValueError("version must be > 0")
        if not self.knowledge_refs and not self.knowledge_gap:
            raise ValueError("SearchPlan requires knowledge_refs or knowledge_gap=true")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PlanDecision:
    case_id: str
    search_plan_id: str
    status: str
    reason_codes: list[str] = field(default_factory=list)
    requested_changes: list[str] = field(default_factory=list)
    decision_record_ref: str | None = None
    decided_by: str = "ANALYST"
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.status = self.status.upper()
        if self.status not in PLAN_DECISIONS:
            raise ValueError(f"status must be one of {sorted(PLAN_DECISIONS)}")
        if self.status in {"AMEND", "REJECT"} and not self.reason_codes:
            raise ValueError("AMEND/REJECT require reason_codes")
        if self.status == "AMEND" and not self.requested_changes:
            raise ValueError("AMEND requires requested_changes")


@dataclass(slots=True)
class EvidencePackage:
    case_id: str
    request_id: str
    search_plan_id: str
    requested_sufficiency: str
    achieved_sufficiency: str
    material_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    lead_refs: list[str] = field(default_factory=list)
    source_attempts: list[dict[str, Any]] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)
    corroboration_notes: list[str] = field(default_factory=list)
    independence_notes: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    unverified_items: list[str] = field(default_factory=list)
    coverage: dict[str, Any] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)
    critical_gaps: list[str] = field(default_factory=list)
    recommended_follow_up: list[str] = field(default_factory=list)
    decision_record_refs: list[str] = field(default_factory=list)
    package_id: str = field(default_factory=lambda: str(uuid4()))
    schema_version: str = "1.0"
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.requested_sufficiency = self.requested_sufficiency.upper()
        self.achieved_sufficiency = self.achieved_sufficiency.upper()
        if self.requested_sufficiency not in SUFFICIENCY_LEVELS:
            raise ValueError("invalid requested_sufficiency")
        if self.achieved_sufficiency not in SUFFICIENCY_LEVELS:
            raise ValueError("invalid achieved_sufficiency")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ResearchGap:
    case_id: str
    parent_request_id: str
    question: str
    why_needed: str
    missing_evidence_type: str
    current_sufficiency: str
    required_sufficiency: str
    related_claims: list[str] = field(default_factory=list)
    related_hypotheses: list[str] = field(default_factory=list)
    priority: str = "NORMAL"
    gap_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.current_sufficiency = self.current_sufficiency.upper()
        self.required_sufficiency = self.required_sufficiency.upper()
        if not self.question.strip() or not self.why_needed.strip() or not self.missing_evidence_type.strip():
            raise ValueError("ResearchGap question/why_needed/missing_evidence_type must not be empty")
        if self.current_sufficiency not in SUFFICIENCY_LEVELS or self.required_sufficiency not in SUFFICIENCY_LEVELS:
            raise ValueError("invalid sufficiency level")


class ResearchWorkflow:
    """Small deterministic state machine for Analyst ↔ OSINT protocol."""

    _TRANSITIONS = {
        "DRAFT": {"ISSUED"},
        "ISSUED": {"PLANNING"},
        "PLANNING": {"PLAN_REVIEW"},
        "PLAN_REVIEW": {"APPROVED", "PLANNING"},
        "APPROVED": {"COLLECTING"},
        "COLLECTING": {"EVIDENCE_DELIVERED"},
        "EVIDENCE_DELIVERED": {"ANALYSIS"},
        "ANALYSIS": {"CLOSED", "RESEARCH_MORE"},
        "RESEARCH_MORE": {"PLANNING"},
        "CLOSED": set(),
    }

    def __init__(self, case_id: str, state: str = "DRAFT") -> None:
        state = state.upper()
        if state not in WORKFLOW_STATES:
            raise ValueError("unknown workflow state")
        self.case_id = case_id
        self.state = state
        self.history: list[dict[str, str]] = []

    def transition(self, new_state: str, *, actor_role: str, reason: str) -> None:
        new_state = new_state.upper()
        if new_state not in self._TRANSITIONS[self.state]:
            raise ValueError(f"invalid transition {self.state} -> {new_state}")
        if not actor_role.strip() or not reason.strip():
            raise ValueError("actor_role and reason are required")
        self.history.append(
            {
                "from": self.state,
                "to": new_state,
                "actor_role": actor_role,
                "reason": reason,
                "at": utc_now_iso(),
            }
        )
        self.state = new_state

    def apply_plan_decision(self, decision: PlanDecision) -> None:
        if self.state != "PLAN_REVIEW":
            raise ValueError("plan decision is only valid in PLAN_REVIEW")
        if decision.status == "ACCEPT":
            self.transition("APPROVED", actor_role=decision.decided_by, reason="plan accepted")
        elif decision.status == "AMEND":
            self.transition("PLANNING", actor_role=decision.decided_by, reason="plan amendment requested")
        else:
            self.transition("PLANNING", actor_role=decision.decided_by, reason="plan rejected; re-plan required")
