import pytest

from father_osint.knowledge_factory import (
    AuditEvent,
    DocumentRecord,
    OfficialSource,
    SourceClass,
    SourceStatus,
)
from father_osint.knowledge_factory_store import KnowledgeFactoryStore


def test_store_upserts_registry_records_and_appends_audit(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source = OfficialSource(
        name="Example regulator",
        domain="example.gov",
        organization="Example regulator",
        source_class=SourceClass.OFFICIAL,
        status=SourceStatus.CANDIDATE,
    )
    store.save_source(source)
    source.trust_basis = "approved registry"
    source.status = SourceStatus.VERIFIED
    source.verified_by = "reviewer-1"
    source.verified_at = "2026-08-21T00:00:00+00:00"
    store.save_source(source)

    document = DocumentRecord(title="152-FZ", document_type="federal_law")
    store.save_document(document)
    document.topic_tags.append("personal-data")
    store.save_document(document)

    store.append_audit(
        AuditEvent(
            actor_id="reviewer-1",
            actor_role="REVIEWER",
            action="VERIFY_SOURCE",
            object_type="SOURCE",
            object_id=source.source_id,
            result="SUCCESS",
        )
    )
    store.append_audit(
        AuditEvent(
            actor_id="agent-1",
            actor_role="OSINT_EXPERT",
            action="REGISTER_DOCUMENT",
            object_type="DOCUMENT",
            object_id=document.document_id,
            result="SUCCESS",
        )
    )

    assert len(store.list_sources()) == 1
    assert store.get_source(source.source_id)["status"] == SourceStatus.VERIFIED.value
    assert len(store.list_documents()) == 1
    assert store.get_document(document.document_id)["topic_tags"] == ["personal-data"]
    assert len(store.list_audit()) == 2


def test_store_creates_originals_boundary(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    assert store.originals_dir.exists()
    assert store.originals_dir.parent == tmp_path


def test_store_batch_rejects_duplicate_ids_without_mutating_registry(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    original = DocumentRecord(title="Original", document_type="federal_law")
    store.save_document(original)

    changed = DocumentRecord(
        title="Changed",
        document_type="federal_law",
        document_id=original.document_id,
    )
    conflicting = DocumentRecord(
        title="Conflicting",
        document_type="federal_law",
        document_id=original.document_id,
    )

    with pytest.raises(ValueError, match="duplicate document_id in batch"):
        store.save_documents((changed, conflicting))

    stored = store.get_document(original.document_id)
    assert stored is not None
    assert stored["title"] == "Original"


def test_store_batch_upserts_multiple_documents_in_one_transition(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    first = DocumentRecord(title="First", document_type="federal_law")
    second = DocumentRecord(title="Second", document_type="regulation")

    store.save_documents((first, second))
    first.topic_tags.append("updated")
    second.topic_tags.append("updated")
    store.save_documents((first, second))

    assert store.get_document(first.document_id)["topic_tags"] == ["updated"]
    assert store.get_document(second.document_id)["topic_tags"] == ["updated"]
