from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class ProfileId(StrEnum):
    RU_ORG = "RU_ORG"
    RU_PERSON = "RU_PERSON"
    INTL_ORG = "INTL_ORG"
    INTL_PERSON = "INTL_PERSON"


class SubjectType(StrEnum):
    ORGANIZATION = "ORGANIZATION"
    PERSON = "PERSON"


class Depth(StrEnum):
    SCREENING = "SCREENING"
    STANDARD = "STANDARD"
    ENHANCED = "ENHANCED"


class Sufficiency(StrEnum):
    MINIMUM = "MINIMUM"
    GOOD = "GOOD"
    DESIRABLE = "DESIRABLE"


class Stream(StrEnum):
    ENTITY_REGISTRY = "ENTITY_REGISTRY"
    BUSINESS_FINANCIAL_OPERATIONS = "BUSINESS_FINANCIAL_OPERATIONS"
    DIGITAL_FOOTPRINT = "DIGITAL_FOOTPRINT"
    LEGAL_SANCTIONS_ADVERSE = "LEGAL_SANCTIONS_ADVERSE"
    RED_TEAM_SOURCE_QUALITY = "RED_TEAM_SOURCE_QUALITY"


class CaseState(StrEnum):
    NEW = "NEW"
    LEGAL_GATE = "LEGAL_GATE"
    IDENTITY_LOCK = "IDENTITY_LOCK"
    PLANNED = "PLANNED"
    COLLECTING = "COLLECTING"
    NORMALIZING = "NORMALIZING"
    ANALYZING = "ANALYZING"
    RED_TEAM = "RED_TEAM"
    REVIEW = "REVIEW"
    DECISION = "DECISION"
    MONITORING = "MONITORING"
    CLOSED = "CLOSED"


class JobState(StrEnum):
    PLANNED = "PLANNED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    FOUND = "FOUND"
    NO_HIT = "NO_HIT"
    BLOCKED = "BLOCKED"
    CONFLICT = "CONFLICT"
    ERROR = "ERROR"
    REVIEWED = "REVIEWED"
    CANCELLED = "CANCELLED"


class IdentityStatus(StrEnum):
    LOCKED = "LOCKED"
    HOLD_MISSING_IDENTIFIERS = "HOLD_MISSING_IDENTIFIERS"
    HOLD_CONFLICT = "HOLD_CONFLICT"


class CoverageStatus(StrEnum):
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    HOLD_EVIDENCE_INSUFFICIENT = "HOLD_EVIDENCE_INSUFFICIENT"
    HOLD_CONFLICT = "HOLD_CONFLICT"
    BLOCKED_BY_POLICY = "BLOCKED_BY_POLICY"


