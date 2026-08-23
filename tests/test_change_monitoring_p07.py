from father_osint.change_monitoring import (
    ChangeDisposition,
    build_bounded_dependency_cone,
    classify_observation,
    synthetic_new_version_sha,
)


def test_unchanged_hash_reuses_existing_objects():
    digest = "a" * 64
    result = classify_observation(
        "DOC-1",
        expected_sha256=digest,
        observed_sha256=digest,
        immutable_local_artifact=True,
    )
    assert result.disposition == ChangeDisposition.UNCHANGED_REUSED
    assert result.changed is False


def test_mutated_immutable_local_artifact_is_not_treated_as_new_version():
    result = classify_observation(
        "DOC-1",
        expected_sha256="a" * 64,
        observed_sha256="b" * 64,
        immutable_local_artifact=True,
    )
    assert result.disposition == ChangeDisposition.IMMUTABLE_INTEGRITY_DRIFT


def test_separate_acquired_bytes_can_be_new_version_candidate():
    prior = "a" * 64
    observed = synthetic_new_version_sha("DOC-1", prior)
    result = classify_observation(
        "DOC-1",
        expected_sha256=prior,
        observed_sha256=observed,
        immutable_local_artifact=False,
    )
    assert result.disposition == ChangeDisposition.NEW_VERSION_CANDIDATE


def test_dependency_cone_rebuilds_only_changed_doc_locally_and_related_cross_scope():
    cone = build_bounded_dependency_cone(
        ["DOC-A"],
        cross_relations=[
            {"document_ids": ["DOC-A", "DOC-B"]},
            {"document_ids": ["DOC-C", "DOC-D"]},
        ],
        conflict_candidates=[{"document_ids": ["DOC-A", "DOC-C"]}],
    )
    assert cone["doc_local_rebuild_document_ids"] == ["DOC-A"]
    assert cone["cross_scope_document_ids"] == ["DOC-A", "DOC-B", "DOC-C"]
    assert cone["full_corpus_rebuild_required"] is False
    assert cone["delta_d14_required"] is True
    assert cone["d15_blocked_until_review"] is True


def test_no_change_has_empty_invalidation_cone():
    cone = build_bounded_dependency_cone([])
    assert cone["doc_local_rebuild_document_ids"] == []
    assert cone["cross_scope_document_ids"] == []
    assert cone["delta_d14_required"] is False
    assert cone["d15_blocked_until_review"] is False
