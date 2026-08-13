from __future__ import annotations

from datetime import datetime, timezone

import pytest

from father_osint.evidence_quality import DeterministicEvidenceQualityAssessor
from father_osint.models import Material, MaterialPackage


def _material(*, locator: str, text: str, content_hash: str, source_class: str | None = None) -> Material:
    metadata = {"transport": "telethon", "chat_id": "100", "message_id": locator.rsplit("/", 1)[-1]}
    if source_class:
        metadata["source_class"] = source_class
    return Material(
        source_type="telegram",
        source_locator=locator,
        title="source",
        raw_text=text,
        published_at="2026-08-10T12:00:00+00:00",
        metadata=metadata,
        content_hash=content_hash,
    )


def test_g7_keeps_all_quality_dimensions_separate_and_forbids_truth_probability() -> None:
    material = _material(
        locator="telegram://100/1",
        text="Telegram evidence quality test",
        content_hash="a" * 64,
        source_class="primary",
    )
    package = MaterialPackage(task_id="task-1", materials=[material])

    result = DeterministicEvidenceQualityAssessor().assess_package(
        package,
        relevant_terms=["telegram", "evidence"],
        reference_time=datetime(2026, 8, 13, tzinfo=timezone.utc),
        case_id="case-1",
    )

    assessment = result.assessments[0]
    assert [dimension.name for dimension in assessment.dimensions] == [
        "reliability",
        "relevance",
        "independence",
        "recency",
        "directness",
        "corroboration",
        "provenance_quality",
    ]
    assert assessment.reliability.state == "UNKNOWN"
    assert assessment.relevance.state == "HIGH"
    assert assessment.directness.state == "HIGH"
    assert assessment.provenance_quality.state == "HIGH"
    with pytest.raises(RuntimeError, match="uncalibrated aggregate truth probability"):
        assessment.aggregate_truth_probability()


def test_g7_repeated_payload_is_not_independent_corroboration() -> None:
    first = _material(
        locator="telegram://100/1",
        text="same observation",
        content_hash="b" * 64,
    )
    second = _material(
        locator="telegram://200/2",
        text="same observation",
        content_hash="b" * 64,
    )
    package = MaterialPackage(task_id="task-2", materials=[first, second], payloads_reused=1)

    result = DeterministicEvidenceQualityAssessor().assess_package(package, case_id="case-2")

    assert all(item.independence.state == "LOW" for item in result.assessments)
    assert all(item.corroboration.state == "LOW" for item in result.assessments)
    assert all("not independent corroboration" in item.corroboration.rationale for item in result.assessments)


def test_g7_source_or_platform_label_does_not_auto_promote_reliability() -> None:
    material = _material(
        locator="telegram://100/3",
        text="official source statement",
        content_hash="c" * 64,
        source_class="primary",
    )
    material.author = "Official Channel"
    package = MaterialPackage(task_id="task-3", materials=[material])

    assessment = DeterministicEvidenceQualityAssessor().assess_package(package).assessments[0]

    assert assessment.reliability.state == "UNKNOWN"
    assert "source-history" in assessment.reliability.rationale.lower()


def test_g7_missing_research_context_keeps_relevance_unknown() -> None:
    material = _material(
        locator="telegram://100/4",
        text="unrelated words",
        content_hash="d" * 64,
    )
    package = MaterialPackage(task_id="task-4", materials=[material])

    assessment = DeterministicEvidenceQualityAssessor().assess_package(package).assessments[0]

    assert assessment.relevance.state == "UNKNOWN"


def test_g7_decision_record_preserves_method_and_knowledge_lineage() -> None:
    material = _material(
        locator="telegram://100/5",
        text="lineage",
        content_hash="e" * 64,
    )
    package = MaterialPackage(task_id="task-5", materials=[material])

    result = DeterministicEvidenceQualityAssessor().assess_package(package, case_id="case-5")

    decision = result.decision_record
    assert decision.case_id == "case-5"
    assert decision.role_id == "OSINT_EXPERT"
    assert "information-evidence-standard.v1" in decision.knowledge_refs
    assert "g7.no-uncalibrated-truth-score" in decision.method_refs
    assert result.assessments[0].assessment_id in decision.output_refs
