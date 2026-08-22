import pytest

from father_osint.knowledge_quality import (
    CompetencyQuestionCounts,
    ConfusionCounts,
    ConstraintCounts,
    CoverageCounts,
    KnowledgeQualitySnapshot,
    MetricProvenance,
    ReuseCounts,
    safe_ratio,
)


def metric_provenance() -> MetricProvenance:
    return MetricProvenance(
        metric_id="KF-METRIC-SET-1",
        metric_version="1.0",
        run_id="run-1",
        corpus_id="corpus-1",
        method_version="extractor-v1",
        timestamp="2026-08-22T12:00:00+00:00",
        gold_set_id="gold-1",
        review_policy_version="review-v1",
    )


def test_precision_recall_f1_are_computed_from_explicit_confusion_counts():
    counts = ConfusionCounts(true_positive=8, false_positive=2, false_negative=4)

    assert counts.precision == pytest.approx(0.8)
    assert counts.recall == pytest.approx(8 / 12)
    assert counts.f1 == pytest.approx(2 * 0.8 * (8 / 12) / (0.8 + (8 / 12)))


def test_undefined_metric_is_not_silently_converted_to_zero_or_one():
    assert safe_ratio(0, 0) is None
    counts = ConfusionCounts()
    assert counts.precision is None
    assert counts.recall is None
    assert counts.f1 is None


def test_coverage_rejects_impossible_counts():
    with pytest.raises(ValueError):
        CoverageCounts(covered=2, total=1)

    assert CoverageCounts(covered=3, total=4).ratio == pytest.approx(0.75)


def test_competency_question_metrics_exclude_not_applicable_from_denominator():
    counts = CompetencyQuestionCounts(
        answered_traceable=3,
        answered_with_limitations=1,
        inconclusive=1,
        gap=1,
        not_applicable=4,
    )

    assert counts.applicable == 6
    assert counts.traceable_rate == pytest.approx(0.5)
    assert counts.coverage_rate == pytest.approx(4 / 6)
    assert counts.gap_rate == pytest.approx(1 / 6)


def test_reuse_and_rework_metrics_remain_separate_dimensions():
    counts = ReuseCounts(
        reused_verified_objects=8,
        newly_created_objects=2,
        reprocessed_objects=3,
        processed_objects=20,
    )

    assert counts.reuse_ratio == pytest.approx(0.8)
    assert counts.rework_ratio == pytest.approx(0.15)


def test_constraint_conformance_is_explicit_and_validated():
    counts = ConstraintCounts(objects_validated=20, objects_conformant=19, violations_total=2)
    assert counts.conformance == pytest.approx(0.95)

    with pytest.raises(ValueError):
        ConstraintCounts(objects_validated=2, objects_conformant=3)


def test_quality_snapshot_has_no_composite_truth_or_quality_score():
    snapshot = KnowledgeQualitySnapshot(
        provenance=metric_provenance(),
        lineage_coverage=CoverageCounts(10, 10),
        locator_coverage=CoverageCounts(9, 10),
        constraint_counts=ConstraintCounts(10, 10, 0),
        competency_questions=CompetencyQuestionCounts(answered_traceable=2, gap=1),
        reuse=ReuseCounts(reused_verified_objects=4, newly_created_objects=1),
        extraction=ConfusionCounts(true_positive=9, false_positive=1, false_negative=2),
    )

    payload = snapshot.to_dict()

    assert "quality_score" not in payload
    assert "truth_probability" not in payload
    assert payload["lineage_coverage"]["ratio"] == 1.0
    assert payload["constraint_counts"]["conformance"] == 1.0
    assert payload["extraction"]["precision"] == pytest.approx(0.9)


def test_metric_provenance_requires_run_corpus_method_and_version_identity():
    with pytest.raises(ValueError):
        MetricProvenance(
            metric_id="",
            metric_version="1",
            run_id="run",
            corpus_id="corpus",
            method_version="method",
            timestamp="2026-08-22T12:00:00+00:00",
        )
