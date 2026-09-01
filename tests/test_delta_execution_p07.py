from pathlib import Path

import pytest

from father_osint.delta_execution import execute_shadow_delta


def test_shadow_delta_reuses_exact_payload_and_covers_graph_without_overlap():
    nodes = [
        {"node_id": "DOC:A", "node_type": "DOCUMENT", "metadata": {"x": 1}},
        {"node_id": "TERM:x", "node_type": "TERM", "metadata": {"x": 2}},
        {"node_id": "REQ:r1", "node_type": "REQUIREMENT", "metadata": {"x": 3}},
    ]
    edges = [
        {"edge_id": "E1", "from_node": "DOC:A", "to_node": "TERM:x"},
        {"edge_id": "E2", "from_node": "DOC:A", "to_node": "REQ:r1"},
    ]
    plan = {
        "rebuild_or_remove_node_ids": ["REQ:r1"],
        "retain_recheck_node_ids": ["TERM:x"],
        "reusable_node_ids": ["DOC:A"],
        "recheck_edge_ids": ["E2"],
        "reusable_edge_ids": ["E1"],
    }

    result = execute_shadow_delta(plan, graph_nodes=nodes, graph_edges=edges)

    assert result.node_coverage_ok is True
    assert result.edge_coverage_ok is True
    assert result.node_sets_disjoint is True
    assert result.edge_sets_disjoint is True
    assert result.reusable_node_payload_match is True
    assert result.reusable_edge_payload_match is True
    assert [row["node_id"] for row in result.reusable_nodes] == ["DOC:A"]
    assert {row["action"] for row in result.node_actions} == {"REBUILD_OR_REMOVE", "RETAIN_RECHECK"}
    assert [row["edge_id"] for row in result.reusable_edges] == ["E1"]
    assert [row["action"] for row in result.edge_actions] == ["RECHECK"]


def test_shadow_delta_fails_closed_on_incomplete_or_overlapping_plan():
    nodes = [{"node_id": "N1"}, {"node_id": "N2"}]
    edges = [{"edge_id": "E1"}]

    with pytest.raises(ValueError, match="does not cover"):
        execute_shadow_delta(
            {
                "rebuild_or_remove_node_ids": ["N1"],
                "retain_recheck_node_ids": [],
                "reusable_node_ids": [],
                "recheck_edge_ids": ["E1"],
                "reusable_edge_ids": [],
            },
            graph_nodes=nodes,
            graph_edges=edges,
        )

    with pytest.raises(ValueError, match="node sets overlap"):
        execute_shadow_delta(
            {
                "rebuild_or_remove_node_ids": ["N1"],
                "retain_recheck_node_ids": [],
                "reusable_node_ids": ["N1", "N2"],
                "recheck_edge_ids": ["E1"],
                "reusable_edge_ids": [],
            },
            graph_nodes=nodes,
            graph_edges=edges,
        )


def test_shadow_delta_runner_contract_keeps_canonical_graph_immutable_and_d15_blocked():
    script = Path("scripts/prove_pdn_delta_shadow_execution.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DELTA_SHADOW_EXECUTION.cmd").read_text(encoding="utf-8")

    assert "P0_7_OBJECT_DELTA_PLAN.json" in script
    assert ".runtime\" / \"pdn_delta_shadow" in script
    assert "nodes_sha256_before" in script
    assert "nodes_sha256_after" in script
    # Payload exactness is covered functionally above. Avoid coupling this runner
    # contract to a particular acceptance-dictionary key spelling.
    assert "reusable_node_payload_match" in script
    assert "reusable_edge_payload_match" in script
    assert "P0_7_DELTA_D14_PACKET.json" in script
    assert '"review_state": "NEEDS_REVIEW"' in script
    assert '"d15_blocked_until_review": True' in script
    assert '"legal_truth_promoted": False' in script
    assert "scripts\\prove_pdn_object_delta_plan.py" in cmd
    assert "scripts\\prove_pdn_delta_shadow_execution.py" in cmd
