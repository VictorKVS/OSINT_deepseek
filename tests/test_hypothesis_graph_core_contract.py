import json
from pathlib import Path


def test_hypothesis_graph_is_the_active_product_contour():
    ontology = json.loads(Path("config/hypothesis_graph_ontology.json").read_text(encoding="utf-8"))
    assert ontology["record_type"] == "HYPOTHESIS_GRAPH_ONTOLOGY"
    assert ontology["active_product_contour"] == "REASONING_GRAPH"
    assert ontology["tool_router_unlocked"] is False
    assert ontology["unlock_condition"] == "GRAPH_CORE_G0_G5_PASS"


def test_reasoning_graph_has_competing_hypotheses_counterevidence_gaps_and_tests():
    ontology = json.loads(Path("config/hypothesis_graph_ontology.json").read_text(encoding="utf-8"))
    node_types = set(ontology["node_types"])
    edge_types = set(ontology["edge_types"])
    for node in ("RQ", "HYP", "ALT_HYP", "FACT", "CLAIM", "EVIDENCE", "SRC", "TEST", "RESULT", "GAP", "CONFLICT"):
        assert node in node_types
    for edge in ("SUPPORTS", "CONTRADICTS", "COMPETES_WITH", "DEPENDS_ON", "TESTED_BY", "REQUIRES", "WEAKENS", "REJECTS", "SUPERSEDES"):
        assert edge in edge_types


def test_hypothesis_graph_blocks_false_precision_and_silent_promotion():
    ontology = json.loads(Path("config/hypothesis_graph_ontology.json").read_text(encoding="utf-8"))
    assert ontology["confidence_policy"]["numeric_confidence_allowed"] is False
    invariants = set(ontology["semantic_invariants"])
    assert "HYPOTHESIS_CANNOT_SILENTLY_PROMOTE_TO_FACT" in invariants
    assert "ABSENCE_OF_EVIDENCE_IS_GAP_NOT_NEGATIVE_FACT" in invariants
    assert "MIRRORS_DO_NOT_CREATE_INDEPENDENT_SUPPORT" in invariants


def test_graph_core_acceptance_needs_no_external_tools():
    ontology = json.loads(Path("config/hypothesis_graph_ontology.json").read_text(encoding="utf-8"))
    fixture = ontology["first_acceptance_fixture"]
    assert fixture["external_tools_required"] is False
    assert fixture["minimum_primary_hypotheses"] >= 1
    assert fixture["minimum_alternative_hypotheses"] >= 1
    assert fixture["minimum_counter_edges"] >= 1
    assert fixture["minimum_gap_nodes"] >= 1
    assert fixture["minimum_test_nodes"] >= 1
    assert fixture["must_preserve_rejected_hypothesis"] is True


def test_product_doc_explicitly_defers_tool_expansion():
    text = Path("docs/10_investigation_workspace/HYPOTHESIS_GRAPH_CORE.md").read_text(encoding="utf-8")
    for token in (
        "The first usable contour is **not a tool dashboard**",
        "Layer A — Reasoning graph (build first)",
        "Layer B — Entity graph (build second)",
        "Layer C — Fusion graph",
        "Tool drawer is hidden/disabled in Graph Core v0.1",
        "Only after G0–G4 pass do we unlock Tool Router work",
    ):
        assert token in text
