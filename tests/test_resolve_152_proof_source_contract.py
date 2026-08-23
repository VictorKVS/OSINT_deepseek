from pathlib import Path

from father_osint.proof_resolution import resolve_local_official_proof


def test_resilient_152_proof_resolver_prefers_verified_local_a0_and_never_requires_network():
    script = Path("scripts/resolve_152_proof_source.py").read_text(encoding="utf-8")
    module = Path("father_osint/proof_resolution.py").read_text(encoding="utf-8")
    cmd = Path("RUN_RESOLVE_152_PROOF_SOURCE.cmd").read_text(encoding="utf-8")

    assert 'TARGET_ID = "DOC-RU-FZ-152-2006"' in script
    assert "batch_review_manifest.json" in script
    assert "pdn_official_source_pack.json" in script
    assert "data\" / \"operator_import\"" in script
    assert "resolve_local_official_proof" in script
    assert "extract_visible_text" in module
    assert "primary_identity_markers" in module
    assert "identity_markers" in module
    assert "EXTRACT_VISIBLE_TEXT__PRIMARY_AND_SECONDARY__NORMALIZED" in module
    assert "OPERATOR_BROWSER_CAPTURE_OF_A0_PUBLICATION_PAGE" in module
    assert '"network_used": False' in script
    assert '"api_required_for_serving": False' in script
    assert '"new_d2_d3_promotion": False' in script
    assert '"legal_truth_promoted": False' in script
    assert "API_CIRCUIT_OPEN=" in script
    assert "scripts\\resolve_152_proof_source.py" in cmd


def test_canonical_resolver_identity_uses_visible_text_not_raw_html_substrings(tmp_path):
    html = """
    <html><body>
      <h1>Федеральный закон <span>о персональных данных</span></h1>
      <div>Дата подписания: <b>27.07.2006</b></div>
      <p>Статья 3. <em>Основные понятия, используемые в настоящем Федеральном законе</em></p>
      <div>152-ФЗ</div>
    </body></html>
    """.encode("utf-8")
    local = tmp_path / "capture.html"
    local.write_bytes(html)
    import hashlib
    digest = hashlib.sha256(html).hexdigest()

    result = resolve_local_official_proof(
        repo_root=tmp_path,
        review_item={"document_id": "DOC1", "artifact_sha256": digest},
        source_item={
            "document_id": "DOC1",
            "primary_identity_markers": [
                "Федеральный закон о персональных данных",
                "Дата подписания: 27.07.2006",
                "Статья 3. Основные понятия, используемые в настоящем Федеральном законе",
            ],
            "identity_markers": ["152-ФЗ", "О персональных данных"],
        },
        local_path=local,
    )

    assert result.identity_error is None
    assert result.identity_pass is True
    assert all(result.primary_identity_markers.values())
    assert all(result.secondary_identity_markers.values())
