from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, *parts: object, length: int = 16) -> str:
    canonical = "|".join(str(part).strip() for part in parts)
    digest = sha256(canonical.encode("utf-8")).hexdigest()[:length].upper()
    return f"{prefix}-{digest}"


def to_primitive(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: to_primitive(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): to_primitive(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_primitive(item) for item in value]
    return value


class SubjectKind(str, Enum):
    PERSON = "PERSON"
    LEGAL_ENTITY = "LEGAL_ENTITY"


class JurisdictionScope(str, Enum):
    RUSSIA = "RUSSIA"
    FOREIGN = "FOREIGN"


class ScreeningDepth(str, Enum):
    BASIC = "BASIC"
    STANDARD = "STANDARD"
    ENHANCED = "ENHANCED"
    DEEP = "DEEP"


class RiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RecheckMode(str, Enum):
    INITIAL = "INITIAL"
    PERIODIC = "PERIODIC"
    EVENT_DRIVEN = "EVENT_DRIVEN"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class CheckStream(str, Enum):
    IDENTITY_REGISTRY = "IDENTITY_REGISTRY"
    BUSINESS_FINANCIAL = "BUSINESS_FINANCIAL"
    DIGITAL_FOOTPRINT = "DIGITAL_FOOTPRINT"
    LEGAL_SANCTIONS_ADVERSE = "LEGAL_SANCTIONS_ADVERSE"
    RED_TEAM_SOURCE_QUALITY = "RED_TEAM_SOURCE_QUALITY"


class CheckStage(str, Enum):
    ADMISSION = "ADMISSION"
    IDENTIFY = "IDENTIFY"
    EXPAND = "EXPAND"
    ASSESS = "ASSESS"
    REVIEW = "REVIEW"


class WorkState(str, Enum):
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Outcome(str, Enum):
    FOUND = "FOUND"
    NO_HIT_IN_SCOPE = "NO_HIT_IN_SCOPE"
    CONFLICT = "CONFLICT"
    BLOCKED_NO_ADAPTER = "BLOCKED_NO_ADAPTER"
    BLOCKED_POLICY = "BLOCKED_POLICY"
    BLOCKED_MISSING_IDENTIFIER = "BLOCKED_MISSING_IDENTIFIER"
    ERROR = "ERROR"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    SKIPPED = "SKIPPED"


class ObservationClass(str, Enum):
    DIRECT_OBSERVATION = "DIRECT_OBSERVATION"
    SOURCE_CLAIM = "SOURCE_CLAIM"
    LEAD = "LEAD"
    INFERENCE_CANDIDATE = "INFERENCE_CANDIDATE"


DEPTH_ORDER = {
    ScreeningDepth.BASIC: 0,
    ScreeningDepth.STANDARD: 1,
    ScreeningDepth.ENHANCED: 2,
    ScreeningDepth.DEEP: 3,
}


@dataclass(slots=True)
class Subject:
    kind: SubjectKind
    display_name: str
    country_code: str
    identifiers: dict[str, str] = field(default_factory=dict)
    aliases: list[str] = field(default_factory=list)
    date_of_birth: str | None = None
    incorporation_date: str | None = None
    citizenships: list[str] = field(default_factory=list)
    known_regions: list[str] = field(default_factory=list)
    access_class: str = "PUBLIC_WITH_PERSONAL_DATA"
    subject_id: str = field(default_factory=lambda: f"SUB-{uuid4()}")

    def __post_init__(self) -> None:
        self.country_code = self.country_code.strip().upper()
        self.display_name = self.display_name.strip()
        if not self.display_name:
            raise ValueError("display_name must not be empty")
        if len(self.country_code) != 2 and self.country_code != "ZZ":
            raise ValueError("country_code must be ISO 3166-1 alpha-2 or ZZ")
        self.identifiers = {
            str(key).strip().lower(): str(value).strip()
            for key, value in self.identifiers.items()
            if str(key).strip() and str(value).strip()
        }

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class ScreeningRequest:
    subject: Subject
    purpose: str
    legal_basis_note: str
    jurisdiction_scope: JurisdictionScope
    depth: ScreeningDepth = ScreeningDepth.STANDARD
    risk_tier: RiskTier = RiskTier.MEDIUM
    recheck_mode: RecheckMode = RecheckMode.INITIAL
    requested_by: str = "ANALYST"
    allowed_source_classes: list[str] = field(default_factory=lambda: ["PUBLIC", "PUBLIC_WITH_PERSONAL_DATA"])
    active_actions_allowed: bool = False
    export_profile: str = "INTERNAL_REVIEW"
    request_id: str = field(default_factory=lambda: f"REQ-{uuid4()}")
    case_id: str = field(default_factory=lambda: f"CASE-{uuid4()}")
    created_at_utc: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.purpose = self.purpose.strip()
        self.legal_basis_note = self.legal_basis_note.strip()
        if len(self.purpose) < 10:
            raise ValueError("purpose must contain at least 10 characters")
        if len(self.legal_basis_note) < 10:
            raise ValueError("legal_basis_note must contain at least 10 characters")
        if self.jurisdiction_scope == JurisdictionScope.RUSSIA and self.subject.country_code != "RU":
            raise ValueError("RUSSIA scope requires subject.country_code=RU")
        if self.jurisdiction_scope == JurisdictionScope.FOREIGN and self.subject.country_code == "RU":
            raise ValueError("FOREIGN scope requires non-RU country_code")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(frozen=True, slots=True)
class CheckDefinition:
    code: str
    title_ru: str
    stream: CheckStream
    stage: CheckStage
    minimum_depth: ScreeningDepth
    subject_kinds: tuple[SubjectKind, ...]
    jurisdiction_scopes: tuple[JurisdictionScope, ...]
    source_families: tuple[str, ...]
    capabilities: tuple[str, ...]
    required_identifiers_any: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    criticality: str = "MEDIUM"
    freshness_days: int = 90
    human_review_if_found: bool = False
    evidence_expectation: str = "At least one provenance-preserved source attempt"
    not_implying: tuple[str, ...] = ()

    def applies_to(self, request: ScreeningRequest) -> bool:
        return (
            request.subject.kind in self.subject_kinds
            and request.jurisdiction_scope in self.jurisdiction_scopes
            and DEPTH_ORDER[request.depth] >= DEPTH_ORDER[self.minimum_depth]
        )

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class WorkItem:
    request_id: str
    check_code: str
    title_ru: str
    stream: CheckStream
    stage: CheckStage
    wave: int
    dependencies: list[str]
    source_families: list[str]
    capabilities: list[str]
    state: WorkState = WorkState.PLANNED
    blocked_reason: str | None = None
    work_item_id: str = ""

    def __post_init__(self) -> None:
        if not self.work_item_id:
            self.work_item_id = stable_id("WKI", self.request_id, self.check_code)

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class ScreeningPlan:
    request_id: str
    case_id: str
    subject_id: str
    profile_id: str
    depth: ScreeningDepth
    risk_tier: RiskTier
    source_pack_ids: list[str]
    work_items: list[WorkItem]
    missing_identity_anchors: list[str]
    stop_conditions: list[str]
    human_review_gates: list[str]
    coverage_domains: list[str]
    plan_id: str = ""
    generated_at_utc: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.plan_id:
            self.plan_id = stable_id("PLN", self.request_id, self.profile_id)

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class Observation:
    statement: str
    classification: ObservationClass
    evidence_refs: list[str]
    source_ids: list[str]
    limitations: list[str] = field(default_factory=list)
    entity_refs: list[str] = field(default_factory=list)
    observation_id: str = field(default_factory=lambda: f"OBS-{uuid4()}")

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("observation statement must not be empty")
        if not self.source_ids:
            raise ValueError("observation requires source_ids")
        if not self.evidence_refs:
            raise ValueError("observation requires evidence_refs")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class CheckResult:
    request_id: str
    work_item_id: str
    check_code: str
    outcome: Outcome
    adapter_id: str | None
    observations: list[Observation] = field(default_factory=list)
    source_attempts: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    human_review_required: bool = False
    started_at_utc: str | None = None
    finished_at_utc: str | None = None
    duration_ms: int = 0
    result_id: str = field(default_factory=lambda: f"RES-{uuid4()}")

    def __post_init__(self) -> None:
        if self.outcome == Outcome.NO_HIT_IN_SCOPE and self.observations:
            raise ValueError("NO_HIT_IN_SCOPE cannot contain positive observations")
        if self.outcome == Outcome.FOUND and not self.observations:
            raise ValueError("FOUND requires at least one observation")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class FactoryRunSummary:
    total: int
    counts_by_outcome: dict[str, int]
    counts_by_stream: dict[str, int]
    started_at_utc: str
    finished_at_utc: str
    duration_ms: int
    peak_parallelism: int
    report_ready: bool
    blocking_gaps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class FactoryRun:
    request: ScreeningRequest
    plan: ScreeningPlan
    results: list[CheckResult]
    summary: FactoryRunSummary
    run_id: str = field(default_factory=lambda: f"RUN-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)
