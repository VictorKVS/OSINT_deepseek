import pytest

from father_osint.source_policy import (
    LegalLifecycle,
    LegalStatusRecord,
    MaterialProfile,
    SourcePolicy,
    TrustTier,
)


def test_a0_source_requires_explicit_trust_basis_and_evidence():
    with pytest.raises(ValueError):
        SourcePolicy(
            source_id="SRC-A0",
            domains=["publication.pravo.gov.ru"],
            trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
        )

    source = SourcePolicy(
        source_id="SRC-A0",
        domains=["PUBLICATION.PRAVO.GOV.RU"],
        trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
        material_profiles=[MaterialProfile.LEGAL],
        trust_basis=["official publication channel"],
        verification_evidence=["registry-evidence-1"],
        search_methods=["exact_number", "title"],
    )
    assert source.domains == ["publication.pravo.gov.ru"]
    assert source.trust_tier == TrustTier.A0_OFFICIAL_PUBLICATION


def test_discovery_source_is_not_promoted_to_official_by_default():
    source = SourcePolicy(
        source_id="SRC-SIGNAL",
        domains=["t.me"],
        trust_tier=TrustTier.A3_DISCOVERY,
        material_profiles=[MaterialProfile.SIGNAL],
    )
    assert source.trust_tier == TrustTier.A3_DISCOVERY
    assert source.verification_evidence == []


def test_legal_status_unknown_is_not_legally_ready():
    status = LegalStatusRecord(document_id="doc-1")
    assert status.lifecycle == LegalLifecycle.UNKNOWN
    assert status.legally_ready is False


def test_effective_document_needs_status_evidence_before_legal_ready():
    status = LegalStatusRecord(
        document_id="doc-152",
        version_id="v-current",
        lifecycle=LegalLifecycle.EFFECTIVE,
        effective_from="2026-01-01",
    )
    assert status.legally_ready is False

    status.status_verified_at = "2026-08-22T00:00:00+00:00"
    status.status_source_refs.append("SRC-RU-PRAVO")
    assert status.legally_ready is True


def test_book_profile_has_no_legal_lifecycle_requirement():
    source = SourcePolicy(
        source_id="SRC-BOOK",
        domains=["publisher.example"],
        trust_tier=TrustTier.A2_AUTHORITATIVE,
        material_profiles=[MaterialProfile.BOOK],
    )
    assert MaterialProfile.BOOK in source.material_profiles
