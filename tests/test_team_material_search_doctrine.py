import json
from pathlib import Path

from scripts.plan_team_role_search import build_plan


def test_search_doctrine_is_authoritative_first_and_gap_bounded():
    doctrine = json.loads(Path("config/team_material_search_doctrine.json").read_text(encoding="utf-8"))
    assert doctrine["unit_of_search"] == "ROLE_TOPIC"
    assert doctrine["source_order"][0]["tier"] == "S0"
    assert doctrine["passes"][0]["pass_id"] == "P1_ANCHOR"
    assert doctrine["passes"][0]["telegram_allowed"] is False
    assert doctrine["stop_rules"]["no_unbounded_role_scraping"] is True
    assert doctrine["stop_rules"]["after_first_pass_search_only_gaps"] is True
    assert doctrine["stop_rules"]["max_gap_passes_per_topic"] == 2
    assert doctrine["stop_rules"]["telegram_alone_never_closes_overall_min"] is True


def test_programmer_plan_starts_with_authoritative_anchor_queries():
    registry = json.loads(Path("config/team_role_material_registry.json").read_text(encoding="utf-8"))
    doctrine = json.loads(Path("config/team_material_search_doctrine.json").read_text(encoding="utf-8"))
    role = next(row for row in registry["roles"] if row["role_id"] == "PROGRAMMER")
    plan = build_plan(role, doctrine, max_queries=80)
    assert plan["role_id"] == "PROGRAMMER"
    assert plan["topics_total"] == len(role["topics"])
    assert plan["policy"]["authoritative_first"] is True
    assert plan["policy"]["telegram_for_anchor_pass"] is False
    assert plan["planned_queries_total"] <= 80
    assert plan["queries"][0]["pass_id"] == "P1_ANCHOR"
    assert all(row["telegram_allowed"] is False for row in plan["queries"] if row["pass_id"] == "P1_ANCHOR")


def test_planner_is_bounded_before_collection():
    registry = json.loads(Path("config/team_role_material_registry.json").read_text(encoding="utf-8"))
    doctrine = json.loads(Path("config/team_material_search_doctrine.json").read_text(encoding="utf-8"))
    role = next(row for row in registry["roles"] if row["role_id"] == "ML_LLM_ENGINEER")
    plan = build_plan(role, doctrine, max_queries=10)
    assert plan["planned_queries_total"] == 10
    assert plan["candidate_queries_before_bound"] > plan["planned_queries_total"]
    assert plan["policy"]["plan_before_collection"] is True
    assert plan["policy"]["kb_auto_promotion"] is False


def test_search_plan_cmd_is_planning_only():
    text = Path("RUN_TEAM_ROLE_SEARCH_PLAN.cmd").read_text(encoding="utf-8")
    assert "plan_team_role_search.py" in text
    assert "performs no Telegram/web collection" in text
    assert "RUN_TEAM_ROLE_ACQUISITION" not in text