@dataclass(slots=True)
class SubjectSeed:
    original_value: str
    official_name: str | None = None
    full_name_original: str | None = None
    jurisdiction: str | None = None
    registration_or_tax_id: str | None = None
    birth_date_or_year: str | None = None
    role_or_employer: str | None = None
    city_or_region: str | None = None
    distinguishing_context: str | None = None
    incorporation_date: str | None = None
    registered_address: str | None = None
    official_domain: str | None = None
    aliases: list[str] = field(default_factory=list)
    candidate_count: int = 1
    decisive_identifier_present: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.original_value.strip():
            raise ValueError("subject.original_value must not be empty")
        if self.candidate_count < 1:
            raise ValueError("candidate_count must be >= 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CaseIntake:
    case_id: str
    profile_id: ProfileId
    purpose: str
    decision_context: str
    requested_by: str
    owner_analyst: str
    legal_basis_or_usage_note: str
    access_class: str
    retention_rule: str
    subject: SubjectSeed
    depth: Depth = Depth.STANDARD
    required_sufficiency: Sufficiency = Sufficiency.GOOD
    allowed_jurisdictions: list[str] = field(default_factory=list)
    prohibited_methods: list[str] = field(default_factory=lambda: [
        "AUTH_BYPASS",
        "CREDENTIAL_ATTACK",
        "EXPLOITATION",
        "PHISHING_DELIVERY",
        "UNRESTRICTED_SHELL",
    ])
    active_actions_allowed: bool = False
    country_pack_id: str | None = None
    created_at_utc: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        for name, value in {
            "purpose": self.purpose,
            "decision_context": self.decision_context,
            "requested_by": self.requested_by,
            "owner_analyst": self.owner_analyst,
            "legal_basis_or_usage_note": self.legal_basis_or_usage_note,
            "access_class": self.access_class,
            "retention_rule": self.retention_rule,
        }.items():
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if self.active_actions_allowed:
            raise ValueError("Due Diligence Factory v1 is passive-only")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["profile_id"] = self.profile_id.value
        data["depth"] = self.depth.value
        data["required_sufficiency"] = self.required_sufficiency.value
        return data


@dataclass(slots=True)
class IdentityDecision:
    case_id: str
    status: IdentityStatus
    entity_key: str | None
    used_identifiers: list[str]
    missing_identifiers: list[str]
    conflict_reasons: list[str]
    automatic_merge_performed: bool = False
    decided_at_utc: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if self.automatic_merge_performed:
            raise ValueError("automatic entity merge is forbidden")
        if self.status == IdentityStatus.LOCKED and not self.entity_key:
            raise ValueError("LOCKED identity requires entity_key")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass(slots=True)
class FactoryJob:
    case_id: str
    job_id: str
    profile_id: ProfileId
    stream: Stream
    source_family: str
    state: JobState = JobState.PLANNED
    priority: int = 100
    passive_public_only: bool = True
    active_actions_allowed: bool = False
    country_pack_id: str | None = None
    input_refs: list[str] = field(default_factory=list)
    created_at_utc: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if self.active_actions_allowed:
            raise ValueError("factory jobs must be passive-only in v1")
        if not self.source_family.strip():
            raise ValueError("source_family must not be empty")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["profile_id"] = self.profile_id.value
        data["stream"] = self.stream.value
        data["state"] = self.state.value
        return data


@dataclass(slots=True)
class FactoryPlan:
    case_id: str
    profile_id: ProfileId
    identity_ref: str
    country_pack_id: str | None
    jobs: list[FactoryJob]
    stop_conditions: list[str]
    human_approval_required: bool
    plan_id: str
    version: int = 1
    created_at_utc: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "profile_id": self.profile_id.value,
            "identity_ref": self.identity_ref,
            "country_pack_id": self.country_pack_id,
            "jobs": [job.to_dict() for job in self.jobs],
            "stop_conditions": list(self.stop_conditions),
            "human_approval_required": self.human_approval_required,
            "plan_id": self.plan_id,
            "version": self.version,
            "created_at_utc": self.created_at_utc,
        }


@dataclass(slots=True)
class Observation:
    observation_id: str
    case_id: str
    job_id: str
    source_family: str
    observation_type: str
    normalized_value: str
    source_ref: str
    capture_sha256: str
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class JobResult:
    case_id: str
    job_id: str
    source_family: str
    state: JobState
    observations: list[Observation] = field(default_factory=list)
    scoped_no_hit_note: str | None = None
    limitations: list[str] = field(default_factory=list)
    error: str | None = None
    duration_ms: int = 0
    started_at_utc: str = field(default_factory=utc_now_iso)
    finished_at_utc: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if self.state == JobState.NO_HIT and not self.scoped_no_hit_note:
            raise ValueError("NO_HIT requires scoped_no_hit_note")
        if self.state == JobState.FOUND and not self.observations:
            raise ValueError("FOUND requires at least one observation")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        data["observations"] = [item.to_dict() for item in self.observations]
        return data


@dataclass(slots=True)
class CoverageAssessment:
    case_id: str
    plan_id: str
    status: CoverageStatus
    mandatory_total: int
    attempted_total: int
    found_total: int
    no_hit_total: int
    blocked_total: int
    conflict_total: int
    error_total: int
    missing_source_families: list[str]
    blocking_reasons: list[str]
    ready_for_human_review: bool
    assessed_at_utc: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data
