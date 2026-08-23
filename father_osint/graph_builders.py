from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Mapping, Sequence


REVIEW_STATE = "CANDIDATE_NEEDS_REVIEW"
PROMOTION_STATE = "NOT_PROMOTED"


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "\x1f".join(" ".join(str(part).split()).casefold() for part in parts)
    return f"{prefix}-{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:24]}"


@dataclass(frozen=True, slots=True)
class GraphRows:
    nodes: tuple[dict[str, object], ...]
    edges: tuple[dict[str, object], ...]


def _node(node_id: str, node_type: str, **metadata: object) -> dict[str, object]:
    return {
        "node_id": node_id,
        "node_type": node_type,
        "metadata": metadata,
        "review_state": REVIEW_STATE,
        "promotion_state": PROMOTION_STATE,
    }


def _edge(
    edge_id: str,
    relation_type: str,
    from_node: str,
    to_node: str,
    **metadata: object,
) -> dict[str, object]:
    return {
        "edge_id": edge_id,
        "relation_type": relation_type,
        "from_node": from_node,
        "to_node": to_node,
        "metadata": metadata,
        "review_state": REVIEW_STATE,
        "promotion_state": PROMOTION_STATE,
    }


def build_document_graph_fragment(
    document_id: str,
    payload: Mapping[str, Sequence[Mapping[str, object]]],
) -> GraphRows:
    nodes: dict[str, dict[str, object]] = {}
    edges: dict[str, dict[str, object]] = {}

    def add_node(row: dict[str, object]) -> None:
        nodes.setdefault(str(row["node_id"]), row)

    def add_edge(row: dict[str, object]) -> None:
        edges.setdefault(str(row["edge_id"]), row)

    doc_node = f"DOC:{document_id}"
    add_node(_node(doc_node, "DOCUMENT", document_id=document_id))

    for term in payload.get("terms", ()):
        canonical_key = str(term["canonical_key"])
        term_node = f"TERM:{canonical_key}"
        add_node(_node(term_node, "TERM", canonical_key=canonical_key, term=term["term"]))
        add_edge(_edge(
            _stable_id("E13", doc_node, term_node, "mentions-term"),
            "DOCUMENT_MENTIONS_TERM",
            doc_node,
            term_node,
        ))

    for definition in payload.get("definitions", ()):
        definition_id = str(definition["definition_id"])
        def_node = f"DEF:{definition_id}"
        add_node(_node(
            def_node,
            "DEFINITION_CANDIDATE",
            definition_id=definition_id,
            canonical_key=definition["canonical_key"],
        ))
        add_edge(_edge(
            _stable_id("E13", doc_node, def_node, "contains-definition"),
            "DOCUMENT_CONTAINS_DEFINITION",
            doc_node,
            def_node,
        ))

    for requirement in payload.get("requirements", ()):
        requirement_id = str(requirement["requirement_id"])
        req_node = f"REQ:{requirement_id}"
        add_node(_node(
            req_node,
            "REQUIREMENT_CANDIDATE",
            requirement_id=requirement_id,
            modality=requirement["modality"],
        ))
        add_edge(_edge(
            _stable_id("E13", doc_node, req_node, "contains-requirement"),
            "DOCUMENT_CONTAINS_REQUIREMENT",
            doc_node,
            req_node,
        ))

    for entity in payload.get("entities", ()):
        canonical_key = str(entity["canonical_key"])
        ent_node = f"ENT:{canonical_key}"
        add_node(_node(
            ent_node,
            "ENTITY_CANDIDATE",
            canonical_key=canonical_key,
            entity=entity["entity"],
            entity_kind=entity["entity_kind"],
        ))
        add_edge(_edge(
            _stable_id("E13", doc_node, ent_node, "mentions-entity"),
            "DOCUMENT_MENTIONS_ENTITY",
            doc_node,
            ent_node,
        ))

    return GraphRows(tuple(nodes.values()), tuple(edges.values()))


def build_internal_graph_fragment(
    relations: Sequence[Mapping[str, object]],
) -> GraphRows:
    edges: list[dict[str, object]] = []
    for relation in relations:
        relation_type = str(relation["relation_type"])
        if relation_type == "TERM_DEFINED_BY":
            from_node = f"TERM:{relation['from_canonical_key']}"
            to_node = f"DEF:{relation['to_definition_id']}"
        elif relation_type == "REQUIREMENT_MENTIONS_ENTITY":
            from_node = f"REQ:{relation['from_requirement_id']}"
            to_node = f"ENT:{relation['canonical_key']}"
        else:
            raise ValueError(f"unsupported D10 relation_type: {relation_type}")
        edges.append(_edge(
            str(relation["relation_id"]),
            relation_type,
            from_node,
            to_node,
            evidence_chunk_id=relation.get("evidence_chunk_id"),
        ))
    return GraphRows((), tuple(edges))


