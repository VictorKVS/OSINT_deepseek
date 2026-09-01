from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .acquisition import AcquisitionRequest, AcquisitionService, ArtifactFetcher
from .document_compiler import DocumentCompiler, DocumentCompilerError
from .knowledge_factory import (
    DocumentRecord,
    DocumentVersion,
    OfficialSource,
    Role,
    SourceClass,
    SourceStatus,
)
from .knowledge_factory_store import KnowledgeFactoryStore
from .source_policy import MaterialProfile, SourcePolicy, TrustTier


class BatchRegistryError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class BatchDocumentResult:
    document_id: str
    title: str
    priority: str
    source_id: str
    source_state: str
    status: str
    tags: tuple[str, ...]
    kb_targets: tuple[str, ...]
    source_url: str | None = None
    artifact_sha256: str | None = None
    artifact_bytes: int | None = None
    mime_type: str | None = None
    version_id: str | None = None
    acquisition_disposition: str | None = None
    manifest_path: str | None = None
    structure_path: str | None = None
    chunks_path: str | None = None
    extracted_text_path: str | None = None
    structure_nodes: int | None = None
    chunks: int | None = None
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "title": self.title,
            "priority": self.priority,
            "source_id": self.source_id,
            "source_state": self.source_state,
            "status": self.status,
            "tags": list(self.tags),
            "kb_targets": list(self.kb_targets),
            "source_url": self.source_url,
            "artifact_sha256": self.artifact_sha256,
            "artifact_bytes": self.artifact_bytes,
            "mime_type": self.mime_type,
            "version_id": self.version_id,
            "acquisition_disposition": self.acquisition_disposition,
            "manifest_path": self.manifest_path,
            "structure_path": self.structure_path,
            "chunks_path": self.chunks_path,
            "extracted_text_path": self.extracted_text_path,
            "structure_nodes": self.structure_nodes,
            "chunks": self.chunks,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class BatchRunResult:
    registry_id: str
    results: tuple[BatchDocumentResult, ...]
    review_json_path: str
    review_md_path: str

    @property
    def counters(self) -> dict[str, int]:
        values = [item.status for item in self.results]
        return {
            "listed": len(values),
            "ready_d5": values.count("READY_D5"),
            "acquired_d3": values.count("ACQUIRED_D3"),
            "source_pending": values.count("SOURCE_PENDING"),
            "disabled": values.count("DISABLED"),
            "acquisition_failed": values.count("ACQUISITION_FAILED"),
            "acquisition_blocked": values.count("ACQUISITION_BLOCKED"),
            "compile_failed": values.count("COMPILE_FAILED"),
        }


