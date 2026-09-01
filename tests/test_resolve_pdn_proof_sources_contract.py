from pathlib import Path


def test_four_document_proof_resolver_is_local_reuse_only_and_one_click():
    module = Path("father_osint/proof_resolution.py").read_text(encoding="utf-8")
    script = Path("scripts/resolve_pdn_proof_sources.py").read_text(encoding="utf-8")
    cmd = Path("RUN_RESOLVE_PDN_PROOF_SOURCES.cmd").read_text(encoding="utf-8")

    assert "resolve_pack_from_files" in module
    assert "resolve_local_official_proof" in module
    assert "OPERATOR_BROWSER_CAPTURE_OF_A0_PUBLICATION_PAGE" in module
    assert "throughput_docs_per_second" in module
    assert "batch_review_manifest.json" in script
    assert "pdn_official_source_pack.json" in script
    assert '"network_used": False' in script
    assert '"api_required_for_serving": False' in script
    assert '"new_d2_d3_promotion": False' in script
    assert '"legal_truth_promoted": False' in script
    assert "ALL_PROOFS_AVAILABLE=" in script
    assert "THROUGHPUT_DOCS_PER_SECOND=" in script
    assert "scripts\\resolve_pdn_proof_sources.py" in cmd
