import hashlib

from father_osint.acquisition import (
    AcquisitionDisposition,
    AcquisitionError,
    AcquisitionRequest,
    AcquisitionService,
    FetchedArtifact,
)
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


class SequenceFetcher:
    def __init__(self, items):
        self.items = list(items)
        self.calls = []

    def fetch(self, url, *, timeout_seconds, max_bytes):
        self.calls.append((url, timeout_seconds, max_bytes))
        item = self.items[min(len(self.calls) - 1, len(self.items) - 1)]
        if isinstance(item, Exception):
            raise item
        return item


def verified_source_and_policy(domain="example.gov"):
    source_id = "SRC-TEST-001"
    source = OfficialSource(
        name="Example regulator",
        domain=domain,
        organization="Example regulator",
        source_class=SourceClass.OFFICIAL,
        status=SourceStatus.VERIFIED,
        trust_basis="approved source registry",
        verified_by="reviewer-1",
        verified_at="2026-08-22T00:00:00+00:00",
        source_id=source_id,
    )
    policy = SourcePolicy(
        source_id=source_id,
        domains=[domain],
        trust_tier=TrustTier.A0_OFFICIAL_PUBLICATION,
        material_profiles=[MaterialProfile.LEGAL],
        trust_basis=["official publication channel"],
        verification_evidence=["reviewed evidence"],
    )
    return source, policy


def request_for(source, policy, document, *, actor_role=Role.OSINT_EXPERT, url=None):
    return AcquisitionRequest(
        source=source,
        source_policy=policy,
        document=document,
        source_url=url or f"https://{policy.domains[0]}/document.pdf",
        file_name="document.pdf",
        actor_id="agent-1",
        actor_role=actor_role,
        timeout_seconds=5,
        max_bytes=1024 * 1024,
        publication_date="2026-08-22",
        version_date="2026-08-22",
    )