def load_registry(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not payload.get("registry_id") or not isinstance(payload.get("sources"), dict):
        raise BatchRegistryError("registry_id and sources are required")
    documents = payload.get("documents")
    if not isinstance(documents, list) or not documents:
        raise BatchRegistryError("documents list is required")
    ids = [item.get("document_id") for item in documents]
    if any(not value for value in ids) or len(set(ids)) != len(ids):
        raise BatchRegistryError("document_id values must be present and unique")
    return payload


def _source_objects(registry: dict[str, Any], source_id: str) -> tuple[OfficialSource, SourcePolicy]:
    try:
        cfg = registry["sources"][source_id]
    except KeyError as exc:
        raise BatchRegistryError(f"unknown source_id {source_id}") from exc

    source = OfficialSource(
        source_id=source_id,
        name=cfg["name"],
        domain=cfg["domain"],
        organization=cfg["organization"],
        source_class=SourceClass(cfg["source_class"]),
        status=SourceStatus(cfg["status"]),
        trust_basis=cfg["trust_basis"],
        verified_by=cfg["verified_by"],
        verified_at=cfg["verified_at"],
        authority_scope=list(cfg.get("authority_scope", [])),
    )
    policy = SourcePolicy(
        source_id=source_id,
        domains=list(cfg.get("domains", [cfg["domain"]])),
        trust_tier=TrustTier(cfg["trust_tier"]),
        material_profiles=[MaterialProfile.LEGAL],
        trust_basis=[cfg["trust_basis"]],
        authority_scope=list(cfg.get("authority_scope", [])),
        verification_evidence=list(cfg.get("verification_evidence", [])),
    )
    return source, policy


def _load_or_create_document(store: KnowledgeFactoryStore, cfg: dict[str, Any]) -> DocumentRecord:
    existing = store.get_document(cfg["document_id"])
    if existing:
        versions = [DocumentVersion(**item) for item in existing.get("versions", [])]
        return DocumentRecord(
            title=existing["title"],
            document_type=existing["document_type"],
            workspace_id=existing.get("workspace_id", "default"),
            owner=existing.get("owner", "system"),
            jurisdiction=existing.get("jurisdiction"),
            language=existing.get("language", "ru"),
            topic_tags=list(existing.get("topic_tags", [])),
            versions=versions,
            current_version_id=existing.get("current_version_id"),
            stage_states=dict(existing.get("stage_states", {})),
            document_id=existing["document_id"],
            created_at=existing["created_at"],
            updated_at=existing["updated_at"],
        )

    return DocumentRecord(
        document_id=cfg["document_id"],
        title=cfg["title"],
        document_type=cfg["document_type"],
        jurisdiction=cfg.get("jurisdiction"),
        language=cfg.get("language", "ru"),
        topic_tags=list(cfg.get("tags", [])),
    )


def _base_result(cfg: dict[str, Any], status: str, *, reason: str = "") -> BatchDocumentResult:
    return BatchDocumentResult(
        document_id=cfg["document_id"],
        title=cfg["title"],
        priority=cfg.get("priority", ""),
        source_id=cfg["source_id"],
        source_state=cfg.get("source_state", "UNKNOWN"),
        source_url=cfg.get("source_url"),
        status=status,
        tags=tuple(cfg.get("tags", [])),
        kb_targets=tuple(cfg.get("kb_targets", [])),
        reason=reason,
    )


def _markdown_review(registry: dict[str, Any], results: list[BatchDocumentResult], counters: dict[str, int]) -> str:
    lines = [
        f"# PDn official corpus review — {registry['registry_id']}",
        "",
        "This file is generated by the batch conveyor. It is a review index, not legal advice and not a semantic KB publication.",
        "",
        "## Counters",
        "",
    ]
    for key, value in counters.items():
        lines.append(f"- `{key}`: {value}")
    lines += [
        "",
        "## Documents",
        "",
        "| Priority | Document | Status | Source state | SHA-256 | Chunks | Reason |",
        "|---|---|---|---|---|---:|---|",
    ]
    for item in results:
        sha = item.artifact_sha256 or "—"
        chunks = str(item.chunks) if item.chunks is not None else "—"
        reason = item.reason.replace("|", "\\|") if item.reason else ""
        lines.append(
            f"| {item.priority} | `{item.document_id}` {item.title} | **{item.status}** | "
            f"{item.source_state} | `{sha}` | {chunks} | {reason} |"
        )
    lines += [
        "",
        "## Review rule",
        "",
        "Only `READY_D5` rows have passed exact acquisition and preliminary structure/chunk preparation. "
        "`SOURCE_PENDING`, `ACQUISITION_*` and `COMPILE_FAILED` rows must not be treated as acquired/processed knowledge.",
        "",
        "For every `READY_D5` item inspect the referenced per-document `manifest.json`, exact original and chunks before D6+ semantic promotion.",
    ]
    return "\n".join(lines) + "\n"


class PdnOfficialBatchRunner:
    def __init__(
        self,
        store: KnowledgeFactoryStore,
        *,
        fetcher: ArtifactFetcher | None = None,
        max_chunk_chars: int = 2400,
    ) -> None:
        self.store = store
        self.fetcher = fetcher
        self.max_chunk_chars = max_chunk_chars

    def run(self, registry: dict[str, Any]) -> BatchRunResult:
        results: list[BatchDocumentResult] = []

        for cfg in registry["documents"]:
            if not cfg.get("enabled", False):
                pending = cfg.get("source_state") in {
                    "SOURCE_PENDING",
                    "OFFICIAL_PUBLICATION_PAGE_ARTIFACT_PENDING",
                }
                results.append(
                    _base_result(
                        cfg,
                        "SOURCE_PENDING" if pending else "DISABLED",
                        reason="exact official artifact locator not yet approved" if pending else "disabled by registry",
                    )
                )
                continue

            source_url = cfg.get("source_url")
            if not source_url:
                results.append(_base_result(cfg, "SOURCE_PENDING", reason="source_url is missing"))
                continue

            try:
                source, policy = _source_objects(registry, cfg["source_id"])
                document = _load_or_create_document(self.store, cfg)
            except Exception as exc:
                results.append(_base_result(cfg, "SOURCE_PENDING", reason=f"registry error: {exc}"))
                continue

            acquisition = AcquisitionService(self.store, fetcher=self.fetcher).acquire(
                AcquisitionRequest(
                    source=source,
                    source_policy=policy,
                    document=document,
                    source_url=source_url,
                    file_name=cfg["file_name"],
                    actor_id="pdn-batch-osint",
                    actor_role=Role.OSINT_EXPERT,
                    publication_date=cfg.get("official_publication_date"),
                    effective_date=cfg.get("effective_from"),
                    version_date=cfg.get("version_date"),
                )
            )

            if acquisition.version is None:
                status = (
                    "ACQUISITION_BLOCKED"
                    if acquisition.disposition.value == "BLOCKED"
                    else "ACQUISITION_FAILED"
                )
                results.append(
                    BatchDocumentResult(
                        **{
                            **_base_result(cfg, status, reason=acquisition.event.reason).to_dict(),
                            "tags": tuple(cfg.get("tags", [])),
                            "kb_targets": tuple(cfg.get("kb_targets", [])),
                        }
                    )
                )
                continue

            version = acquisition.version
            try:
                compiled = DocumentCompiler(self.store).compile(
                    document,
                    actor_id="pdn-batch-curator",
                    actor_role=Role.KNOWLEDGE_CURATOR,
                    max_chunk_chars=self.max_chunk_chars,
                )
            except DocumentCompilerError as exc:
                results.append(
                    BatchDocumentResult(
                        document_id=cfg["document_id"],
                        title=cfg["title"],
                        priority=cfg.get("priority", ""),
                        source_id=cfg["source_id"],
                        source_state=cfg.get("source_state", "UNKNOWN"),
                        source_url=version.source_url,
                        status="COMPILE_FAILED",
                        tags=tuple(cfg.get("tags", [])),
                        kb_targets=tuple(cfg.get("kb_targets", [])),
                        artifact_sha256=version.sha256,
                        artifact_bytes=version.file_size,
                        mime_type=version.mime_type,
                        version_id=version.version_id,
                        acquisition_disposition=acquisition.disposition.value,
                        reason=str(exc),
                    )
                )
                continue

            results.append(
                BatchDocumentResult(
                    document_id=cfg["document_id"],
                    title=cfg["title"],
                    priority=cfg.get("priority", ""),
                    source_id=cfg["source_id"],
                    source_state=cfg.get("source_state", "UNKNOWN"),
                    source_url=version.source_url,
                    status="READY_D5",
                    tags=tuple(cfg.get("tags", [])),
                    kb_targets=tuple(cfg.get("kb_targets", [])),
                    artifact_sha256=version.sha256,
                    artifact_bytes=version.file_size,
                    mime_type=version.mime_type,
                    version_id=version.version_id,
                    acquisition_disposition=acquisition.disposition.value,
                    manifest_path=compiled.manifest_path,
                    structure_path=compiled.structure_path,
                    chunks_path=compiled.chunks_path,
                    extracted_text_path=compiled.extracted_text_path,
                    structure_nodes=len(compiled.structure_nodes),
                    chunks=len(compiled.chunks),
                    reason="; ".join(compiled.warnings),
                )
            )

        review_dir = self.store.root / "review"
        review_dir.mkdir(parents=True, exist_ok=True)
        review_json = review_dir / "batch_review_manifest.json"
        review_md = review_dir / "REVIEW.md"

        preliminary = BatchRunResult(
            registry_id=registry["registry_id"],
            results=tuple(results),
            review_json_path=review_json.relative_to(self.store.root).as_posix(),
            review_md_path=review_md.relative_to(self.store.root).as_posix(),
        )
        payload = {
            "schema_version": "1.0",
            "registry_id": registry["registry_id"],
            "purpose": registry.get("purpose"),
            "counters": preliminary.counters,
            "documents": [item.to_dict() for item in results],
            "semantic_extraction_performed": False,
            "review_required_before_d6": True,
        }
        review_json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        review_md.write_text(
            _markdown_review(registry, results, preliminary.counters),
            encoding="utf-8",
            newline="\n",
        )
        return preliminary
