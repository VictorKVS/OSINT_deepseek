from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Iterable, Mapping, Sequence


CROSS_TERM_RELATION = "SHARED_TERM_ACROSS_DOCUMENTS"
CROSS_ENTITY_RELATION = "SHARED_ENTITY_ACROSS_DOCUMENTS"
DEFINITION_VARIANCE_CANDIDATE = "DEFINITION_VARIANCE_CANDIDATE"
REQUIREMENT_OVERLAP_CANDIDATE = "REQUIREMENT_OVERLAP_CANDIDATE"


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "\x1f".join(" ".join(str(part).split()).casefold() for part in parts)
    return f"{prefix}-{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:24]}"


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _canonical_keys(rows: Sequence[Mapping[str, object]]) -> set[str]:
    keys: set[str] = set()
    for row in rows:
        value = str(row.get("canonical_key") or "")
        if not value:
            raise ValueError("canonical_key missing")
        keys.add(value)
    return keys


def normalized_requirement_statement(row: Mapping[str, object]) -> str:
    statement = str(row.get("statement") or "")
    if not statement:
        raise ValueError("requirement statement missing")
    return _norm(statement)


def cross_relation_signature(row: Mapping[str, object]) -> tuple[str, str]:
    relation_type = str(row.get("relation_type") or "")
    canonical_key = str(row.get("canonical_key") or "")
    if relation_type not in {CROSS_TERM_RELATION, CROSS_ENTITY_RELATION} or not canonical_key:
        raise ValueError("invalid D11 relation signature")
    return relation_type, canonical_key


def collect_cross_relation_signatures(
    all_terms: Sequence[Mapping[str, object]],
    all_entities: Sequence[Mapping[str, object]],
) -> set[tuple[str, str]]:
    return {
        *((CROSS_TERM_RELATION, key) for key in _canonical_keys(all_terms)),
        *((CROSS_ENTITY_RELATION, key) for key in _canonical_keys(all_entities)),
    }


def changed_document_cross_relation_signatures(
    *,
    old_terms: Sequence[Mapping[str, object]],
    old_entities: Sequence[Mapping[str, object]],
    new_terms: Sequence[Mapping[str, object]],
    new_entities: Sequence[Mapping[str, object]],
) -> set[tuple[str, str]]:
    """Return only D11 signatures whose document-membership can change.

    D11 relation payload depends on the set of supporting document IDs for a
    canonical key, not on mention counts. When exactly one document changes,
    a signature needs rebuilding only when that document gains or loses the
    corresponding canonical key. Keys that remain present in both versions do
    not alter D11 membership and their existing relation payload is reusable.
    """

    affected: set[tuple[str, str]] = set()
    old_term_keys = _canonical_keys(old_terms)
    new_term_keys = _canonical_keys(new_terms)
    old_entity_keys = _canonical_keys(old_entities)
    new_entity_keys = _canonical_keys(new_entities)

    affected.update((CROSS_TERM_RELATION, key) for key in old_term_keys ^ new_term_keys)
    affected.update((CROSS_ENTITY_RELATION, key) for key in old_entity_keys ^ new_entity_keys)
    return affected


def changed_document_conflict_signatures(
    *,
    old_definitions: Sequence[Mapping[str, object]],
    old_requirements: Sequence[Mapping[str, object]],
    new_definitions: Sequence[Mapping[str, object]],
    new_requirements: Sequence[Mapping[str, object]],
) -> set[tuple[str, str]]:
    """Return D12 signatures that may change when exactly one document changes.

    D12 payload is content-sensitive, not only membership-sensitive. A changed
    document can keep the same definition canonical key or normalized
    requirement statement while changing the candidate's supporting object IDs
    or normalized definition set. Therefore the affected set is the UNION of
    old and new signatures for that document, not a symmetric difference.
    """

    affected: set[tuple[str, str]] = set()
    affected.update(
        (DEFINITION_VARIANCE_CANDIDATE, key)
        for key in (_canonical_keys(old_definitions) | _canonical_keys(new_definitions))
    )
    affected.update(
        (REQUIREMENT_OVERLAP_CANDIDATE, normalized_requirement_statement(row))
        for row in [*old_requirements, *new_requirements]
    )
    return affected


def conflict_candidate_signature(
    row: Mapping[str, object],
    *,
    requirement_statement_by_id: Mapping[str, str],
) -> tuple[str, str]:
    candidate_type = str(row.get("candidate_type") or "")
    if candidate_type == DEFINITION_VARIANCE_CANDIDATE:
        canonical_key = str(row.get("canonical_key") or "")
        if not canonical_key:
            raise ValueError("definition candidate canonical_key missing")
        return candidate_type, canonical_key
    if candidate_type == REQUIREMENT_OVERLAP_CANDIDATE:
        requirement_ids = row.get("requirement_ids")
        if not isinstance(requirement_ids, Sequence) or isinstance(requirement_ids, (str, bytes)) or not requirement_ids:
            raise ValueError("requirement-overlap candidate requirement_ids missing")
        keys = {
            requirement_statement_by_id.get(str(requirement_id), "")
            for requirement_id in requirement_ids
        }
        keys.discard("")
        if len(keys) != 1:
            raise ValueError("cannot recover one normalized statement for requirement-overlap candidate")
        return candidate_type, next(iter(keys))
    raise ValueError(f"unsupported D12 candidate type: {candidate_type}")


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


