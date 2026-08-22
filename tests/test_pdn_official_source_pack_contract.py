import json
from pathlib import Path


def test_official_source_pack_is_bounded_and_garant_hold():
    payload = json.loads(Path("config/pdn_official_source_pack.json").read_text(encoding="utf-8"))
    assert payload["pack_id"] == "PDN-OFFICIAL-SOURCE-PACK-001"
    assert "GARANT" in payload["policy"]
    assert "HOLD" in payload["policy"]
    ids = [item["document_id"] for item in payload["documents"]]
    assert ids == [
        "DOC-RU-FZ-152-2006",
        "DOC-RU-PP-1119-2012",
        "DOC-RU-FSTEC-21-2013",
        "DOC-RU-FSB-378-2014",
    ]
    for item in payload["documents"]:
        assert item["preferred_operator_source"]["trust_tier"] in {
            "A0_OFFICIAL_PUBLICATION",
            "A1_OFFICIAL_ORGAN",
        }
        assert item["publication_anchor"]["trust_tier"] == "A0_OFFICIAL_PUBLICATION"
        assert item["primary_identity_markers"]
        assert item["identity_markers"]


def test_official_source_pack_one_click_helpers_exist():
    opener = Path("OPEN_PDN_OFFICIAL_SOURCE_PACK.cmd").read_text(encoding="utf-8")
    inventory = Path("RUN_PDN_OFFICIAL_SOURCE_PACK_INVENTORY.cmd").read_text(encoding="utf-8")
    script = Path("scripts/inventory_pdn_official_downloads.py").read_text(encoding="utf-8")

    assert "start_pdn_official_source_pack_session.py" in opener
    assert "GARANT is HOLD" in opener
    assert "inventory_pdn_official_downloads.py" in inventory
    assert "PRIMARY_AND_SECONDARY" in script
    assert "D0_D3_VERIFIED_OPERATOR_CAPTURE" in script
    assert "provenance_rule" in script
