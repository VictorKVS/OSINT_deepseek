import pytest

from father_osint.knowledge_factory import (
    AuditEvent,
    ClauseRef,
    DocumentRecord,
    DocumentVersion,
    KnowledgeNode,
    KnowledgeRelation,
    OfficialSource,
    Permission,
    PipelineStage,
    Role,
    SourceClass,
    SourceStatus,
    StageState,
    is_allowed,
)
from father_osint.ui_contracts import (
    ThemeMode,
    ViewMode,
    node_to_table_row,
    project_node,
    relation_to_table_row,
    stage_badge,
)


def test_verified_official_source_requires_verification_basis():
    with pytest.raises(ValueError):
        OfficialSource(
            name="Example regulator",
            domain="example.gov",
            organization="Example regulator",
            source_class=SourceClass.OFFICIAL,
            status=SourceStatus.VERIFIED,
        )

    source = OfficialSource(
        name="Example regulator",
        domain="EXAMPLE.GOV",
        organization="Example regulator",
        source_class=SourceClass.OFFICIAL,
        status=SourceStatus.VERIFIED,
        trust_basis="Approved source registry entry",
        verified_by="reviewer-1",
        verified_at="2026-08-21T00:00:00+00:00",
    )
    assert source.domain == "example.gov"
    assert source.status == SourceStatus.VERIFIED


def test_document_stage_cannot_skip_predecessor():
    record = DocumentRecord(title="152-FZ", document_type="federal_law")

    with pytest.raises(ValueError):
        record.set_stage_state(PipelineStage.D3_INTEGRITY_METADATA_VERIFIED, StageState.VERIFIED)

    record.set_stage_state(PipelineStage.D0_SOURCE_DISCOVERED, StageState.DONE)
    record.set_stage_state(PipelineStage.D1_SOURCE_VERIFIED, StageState.VERIFIED)
    record.set_stage_state(PipelineStage.D2_ORIGINAL_ACQUIRED, StageState.DONE)
    record.set_stage_state(PipelineStage.D3_INTEGRITY_METADATA_VERIFIED, StageState.VERIFIED)

    assert record.current_stage == PipelineStage.D3_INTEGRITY_METADATA_VERIFIED


def test_document_versions_are_append_preserving_and_hash_validated():
    record = DocumentRecord(title="152-FZ", document_type="federal_law")
    version = DocumentVersion(
        source_id="source-1",
        source_url="https://example.gov/document",
        sha256="a" * 64,
        local_path="originals/152-fz.pdf",
        file_name="152-fz.pdf",
        file_size=100,
    )

    record.add_version(version)
    record.add_version(version)

    assert len(record.versions) == 1
    assert record.current_version_id == version.version_id

    with pytest.raises(ValueError):
        DocumentVersion(
            source_id="source-1",
            source_url="https://example.gov/document",
            sha256="bad",
            local_path="x",
            file_name="x",
        )


def test_rbac_separates_admin_and_security_admin():
    assert is_allowed(Role.ADMINISTRATOR, Permission.MANAGE_USERS)
    assert not is_allowed(Role.ADMINISTRATOR, Permission.MANAGE_SECURITY)
    assert is_allowed(Role.SECURITY_ADMINISTRATOR, Permission.MANAGE_SECURITY)
    assert not is_allowed(Role.SECURITY_ADMINISTRATOR, Permission.MANAGE_USERS)
    assert is_allowed(Role.SYSTEM_OWNER, Permission.PUBLISH_KB)


def test_audit_event_requires_action_identity():
    event = AuditEvent(
        actor_id="agent-1",
        actor_role=Role.OSINT_EXPERT.value,
        action="DOWNLOAD_DOCUMENT",
        object_type="DOCUMENT",
        object_id="doc-1",
        result="SUCCESS",
    )
    assert event.action == "DOWNLOAD_DOCUMENT"

    with pytest.raises(ValueError):
        AuditEvent(
            actor_id="",
            actor_role=Role.OSINT_EXPERT.value,
            action="DOWNLOAD_DOCUMENT",
            object_type="DOCUMENT",
            object_id="doc-1",
            result="SUCCESS",
        )


def test_graph_and_table_are_projections_of_same_node_relation_model():
    refs = [
        ClauseRef(document_id="doc-152", locator="art. 3"),
        ClauseRef(document_id="doc-1119", locator="p. 2"),
    ]
    node = KnowledgeNode(node_type="TERM", label="operator", document_refs=refs)
    other = KnowledgeNode(node_type="REQUIREMENT", label="protect personal data")
    relation = KnowledgeRelation(
        from_node_id=node.node_id,
        to_node_id=other.node_id,
        relation_type="APPLIES_TO",
        evidence_refs=refs,
        rationale="The cited clauses establish the relation",
        method_ref="relation-method-v1",
        reviewer="reviewer-1",
    )

    graph_node = project_node(node)
    table_node = node_to_table_row(node)
    table_relation = relation_to_table_row(relation)

    assert graph_node.document_count == 2
    assert graph_node.color_token == "violet"
    assert table_node.document_ids == ["doc-1119", "doc-152"]
    assert table_relation.evidence_clauses == ["art. 3", "p. 2"]
    assert table_relation.method_ref == "relation-method-v1"


def test_ui_contract_reserves_day_night_and_parallel_views():
    assert {item.value for item in ThemeMode} == {"DAY", "NIGHT", "SYSTEM"}
    assert {item.value for item in ViewMode} == {"GRAPH", "TABLE", "DOCUMENT_LIST"}
    badge = stage_badge(PipelineStage.D6_TERMS_EXTRACTED, StageState.IN_PROGRESS)
    assert badge["color_token"] == "yellow"
