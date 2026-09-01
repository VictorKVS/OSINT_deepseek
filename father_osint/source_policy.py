from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TrustTier(str, Enum):
    A0_OFFICIAL_PUBLICATION = "A0_OFFICIAL_PUBLICATION"
    A1_OFFICIAL_ORGAN = "A1_OFFICIAL_ORGAN"
    A2_AUTHORITATIVE = "A2_AUTHORITATIVE"
    A3_DISCOVERY = "A3_DISCOVERY"
    UNKNOWN = "UNKNOWN"


class MaterialProfile(str, Enum):
    LEGAL = "LEGAL"
    STANDARD = "STANDARD"
    BOOK = "BOOK"
    SCIENCE = "SCIENCE"
    VENDOR_DOC = "VENDOR_DOC"
    WEB = "WEB"
    SIGNAL = "SIGNAL"


class LegalLifecycle(str, Enum):
    DRAFT = "DRAFT"
    PUBLIC_CONSULTATION = "PUBLIC_CONSULTATION"
    ADOPTED_NOT_PUBLISHED = "ADOPTED_NOT_PUBLISHED"
    OFFICIALLY_PUBLISHED = "OFFICIALLY_PUBLISHED"
    NOT_YET_EFFECTIVE = "NOT_YET_EFFECTIVE"
    EFFECTIVE = "EFFECTIVE"
    PARTIALLY_EFFECTIVE = "PARTIALLY_EFFECTIVE"
    SUSPENDED = "SUSPENDED"
    REPEALED = "REPEALED"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class SourcePolicy:
    source_id: str
    domains: list[str]
    trust_tier: TrustTier
    material_profiles: list[MaterialProfile] = field(default_factory=list)
    trust_basis: list[str] = field(default_factory=list)
    authority_scope: list[str] = field(default_factory=list)
    search_methods: list[str] = field(default_factory=list)
    monitoring_enabled: bool = True
    monitoring_cadence: str = "WEEKLY"
    verification_evidence: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.domains = [d.strip().lower() for d in self.domains if d.strip()]
        if not self.source_id.strip() or not self.domains:
            raise ValueError("source_id and at least one domain are required")
        if self.trust_tier in {TrustTier.A0_OFFICIAL_PUBLICATION, TrustTier.A1_OFFICIAL_ORGAN}:
            if not self.trust_basis or not self.verification_evidence:
                raise ValueError("A0/A1 sources require explicit trust basis and verification evidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "domains": self.domains,
            "trust_tier": self.trust_tier.value,
            "material_profiles": [p.value for p in self.material_profiles],
            "trust_basis": list(self.trust_basis),
            "authority_scope": list(self.authority_scope),
            "search_methods": list(self.search_methods),
            "monitoring_enabled": self.monitoring_enabled,
            "monitoring_cadence": self.monitoring_cadence,
            "verification_evidence": list(self.verification_evidence),
        }


@dataclass(slots=True)
class LegalStatusRecord:
    document_id: str
    version_id: str | None = None
    lifecycle: LegalLifecycle = LegalLifecycle.UNKNOWN
    document_date: str | None = None
    official_publication_date: str | None = None
    effective_from: str | None = None
    effective_to: str | None = None
    status_verified_at: str | None = None
    status_source_refs: list[str] = field(default_factory=list)
    legal_basis_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    @property
    def legally_ready(self) -> bool:
        if self.lifecycle == LegalLifecycle.UNKNOWN:
            return False
        return bool(self.status_verified_at and self.status_source_refs)

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "version_id": self.version_id,
            "lifecycle": self.lifecycle.value,
            "document_date": self.document_date,
            "official_publication_date": self.official_publication_date,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "status_verified_at": self.status_verified_at,
            "status_source_refs": list(self.status_source_refs),
            "legal_basis_refs": list(self.legal_basis_refs),
            "limitations": list(self.limitations),
            "legally_ready": self.legally_ready,
        }