def build_cross_relations_for_signatures(
    all_terms: Sequence[Mapping[str, object]],
    all_entities: Sequence[Mapping[str, object]],
    signatures: Iterable[tuple[str, str]],
) -> list[dict[str, object]]:
    """Build D11 rows only for requested relation-type/canonical-key signatures."""

    requested = {(str(relation_type), str(canonical_key)) for relation_type, canonical_key in signatures}
    invalid_types = {
        relation_type
        for relation_type, _ in requested
        if relation_type not in {CROSS_TERM_RELATION, CROSS_ENTITY_RELATION}
    }
    if invalid_types:
        raise ValueError("unsupported D11 relation types: " + ", ".join(sorted(invalid_types)))

    groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    for relation_type, rows in (
        (CROSS_TERM_RELATION, all_terms),
        (CROSS_ENTITY_RELATION, all_entities),
    ):
        for row in rows:
            canonical_key = str(row.get("canonical_key") or "")
            signature = (relation_type, canonical_key)
            if signature not in requested:
                continue
            lineage = row.get("lineage")
            if not isinstance(lineage, Mapping):
                raise ValueError("cross-relation lineage missing")
            groups[signature].add(str(lineage["document_id"]))

    cross: list[dict[str, object]] = []
    for relation_type, canonical_key in sorted(requested):
        docs = sorted(groups.get((relation_type, canonical_key), set()))
        if len(docs) < 2:
            continue
        cross.append({
            "relation_id": _stable_id("REL11", relation_type, canonical_key, *docs),
            "relation_type": relation_type,
            "canonical_key": canonical_key,
            "document_ids": docs,
            "review_state": "CANDIDATE_NEEDS_REVIEW",
            "promotion_state": "NOT_PROMOTED",
        })
    return cross


def build_cross_relations(
    all_terms: Sequence[Mapping[str, object]],
    all_entities: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    signatures = collect_cross_relation_signatures(all_terms, all_entities)
    return build_cross_relations_for_signatures(all_terms, all_entities, signatures)


def build_conflict_candidates_for_signatures(
    all_definitions: Sequence[Mapping[str, object]],
    all_requirements: Sequence[Mapping[str, object]],
    signatures: Iterable[tuple[str, str]],
) -> list[dict[str, object]]:
    """Build D12 candidates only for requested content-sensitive signatures."""

    requested = {(str(candidate_type), str(key)) for candidate_type, key in signatures}
    invalid_types = {
        candidate_type
        for candidate_type, _ in requested
        if candidate_type not in {DEFINITION_VARIANCE_CANDIDATE, REQUIREMENT_OVERLAP_CANDIDATE}
    }
    if invalid_types:
        raise ValueError("unsupported D12 candidate types: " + ", ".join(sorted(invalid_types)))

    conflicts: list[dict[str, object]] = []

    definition_groups: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    requested_definition_keys = {
        key for candidate_type, key in requested if candidate_type == DEFINITION_VARIANCE_CANDIDATE
    }
    for definition in all_definitions:
        canonical_key = str(definition.get("canonical_key") or "")
        if canonical_key in requested_definition_keys:
            definition_groups[canonical_key].append(definition)
    for canonical_key in sorted(requested_definition_keys):
        rows = definition_groups.get(canonical_key, [])
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
                "candidate_type": DEFINITION_VARIANCE_CANDIDATE,
                "canonical_key": canonical_key,
                "document_ids": docs,
                "definition_ids": sorted(str(row["definition_id"]) for row in rows),
                "confirmed_conflict": False,
                "review_state": "CANDIDATE_NEEDS_REVIEW",
                "promotion_state": "NOT_PROMOTED",
            })

    requirement_groups: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    requested_statement_keys = {
        key for candidate_type, key in requested if candidate_type == REQUIREMENT_OVERLAP_CANDIDATE
    }
    for requirement in all_requirements:
        statement_key = normalized_requirement_statement(requirement)
        if statement_key in requested_statement_keys:
            requirement_groups[statement_key].append(requirement)
    for statement_key in sorted(requested_statement_keys):
        rows = requirement_groups.get(statement_key, [])
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
                "candidate_type": REQUIREMENT_OVERLAP_CANDIDATE,
                "document_ids": docs,
                "requirement_ids": sorted(str(row["requirement_id"]) for row in rows),
                "confirmed_conflict": False,
                "review_state": "CANDIDATE_NEEDS_REVIEW",
                "promotion_state": "NOT_PROMOTED",
            })
    return conflicts


def build_conflict_candidates(
    all_definitions: Sequence[Mapping[str, object]],
    all_requirements: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    signatures: set[tuple[str, str]] = set()
    signatures.update(
        (DEFINITION_VARIANCE_CANDIDATE, key)
        for key in _canonical_keys(all_definitions)
    )
    signatures.update(
        (REQUIREMENT_OVERLAP_CANDIDATE, normalized_requirement_statement(row))
        for row in all_requirements
    )
    return build_conflict_candidates_for_signatures(all_definitions, all_requirements, signatures)


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
