from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Mapping, Sequence


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "\x1f".join(" ".join(str(part).split()).casefold() for part in parts)
    return f"{prefix}-{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:24]}"


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def build_internal_relations_for_document(
    document_id: str,
    payload: Mapping[str, Sequence[Mapping[str, object]]],
) -> list[dict[str, object]]:
    """Build deterministic D10 relations for exactly one document.

    This is intentionally document-local so a changed document can be rebuilt
    while unchanged documents reuse their existing D10 relation payloads.
    """

    entities_by_chunk: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for entity in payload.get("entities", ()):
        lineage = entity.get("lineage")
        if not isinstance(lineage, Mapping):
            raise ValueError("entity lineage missing")
        entities_by_chunk[str(lineage["chunk_id"])].append(entity)

    internal: list[dict[str, object]] = []
    for definition in payload.get("definitions", ()):
        lineage = definition.get("lineage")
        if not isinstance(lineage, Mapping):
            raise ValueError("definition lineage missing")
        internal.append({
            "relation_id": _stable_id("REL10", document_id, definition["definition_id"], "defines"),
            "relation_type": "TERM_DEFINED_BY",
            "document_id": document_id,
            "from_canonical_key": definition["canonical_key"],
            "to_definition_id": definition["definition_id"],
            "evidence_chunk_id": lineage["chunk_id"],
            "review_state": "CANDIDATE_NEEDS_REVIEW",
            "promotion_state": "NOT_PROMOTED",
        })

    for requirement in payload.get("requirements", ()):
        lineage = requirement.get("lineage")
        if not isinstance(lineage, Mapping):
            raise ValueError("requirement lineage missing")
        chunk_id = str(lineage["chunk_id"])
        for entity in entities_by_chunk.get(chunk_id, ()):
            internal.append({
                "relation_id": _stable_id("REL10", requirement["requirement_id"], entity["entity_mention_id"]),
                "relation_type": "REQUIREMENT_MENTIONS_ENTITY",
                "document_id": document_id,
                "from_requirement_id": requirement["requirement_id"],
                "to_entity_mention_id": entity["entity_mention_id"],
                "canonical_key": entity["canonical_key"],
                "evidence_chunk_id": chunk_id,
                "review_state": "CANDIDATE_NEEDS_REVIEW",
                "promotion_state": "NOT_PROMOTED",
            })
    return internal


def build_cross_relations(
    all_terms: Sequence[Mapping[str, object]],
    all_entities: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    cross: list[dict[str, object]] = []
    for relation_type, rows in (
        ("SHARED_TERM_ACROSS_DOCUMENTS", all_terms),
        ("SHARED_ENTITY_ACROSS_DOCUMENTS", all_entities),
    ):
        groups: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            lineage = row.get("lineage")
            if not isinstance(lineage, Mapping):
                raise ValueError("cross-relation lineage missing")
            groups[str(row["canonical_key"])].add(str(lineage["document_id"]))
        for canonical_key, document_ids in groups.items():
            if len(document_ids) < 2:
                continue
            docs = sorted(document_ids)
            cross.append({
                "relation_id": _stable_id("REL11", relation_type, canonical_key, *docs),
                "relation_type": relation_type,
                "canonical_key": canonical_key,
                "document_ids": docs,
                "review_state": "CANDIDATE_NEEDS_REVIEW",
                "promotion_state": "NOT_PROMOTED",
            })
    return cross


def build_conflict_candidates(
    all_definitions: Sequence[Mapping[str, object]],
    all_requirements: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    conflicts: list[dict[str, object]] = []

    definition_groups: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for definition in all_definitions:
        definition_groups[str(definition["canonical_key"])].append(definition)
    for canonical_key, rows in definition_groups.items():
        normalized = {_norm(str(row["definition"])) for row in rows}
        documents: set[str] = set()
        for row in rows:
            lineage = row.get("lineage")
            if not isinstance(lineage, Mapping):
                raise ValueError("definition lineage missing")
            documents.add(str(lineage["document_id"]))
        docs = sorted(documents)
        if len(normalized) > 1 and len(docs) > 1:
            conflicts.append({
                "candidate_id": _stable_id("CON12", "definition-variance", canonical_key, *docs),
                "candidate_type": "DEFINITION_VARIANCE_CANDIDATE",
                "canonical_key": canonical_key,
                "document_ids": docs,
                "definition_ids": sorted(str(row["definition_id"]) for row in rows),
                "confirmed_conflict": False,
                "review_state": "CANDIDATE_NEEDS_REVIEW",
                "promotion_state": "NOT_PROMOTED",
            })

    requirement_groups: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for requirement in all_requirements:
        requirement_groups[_norm(str(requirement["statement"]))].append(requirement)
    for statement_key, rows in requirement_groups.items():
        documents: set[str] = set()
        for row in rows:
            lineage = row.get("lineage")
            if not isinstance(lineage, Mapping):
                raise ValueError("requirement lineage missing")
            documents.add(str(lineage["document_id"]))
        docs = sorted(documents)
        if len(docs) > 1:
            conflicts.append({
                "candidate_id": _stable_id("CON12", "requirement-overlap", statement_key, *docs),
                "candidate_type": "REQUIREMENT_OVERLAP_CANDIDATE",
                "document_ids": docs,
                "requirement_ids": sorted(str(row["requirement_id"]) for row in rows),
                "confirmed_conflict": False,
                "review_state": "CANDIDATE_NEEDS_REVIEW",
                "promotion_state": "NOT_PROMOTED",
            })
    return conflicts


def build_relation_sets(
    per_doc: Mapping[str, Mapping[str, Sequence[Mapping[str, object]]]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    internal: list[dict[str, object]] = []
    all_terms: list[Mapping[str, object]] = []
    all_definitions: list[Mapping[str, object]] = []
    all_requirements: list[Mapping[str, object]] = []
    all_entities: list[Mapping[str, object]] = []

    for document_id, payload in per_doc.items():
        internal.extend(build_internal_relations_for_document(document_id, payload))
        all_terms.extend(payload.get("terms", ()))
        all_definitions.extend(payload.get("definitions", ()))
        all_requirements.extend(payload.get("requirements", ()))
        all_entities.extend(payload.get("entities", ()))

    return (
        internal,
        build_cross_relations(all_terms, all_entities),
        build_conflict_candidates(all_definitions, all_requirements),
    )
