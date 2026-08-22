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
                    role=LegalSourceRole.CONSOLIDATED_REFERENCE,
                    trust_tier=TrustTier.A2_AUTHORITATIVE,
                    url="https://base.garant.ru/example",
                    mode=RepresentationMode.VERIFY_ONLY,
                    authority="GARANT",
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
                role=LegalSourceRole.CONSOLIDATED_REFERENCE,
                trust_tier=TrustTier.A2_AUTHORITATIVE,
                url="https://base.garant.ru/example",
                mode=RepresentationMode.VERIFY_ONLY,
                authority="GARANT",
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
        for item in bundle.by_role(LegalSourceRole.CONSOLIDATED_REFERENCE):
            assert item.trust_tier == TrustTier.A2_AUTHORITATIVE
            assert item.mode == RepresentationMode.VERIFY_ONLY
            assert item.redistribution_allowed is False
