from __future__ import annotations

import hashlib
import urllib.request
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Protocol
from urllib.parse import urlparse
from uuid import uuid4

from .knowledge_factory import (
    AuditEvent,
    DocumentRecord,
    DocumentVersion,
    OfficialSource,
    Permission,
    PipelineStage,
    Role,
    SourceStatus,
    StageState,
    is_allowed,
)
from .knowledge_factory_store import KnowledgeFactoryStore
from .models import utc_now_iso
from .source_policy import SourcePolicy, TrustTier


class AcquisitionError(RuntimeError):
    """Expected bounded acquisition failure."""


class AcquisitionDisposition(str, Enum):
    CREATED = "CREATED"
    REUSED = "REUSED"
    NEW_VERSION = "NEW_VERSION"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass(slots=True)
class FetchedArtifact:
    data: bytes
    mime_type: str | None = None
    final_url: str | None = None


class ArtifactFetcher(Protocol):
    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        ...


class UrllibArtifactFetcher:
    """Small stdlib-only HTTP(S) fetcher for the M1 acquisition boundary."""

    user_agent = "FATHER-KnowledgeFactory/0.1"

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise AcquisitionError(f"artifact exceeds max_bytes={max_bytes}")
                content_type = response.headers.get_content_type() if response.headers else None
                return FetchedArtifact(
                    data=data,
                    mime_type=content_type,
                    final_url=response.geturl(),
                )
        except AcquisitionError:
            raise
        except Exception as exc:  # network/transport boundary: normalize to explicit failure
            raise AcquisitionError(f"fetch failed: {exc}") from exc


@dataclass(slots=True)
class AcquisitionRequest:
    source: OfficialSource
    source_policy: SourcePolicy
    document: DocumentRecord
    source_url: str
    file_name: str
    actor_id: str
    actor_role: Role | str = Role.OSINT_EXPERT
    timeout_seconds: float = 15.0
    max_bytes: int = 50 * 1024 * 1024
    mime_type_hint: str | None = None
    publication_date: str | None = None
    effective_date: str | None = None
    version_date: str | None = None

    def __post_init__(self) -> None:
        if not self.source_url.strip():
            raise ValueError("source_url is required")
        if not Path(self.file_name).name.strip():
            raise ValueError("file_name is required")
        if not self.actor_id.strip():
            raise ValueError("actor_id is required")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        if self.max_bytes <= 0:
            raise ValueError("max_bytes must be > 0")


@dataclass(slots=True)
class AcquisitionEvent:
    source_id: str
    document_id: str
    source_url: str
    result: AcquisitionDisposition
    actor_id: str
    actor_role: str
    artifact_sha256: str | None = None
    byte_length: int | None = None
    mime_type: str | None = None
    local_path: str | None = None
    artifact_reused: bool = False
    version_created: bool = False
    version_id: str | None = None
    reason: str = ""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    acquired_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["result"] = self.result.value
        return data


@dataclass(slots=True)
class AcquisitionResponse:
    disposition: AcquisitionDisposition
    event: AcquisitionEvent
    document: DocumentRecord
    version: DocumentVersion | None = None


