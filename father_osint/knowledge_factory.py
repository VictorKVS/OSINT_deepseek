from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .models import utc_now_iso


class PipelineStage(str, Enum):
    D0_SOURCE_DISCOVERED = "D0_SOURCE_DISCOVERED"
    D1_SOURCE_VERIFIED = "D1_SOURCE_VERIFIED"
    D2_ORIGINAL_ACQUIRED = "D2_ORIGINAL_ACQUIRED"
    D3_INTEGRITY_METADATA_VERIFIED = "D3_INTEGRITY_METADATA_VERIFIED"
    D4_STRUCTURE_PARSED = "D4_STRUCTURE_PARSED"
    D5_CHUNKED = "D5_CHUNKED"
    D6_TERMS_EXTRACTED = "D6_TERMS_EXTRACTED"
    D7_DEFINITIONS_EXTRACTED = "D7_DEFINITIONS_EXTRACTED"
    D8_REQUIREMENTS_EXTRACTED = "D8_REQUIREMENTS_EXTRACTED"
    D9_ENTITIES_EXTRACTED = "D9_ENTITIES_EXTRACTED"
    D10_INTERNAL_RELATIONS = "D10_INTERNAL_RELATIONS"
    D11_CROSS_DOCUMENT_RELATIONS = "D11_CROSS_DOCUMENT_RELATIONS"
    D12_CONFLICTS_OVERLAPS = "D12_CONFLICTS_OVERLAPS"
    D13_KNOWLEDGE_GRAPH_READY = "D13_KNOWLEDGE_GRAPH_READY"
    D14_EXPERT_REVIEWED = "D14_EXPERT_REVIEWED"
    D15_KB_READY = "D15_KB_READY"


PIPELINE_ORDER = tuple(PipelineStage)


class StageState(str, Enum):
    NOT_DONE = "NOT_DONE"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    DONE = "DONE"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SourceClass(str, Enum):
    OFFICIAL = "OFFICIAL"
    AUTHORITATIVE = "AUTHORITATIVE"
    SECONDARY = "SECONDARY"
    SIGNAL = "SIGNAL"
    UNKNOWN = "UNKNOWN"


class SourceStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class Role(str, Enum):
    VIEWER = "VIEWER"
    ANALYST = "ANALYST"
    OSINT_EXPERT = "OSINT_EXPERT"
    KNOWLEDGE_CURATOR = "KNOWLEDGE_CURATOR"
    REVIEWER = "REVIEWER"
    ADMINISTRATOR = "ADMINISTRATOR"
    SECURITY_ADMINISTRATOR = "SECURITY_ADMINISTRATOR"
    SYSTEM_OWNER = "SYSTEM_OWNER"


class Permission(str, Enum):
    VIEW = "VIEW"
    CREATE_TASK = "CREATE_TASK"
    ACQUIRE_DOCUMENT = "ACQUIRE_DOCUMENT"
    REGISTER_SOURCE = "REGISTER_SOURCE"
    VERIFY_SOURCE = "VERIFY_SOURCE"
    ADVANCE_PIPELINE = "ADVANCE_PIPELINE"
    REVIEW_DOCUMENT = "REVIEW_DOCUMENT"
    PUBLISH_KB = "PUBLISH_KB"
    MANAGE_USERS = "MANAGE_USERS"
    MANAGE_SECURITY = "MANAGE_SECURITY"
    VIEW_AUDIT = "VIEW_AUDIT"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.VIEWER: frozenset({Permission.VIEW}),
    Role.ANALYST: frozenset({Permission.VIEW, Permission.CREATE_TASK, Permission.VIEW_AUDIT}),
    Role.OSINT_EXPERT: frozenset({
        Permission.VIEW,
        Permission.CREATE_TASK,
        Permission.ACQUIRE_DOCUMENT,
        Permission.REGISTER_SOURCE,
        Permission.ADVANCE_PIPELINE,
        Permission.VIEW_AUDIT,
    }),
    Role.KNOWLEDGE_CURATOR: frozenset({
        Permission.VIEW,
        Permission.ADVANCE_PIPELINE,
        Permission.REVIEW_DOCUMENT,
        Permission.VIEW_AUDIT,
    }),
    Role.REVIEWER: frozenset({Permission.VIEW, Permission.REVIEW_DOCUMENT, Permission.VIEW_AUDIT}),
    Role.ADMINISTRATOR: frozenset({Permission.VIEW, Permission.MANAGE_USERS, Permission.VIEW_AUDIT}),
    Role.SECURITY_ADMINISTRATOR: frozenset({
        Permission.VIEW,
        Permission.MANAGE_SECURITY,
        Permission.VIEW_AUDIT,
    }),
    Role.SYSTEM_OWNER: frozenset(Permission),
}


def is_allowed(role: Role | str, permission: Permission | str) -> bool:
    role_value = role if isinstance(role, Role) else Role(str(role))
    permission_value = permission if isinstance(permission, Permission) else Permission(str(permission))
    return permission_value in ROLE_PERMISSIONS[role_value]