def build_cross_graph_fragment(
    relations: Sequence[Mapping[str, object]],
) -> GraphRows:
    edges: list[dict[str, object]] = []
    for relation in relations:
        docs = [f"DOC:{value}" for value in relation.get("document_ids", [])]
        for left_index, left in enumerate(docs):
            for right in docs[left_index + 1:]:
                edges.append(_edge(
                    _stable_id("E13", str(relation["relation_id"]), left, right),
                    str(relation["relation_type"]),
                    left,
                    right,
                    canonical_key=relation.get("canonical_key"),
                ))
    return GraphRows((), tuple(edges))


def build_conflict_graph_fragment(
    candidates: Sequence[Mapping[str, object]],
) -> GraphRows:
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    for candidate in candidates:
        conflict_node = f"CON:{candidate['candidate_id']}"
        nodes.append(_node(
            conflict_node,
            "CONFLICT_OR_OVERLAP_CANDIDATE",
            candidate_id=candidate["candidate_id"],
            candidate_type=candidate["candidate_type"],
            confirmed_conflict=False,
        ))
        for document_id in candidate.get("document_ids", []):
            doc_node = f"DOC:{document_id}"
            edges.append(_edge(
                _stable_id("E13", conflict_node, doc_node),
                "CANDIDATE_INVOLVES_DOCUMENT",
                conflict_node,
                doc_node,
            ))
    return GraphRows(tuple(nodes), tuple(edges))


def merge_graph_fragments(*fragments: GraphRows) -> GraphRows:
    nodes: dict[str, dict[str, object]] = {}
    edges: dict[str, dict[str, object]] = {}
    for fragment in fragments:
        for row in fragment.nodes:
            nodes.setdefault(str(row["node_id"]), dict(row))
        for row in fragment.edges:
            edges.setdefault(str(row["edge_id"]), dict(row))
    return GraphRows(tuple(nodes.values()), tuple(edges.values()))


def build_graph_rows(
    per_doc: Mapping[str, Mapping[str, Sequence[Mapping[str, object]]]],
    internal_relations: Sequence[Mapping[str, object]],
    cross_relations: Sequence[Mapping[str, object]],
    conflict_candidates: Sequence[Mapping[str, object]],
    *,
    document_order: Sequence[str],
) -> GraphRows:
    fragments = [
        *(build_document_graph_fragment(document_id, per_doc[document_id]) for document_id in document_order),
        build_internal_graph_fragment(internal_relations),
        build_cross_graph_fragment(cross_relations),
        build_conflict_graph_fragment(conflict_candidates),
    ]
    graph = merge_graph_fragments(*fragments)
    node_ids = {str(row["node_id"]) for row in graph.nodes}
    missing = [
        str(row["edge_id"])
        for row in graph.edges
        if str(row["from_node"]) not in node_ids or str(row["to_node"]) not in node_ids
    ]
    if missing:
        raise ValueError("D13 graph endpoints missing: " + ", ".join(missing[:10]))
    return graph


def materialize_selective_graph(
    canonical_nodes: Sequence[Mapping[str, object]],
    canonical_edges: Sequence[Mapping[str, object]],
    *,
    old_fragments: Sequence[GraphRows],
    new_fragments: Sequence[GraphRows],
    refreshed_shared_nodes: Sequence[Mapping[str, object]] = (),
) -> GraphRows:
    """Replace only affected D13 fragments while reusing the canonical graph.

    Old fragment edge IDs define the exact invalidation set. New fragments are
    overlaid. Old affected nodes that disappear are removed only when no final
    edge references them; this preserves shared TERM/ENTITY nodes still supported
    elsewhere. `refreshed_shared_nodes` lets the caller refresh metadata for a
    shared node whose first supporting document changed or disappeared.
    """

    old_node_ids = {
        str(row["node_id"])
        for fragment in old_fragments
        for row in fragment.nodes
    }
    old_edge_ids = {
        str(row["edge_id"])
        for fragment in old_fragments
        for row in fragment.edges
    }

    nodes = {str(row["node_id"]): dict(row) for row in canonical_nodes}
    edges = {
        str(row["edge_id"]): dict(row)
        for row in canonical_edges
        if str(row["edge_id"]) not in old_edge_ids
    }

    new_node_ids: set[str] = set()
    for fragment in new_fragments:
        for row in fragment.nodes:
            node_id = str(row["node_id"])
            new_node_ids.add(node_id)
            nodes[node_id] = dict(row)
        for row in fragment.edges:
            edges[str(row["edge_id"])] = dict(row)

    for row in refreshed_shared_nodes:
        node_id = str(row["node_id"])
        new_node_ids.add(node_id)
        nodes[node_id] = dict(row)

    referenced = {
        str(value)
        for edge in edges.values()
        for value in (edge["from_node"], edge["to_node"])
    }
    for node_id in old_node_ids - new_node_ids:
        if node_id not in referenced:
            nodes.pop(node_id, None)

    node_ids = set(nodes)
    missing = [
        edge_id
        for edge_id, row in edges.items()
        if str(row["from_node"]) not in node_ids or str(row["to_node"]) not in node_ids
    ]
    if missing:
        raise ValueError("selective D13 graph endpoints missing: " + ", ".join(missing[:10]))

    return GraphRows(tuple(nodes.values()), tuple(edges.values()))
