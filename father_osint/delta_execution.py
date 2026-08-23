from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable, Mapping


def _canonical_payload(rows: Iterable[Mapping[str, object]], *, id_field: str) -> bytes:
    ordered = sorted((dict(row) for row in rows), key=lambda row: str(row.get(id_field) or ""))
    return ("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for row in ordered) + ("\n" if ordered else "")).encode("utf-8")


def _payload_sha256(rows: Iterable[Mapping[str, object]], *, id_field: str) -> str:
    return hashlib.sha256(_canonical_payload(rows, id_field=id_field)).hexdigest()


@dataclass(frozen=True, slots=True)
class ShadowDeltaExecution:
    reusable_nodes: tuple[dict[str, object], ...]
    reusable_edges: tuple[dict[str, object], ...]
    node_actions: tuple[dict[str, object], ...]
    edge_actions: tuple[dict[str, object], ...]
    node_coverage_ok: bool
    edge_coverage_ok: bool
    node_sets_disjoint: bool
    edge_sets_disjoint: bool
    reusable_node_payload_match: bool
    reusable_edge_payload_match: bool

    def summary(self) -> dict[str, object]:
        return {
            "reused_nodes": len(self.reusable_nodes),
            "reused_edges": len(self.reusable_edges),
            "node_actions": len(self.node_actions),
            "edge_actions": len(self.edge_actions),
            "node_coverage_ok": self.node_coverage_ok,
            "edge_coverage_ok": self.edge_coverage_ok,
            "node_sets_disjoint": self.node_sets_disjoint,
            "edge_sets_disjoint": self.edge_sets_disjoint,
            "reusable_node_payload_match": self.reusable_node_payload_match,
            "reusable_edge_payload_match": self.reusable_edge_payload_match,
        }


def execute_shadow_delta(
    plan: Mapping[str, object],
    *,
    graph_nodes: Iterable[Mapping[str, object]],
    graph_edges: Iterable[Mapping[str, object]],
) -> ShadowDeltaExecution:
    """Execute an invalidation plan without mutating the canonical graph.

    Reusable graph objects are copied byte-semantically into the shadow result.
    Affected objects are represented only by explicit action records; this
    function never fabricates replacement knowledge and never promotes D14/D15.
    """

    nodes = [dict(row) for row in graph_nodes]
    edges = [dict(row) for row in graph_edges]
    node_by_id = {str(row.get("node_id") or ""): row for row in nodes if row.get("node_id")}
    edge_by_id = {str(row.get("edge_id") or ""): row for row in edges if row.get("edge_id")}

    rebuild_nodes = {str(value) for value in plan.get("rebuild_or_remove_node_ids", [])}
    retain_recheck_nodes = {str(value) for value in plan.get("retain_recheck_node_ids", [])}
    reusable_node_ids = {str(value) for value in plan.get("reusable_node_ids", [])}
    recheck_edge_ids = {str(value) for value in plan.get("recheck_edge_ids", [])}
    reusable_edge_ids = {str(value) for value in plan.get("reusable_edge_ids", [])}

    node_sets_disjoint = not (
        rebuild_nodes & retain_recheck_nodes
        or rebuild_nodes & reusable_node_ids
        or retain_recheck_nodes & reusable_node_ids
    )
    edge_sets_disjoint = not (recheck_edge_ids & reusable_edge_ids)

    planned_node_ids = rebuild_nodes | retain_recheck_nodes | reusable_node_ids
    planned_edge_ids = recheck_edge_ids | reusable_edge_ids
    node_coverage_ok = planned_node_ids == set(node_by_id)
    edge_coverage_ok = planned_edge_ids == set(edge_by_id)

    unknown_nodes = planned_node_ids - set(node_by_id)
    unknown_edges = planned_edge_ids - set(edge_by_id)
    if unknown_nodes:
        raise ValueError("delta plan references unknown graph nodes: " + ", ".join(sorted(unknown_nodes)[:10]))
    if unknown_edges:
        raise ValueError("delta plan references unknown graph edges: " + ", ".join(sorted(unknown_edges)[:10]))
    if not node_sets_disjoint:
        raise ValueError("delta plan node sets overlap")
    if not edge_sets_disjoint:
        raise ValueError("delta plan edge sets overlap")
    if not node_coverage_ok:
        raise ValueError("delta plan does not cover the complete current graph node set")
    if not edge_coverage_ok:
        raise ValueError("delta plan does not cover the complete current graph edge set")

    reusable_nodes = tuple(node_by_id[node_id] for node_id in sorted(reusable_node_ids))
    reusable_edges = tuple(edge_by_id[edge_id] for edge_id in sorted(reusable_edge_ids))

    node_actions = tuple(
        [
            {
                "node_id": node_id,
                "action": "REBUILD_OR_REMOVE",
                "reason": "DERIVED_FROM_CHANGED_DOCUMENT",
                "review_required": True,
                "promotion_state": "NOT_PROMOTED",
            }
            for node_id in sorted(rebuild_nodes)
        ]
        + [
            {
                "node_id": node_id,
                "action": "RETAIN_RECHECK",
                "reason": "SHARED_OBJECT_HAS_OTHER_SUPPORT_BUT_CHANGED_DOCUMENT_CONTRIBUTED",
                "review_required": True,
                "promotion_state": "NOT_PROMOTED",
            }
            for node_id in sorted(retain_recheck_nodes)
        ]
    )
    edge_actions = tuple(
        {
            "edge_id": edge_id,
            "action": "RECHECK",
            "reason": "DEPENDENCY_CONE_INTERSECTS_CHANGED_DOCUMENT",
            "review_required": True,
            "promotion_state": "NOT_PROMOTED",
        }
        for edge_id in sorted(recheck_edge_ids)
    )

    source_reusable_nodes = [node_by_id[node_id] for node_id in sorted(reusable_node_ids)]
    source_reusable_edges = [edge_by_id[edge_id] for edge_id in sorted(reusable_edge_ids)]
    reusable_node_payload_match = _payload_sha256(source_reusable_nodes, id_field="node_id") == _payload_sha256(reusable_nodes, id_field="node_id")
    reusable_edge_payload_match = _payload_sha256(source_reusable_edges, id_field="edge_id") == _payload_sha256(reusable_edges, id_field="edge_id")

    return ShadowDeltaExecution(
        reusable_nodes=reusable_nodes,
        reusable_edges=reusable_edges,
        node_actions=node_actions,
        edge_actions=edge_actions,
        node_coverage_ok=node_coverage_ok,
        edge_coverage_ok=edge_coverage_ok,
        node_sets_disjoint=node_sets_disjoint,
        edge_sets_disjoint=edge_sets_disjoint,
        reusable_node_payload_match=reusable_node_payload_match,
        reusable_edge_payload_match=reusable_edge_payload_match,
    )
