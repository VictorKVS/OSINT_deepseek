from pathlib import Path

import pytest

from father_osint.external_assets import ExternalAssetPolicyError, authorize_external_asset, load_external_assets


def test_external_asset_registry_loads_unique_fail_closed_roles():
    assets = load_external_assets()
    assert "publication-pravo-official-api" in assets
    assert "rg-official-announcement-feed" in assets
    assert "rg-official-doc-index" in assets
    assert "ruslawod-corpus" in assets
    assert "ansvar-russian-law-mcp-code" in assets
    assert "ansvar-russian-law-mcp-prebuilt-db" in assets
    assert all(asset.legal_truth_promoted is False for asset in assets.values())


def test_quarantined_prebuilt_mcp_content_cannot_be_imported_or_promoted():
    asset = load_external_assets()["ansvar-russian-law-mcp-prebuilt-db"]
    assert asset.adoption == "REJECT"
    assert asset.content_reuse_mode == "NONE"
    assert asset.status == "QUARANTINED_IDENTITY_COLLISIONS"

    with pytest.raises(ExternalAssetPolicyError):
        authorize_external_asset("ansvar-russian-law-mcp-prebuilt-db", "candidate_import")
    with pytest.raises(ExternalAssetPolicyError):
        authorize_external_asset("ansvar-russian-law-mcp-prebuilt-db", "canonical_promotion")


def test_mcp_code_patterns_can_be_referenced_without_reusing_quarantined_content():
    asset = authorize_external_asset("ansvar-russian-law-mcp-code", "algorithm_reuse")
    assert asset.role == "ALGORITHM_DONOR"
    assert asset.algorithm_reuse_allowed is True
    with pytest.raises(ExternalAssetPolicyError):
        authorize_external_asset("ansvar-russian-law-mcp-code", "candidate_import")


def test_ruslawod_is_candidate_only_and_never_direct_promotion():
    asset = authorize_external_asset("ruslawod-corpus", "candidate_import")
    assert asset.content_reuse_mode == "CANDIDATE_ONLY"
    with pytest.raises(ExternalAssetPolicyError):
        authorize_external_asset("ruslawod-corpus", "canonical_promotion")


def test_official_discovery_adapters_are_proof_source_wrappers_but_never_direct_promotion():
    for asset_id in (
        "publication-pravo-official-api",
        "rg-official-announcement-feed",
        "rg-official-doc-index",
    ):
        asset = authorize_external_asset(asset_id, "proof_acquisition")
        assert asset.role == "PROOF_SOURCE"
        with pytest.raises(ExternalAssetPolicyError):
            authorize_external_asset(asset_id, "candidate_import")
        with pytest.raises(ExternalAssetPolicyError):
            authorize_external_asset(asset_id, "canonical_promotion")

    assert load_external_assets()["publication-pravo-official-api"].status == "PENDING_RUNTIME_ACCEPTANCE"
    assert load_external_assets()["rg-official-announcement-feed"].status == "PENDING_RUNTIME_ACCEPTANCE"
    assert load_external_assets()["rg-official-doc-index"].status == "RUNTIME_401_ON_WORKSTATION"
