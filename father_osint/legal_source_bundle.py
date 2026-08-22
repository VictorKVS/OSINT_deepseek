from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
from urllib.parse import urlparse

from .source_policy import TrustTier


class LegalSourceRole(str, Enum):
    PUBLICATION_EVIDENCE = "PUBLICATION_EVIDENCE"
    GOVERNMENT_COPY = "GOVERNMENT_COPY"
    VERSION_TIMELINE_PROVIDER = "VERSION_TIMELINE_PROVIDER"
    CONSOLIDATED_REFERENCE = "CONSOLIDATED_REFERENCE"
    VERIFICATION_REFERENCE = "VERIFICATION_REFERENCE"


class RepresentationMode(str, Enum):
    AUTO_FETCH = "AUTO_FETCH"
    OPERATOR_IMPORT = "OPERATOR_IMPORT"
    VERIFY_ONLY = "VERIFY_ONLY"
    REFERENCE_ONLY = "REFERENCE_ONLY"


@dataclass(frozen=True, slots=True)
class LegalSourceRepresentation:
    source_id: str
    role: LegalSourceRole
    trust_tier: TrustTier
    url: str
    mode: RepresentationMode
    authority: str
    redistribution_allowed: bool = False
    artifact_locator: str | None = None
    edition: str | None = None
    timeline_priority: int | None = None
    identity_markers: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.authority.strip():
            raise ValueError("source_id and authority are required")
        parsed = urlparse(self.url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("representation URL must be absolute HTTP(S)")
        if self.role == LegalSourceRole.PUBLICATION_EVIDENCE and self.trust_tier not in {
            TrustTier.A0_OFFICIAL_PUBLICATION,
            TrustTier.A1_OFFICIAL_ORGAN,
        }:
            raise ValueError("publication evidence must be A0/A1")
        if self.role in {
            LegalSourceRole.VERSION_TIMELINE_PROVIDER,
            LegalSourceRole.CONSOLIDATED_REFERENCE,
        } and self.trust_tier != TrustTier.A2_AUTHORITATIVE:
            raise ValueError("timeline/consolidated references must be A2_AUTHORITATIVE")
        if self.timeline_priority is not None and self.timeline_priority < 1:
            raise ValueError("timeline_priority must be >= 1")
        if self.role == LegalSourceRole.VERSION_TIMELINE_PROVIDER and not self.identity_markers:
            raise ValueError("timeline provider requires identity_markers")
        if any(not marker.strip() for marker in self.identity_markers):
            raise ValueError("identity_markers cannot contain blank values")
        if self.mode in {RepresentationMode.VERIFY_ONLY, RepresentationMode.REFERENCE_ONLY} and self.redistribution_allowed:
            raise ValueError("verify/reference-only sources cannot be marked redistributable")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LegalSourceRepresentation":
        return cls(
            source_id=str(data["source_id"]),
            role=LegalSourceRole(data["role"]),
            trust_tier=TrustTier(data["trust_tier"]),
            url=str(data["url"]),
            mode=RepresentationMode(data["mode"]),
            authority=str(data["authority"]),
            redistribution_allowed=bool(data.get("redistribution_allowed", False)),
            artifact_locator=data.get("artifact_locator"),
            edition=data.get("edition"),
            timeline_priority=data.get("timeline_priority"),
            identity_markers=tuple(str(item) for item in data.get("identity_markers", [])),
            notes=tuple(data.get("notes", [])),
        )


@dataclass(frozen=True, slots=True)
class LegalSourceBundle:
    document_id: str
    representations: tuple[LegalSourceRepresentation, ...]

    def __post_init__(self) -> None:
        if not self.document_id.strip():
            raise ValueError("document_id is required")
        if not self.representations:
            raise ValueError("at least one source representation is required")
        if not any(
            item.role == LegalSourceRole.PUBLICATION_EVIDENCE
            and item.trust_tier in {TrustTier.A0_OFFICIAL_PUBLICATION, TrustTier.A1_OFFICIAL_ORGAN}
            for item in self.representations
        ):
            raise ValueError("legal source bundle requires A0/A1 publication evidence")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LegalSourceBundle":
        return cls(
            document_id=str(data["document_id"]),
            representations=tuple(
                LegalSourceRepresentation.from_dict(item)
                for item in data.get("representations", [])
            ),
        )

    def by_role(self, role: LegalSourceRole) -> tuple[LegalSourceRepresentation, ...]:
        return tuple(item for item in self.representations if item.role == role)

    def acquisition_candidates(self) -> tuple[LegalSourceRepresentation, ...]:
        return tuple(
            item
            for item in self.representations
            if item.mode in {RepresentationMode.AUTO_FETCH, RepresentationMode.OPERATOR_IMPORT}
            and item.trust_tier in {
                TrustTier.A0_OFFICIAL_PUBLICATION,
                TrustTier.A1_OFFICIAL_ORGAN,
            }
        )

    def verification_references(self) -> tuple[LegalSourceRepresentation, ...]:
        return tuple(
            item
            for item in self.representations
            if item.mode in {RepresentationMode.VERIFY_ONLY, RepresentationMode.REFERENCE_ONLY}
        )

    def timeline_providers(self) -> tuple[LegalSourceRepresentation, ...]:
        return tuple(
            sorted(
                (
                    item
                    for item in self.representations
                    if item.role == LegalSourceRole.VERSION_TIMELINE_PROVIDER
                ),
                key=lambda item: item.timeline_priority or 999,
            )
        )

    def preferred_timeline_provider(self) -> LegalSourceRepresentation | None:
        providers = self.timeline_providers()
        return providers[0] if providers else None

    def has_authoritative_consolidated_reference(self) -> bool:
        return any(
            item.role in {
                LegalSourceRole.VERSION_TIMELINE_PROVIDER,
                LegalSourceRole.CONSOLIDATED_REFERENCE,
            }
            and item.trust_tier == TrustTier.A2_AUTHORITATIVE
            for item in self.representations
        )
