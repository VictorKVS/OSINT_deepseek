import json
from pathlib import Path


def test_library_order_policy_is_multisource_bounded_and_non_promoting():
    policy = json.loads(Path("config/library_order_policy.json").read_text(encoding="utf-8"))
    assert policy["status"] == "ACTIVE"
    assert int(policy["max_parallel_streams"]) == 5
    assert policy["default_sources"] == [
        "RU_OFFICIAL_REGULATORY",
        "OFFICIAL_WEB",
        "GITHUB",
        "TELEGRAM",
        "LOCAL_LIBRARY",
    ]
    assert policy["regulatory_first_policy"]["required_before_global_maturity_claim"] is True
    assert policy["copyright_policy"]["auto_download_commercial_books_from_unverified_mirrors"] is False
    assert policy["promotion_policy"]["kb_auto_promotion"] is False
    assert policy["promotion_policy"]["human_review_required"] is True


def test_library_order_creator_resolves_role_topics_and_trace():
    text = Path("scripts/create_library_order.py").read_text(encoding="utf-8")
    assert "team_role_material_registry.json" in text
    assert "role_ru_regulatory_baseline.json" in text
    assert "FATHER_LIBRARY_ORDER" in text
    assert "maturity_target" in text
    assert "knowledge_base_id" in text
    assert "FATHER_TRACE_ID" in text
    assert "STAGE_0_RU_REGULATORY_BASELINE" in text
    assert "RUN_STAGE_1_ACQUISITION" in text
    assert '"kb_auto_promotion": False' in text


def test_library_order_runner_reuses_proven_stage1_and_prepares_stage2_handoff():
    text = Path("scripts/run_library_order.py").read_text(encoding="utf-8")
    assert "validate_ru_stage" in text
    assert "BLOCKED_RU_REGULATORY_BASELINE" in text
    assert "run_team_role_acquisition_live.py" in text
    assert "analyze_team_role_telegram_coverage.py" in text
    assert "LIBRARY_ORDER_STAGE2_HANDOFF" in text
    assert "STAGE_2_DOCUMENT_COMPILER" in text
    assert "WAITING_SOURCE_CHANNELS" in text
    assert "SOURCE_CHANNEL_PENDING" in text
    assert "Downloaded file counts do not prove the requested role maturity" in text
    assert "Russian applicability and global authoritative coverage remain separate gates" in text
    assert '"kb_auto_promotion": False' in text


def test_library_order_docs_define_operator_managed_conveyor():
    text = Path("docs/LIBRARY_ORDER_CONVEYOR.md").read_text(encoding="utf-8")
    assert "LIBRARY_ORDER" in text
    assert "role_id" in text
    assert "MIN" in text and "MEDIUM" in text and "MAX" in text
    assert "OFFICIAL_WEB" in text and "GITHUB" in text and "TELEGRAM" in text and "LOCAL_LIBRARY" in text
    assert "human review" in text.lower()
