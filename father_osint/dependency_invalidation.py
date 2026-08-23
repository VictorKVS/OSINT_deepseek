from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class ObjectDeltaPlan:
    changed_document_ids: tuple[str, ...]
    rebuild_or_remove_node_ids: tuple[str, ...]
    retain_recheck_node_ids: tuple[str, ...]
    recheck_edge_ids: tuple[str, ...]
    cross_relation_ids: tuple[str, ...]
    conflict_candidate_ids: tuple[str, ...]
    reusable_node_ids: tuple[str, ...]
    reusable_edge_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "changed_document_ids": list(self.changed_document_ids),
            "rebuild_or_remove_node_ids": list(self.rebuild_or_remove_node_ids),
            "retain_recheck_node_ids": list(self.retain_recheck_node_ids),
            "recheck_edge_ids": list(self.recheck_edge_ids),
            "cross_relation_ids": list(self.cross_relation_ids),
            "conflict_candidate_ids": list(self.conflict_candidate_ids),
            "reusable_node_ids": list(self.reusable_node_ids),
            "reusable_edge_ids": list(self.reusable_edge_ids),
        }


def _doc_ids(value: object) -> set[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return set()
    return {str(item) for item in value if str(item)}


def build_object_delta_plan(
    changed_document_ids: Iterable[str],
    *,
    graph_nodes: Iterable[Mapping[str, object]],
    graph_edges: Iterable[Mapping[str, object]],
    internal_relations: Iterable[Mapping[str, object]],
    cross_relations: Iterable[Mapping[str, object]],
    conflict_candidates: Iterable[Mapping[str, object]],
) -> ObjectDeltaPlan:
    """Plan object-level invalidation without mutating the current graph.

    Document identity nodes remain stable across versions. Definition and
    requirement nodes supported by a changed document must be rebuilt because
    their IDs/contents are version-derived. Shared TERM/ENTITY nodes are kept
    when an unaffected document still supports them; only their changed support
    edge is rechecked. Cross-document relations/conflict candidates touching a
    changed document are re-evaluated, while unrelated objects remain reusable.
    """

    changed = {str(item) for item in changed_document_ids if str(item)}
    nodes = [dict(row) for row in graph_nodes]
    edges = [dict(row) for row in graph_edges]
    node_ids = {str(row.get("node_id")) for row in nodes if row.get("node_id")}
    edge_ids = {str(row.get("edge_id")) for row in edges if row.get("edge_id")}
    changed_doc_nodes = {f"DOC:{document_id}" for document_id in changed}

    rebuild_nodes: set[str] = set()
    retain_recheck_nodes: set[str] = set()
    recheck_edges: set[str] = set()

    # Direct document-derived graph objects.
    support_docs_by_shared_node: dict[str, set[str]] = {}
    for edge in edges:
        edge_id = str(edge.get("edge_id") or "")
        relation_type = str(edge.get("relation_type") or "")
        left = str(edge.get("from_node") or "")
        right = str(edge.get("to_node") or "")

        if relation_type in {"DOCUMENT_MENTIONS_TERM", "DOCUMENT_MENTIONS_ENTITY"} and left.startswith("DOC:"):
            support_docs_by_shared_node.setdefault(right, set()).add(left.removeprefix("DOC:"))

        if left in changed_doc_nodes or right in changed_doc_nodes:
            if edge_id:
                recheck_edges.add(edge_id)
            if relation_type in {"DOCUMENT_CONTAINS_DEFINITION", "DOCUMENT_CONTAINS_REQUIREMENT"}:
                target = right if left in changed_doc_nodes else left
                if target:
                    rebuild_nodes.add(target)
            elif relation_type in {"DOCUMENT_MENTIONS_TERM", "DOCUMENT_MENTIONS_ENTITY"}:
                target = right if left in changed_doc_nodes else left
                if target:
                    retain_recheck_nodes.add(target)

    # Internal relation edges use the same relation IDs in D13.
    for relation in internal_relations:
        if str(relation.get("document_id") or "") in changed:
            relation_id = str(relation.get("relation_id") or "")
            if relation_id:
                recheck_edges.add(relation_id)

    # Shared nodes with no unaffected support cannot be blindly retained.
    for node_id in list(retain_recheck_nodes):
        support_docs = support_docs_by_shared_node.get(node_id, set())
        if support_docs and not (support_docs - changed):
            retain_recheck_nodes.remove(node_id)
            rebuild_nodes.add(node_id)

    cross_relation_ids: set[str] = set()
    for relation in cross_relations:
        if changed & _doc_ids(relation.get("document_ids")):
            relation_id = str(relation.get("relation_id") or "")
            if relation_id:
                cross_relation_ids.add(relation_id)

    conflict_ids: set[str] = set()
    conflict_nodes: set[str] = set()
    for candidate in conflict_candidates:
        if changed & _doc_ids(candidate.get("document_ids")):
            candidate_id = str(candidate.get("candidate_id") or "")
            if candidate_id:
                conflict_ids.add(candidate_id)
                conflict_nodes.add(f"CON:{candidate_id}")

    # Any D13 edge touching an affected conflict node or a changed document in
    # cross-document relation space must be rechecked.
    for edge in edges:
        edge_id = str(edge.get("edge_id") or "")
        relation_type = str(edge.get("relation_type") or "")
        left = str(edge.get("from_node") or "")
        right = str(edge.get("to_node") or "")
        if left in conflict_nodes or right in conflict_nodes:
            if edge_id:
                recheck_edges.add(edge_id)
        if relation_type in {"SHARED_TERM_ACROSS_DOCUMENTS", "SHARED_ENTITY_ACROSS_DOCUMENTS"}:
            if left in changed_doc_nodes or right in changed_doc_nodes:
                if edge_id:
                    recheck_edges.add(edge_id)

    # Conflict nodes themselves remain stable candidate identities but need a
    # fresh decision/evidence calculation, so retain them with recheck semantics.
    retain_recheck_nodes.update(conflict_nodes & node_ids)

    affected_nodes = rebuild_nodes | retain_recheck_nodes
    reusable_nodes = node_ids - affected_nodes
    reusable_edges = edge_ids - recheck_edges

    return ObjectDeltaPlan(
        changed_document_ids=tuple(sorted(changed)),
        rebuild_or_remove_node_ids=tuple(sorted(rebuild_nodes)),
        retain_recheck_node_ids=tuple(sorted(retain_recheck_nodes)),
        recheck_edge_ids=tuple(sorted(recheck_edges)),
        cross_relation_ids=tuple(sorted(cross_relation_ids)),
        conflict_candidate_ids=tuple(sorted(conflict_ids)),
        reusable_node_ids=tuple(sorted(reusable_nodes)),
        reusable_edge_ids=tuple(sorted(reusable_edges)),
    )
