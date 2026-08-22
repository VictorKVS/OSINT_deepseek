from pathlib import Path


def test_official_source_pack_starts_clean_session_and_uses_publication_anchors():
    starter = Path("scripts/start_pdn_official_source_pack_session.py").read_text(encoding="utf-8")
    opener = Path("OPEN_PDN_OFFICIAL_SOURCE_PACK.cmd").read_text(encoding="utf-8")

    assert '"pdn_official_source_pack_session.json"' in starter
    assert 'item["publication_anchor"]["url"]' in starter
    assert "webbrowser.open" in starter
    assert "GARANT" in starter
    assert "scripts\\start_pdn_official_source_pack_session.py" in opener


def test_official_source_pack_inventory_requires_session_recent_html_and_byte_identity():
    script = Path("scripts/inventory_pdn_official_downloads.py").read_text(encoding="utf-8")

    assert "SESSION_MISSING" in script
    assert 'SUPPORTED_SUFFIXES = {".html", ".htm"}' in script
    assert "started_epoch - 5" in script
    assert "extract_visible_text" in script
    assert "identity_markers" in script
    assert "sha256" in script
    assert "D0_D3_VERIFIED_OPERATOR_CAPTURE" in script
    assert "garant_used" in script