class AcquisitionService:
    """Bounded D0-D3 Knowledge Factory acquisition service.

    External bytes are treated only as data. The service preserves exact bytes,
    computes SHA-256 itself, records append-only acquisition/audit observations,
    and never promotes a document beyond D3.
    """

    _trusted_policy_tiers = {
        TrustTier.A0_OFFICIAL_PUBLICATION,
        TrustTier.A1_OFFICIAL_ORGAN,
        TrustTier.A2_AUTHORITATIVE,
    }
    _completed_states = {
        StageState.DONE.value,
        StageState.VERIFIED.value,
        StageState.NOT_APPLICABLE.value,
    }

    def __init__(self, store: KnowledgeFactoryStore, fetcher: ArtifactFetcher | None = None) -> None:
        self.store = store
        self.fetcher = fetcher or UrllibArtifactFetcher()

    @staticmethod
    def _role_value(role: Role | str) -> str:
        return role.value if isinstance(role, Role) else Role(str(role)).value

    @staticmethod
    def _url_host(url: str) -> str:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise AcquisitionError("only absolute HTTP(S) source URLs are allowed")
        return parsed.hostname.lower().rstrip(".")

    @classmethod
    def _host_allowed(cls, url: str, policy: SourcePolicy) -> bool:
        host = cls._url_host(url)
        return any(host == domain or host.endswith("." + domain) for domain in policy.domains)

    @classmethod
    def _stage_completed(cls, document: DocumentRecord, stage: PipelineStage) -> bool:
        return document.stage_states.get(stage.value) in cls._completed_states

    @staticmethod
    def _hash_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _append_event_and_audit(self, event: AcquisitionEvent) -> None:
        self.store.append_acquisition(event.to_dict())
        self.store.append_audit(
            AuditEvent(
                actor_id=event.actor_id,
                actor_role=event.actor_role,
                action="ACQUIRE_DOCUMENT",
                object_type="DOCUMENT",
                object_id=event.document_id,
                result=event.result.value,
                reason=event.reason,
                metadata={
                    "acquisition_event_id": event.event_id,
                    "source_id": event.source_id,
                    "source_url": event.source_url,
                    "artifact_sha256": event.artifact_sha256,
                    "byte_length": event.byte_length,
                    "mime_type": event.mime_type,
                    "local_path": event.local_path,
                    "artifact_reused": event.artifact_reused,
                    "version_created": event.version_created,
                    "version_id": event.version_id,
                },
            )
        )

    def _blocked(self, request: AcquisitionRequest, reason: str) -> AcquisitionResponse:
        event = AcquisitionEvent(
            source_id=request.source.source_id,
            document_id=request.document.document_id,
            source_url=request.source_url,
            result=AcquisitionDisposition.BLOCKED,
            actor_id=request.actor_id,
            actor_role=self._role_value(request.actor_role),
            reason=reason,
        )
        self._append_event_and_audit(event)
        return AcquisitionResponse(event.result, event, request.document)

    def _failed(self, request: AcquisitionRequest, reason: str) -> AcquisitionResponse:
        if not self._stage_completed(request.document, PipelineStage.D2_ORIGINAL_ACQUIRED):
            request.document.set_stage_state(PipelineStage.D2_ORIGINAL_ACQUIRED, StageState.FAILED)
            self.store.save_document(request.document)
        event = AcquisitionEvent(
            source_id=request.source.source_id,
            document_id=request.document.document_id,
            source_url=request.source_url,
            result=AcquisitionDisposition.FAILED,
            actor_id=request.actor_id,
            actor_role=self._role_value(request.actor_role),
            reason=reason,
        )
        self._append_event_and_audit(event)
        return AcquisitionResponse(event.result, event, request.document)

    def acquire(self, request: AcquisitionRequest) -> AcquisitionResponse:
        role_value = self._role_value(request.actor_role)
        if not is_allowed(Role(role_value), Permission.ACQUIRE_DOCUMENT):
            return self._blocked(request, f"role {role_value} cannot acquire documents")

        source = request.source
        policy = request.source_policy

        if source.source_id != policy.source_id:
            return self._blocked(request, "source_id does not match SourcePolicy")
        if source.status != SourceStatus.VERIFIED:
            if not self._stage_completed(request.document, PipelineStage.D0_SOURCE_DISCOVERED):
                request.document.set_stage_state(PipelineStage.D0_SOURCE_DISCOVERED, StageState.DONE)
            request.document.set_stage_state(PipelineStage.D1_SOURCE_VERIFIED, StageState.BLOCKED)
            self.store.save_document(request.document)
            return self._blocked(request, "source is not VERIFIED")
        if policy.trust_tier not in self._trusted_policy_tiers:
            return self._blocked(request, f"source policy tier {policy.trust_tier.value} is not acquisition-trusted")

        try:
            if not self._host_allowed(request.source_url, policy):
                return self._blocked(request, "source URL host is outside SourcePolicy domains")
        except AcquisitionError as exc:
            return self._blocked(request, str(exc))

        self.store.save_source(source)
        if not self._stage_completed(request.document, PipelineStage.D0_SOURCE_DISCOVERED):
            request.document.set_stage_state(PipelineStage.D0_SOURCE_DISCOVERED, StageState.DONE)
        if not self._stage_completed(request.document, PipelineStage.D1_SOURCE_VERIFIED):
            request.document.set_stage_state(PipelineStage.D1_SOURCE_VERIFIED, StageState.VERIFIED)
        self.store.save_document(request.document)

        try:
            fetched = self.fetcher.fetch(
                request.source_url,
                timeout_seconds=request.timeout_seconds,
                max_bytes=request.max_bytes,
            )
            if not fetched.data:
                raise AcquisitionError("empty artifact is not accepted")
            final_url = fetched.final_url or request.source_url
            if not self._host_allowed(final_url, policy):
                raise AcquisitionError("redirect/final URL host is outside SourcePolicy domains")
        except Exception as exc:
            reason = str(exc) if isinstance(exc, AcquisitionError) else f"fetcher failed: {exc}"
            return self._failed(request, reason)

        digest = self._hash_bytes(fetched.data)
        artifact_path = self.store.originals_dir / f"{digest}.bin"
        artifact_reused = artifact_path.exists()

        if artifact_reused:
            existing_digest = self._hash_bytes(artifact_path.read_bytes())
            if existing_digest != digest:
                return self._failed(request, "content-addressed artifact integrity mismatch")
        else:
            tmp_path = self.store.originals_dir / f".{digest}.{uuid4().hex}.tmp"
            tmp_path.write_bytes(fetched.data)
            if self._hash_bytes(tmp_path.read_bytes()) != digest:
                tmp_path.unlink(missing_ok=True)
                return self._failed(request, "written artifact failed SHA-256 verification")
            tmp_path.replace(artifact_path)

        relative_path = artifact_path.relative_to(self.store.root).as_posix()
        mime_type = fetched.mime_type or request.mime_type_hint or "application/octet-stream"
        existing_version = next(
            (
                version
                for version in request.document.versions
                if version.sha256 == digest and version.source_id == source.source_id
            ),
            None,
        )

        version_created = existing_version is None
        if existing_version is None:
            had_prior_versions = bool(request.document.versions)
            version = DocumentVersion(
                source_id=source.source_id,
                source_url=final_url,
                sha256=digest,
                local_path=relative_path,
                file_name=Path(request.file_name).name,
                mime_type=mime_type,
                file_size=len(fetched.data),
                publication_date=request.publication_date,
                effective_date=request.effective_date,
                version_date=request.version_date,
            )
            request.document.add_version(version)
            disposition = (
                AcquisitionDisposition.NEW_VERSION if had_prior_versions else AcquisitionDisposition.CREATED
            )
        else:
            version = existing_version
            request.document.current_version_id = existing_version.version_id
            disposition = AcquisitionDisposition.REUSED

        if not self._stage_completed(request.document, PipelineStage.D2_ORIGINAL_ACQUIRED):
            request.document.set_stage_state(PipelineStage.D2_ORIGINAL_ACQUIRED, StageState.DONE)
        if not self._stage_completed(request.document, PipelineStage.D3_INTEGRITY_METADATA_VERIFIED):
            request.document.set_stage_state(PipelineStage.D3_INTEGRITY_METADATA_VERIFIED, StageState.VERIFIED)
        self.store.save_document(request.document)

        event = AcquisitionEvent(
            source_id=source.source_id,
            document_id=request.document.document_id,
            source_url=final_url,
            result=disposition,
            actor_id=request.actor_id,
            actor_role=role_value,
            artifact_sha256=digest,
            byte_length=len(fetched.data),
            mime_type=mime_type,
            local_path=relative_path,
            artifact_reused=artifact_reused,
            version_created=version_created,
            version_id=version.version_id,
        )
        self._append_event_and_audit(event)
        return AcquisitionResponse(disposition, event, request.document, version)
