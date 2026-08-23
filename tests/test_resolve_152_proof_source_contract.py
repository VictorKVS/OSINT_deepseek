from pathlib import Path

from scripts.resolve_152_proof_source import _identity_result


def test_resilient_152_proof_resolver_prefers_verified_local_a0_and_never_requires_network():
    script = Path("scripts/resolve_152_proof_source.py").read_text(encoding="utf-8")
    cmd = Path("RUN_RESOLVE_152_PROOF_SOURCE.cmd").read_text(encoding="utf-8")

    assert 'TARGET_ID = "DOC-RU-FZ-152-2006"' in script
    assert "batch_review_manifest.json" in script
    assert "pdn_official_source_pack.json" in script
    assert "data\" / \"operator_import\"" in script
    assert "artifact_sha256" in script
    assert "extract_visible_text" in script
    assert "primary_identity_markers" in script
    assert "identity_markers" in script
    assert "EXTRACT_VISIBLE_TEXT__PRIMARY_AND_SECONDARY__NORMALIZED" in script
    assert '"network_used": False' in script
    assert '"api_required_for_serving": False' in script
    assert '"new_d2_d3_promotion": False' in script
    assert '"legal_truth_promoted": False' in script
    assert "LOCAL_A0_VERIFIED_CACHE" in script
    assert "API_CIRCUIT_OPEN=" in script
    assert "scripts\\resolve_152_proof_source.py" in cmd


def test_resolver_identity_uses_visible_text_not_raw_html_substrings():
    html = """
    <html><body>
      <h1>Федеральный закон <span>о персональных данных</span></h1>
      <div>Дата подписания: <b>27.07.2006</b></div>
      <p>Статья 3. <em>Основные понятия, используемые в настоящем Федеральном законе</em></p>
      <div>152-ФЗ</div>
    </body></html>
    """.encode("utf-8")
    source_doc = {
        "primary_identity_markers": [
            "Федеральный закон о персональных данных",
            "Дата подписания: 27.07.2006",
            "Статья 3. Основные понятия, используемые в настоящем Федеральном законе",
        ],
        "identity_markers": ["152-ФЗ", "О персональных данных"],
    }

    passed, primary, secondary, error = _identity_result(html, source_doc)

    assert error is None
    assert passed is True
    assert all(primary.values())
    assert all(secondary.values())