@dataclass(slots=True)
class OfficialSource:
    name: str
    domain: str
    organization: str
    source_class: SourceClass = SourceClass.UNKNOWN
    authority_scope: list[str] = field(default_factory=list)
    accepted_document_types: list[str] = field(default_factory=list)
    trust_basis: str = ""
    status: SourceStatus = SourceStatus.CANDIDATE
    verified_by: str | None = None
    verified_at: str | None = None
    source_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        self.domain = self.domain.strip().lower()
        if not self.name.strip() or not self.domain or not self.organization.strip():
            raise ValueError("source name, domain and organization are required")
        if self.status == SourceStatus.VERIFIED:
            if self.source_class not in {SourceClass.OFFICIAL, SourceClass.AUTHORITATIVE}:
                raise ValueError("verified source must be OFFICIAL or AUTHORITATIVE")
            if not self.trust_basis.strip() or not self.verified_by or not self.verified_at:
                raise ValueError("verified source requires trust_basis, verified_by and verified_at")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DocumentVersion:
    source_id: str
    source_url: str
    sha256: str
    local_path: str
    file_name: str
    mime_type: str | None = None
    file_size: int | None = None
    publication_date: str | None = None
    effective_date: str | None = None
    version_date: str | None = None
    acquired_at: str = field(default_factory=utc_now_iso)
    version_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.source_url.strip():
            raise ValueError("source_id and source_url are required")
        normalized = self.sha256.strip().lower()
        if len(normalized) != 64 or any(ch not in "0123456789abcdef" for ch in normalized):
            raise ValueError("sha256 must be a 64-character hexadecimal digest")
        self.sha256 = normalized
        if not self.local_path.strip() or not self.file_name.strip():
            raise ValueError("local_path and file_name are required")
        if self.file_size is not None and self.file_size < 0:
            raise ValueError("file_size must be >= 0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DocumentRecord:
    title: str
    document_type: str
    workspace_id: str = "default"
    owner: str = "system"
    jurisdiction: str | None = None
    language: str = "ru"
    topic_tags: list[str] = field(default_factory=list)
    versions: list[DocumentVersion] = field(default_factory=list)
    current_version_id: str | None = None
    stage_states: dict[str, str] = field(default_factory=dict)
    document_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.title.strip() or not self.document_type.strip():
            raise ValueError("title and document_type are required")
        if not self.stage_states:
            self.stage_states = {stage.value: StageState.NOT_DONE.value for stage in PIPELINE_ORDER}

    @property
    def current_stage(self) -> PipelineStage:
        completed = {
            StageState.DONE.value,
            StageState.VERIFIED.value,
            StageState.NOT_APPLICABLE.value,
        }
        current = PIPELINE_ORDER[0]
        for stage in PIPELINE_ORDER:
            if self.stage_states.get(stage.value) in completed:
                current = stage
            else:
                break
        return current

    def set_stage_state(self, stage: PipelineStage | str, state: StageState | str) -> None:
        stage_value = stage if isinstance(stage, PipelineStage) else PipelineStage(str(stage))
        state_value = state if isinstance(state, StageState) else StageState(str(state))
        index = PIPELINE_ORDER.index(stage_value)
        if state_value in {StageState.DONE, StageState.VERIFIED} and index > 0:
            predecessor = PIPELINE_ORDER[index - 1]
            predecessor_state = StageState(self.stage_states[predecessor.value])
            if predecessor_state not in {StageState.DONE, StageState.VERIFIED, StageState.NOT_APPLICABLE}:
                raise ValueError(f"cannot complete {stage_value.value} before {predecessor.value}")
        self.stage_states[stage_value.value] = state_value.value
        self.updated_at = utc_now_iso()

    def add_version(self, version: DocumentVersion) -> None:
        if any(existing.version_id == version.version_id for existing in self.versions):
            return
        self.versions.append(version)
        self.current_version_id = version.version_id
        self.updated_at = utc_now_iso()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["versions"] = [version.to_dict() for version in self.versions]
        return data


@dataclass(slots=True)
class AuditEvent:
    actor_id: str
    actor_role: str
    action: str
    object_type: str
    object_id: str
    result: str
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        required = (self.actor_id, self.actor_role, self.action, self.object_type, self.object_id, self.result)
        if any(not str(value).strip() for value in required):
            raise ValueError("audit event identity/action/result fields are required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ClauseRef:
    document_id: str
    locator: str
    title: str | None = None
    version_id: str | None = None


@dataclass(slots=True)
class KnowledgeNode:
    node_type: str
    label: str
    document_refs: list[ClauseRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.node_type.strip() or not self.label.strip():
            raise ValueError("node_type and label are required")


@dataclass(slots=True)
class KnowledgeRelation:
    from_node_id: str
    to_node_id: str
    relation_type: str
    evidence_refs: list[ClauseRef] = field(default_factory=list)
    rationale: str = ""
    method_ref: str | None = None
    reviewer: str | None = None
    status: str = "DRAFT"
    relation_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.from_node_id.strip() or not self.to_node_id.strip() or not self.relation_type.strip():
            raise ValueError("relation endpoints and relation_type are required")
