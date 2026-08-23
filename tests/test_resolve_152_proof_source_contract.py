from pathlib import Path


def test_resilient_152_proof_resolver_prefers_verified_local_a0_and_never_requires_network():
    script = Path("scripts/resolve_152_proof_source.py").read_text(encoding="utf-8")
    cmd = Path("RUN_RESOLVE_152_PROOF_SOURCE.cmd").read_text(encoding="utf-8")

    assert 'TARGET_ID = "DOC-RU-FZ-152-2006"' in script
    assert "batch_review_manifest.json" in script
    assert "pdn_official_source_pack.json" in script
    assert "data\" / \"operator_import\"" in script
    assert "artifact_sha256" in script
    assert "primary_identity_markers" in script
    assert '"network_used": False' in script
    assert '"api_required_for_serving": False' in script
    assert '"new_d2_d3_promotion": False' in script
    assert '"legal_truth_promoted": False' in script
    assert "LOCAL_A0_VERIFIED_CACHE" in script
    assert "API_CIRCUIT_OPEN=" in script
    assert "scripts\\resolve_152_proof_source.py" in cmd
