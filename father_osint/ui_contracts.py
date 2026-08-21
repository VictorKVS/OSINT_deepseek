from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .knowledge_factory import ClauseRef, KnowledgeNode, KnowledgeRelation, PipelineStage, StageState


class ThemeMode(str, Enum):
    DAY = "DAY"
    NIGHT = "NIGHT"
    SYSTEM = "SYSTEM"


class ViewMode(str, Enum):
    GRAPH = "GRAPH"
    TABLE = "TABLE"
    DOCUMENT_LIST = "DOCUMENT_LIST"


NODE_TYPE_TOKENS: dict[str, str] = {
    "DOCUMENT": "blue",
    "CLAUSE": "cyan",
    "TERM": "violet",
    "DEFINITION": "purple",
    "REQUIREMENT": "amber",
    "ENTITY": "teal",
    "CONTROL": "green",
    "CONFLICT": "red",
    "SOURCE": "indigo",
    "METHOD": "orange",
    "UNKNOWN": "gray",
}


STAGE_STATE_TOKENS: dict[StageState, str] = {
    StageState.DONE: "green",
    StageState.VERIFIED: "green",
    StageState.IN_PROGRESS: "yellow",
    StageState.NEEDS_REVIEW: "yellow",
    StageState.NOT_DONE: "red",
    StageState.BLOCKED: "red",
    StageState.FAILED: "error",
    StageState.NOT_APPLICABLE: "gray",
}


@dataclass(slots=True)
class GraphNodeView:
    node_id: str
    label: str
    node_type: str
    color_token: str
    document_count: int
    clause_refs: list[ClauseRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GraphEdgeView:
    relation_id: str
    source: str
    target: str
    relation_type: str
    status: str
    evidence_count: int
    rationale: str


@dataclass(slots=True)
class NodeTableRow:
    node_id: str
    node_type: str
    label: str
    document_count: int
    document_ids: list[str]
    clause_locators: list[str]


@dataclass(slots=True)
class RelationTableRow:
    relation_id: str
    from_node_id: str
    to_node_id: str
    relation_type: str
    status: str
    evidence_documents: list[str]
    evidence_clauses: list[str]
    rationale: str
    method_ref: str | None
    reviewer: str | None


def project_node(node: KnowledgeNode) -> GraphNodeView:
    return GraphNodeView(
        node_id=node.node_id,
        label=node.label,
        node_type=node.node_type,
        color_token=NODE_TYPE_TOKENS.get(node.node_type.upper(), NODE_TYPE_TOKENS["UNKNOWN"]),
        document_count=len({ref.document_id for ref in node.document_refs}),
        clause_refs=list(node.document_refs),
        metadata=dict(node.metadata),
    )


def node_to_table_row(node: KnowledgeNode) -> NodeTableRow:
    return NodeTableRow(
        node_id=node.node_id,
        node_type=node.node_type,
        label=node.label,
        document_count=len({ref.document_id for ref in node.document_refs}),
        document_ids=sorted({ref.document_id for ref in node.document_refs}),
        clause_locators=[ref.locator for ref in node.document_refs],
    )


def project_relation(relation: KnowledgeRelation) -> GraphEdgeView:
    return GraphEdgeView(
        relation_id=relation.relation_id,
        source=relation.from_node_id,
        target=relation.to_node_id,
        relation_type=relation.relation_type,
        status=relation.status,
        evidence_count=len(relation.evidence_refs),
        rationale=relation.rationale,
    )


def relation_to_table_row(relation: KnowledgeRelation) -> RelationTableRow:
    return RelationTableRow(
        relation_id=relation.relation_id,
        from_node_id=relation.from_node_id,
        to_node_id=relation.to_node_id,
        relation_type=relation.relation_type,
        status=relation.status,
        evidence_documents=sorted({ref.document_id for ref in relation.evidence_refs}),
        evidence_clauses=[ref.locator for ref in relation.evidence_refs],
        rationale=relation.rationale,
        method_ref=relation.method_ref,
        reviewer=relation.reviewer,
    )


def stage_badge(stage: PipelineStage, state: StageState) -> dict[str, str]:
    return {
        "stage": stage.value,
        "state": state.value,
        "color_token": STAGE_STATE_TOKENS[state],
    }
