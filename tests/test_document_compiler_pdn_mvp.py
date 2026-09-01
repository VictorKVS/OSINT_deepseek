import hashlib
import json

import pytest

from father_osint.acquisition import AcquisitionRequest, AcquisitionService, FetchedArtifact
from father_osint.document_compiler import DocumentCompiler, DocumentCompilerError
from father_osint.knowledge_factory import (
    DocumentRecord,
    OfficialSource,
    PipelineStage,
    Role,
    SourceClass,
    SourceStatus,
    StageState,
)
from father_osint.knowledge_factory_store import KnowledgeFactoryStore
from father_osint.source_policy import MaterialProfile, SourcePolicy, TrustTier


LEGAL_HTML = """
<html><body>
<h1>Федеральный закон О персональных данных</h1>
<h2>Глава 1. Общие положения</h2>
<p>Статья 1. Сфера действия настоящего Федерального закона</p>
<p>1. Настоящим Федеральным законом регулируются отношения, связанные с обработкой персональных данных.</p>
<p>2. Положения настоящего Федерального закона применяются в предусмотренных законом случаях.</p>
<p>Статья 2. Цель настоящего Федерального закона</p>
<p>Целью настоящего Федерального закона является обеспечение защиты прав и свобод человека и гражданина.</p>
<h2>Глава 2. Принципы и условия обработки персональных данных</h2>
<p>Статья 5. Принципы обработки персональных данных</p>
<p>1. Обработка персональных данных должна осуществляться на законной и справедливой основе.</p>
</body></html>
""".encode("utf-8")


class StaticFetcher:
    def __init__(self, data: bytes = LEGAL_HTML):
        self.data = data
        self.calls = 0

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        self.calls += 1
        return FetchedArtifact(data=self.data, mime_type="text/html", final_url=url)


def source_and_policy():
    source = OfficialSource(
        source_id="SRC-RU-PRAVO-001",
        name="Official Internet Portal of Legal Information",
        domain="pravo.gov.ru",
        organization="Official Internet Portal of Legal Information",
        source_class=SourceClass.OFFICIAL,
        trust_basis="Official state legal-information portal",
        status=SourceStatus.VERIFIED,
        verified_by="source-registry-review",
        verified_at="2026-08-22T00:00:00+00:00",
    )
    policy = SourcePolicy(
        source_id=source.source_id,
        domains=["pravo.gov.ru"],
        trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
        material_profiles=[MaterialProfile.LEGAL],
        trust_basis=["official_state_legal_information_portal"],
        authority_scope=["federal_laws"],
        verification_evidence=["portal_states_federal_law_texts_have_official_status"],
    )
    return source, policy


def acquire_to_d3(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = source_and_policy()
    document = DocumentRecord(
        document_id="DOC-RU-FZ-152-2006",
        title="Федеральный закон №152-ФЗ О персональных данных",
        document_type="federal_law",
        jurisdiction="RU",
        topic_tags=["personal_data", "152-fz"],
    )
    response = AcquisitionService(store, fetcher=StaticFetcher()).acquire(
        AcquisitionRequest(
            source=source,
            source_policy=policy,
            document=document,
            source_url="https://ips.pravo.gov.ru/api/ips/legislation/document?example=152-fz",
            file_name="152-fz.html",
            actor_id="osint-test",
            actor_role=Role.OSINT_EXPERT,
            version_date="2025-09-01",
        )
    )
    assert response.version is not None
    assert document.stage_states[PipelineStage.D3_INTEGRITY_METADATA_VERIFIED.value] == StageState.VERIFIED.value
    return store, document, response.version


def test_vertical_official_acquisition_to_preliminary_pdn_chunks(tmp_path):
    store, document, version = acquire_to_d3(tmp_path)

    result = DocumentCompiler(store).compile(document, actor_id="curator-test")

    assert document.stage_states[PipelineStage.D4_STRUCTURE_PARSED.value] == StageState.DONE.value
    assert document.stage_states[PipelineStage.D5_CHUNKED.value] == StageState.DONE.value
    assert result.artifact_sha256 == hashlib.sha256(LEGAL_HTML).hexdigest()
    assert {node.node_type for node in result.structure_nodes} >= {"DOCUMENT", "CHAPTER", "ARTICLE"}
    assert {node.locator for node in result.structure_nodes} >= {"article:1", "article:2", "article:5"}
    assert result.chunks
    assert all(chunk.artifact_sha256 == version.sha256 for chunk in result.chunks)
    assert all(chunk.structure_node_id for chunk in result.chunks)
    assert any("Статья 5" in chunk.text for chunk in result.chunks)

    manifest = json.loads((store.root / result.manifest_path).read_text(encoding="utf-8"))
    assert manifest["semantic_extraction_performed"] is False
    assert manifest["artifact_sha256"] == version.sha256
    assert manifest["structure_nodes"] == len(result.structure_nodes)
    assert manifest["chunks"] == len(result.chunks)


def test_compiler_is_deterministic_for_same_version_and_parser(tmp_path):
    store, document, _ = acquire_to_d3(tmp_path)
    compiler = DocumentCompiler(store)

    first = compiler.compile(document, actor_id="curator-test")
    second = compiler.compile(document, actor_id="curator-test")

    assert [node.node_id for node in first.structure_nodes] == [node.node_id for node in second.structure_nodes]
    assert [chunk.chunk_id for chunk in first.chunks] == [chunk.chunk_id for chunk in second.chunks]


def test_compiler_refuses_to_run_before_d3(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    document = DocumentRecord(title="draft", document_type="federal_law")

    with pytest.raises(DocumentCompilerError, match="D3"):
        DocumentCompiler(store).compile(document, actor_id="curator-test")


def test_compiler_detects_original_integrity_loss(tmp_path):
    store, document, version = acquire_to_d3(tmp_path)
    (store.root / version.local_path).write_bytes(b"tampered")

    with pytest.raises(DocumentCompilerError, match="SHA-256"):
        DocumentCompiler(store).compile(document, actor_id="curator-test")


def test_compiler_blocks_role_without_pipeline_permission(tmp_path):
    store, document, _ = acquire_to_d3(tmp_path)

    with pytest.raises(DocumentCompilerError, match="cannot advance"):
        DocumentCompiler(store).compile(
            document,
            actor_id="viewer-test",
            actor_role=Role.VIEWER,
        )


def test_preliminary_chunking_keeps_semantics_unpromoted(tmp_path):
    store, document, _ = acquire_to_d3(tmp_path)
    result = DocumentCompiler(store).compile(document, actor_id="curator-test")

    assert document.stage_states[PipelineStage.D6_TERMS_EXTRACTED.value] == StageState.NOT_DONE.value
    assert document.stage_states[PipelineStage.D8_REQUIREMENTS_EXTRACTED.value] == StageState.NOT_DONE.value
    manifest = json.loads((store.root / result.manifest_path).read_text(encoding="utf-8"))
    assert manifest["semantic_extraction_performed"] is False