def test_basic_exact_acquisition_preserves_bytes_hash_version_and_audit(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Test act", document_type="legal_act")
    payload = b"%PDF-1.7\nexact-test-bytes"
    fetcher = SequenceFetcher(
        [FetchedArtifact(payload, mime_type="application/pdf", final_url="https://example.gov/document.pdf")]
    )
    service = AcquisitionService(store, fetcher)

    response = service.acquire(request_for(source, policy, document))

    digest = hashlib.sha256(payload).hexdigest()
    assert response.disposition == AcquisitionDisposition.CREATED
    assert response.version is not None
    assert response.version.sha256 == digest
    assert response.version.file_size == len(payload)
    assert response.version.mime_type == "application/pdf"
    assert document.stage_states[PipelineStage.D0_SOURCE_DISCOVERED.value] == StageState.DONE.value
    assert document.stage_states[PipelineStage.D1_SOURCE_VERIFIED.value] == StageState.VERIFIED.value
    assert document.stage_states[PipelineStage.D2_ORIGINAL_ACQUIRED.value] == StageState.DONE.value
    assert document.stage_states[PipelineStage.D3_INTEGRITY_METADATA_VERIFIED.value] == StageState.VERIFIED.value

    original_path = tmp_path / response.version.local_path
    assert original_path.read_bytes() == payload
    assert original_path.name == f"{digest}.bin"
    assert len(store.list_acquisitions()) == 1
    assert len(store.list_audit()) == 1
    assert store.get_source(source.source_id) is not None
    assert store.get_document(document.document_id) is not None
    assert store.acquisition_counters() == {
        "attempts": 1,
        "successes": 1,
        "failures": 0,
        "blocked": 0,
        "bytes_acquired": len(payload),
        "artifacts_reused": 0,
        "versions_created": 1,
    }


def test_repeated_unchanged_acquisition_reuses_artifact_and_version_but_keeps_observation(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Test act", document_type="legal_act")
    payload = b"same exact bytes"
    artifact = FetchedArtifact(payload, mime_type="application/pdf", final_url="https://example.gov/document.pdf")
    service = AcquisitionService(store, SequenceFetcher([artifact, artifact]))
    request = request_for(source, policy, document)

    first = service.acquire(request)
    second = service.acquire(request)

    assert first.disposition == AcquisitionDisposition.CREATED
    assert second.disposition == AcquisitionDisposition.REUSED
    assert len(document.versions) == 1
    assert len(store.list_acquisitions()) == 2
    assert len(store.list_audit()) == 2
    assert store.list_acquisitions()[1]["artifact_reused"] is True
    counters = store.acquisition_counters()
    assert counters["attempts"] == 2
    assert counters["successes"] == 2
    assert counters["artifacts_reused"] == 1
    assert counters["versions_created"] == 1


def test_changed_bytes_create_new_version_without_overwriting_old_original(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Versioned act", document_type="legal_act")
    first_payload = b"version-one"
    second_payload = b"version-two"
    fetcher = SequenceFetcher(
        [
            FetchedArtifact(first_payload, "application/pdf", "https://example.gov/document.pdf"),
            FetchedArtifact(second_payload, "application/pdf", "https://example.gov/document.pdf"),
        ]
    )
    service = AcquisitionService(store, fetcher)
    request = request_for(source, policy, document)

    first = service.acquire(request)
    second = service.acquire(request)

    assert first.disposition == AcquisitionDisposition.CREATED
    assert second.disposition == AcquisitionDisposition.NEW_VERSION
    assert len(document.versions) == 2
    assert document.current_version_id == second.version.version_id
    assert (tmp_path / first.version.local_path).read_bytes() == first_payload
    assert (tmp_path / second.version.local_path).read_bytes() == second_payload
    assert first.version.sha256 != second.version.sha256


def test_unverified_source_is_blocked_before_fetch_and_cannot_reach_d2(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    source.status = SourceStatus.CANDIDATE
    document = DocumentRecord(title="Blocked act", document_type="legal_act")
    fetcher = SequenceFetcher([FetchedArtifact(b"should-not-fetch", "application/pdf")])
    service = AcquisitionService(store, fetcher)

    response = service.acquire(request_for(source, policy, document))

    assert response.disposition == AcquisitionDisposition.BLOCKED
    assert fetcher.calls == []
    assert document.stage_states[PipelineStage.D0_SOURCE_DISCOVERED.value] == StageState.DONE.value
    assert document.stage_states[PipelineStage.D1_SOURCE_VERIFIED.value] == StageState.BLOCKED.value
    assert document.stage_states[PipelineStage.D2_ORIGINAL_ACQUIRED.value] == StageState.NOT_DONE.value
    assert store.acquisition_counters()["blocked"] == 1


def test_off_policy_host_is_blocked_without_network_call(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Blocked mirror", document_type="legal_act")
    fetcher = SequenceFetcher([FetchedArtifact(b"mirror", "application/pdf")])
    service = AcquisitionService(store, fetcher)

    response = service.acquire(
        request_for(source, policy, document, url="https://untrusted.example/document.pdf")
    )

    assert response.disposition == AcquisitionDisposition.BLOCKED
    assert fetcher.calls == []
    assert len(document.versions) == 0


def test_redirect_outside_policy_fails_after_fetch_without_promoting_bytes(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Redirected act", document_type="legal_act")
    fetcher = SequenceFetcher(
        [FetchedArtifact(b"bytes", "application/pdf", "https://evil.example/document.pdf")]
    )
    service = AcquisitionService(store, fetcher)

    response = service.acquire(request_for(source, policy, document))

    assert response.disposition == AcquisitionDisposition.FAILED
    assert document.stage_states[PipelineStage.D2_ORIGINAL_ACQUIRED.value] == StageState.FAILED.value
    assert document.stage_states[PipelineStage.D3_INTEGRITY_METADATA_VERIFIED.value] == StageState.NOT_DONE.value
    assert list(store.originals_dir.iterdir()) == []


def test_fetch_failure_is_explicit_and_does_not_create_false_version(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Unavailable act", document_type="legal_act")
    fetcher = SequenceFetcher([AcquisitionError("timeout")])
    service = AcquisitionService(store, fetcher)

    response = service.acquire(request_for(source, policy, document))

    assert response.disposition == AcquisitionDisposition.FAILED
    assert len(document.versions) == 0
    assert document.stage_states[PipelineStage.D1_SOURCE_VERIFIED.value] == StageState.VERIFIED.value
    assert document.stage_states[PipelineStage.D2_ORIGINAL_ACQUIRED.value] == StageState.FAILED.value
    assert store.acquisition_counters()["failures"] == 1


def test_role_without_acquisition_permission_is_blocked_without_mutating_pipeline(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="RBAC act", document_type="legal_act")
    fetcher = SequenceFetcher([FetchedArtifact(b"should-not-fetch", "application/pdf")])
    service = AcquisitionService(store, fetcher)

    response = service.acquire(
        request_for(source, policy, document, actor_role=Role.ANALYST)
    )

    assert response.disposition == AcquisitionDisposition.BLOCKED
    assert fetcher.calls == []
    assert all(state == StageState.NOT_DONE.value for state in document.stage_states.values())
    assert store.acquisition_counters()["blocked"] == 1


def test_existing_content_addressed_blob_is_verified_before_reuse(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    source, policy = verified_source_and_policy()
    document = DocumentRecord(title="Corruption check", document_type="legal_act")
    payload = b"expected-bytes"
    digest = hashlib.sha256(payload).hexdigest()
    corrupt_path = store.originals_dir / f"{digest}.bin"
    corrupt_path.write_bytes(b"corrupt")
    service = AcquisitionService(
        store,
        SequenceFetcher([FetchedArtifact(payload, "application/pdf", "https://example.gov/document.pdf")]),
    )

    response = service.acquire(request_for(source, policy, document))

    assert response.disposition == AcquisitionDisposition.FAILED
    assert corrupt_path.read_bytes() == b"corrupt"
    assert len(document.versions) == 0
    assert document.stage_states[PipelineStage.D3_INTEGRITY_METADATA_VERIFIED.value] == StageState.NOT_DONE.value
