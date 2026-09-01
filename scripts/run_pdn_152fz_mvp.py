from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.acquisition import AcquisitionRequest, AcquisitionService
from father_osint.document_compiler import DocumentCompiler
from father_osint.knowledge_factory import (
    DocumentRecord,
    DocumentVersion,
    OfficialSource,
    Role,
    SourceClass,
    SourceStatus,
)
from father_osint.knowledge_factory_store import KnowledgeFactoryStore
from father_osint.source_policy import MaterialProfile, SourcePolicy, TrustTier


DEFAULT_CONFIG = REPO_ROOT / "config" / "pdn_mvp_152fz.json"


def load_document(store: KnowledgeFactoryStore, config: dict) -> DocumentRecord:
    doc_cfg = config["document"]
    existing = store.get_document(doc_cfg["document_id"])
    if not existing:
        return DocumentRecord(
            document_id=doc_cfg["document_id"],
            title=doc_cfg["title"],
            document_type=doc_cfg["document_type"],
            jurisdiction=doc_cfg.get("jurisdiction"),
            language=doc_cfg.get("language", "ru"),
            topic_tags=list(doc_cfg.get("topic_tags", [])),
        )

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


def build_source(config: dict) -> tuple[OfficialSource, SourcePolicy]:
    source_cfg = config["source"]
    policy_cfg = config["source_policy"]
    source = OfficialSource(
        source_id=source_cfg["source_id"],
        name=source_cfg["name"],
        domain=source_cfg["domain"],
        organization=source_cfg["organization"],
        source_class=SourceClass(source_cfg["source_class"]),
        status=SourceStatus(source_cfg["status"]),
        trust_basis=source_cfg["trust_basis"],
        verified_by=source_cfg["verified_by"],
        verified_at=source_cfg["verified_at"],
        authority_scope=list(policy_cfg.get("authority_scope", [])),
        accepted_document_types=[config["document"]["document_type"]],
    )
    policy = SourcePolicy(
        source_id=source.source_id,
        domains=list(policy_cfg["domains"]),
        trust_tier=TrustTier(policy_cfg["trust_tier"]),
        material_profiles=[MaterialProfile(value) for value in policy_cfg.get("material_profiles", [])],
        trust_basis=list(policy_cfg.get("trust_basis", [])),
        authority_scope=list(policy_cfg.get("authority_scope", [])),
        verification_evidence=list(policy_cfg.get("verification_evidence", [])),
    )
    return source, policy


def main() -> int:
    parser = argparse.ArgumentParser(
        description="FATHER PDn MVP: official 152-FZ acquisition -> exact original -> D4 structure -> D5 chunks"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--root", default=str(REPO_ROOT / "data" / "knowledge_factory" / "pdn_mvp"))
    parser.add_argument("--url", default=None, help="Override official source URL")
    parser.add_argument("--max-chunk-chars", type=int, default=2400)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    live_cfg = config["live_acquisition"]
    source_url = args.url or live_cfg["source_url"]

    store = KnowledgeFactoryStore(args.root)
    source, policy = build_source(config)
    document = load_document(store, config)

    acquisition = AcquisitionService(store).acquire(
        AcquisitionRequest(
            source=source,
            source_policy=policy,
            document=document,
            source_url=source_url,
            file_name=live_cfg["file_name"],
            actor_id="pdn-mvp-osint",
            actor_role=Role.OSINT_EXPERT,
            version_date=live_cfg.get("version_date_observed"),
        )
    )

    if acquisition.version is None:
        print(
            json.dumps(
                {
                    "status": "ACQUISITION_FAILED",
                    "disposition": acquisition.disposition.value,
                    "reason": acquisition.event.reason,
                    "source_url": source_url,
                    "root": str(store.root),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    compiled = DocumentCompiler(store).compile(
        document,
        actor_id="pdn-mvp-curator",
        actor_role=Role.KNOWLEDGE_CURATOR,
        max_chunk_chars=args.max_chunk_chars,
    )

    output = {
        "status": "PASS_D0_D5_PRELIMINARY",
        "document_id": document.document_id,
        "title": document.title,
        "source_url": acquisition.version.source_url,
        "artifact_sha256": acquisition.version.sha256,
        "artifact_bytes": acquisition.version.file_size,
        "mime_type": acquisition.version.mime_type,
        "acquisition_disposition": acquisition.disposition.value,
        "parser_version": compiled.parser_version,
        "structure_nodes": len(compiled.structure_nodes),
        "chunks": len(compiled.chunks),
        "warnings": list(compiled.warnings),
        "manifest": compiled.manifest_path,
        "structure": compiled.structure_path,
        "chunks_file": compiled.chunks_path,
        "extracted_text": compiled.extracted_text_path,
        "semantic_extraction_performed": False,
        "next_stage": "D6 terminology/concepts/definitions/requirements analysis",
        "store_root": str(store.root),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
