import json
from pathlib import Path


def test_library_order_policy_requires_ru_regulatory_layer_first():
    policy = json.loads(Path("config/library_order_policy.json").read_text(encoding="utf-8"))
    rule = policy["regulatory_first_policy"]
    assert rule["mode"] == "RU_REGULATORY_AND_NATIONAL_STANDARDS_FIRST"
    assert rule["required_before_global_maturity_claim"] is True
    assert rule["superseded_documents_do_not_close_current_gate"] is True
    assert policy["pipeline"][1] == "STAGE_0_RU_REGULATORY_BASELINE"
    assert "RU_REGULATORY_BASELINE" in policy["maturity_levels"]["MIN"]["required_dimensions"]


def test_programmer_ru_baseline_has_current_official_seed_and_supersession():
    baseline = json.loads(Path("config/role_ru_regulatory_baseline.json").read_text(encoding="utf-8"))
    programmer = baseline["roles"]["PROGRAMMER"]
    docs = {row["designation"]: row for row in programmer["documents"]}
    for designation in (
        "ГОСТ 19.101-2024",
        "ГОСТ 19.102-77",
        "ГОСТ Р ИСО/МЭК 12207-2010",
        "ГОСТ Р 56939-2024",
        "ГОСТ Р 58412-2019",
        "ГОСТ Р 71207-2024",
    ):
        assert docs[designation]["status"] == "ACTIVE"
        assert docs[designation]["verification_state"] == "OFFICIAL_METADATA_VERIFIED"
        assert docs[designation]["official_source"].startswith("https://protect.gost.ru/")
    superseded = {row["designation"]: row["superseded_by"] for row in programmer["known_superseded"]}
    assert superseded["ГОСТ 19.101-77"] == "ГОСТ 19.101-2024"
    assert superseded["ГОСТ Р 56939-2016"] == "ГОСТ Р 56939-2024"


def test_library_order_creation_embeds_ru_stage_and_blocks_missing_roles():
    text = Path("scripts/create_library_order.py").read_text(encoding="utf-8")
    assert "role_ru_regulatory_baseline.json" in text
    assert '"STAGE_0_RU_REGULATORY_BASELINE"' in text
    assert '"RU_REGULATORY_BASELINE_GAP"' in text
    assert '"current_stage": "STAGE_0_RU_REGULATORY_BASELINE"' in text


def test_library_order_runner_enforces_ru_stage_before_acquisition():
    text = Path("scripts/run_library_order.py").read_text(encoding="utf-8")
    assert "validate_ru_stage" in text
    assert "BLOCKED_RU_REGULATORY_BASELINE" in text
    assert text.index('order["current_stage"] = "STAGE_0_RU_REGULATORY_BASELINE"') < text.index('order["current_stage"] = "STAGE_1_ACQUISITION"')
    assert 'requested_sources - {"TELEGRAM", "RU_OFFICIAL_REGULATORY"}' in text


def test_control_center_exposes_library_order_ui_and_action():
    html = Path("osint_web/static/index.html").read_text(encoding="utf-8")
    js = Path("osint_web/static/app.js").read_text(encoding="utf-8")
    app = Path("osint_web/app.py").read_text(encoding="utf-8")
    assert "Заказать библиотеку роли" in html
    assert "0 · Нормативка РФ" in html
    assert "libraryStartBtn" in html
    assert "LIBRARY_ORDER_START" in js
    assert 'action == "LIBRARY_ORDER_START"' in app
    assert 'parsed.path == "/api/library-orders"' in app
    assert "start_library_order.py" in app
