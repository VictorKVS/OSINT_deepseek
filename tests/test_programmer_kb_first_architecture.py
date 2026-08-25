import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_programmer_kb_build_order_is_region_standards_languages_algorithms_training():
    cfg = load("config/programmer_kb_first_architecture.json")
    assert cfg["status"] == "ACTIVE_P0"
    assert cfg["region_model"]["first_profile"] == "RU"
    ids = [row["id"] for row in cfg["mandatory_build_order"]]
    assert ids == [
        "REGION_AND_NORMATIVE_BASE",
        "PROGRAMMING_STANDARDS_LAYER",
        "LANGUAGE_KNOWLEDGE_LAYER",
        "LANGUAGE_SELECTION_RULES",
        "ALGORITHMS_SCIENTIFIC_LAYER",
        "ENGINEERING_COMPOSITION",
        "TASK_AND_TRAINING_MAPPING",
    ]


def test_training_is_held_until_programming_kb_min_gate():
    cfg = load("config/programmer_kb_first_architecture.json")
    state = cfg["training_state"]
    assert state["existing_40_derived_candidates"] == "HOLD_UNTIL_PROGRAMMING_KB_MIN_READY"
    assert state["new_task_expansion"] == "PAUSED"
    assert state["model_training"] == "DISABLED_UNTIL_KB_GATE"
    assert len(cfg["programming_kb_min_gate"]) >= 7


def test_knowledge_graph_can_represent_regional_norms_languages_algorithms_and_tasks():
    cfg = load("config/programmer_kb_first_architecture.json")
    node_types = set(cfg["knowledge_node_types"])
    relations = set(cfg["relation_types"])
    for required in {
        "REGION_PROFILE",
        "LEGAL_NORM",
        "STANDARD",
        "APPLICABILITY_RULE",
        "LANGUAGE",
        "LANGUAGE_SELECTION_RULE",
        "ALGORITHM",
        "DATA_STRUCTURE",
        "COMPLEXITY_BOUND",
        "DECISION_RULE",
        "SOURCE",
    }:
        assert required in node_types
    for required in {
        "APPLIES_IN_REGION",
        "MANDATORY_IF",
        "SUPERSEDES",
        "SUPPORTED_BY",
        "PREFERRED_WHEN",
        "AVOID_WHEN",
        "HAS_PRECONDITION",
        "HAS_COMPLEXITY",
        "VERIFIED_BY",
        "TEACHES",
    }:
        assert required in relations


def test_existing_ru_normative_scope_is_reused_not_duplicated():
    cfg = load("config/programmer_kb_first_architecture.json")
    ru = load("config/programmer_ru_normative_scope.json")
    assert cfg["region_model"]["ru_normative_scope_ref"] == "config/programmer_ru_normative_scope.json"
    assert ru["role_id"] == "PROGRAMMER"
    sectors = {row["sector_id"] for row in ru["sectors"]}
    assert "ESPD_GOST_19" in sectors
    assert "SOFTWARE_LIFECYCLE_AND_ENGINEERING" in sectors
    assert "SECURE_SOFTWARE_DEVELOPMENT" in sectors
    assert "AUTOMATED_SYSTEMS_GOST_34" in sectors
