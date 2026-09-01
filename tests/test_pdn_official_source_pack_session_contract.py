from pathlib import Path


def test_official_source_pack_starts_clean_session_and_uses_publication_anchors():
    starter = Path("scripts/start_pdn_official_source_pack_session.py").read_text(encoding="utf-8")
    opener = Path("OPEN_PDN_OFFICIAL_SOURCE_PACK.cmd").read_text(encoding="utf-8")

    assert '"pdn_official_source_pack_session.json"' in starter
    assert 'item["publication_anchor"]["url"]' in starter
    assert "webbrowser.open" in starter
    assert "GARANT" in starter
    assert "scripts\\start_pdn_official_source_pack_session.py" in opener


def test_official_source_pack_inventory_requires_session_recent_html_and_strong_unique_identity():
    script = Path("scripts/inventory_pdn_official_downloads.py").read_text(encoding="utf-8")

    assert "SESSION_MISSING" in script
    assert 'SUPPORTED_SUFFIXES = {".html", ".htm"}' in script
    assert "started_epoch - 5" in script
    assert "extract_visible_text" in script
    assert "primary_identity_markers" in script
    assert "identity_markers" in script
    assert "PRIMARY_AND_SECONDARY" in script
    assert "AMBIGUOUS_IDENTITY" in script
    assert "candidate_match_cardinality" in script
    assert "sha256" in script
    assert "D0_D3_VERIFIED_OPERATOR_CAPTURE" in script
    assert "garant_used" in script


def test_official_source_pack_registry_has_primary_identity_profiles_for_all_targets():
    import json

    payload = json.loads(Path("config/pdn_official_source_pack.json").read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.1"
    assert len(payload["documents"]) == 4
    for item in payload["documents"]:
        assert len(item["primary_identity_markers"]) >= 3
        assert item["identity_markers"]

    fz152 = next(item for item in payload["documents"] if item["document_id"] == "DOC-RU-FZ-152-2006")
    assert "Дата подписания: 27.07.2006" in fz152["primary_identity_markers"]
    assert "27 июля 2006" not in fz152["identity_markers"]
    assert fz152["identity_markers"] == ["О персональных данных"]
