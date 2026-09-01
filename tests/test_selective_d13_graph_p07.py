from pathlib import Path

from father_osint.graph_builders import (
    GraphRows,
    build_document_graph_fragment,
    materialize_selective_graph,
)


def _payload(document_id: str, *, requirement_id: str | None = None):
    requirements = []
    if requirement_id:
        requirements.append({"requirement_id": requirement_id, "modality": "OBLIGATION"})
    return {
        "terms": [{"canonical_key": "shared", "term": "shared"}],
        "definitions": [],
        "requirements": requirements,
        "entities": [],
    }


def test_selective_graph_replaces_changed_fragment_and_reuses_unaffected_payload():
    old_a = build_document_graph_fragment("A", _payload("A", requirement_id="old"))
    new_a = build_document_graph_fragment("A", _payload("A", requirement_id="new"))
    b = build_document_graph_fragment("B", _payload("B"))

    canonical_nodes = list(old_a.nodes) + [row for row in b.nodes if row["node_id"] not in {item["node_id"] for item in old_a.nodes}]
    canonical_edges = list(old_a.edges) + list(b.edges)

    result = materialize_selective_graph(
        canonical_nodes,
        canonical_edges,
        old_fragments=[old_a],
        new_fragments=[new_a],
    )

    node_ids = {row["node_id"] for row in result.nodes}
    edge_ids = {row["edge_id"] for row in result.edges}
    assert "REQ:old" not in node_ids
    assert "REQ:new" in node_ids
    assert "DOC:B" in node_ids
    assert any(row["from_node"] == "DOC:B" and row["to_node"] == "TERM:shared" for row in result.edges)
    assert len(edge_ids) == len(result.edges)


def test_shared_node_survives_when_old_changed_fragment_drops_it_but_unaffected_edge_references_it():
    old_a = GraphRows(
        nodes=(
            {"node_id": "DOC:A", "node_type": "DOCUMENT", "metadata": {}, "review_state": "CANDIDATE_NEEDS_REVIEW", "promotion_state": "NOT_PROMOTED"},
            {"node_id": "TERM:x", "node_type": "TERM", "metadata": {"term": "x"}, "review_state": "CANDIDATE_NEEDS_REVIEW", "promotion_state": "NOT_PROMOTED"},
        ),
        edges=(
            {"edge_id": "a-x", "relation_type": "DOCUMENT_MENTIONS_TERM", "from_node": "DOC:A", "to_node": "TERM:x", "metadata": {}, "review_state": "CANDIDATE_NEEDS_REVIEW", "promotion_state": "NOT_PROMOTED"},
        ),
    )
    canonical_nodes = list(old_a.nodes) + [
        {"node_id": "DOC:B", "node_type": "DOCUMENT", "metadata": {}, "review_state": "CANDIDATE_NEEDS_REVIEW", "promotion_state": "NOT_PROMOTED"},
    ]
    canonical_edges = list(old_a.edges) + [
        {"edge_id": "b-x", "relation_type": "DOCUMENT_MENTIONS_TERM", "from_node": "DOC:B", "to_node": "TERM:x", "metadata": {}, "review_state": "CANDIDATE_NEEDS_REVIEW", "promotion_state": "NOT_PROMOTED"},
    ]
    new_a = GraphRows(nodes=(old_a.nodes[0],), edges=())

    result = materialize_selective_graph(
        canonical_nodes,
        canonical_edges,
        old_fragments=[old_a],
        new_fragments=[new_a],
    )

    assert "TERM:x" in {row["node_id"] for row in result.nodes}
    assert "a-x" not in {row["edge_id"] for row in result.edges}
    assert "b-x" in {row["edge_id"] for row in result.edges}


def test_dual_path_d13_runner_is_fragment_selective_and_logged():
    script = Path("scripts/prove_pdn_dual_path_d13.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DUAL_PATH_D13_REBUILD.cmd").read_text(encoding="utf-8")

    assert "materialize_selective_graph" in script
    assert "full_graph_rebuild_in_selective_path" in script
    assert "explicit_reused_nodes_exact" in script
    assert "explicit_reused_edges_exact" in script
    assert '"legal_truth_promoted": False' in script
    assert "PDN_DUAL_PATH_D13_REBUILD" in cmd
    assert "run_logged_python_sequence.ps1" in cmd
