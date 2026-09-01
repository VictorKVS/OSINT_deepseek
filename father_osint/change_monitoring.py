from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable, Mapping, Sequence

from .knowledge_factory import PipelineStage


class ChangeDisposition(str, Enum):
    UNCHANGED_REUSED = "UNCHANGED_REUSED"
    NEW_VERSION_CANDIDATE = "NEW_VERSION_CANDIDATE"
    IMMUTABLE_INTEGRITY_DRIFT = "IMMUTABLE_INTEGRITY_DRIFT"


@dataclass(frozen=True, slots=True)
class VersionObservation:
    document_id: str
    expected_sha256: str
    observed_sha256: str
    disposition: ChangeDisposition

    @property
    def changed(self) -> bool:
        return self.disposition != ChangeDisposition.UNCHANGED_REUSED

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["disposition"] = self.disposition.value
        payload["changed"] = self.changed
        return payload


def _valid_sha256(value: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 64 or any(ch not in "0123456789abcdef" for ch in normalized):
        raise ValueError("sha256 must be a 64-character hexadecimal digest")
    return normalized


def classify_observation(
    document_id: str,
    *,
    expected_sha256: str,
    observed_sha256: str,
    immutable_local_artifact: bool,
) -> VersionObservation:
    expected = _valid_sha256(expected_sha256)
    observed = _valid_sha256(observed_sha256)
    if expected == observed:
        disposition = ChangeDisposition.UNCHANGED_REUSED
    elif immutable_local_artifact:
        disposition = ChangeDisposition.IMMUTABLE_INTEGRITY_DRIFT
    else:
        disposition = ChangeDisposition.NEW_VERSION_CANDIDATE
    return VersionObservation(document_id, expected, observed, disposition)


DOC_LOCAL_INVALIDATION_STAGES = (
    PipelineStage.D4_STRUCTURE_PARSED.value,
    PipelineStage.D5_CHUNKED.value,
    PipelineStage.D6_TERMS_EXTRACTED.value,
    PipelineStage.D7_DEFINITIONS_EXTRACTED.value,
    PipelineStage.D8_REQUIREMENTS_EXTRACTED.value,
    PipelineStage.D9_ENTITIES_EXTRACTED.value,
    PipelineStage.D10_INTERNAL_RELATIONS.value,
)

CROSS_DOCUMENT_INVALIDATION_STAGES = (
    PipelineStage.D11_CROSS_DOCUMENT_RELATIONS.value,
    PipelineStage.D12_CONFLICTS_OVERLAPS.value,
    PipelineStage.D13_KNOWLEDGE_GRAPH_READY.value,
)


def _related_documents(
    changed: set[str],
    relation_rows: Iterable[Mapping[str, object]],
) -> set[str]:
    related = set(changed)
    for row in relation_rows:
        docs_raw = row.get("document_ids", [])
        if not isinstance(docs_raw, Sequence) or isinstance(docs_raw, (str, bytes)):
            continue
        docs = {str(item) for item in docs_raw if str(item)}
        if changed & docs:
            related.update(docs)
    return related


def build_bounded_dependency_cone(
    changed_document_ids: Iterable[str],
    *,
    cross_relations: Iterable[Mapping[str, object]] = (),
    conflict_candidates: Iterable[Mapping[str, object]] = (),
) -> dict[str, object]:
    changed = {str(item) for item in changed_document_ids if str(item)}
    if not changed:
        return {
            "changed_document_ids": [],
            "doc_local_rebuild_document_ids": [],
            "doc_local_stages": [],
            "cross_scope_document_ids": [],
            "cross_document_stages": [],
            "delta_d14_required": False,
            "d15_blocked_until_review": False,
            "full_corpus_rebuild_required": False,
        }

    relation_scope = _related_documents(changed, cross_relations)
    conflict_scope = _related_documents(changed, conflict_candidates)
    cross_scope = sorted(relation_scope | conflict_scope)
    return {
        "changed_document_ids": sorted(changed),
        "doc_local_rebuild_document_ids": sorted(changed),
        "doc_local_stages": list(DOC_LOCAL_INVALIDATION_STAGES),
        "cross_scope_document_ids": cross_scope,
        "cross_document_stages": list(CROSS_DOCUMENT_INVALIDATION_STAGES),
        "delta_d14_required": True,
        "d15_blocked_until_review": True,
        "full_corpus_rebuild_required": False,
    }


def synthetic_new_version_sha(document_id: str, prior_sha256: str) -> str:
    prior = _valid_sha256(prior_sha256)
    payload = f"P0.7-SYNTHETIC-NEW-VERSION\x1f{document_id}\x1f{prior}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
