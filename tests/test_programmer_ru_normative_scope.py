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
    assert sectors["FSTEC_AND_REGULATED_INFORMATION_SYSTEMS"]["state"] == "CONDITIONAL_CURRENT_PRIMARY_SEEDED_WITH_WATCH"
    assert sectors["FSTEC_AND_REGULATED_INFORMATION_SYSTEMS"]["inventory_ref"] == "config/programmer_ru_fstec_regulated_systems.json"
    assert "08.05.2026 № 137" in sectors["FSTEC_AND_REGULATED_INFORMATION_SYSTEMS"]["scheduled_change"]
    assert sectors["AUTOMATED_SYSTEMS_GOST_34"]["state"] == "CONDITIONAL_CORE_VERIFIED"
    assert sectors["KII_187_FZ"]["state"] == "CONDITIONAL_PRIMARY_LAW_SEEDED"
    assert sectors["STATE_INFORMATION_SYSTEMS"]["state"] == "CONDITIONAL_PRIMARY_RULE_SEEDED_MAPPING_REQUIRED"
    assert scope["global_layer_gate"]["allowed_to_claim_role_maturity_before_ru_applicability_review"] is False


def test_programmer_fstec_overlay_tracks_current_and_future_dated_requirements():
    inv = json.loads(Path("config/programmer_ru_fstec_regulated_systems.json").read_text(encoding="utf-8"))
    assert inv["applicability_class"] == "CONDITIONAL_REGULATED_CONTEXT"
    contexts = {row["context_id"]: row for row in inv["contexts"]}
    gis = contexts["STATE_AND_GOVERNMENT_INFORMATION_SYSTEMS"]
    docs = {row["designation"]: row for row in gis["documents"]}
    assert docs["Приказ ФСТЭК России от 11.04.2025 № 117"]["status_on_snapshot_date"] == "ACTIVE"
    assert docs["Приказ ФСТЭК России от 08.05.2026 № 137"]["status_on_snapshot_date"] == "PUBLISHED_NOT_YET_EFFECTIVE"
    assert docs["Приказ ФСТЭК России от 08.05.2026 № 137"]["effective_from"] == "2026-09-01"
    assert inv["currentness_watch"][0]["watch_date"] == "2026-09-01"
