import json
from pathlib import Path


def test_programmer_espd_snapshot_is_complete_and_current():
    inv = json.loads(Path("config/programmer_ru_espd_inventory.json").read_text(encoding="utf-8"))
    assert inv["counts"] == {"active": 28, "superseded": 1, "catalog_records": 29}
    records = inv["records"]
    active = {row["designation"] for row in records if row["status"] == "ACTIVE"}
    assert len(active) == 28
    assert "ГОСТ 19.001-77" in active
    assert "ГОСТ 19.101-2024" in active
    assert "ГОСТ 19.701-90" in active
    old = next(row for row in records if row["designation"] == "ГОСТ 19.101-77")
    assert old["status"] == "SUPERSEDED"
    assert old["superseded_by"] == "ГОСТ 19.101-2024"
    assert inv["rules"]["applicability_is_not_inferred_from_active_status"] is True


def test_programmer_automated_systems_layer_tracks_current_replacements():
    inv = json.loads(Path("config/programmer_ru_automated_systems_conditional.json").read_text(encoding="utf-8"))
    assert inv["applicability_class"] == "CONDITIONAL_PROJECT_CONTEXT"
    current = {row["designation"] for row in inv["current_documents"]}
    assert {
        "ГОСТ Р 59853-2021",
        "ГОСТ 34.201-2020",
        "ГОСТ Р 59793-2021",
        "ГОСТ 34.602-2020",
        "ГОСТ Р 59792-2021",
    } <= current
    historical = {row["designation"]: row for row in inv["historical_do_not_use_as_current"]}
    assert historical["ГОСТ 34.601-90"]["use_in_rf"] == "ГОСТ Р 59793-2021"
    assert historical["ГОСТ 34.603-92"]["use_in_rf"] == "ГОСТ Р 59792-2021"
    assert historical["ГОСТ 34.003-90"]["use_in_rf"] == "ГОСТ Р 59853-2021"
    assert historical["ГОСТ 34.602-89"]["superseded_by"] == "ГОСТ 34.602-2020"


def test_programmer_normative_scope_is_measurable_not_all_or_nothing_claim():
    scope = json.loads(Path("config/programmer_ru_normative_scope.json").read_text(encoding="utf-8"))
    sectors = {row["sector_id"]: row for row in scope["sectors"]}
    assert sectors["ESPD_GOST_19"]["state"] == "COMPLETE_CURRENT_CATALOG_STATUS"
    assert sectors["FSTEC_AND_REGULATED_INFORMATION_SYSTEMS"]["state"] == "RESEARCH_REQUIRED"
    assert sectors["AUTOMATED_SYSTEMS_GOST_34"]["state"] == "CONDITIONAL_CORE_VERIFIED"
    assert sectors["KII_187_FZ"]["state"] == "CONDITIONAL_PRIMARY_LAW_SEEDED"
    assert scope["global_layer_gate"]["allowed_to_claim_role_maturity_before_ru_applicability_review"] is False
