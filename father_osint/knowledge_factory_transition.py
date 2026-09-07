from __future__ import annotations

import hashlib
import json
from typing import Iterable

from .knowledge_factory import DocumentRecord, PIPELINE_ORDER, PipelineStage


def document_stage_snapshot(
    documents: Iterable[DocumentRecord],
    through_stage: PipelineStage,
) -> list[dict[str, object]]:
    """Build a stable evidence snapshot for a bounded document stage transition.

    The snapshot binds document identity, current version content hash, and all
    pipeline states up to the requested stage. Volatile metadata such as
    ``updated_at`` is intentionally excluded so harmless later bookkeeping does
    not invalidate the evidence receipt.
    """
    through_index = PIPELINE_ORDER.index(through_stage)
    stages = PIPELINE_ORDER[: through_index + 1]
    snapshot: list[dict[str, object]] = []

    for document in sorted(documents, key=lambda item: item.document_id):
        if not document.current_version_id:
            raise ValueError(f"document has no current version: {document.document_id}")
        current_version = next(
            (version for version in document.versions if version.version_id == document.current_version_id),
            None,
        )
        if current_version is None:
            raise ValueError(f"current version is missing from document history: {document.document_id}")

        snapshot.append({
            "document_id": document.document_id,
            "current_version_id": document.current_version_id,
            "current_version_sha256": current_version.sha256,
            "stage_states": {
                stage.value: document.stage_states.get(stage.value)
                for stage in stages
            },
        })
    return snapshot


def document_stage_snapshot_sha256(
    documents: Iterable[DocumentRecord],
    through_stage: PipelineStage,
) -> str:
    snapshot = document_stage_snapshot(documents, through_stage)
    raw = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
