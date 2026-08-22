import json
from pathlib import Path

import pytest

from father_osint.legal_source_bundle import (
    LegalSourceBundle,
    LegalSourceRepresentation,
    LegalSourceRole,
    RepresentationMode,
)
from father_osint.source_policy import TrustTier


def test_bundle_requires_official_publication_evidence():
    with pytest.raises(ValueError, match="requires A0/A1 publication evidence"):
        LegalSourceBundle(
            document_id="DOC-1",
            representations=(
                LegalSourceRepresentation(
                    source_id="GARANT",
                    role=LegalSourceRole.VERSION_TIMELINE_PROVIDER,
                    trust_tier=TrustTier.A2_AUTHORITATIVE,
                    url="https://base.garant.ru/example",
                    mode=RepresentationMode.VERIFY_ONLY,
                    authority="GARANT",
                    timeline_priority=1,
                ),
            ),
        )


def test_a2_consolidated_reference_cannot_pose_as_publication():
    with pytest.raises(ValueError, match="publication evidence must be A0/A1"):
        LegalSourceRepresentation(
            source_id="CONSULTANT",
            role=LegalSourceRole.PUBLICATION_EVIDENCE,
            trust_tier=TrustTier.A2_AUTHORITATIVE,
            url="https://www.consultant.ru/document/example",
            mode=RepresentationMode.VERIFY_ONLY,
            authority="ConsultantPlus",
        )


def test_timeline_provider_is_a2_and_sorted_by_priority():
    official = LegalSourceRepresentation(
        source_id="OFFICIAL",
        role=LegalSourceRole.PUBLICATION_EVIDENCE,
        trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
        url="https://official.example/doc",
        mode=RepresentationMode.OPERATOR_IMPORT,
        authority="official publication",
    )
    consultant = LegalSourceRepresentation(
        source_id="CONSULTANT",
        role=LegalSourceRole.VERSION_TIMELINE_PROVIDER,
        trust_tier=TrustTier.A2_AUTHORITATIVE,
        url="https://www.consultant.ru/document/example",
        mode=RepresentationMode.VERIFY_ONLY,
        authority="ConsultantPlus",
        timeline_priority=2,
    )
    garant = LegalSourceRepresentation(
        source_id="GARANT",
        role=LegalSourceRole.VERSION_TIMELINE_PROVIDER,
        trust_tier=TrustTier.A2_AUTHORITATIVE,
        url="https://base.garant.ru/example",
        mode=RepresentationMode.VERIFY_ONLY,
        authority="GARANT",
        timeline_priority=1,
    )
    bundle = LegalSourceBundle(document_id="DOC-1", representations=(official, consultant, garant))

    assert [item.source_id for item in bundle.timeline_providers()] == ["GARANT", "CONSULTANT"]
    assert bundle.preferred_timeline_provider().source_id == "GARANT"


def test_acquisition_candidates_exclude_verify_only_a2():
    bundle = LegalSourceBundle(
        document_id="DOC-1",
        representations=(
            LegalSourceRepresentation(
                source_id="OFFICIAL",
                role=LegalSourceRole.PUBLICATION_EVIDENCE,
                trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
                url="https://official.example/doc",
                mode=RepresentationMode.OPERATOR_IMPORT,
                authority="official publication",
            ),
            LegalSourceRepresentation(
                source_id="GARANT",
                role=LegalSourceRole.VERSION_TIMELINE_PROVIDER,
                trust_tier=TrustTier.A2_AUTHORITATIVE,
                url="https://base.garant.ru/example",
                mode=RepresentationMode.VERIFY_ONLY,
                authority="GARANT",
                timeline_priority=1,
            ),
        ),
    )

    assert [item.source_id for item in bundle.acquisition_candidates()] == ["OFFICIAL"]
    assert [item.source_id for item in bundle.verification_references()] == ["GARANT"]
    assert bundle.has_authoritative_consolidated_reference() is True


def test_pdn_bundle_registry_is_parseable_and_keeps_a2_verify_only():
    registry_path = Path("config/pdn_source_bundles.json")
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    bundles = tuple(LegalSourceBundle.from_dict(item) for item in payload["bundles"])

    assert len(bundles) >= 4
    for bundle in bundles:
        providers = bundle.by_role(LegalSourceRole.VERSION_TIMELINE_PROVIDER)
        assert providers
        assert providers[0].source_id == "SRC-RU-GARANT-001"
        assert providers[0].timeline_priority == 1
        for item in providers + bundle.by_role(LegalSourceRole.CONSOLIDATED_REFERENCE):
            assert item.trust_tier == TrustTier.A2_AUTHORITATIVE
            assert item.mode == RepresentationMode.VERIFY_ONLY
            assert item.redistribution_allowed is False
