import pytest

from father_osint.source_policy import (
    LegalLifecycle,
    LegalStatusRecord,
    MaterialProfile,
    SourcePolicy,
    TrustTier,
)


def test_a0_requires_verification_evidence():
    with pytest.raises(ValueError):
        SourcePolicy(
            source_id="SRC-1",
            domains=["example.gov"],
            trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
            material_profiles=[MaterialProfile.LEGAL],
            trust_basis=["official publication"],
            verification_evidence=[],
        )


def test_verified_legal_status_is_ready_only_with_trace():
    record = LegalStatusRecord(
        document_id="DOC-1",
        lifecycle=LegalLifecycle.EFFECTIVE,
        status_verified_at="2026-08-22T00:00:00+00:00",
        status_source_refs=["SRC-RU-PRAVO-001"],
    )
    assert record.legally_ready is True


def test_unknown_legal_status_is_not_ready():
    record = LegalStatusRecord(
        document_id="DOC-1",
        lifecycle=LegalLifecycle.UNKNOWN,
        status_verified_at="2026-08-22T00:00:00+00:00",
        status_source_refs=["SRC-RU-PRAVO-001"],
    )
    assert record.legally_ready is False


def test_a3_signal_can_exist_without_official_trust_evidence():
    source = SourcePolicy(
        source_id="SIGNAL-1",
        domains=["t.me"],
        trust_tier=TrustTier.A3_DISCOVERY,
        material_profiles=[MaterialProfile.SIGNAL],
    )
    assert source.trust_tier is TrustTier.A3_DISCOVERY
