from father_osint.dependency_invalidation import build_object_delta_plan


def test_object_delta_preserves_shared_nodes_with_unaffected_support():
    nodes = [
        {"node_id": "DOC:A"},
        {"node_id": "DOC:B"},
        {"node_id": "TERM:x"},
        {"node_id": "DEF:d1"},
        {"node_id": "CON:c1"},
    ]
    edges = [
        {"edge_id": "e1", "relation_type": "DOCUMENT_MENTIONS_TERM", "from_node": "DOC:A", "to_node": "TERM:x"},
        {"edge_id": "e2", "relation_type": "DOCUMENT_MENTIONS_TERM", "from_node": "DOC:B", "to_node": "TERM:x"},
        {"edge_id": "e3", "relation_type": "DOCUMENT_CONTAINS_DEFINITION", "from_node": "DOC:A", "to_node": "DEF:d1"},
        {"edge_id": "e4", "relation_type": "CANDIDATE_INVOLVES_DOCUMENT", "from_node": "CON:c1", "to_node": "DOC:A"},
    ]
    plan = build_object_delta_plan(
        ["A"],
        graph_nodes=nodes,
        graph_edges=edges,
        internal_relations=[],
        cross_relations=[{"relation_id": "r1", "document_ids": ["A", "B"]}],
        conflict_candidates=[{"candidate_id": "c1", "document_ids": ["A", "B"]}],
    )

    assert "DEF:d1" in plan.rebuild_or_remove_node_ids
    assert "TERM:x" in plan.retain_recheck_node_ids
    assert "CON:c1" in plan.retain_recheck_node_ids
    assert "DOC:B" in plan.reusable_node_ids
    assert "r1" in plan.cross_relation_ids
    assert "c1" in plan.conflict_candidate_ids
    assert "e1" in plan.recheck_edge_ids
    assert "e2" in plan.reusable_edge_ids


def test_shared_node_without_other_support_is_rebuilt_not_blindly_retained():
    plan = build_object_delta_plan(
        ["A"],
        graph_nodes=[{"node_id": "DOC:A"}, {"node_id": "TERM:x"}],
        graph_edges=[
            {"edge_id": "e1", "relation_type": "DOCUMENT_MENTIONS_TERM", "from_node": "DOC:A", "to_node": "TERM:x"},
        ],
        internal_relations=[],
        cross_relations=[],
        conflict_candidates=[],
    )
    assert "TERM:x" in plan.rebuild_or_remove_node_ids
    assert "TERM:x" not in plan.retain_recheck_node_ids


def test_empty_change_set_reuses_everything():
    plan = build_object_delta_plan(
        [],
        graph_nodes=[{"node_id": "DOC:A"}],
        graph_edges=[{"edge_id": "e1", "relation_type": "X", "from_node": "DOC:A", "to_node": "DOC:A"}],
        internal_relations=[],
        cross_relations=[],
        conflict_candidates=[],
    )
    assert plan.rebuild_or_remove_node_ids == ()
    assert plan.recheck_edge_ids == ()
    assert plan.reusable_node_ids == ("DOC:A",)
    assert plan.reusable_edge_ids == ("e1",)
