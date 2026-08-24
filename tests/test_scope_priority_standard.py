import json
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_global_scope_priority_standard_is_two_axis_and_mandatory():
    standard = load("config/father_scope_priority_standard.json")
    assert standard["status"] == "MANDATORY"
    assert standard["allowed_maturity_values"] == ["MIN", "MEDIUM", "MAX"]
    assert standard["allowed_importance_values"] == ["NECESSARY", "DESIRABLE", "INTERESTING_LATER"]
    assert standard["planning_rules"]["importance_does_not_imply_maturity"] is True
    assert standard["planning_rules"]["maturity_does_not_imply_importance"] is True
    assert standard["planning_rules"]["deferred_items_must_not_disappear"] is True


def test_every_seeded_area_has_complete_3x3_matrix():
    matrix = load("config/father_area_priority_matrix.json")
    assert matrix["classification_standard"] == "config/father_scope_priority_standard.json"
    assert matrix["areas"]
    maturity = ("MIN", "MEDIUM", "MAX")
    importance = ("NECESSARY", "DESIRABLE", "INTERESTING_LATER")
    for area in matrix["areas"]:
        assert area["area_id"]
        for level in maturity:
            assert level in area
            for priority in importance:
                assert priority in area[level]
                assert isinstance(area[level][priority], list)


def test_global_document_bindings_carry_maturity_and_importance():
    policy = load("config/global_document_registry_policy.json")
    fields = set(policy["required_binding_fields"])
    assert {"maturity_level", "importance_class"} <= fields
    assert policy["allowed_maturity_values"] == ["MIN", "MEDIUM", "MAX"]
    assert policy["allowed_importance_values"] == ["NECESSARY", "DESIRABLE", "INTERESTING_LATER"]
    assert policy["acceptance_gates"]["every_binding_has_two_axis_classification"] is True
    assert policy["acceptance_gates"]["unresolved_necessary_binding_at_or_below_target_maturity_blocks_completion"] is True


def test_library_orders_execute_necessary_before_optional_work():
    policy = load("config/library_order_policy.json")
    execution = policy["priority_execution"]
    assert execution["default_importance_order"] == ["NECESSARY", "DESIRABLE", "INTERESTING_LATER"]
    assert execution["auto_execute"] == ["NECESSARY"]
    assert execution["queue_after_core"] == ["DESIRABLE"]
    assert execution["hold_by_default"] == ["INTERESTING_LATER"]
    assert policy["classification_standard"] == "config/father_scope_priority_standard.json"


def test_docs_explain_that_the_axes_are_independent():
    text = Path("docs/FATHER_SCOPE_PRIORITY_STANDARD.md").read_text(encoding="utf-8")
    assert "MIN" in text and "MEDIUM" in text and "MAX" in text
    assert "NECESSARY" in text and "DESIRABLE" in text and "INTERESTING_LATER" in text
    assert "The axes must never be collapsed into one score" in text
    assert "Global Document Registry" in text
