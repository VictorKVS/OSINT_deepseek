from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


def safe_ratio(numerator: int | float, denominator: int | float) -> float | None:
    """Return a ratio or None when it is mathematically undefined.

    Knowledge Factory metrics deliberately preserve undefined states instead of
    converting missing denominators into misleading zero/one scores.
    """

    if denominator < 0 or numerator < 0:
        raise ValueError("metric counts must be >= 0")
    if denominator == 0:
        return None
    return float(numerator) / float(denominator)


@dataclass(frozen=True, slots=True)
class ConfusionCounts:
    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0

    def __post_init__(self) -> None:
        if min(self.true_positive, self.false_positive, self.false_negative) < 0:
            raise ValueError("confusion counts must be >= 0")

    @property
    def precision(self) -> float | None:
        return safe_ratio(self.true_positive, self.true_positive + self.false_positive)

    @property
    def recall(self) -> float | None:
        return safe_ratio(self.true_positive, self.true_positive + self.false_negative)

    @property
    def f1(self) -> float | None:
        precision = self.precision
        recall = self.recall
        if precision is None or recall is None or precision + recall == 0:
            return None if precision is None or recall is None else 0.0
        return 2.0 * precision * recall / (precision + recall)

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
        }


@dataclass(frozen=True, slots=True)
class CoverageCounts:
    covered: int
    total: int

    def __post_init__(self) -> None:
        if self.covered < 0 or self.total < 0:
            raise ValueError("coverage counts must be >= 0")
        if self.covered > self.total:
            raise ValueError("covered cannot exceed total")

    @property
    def ratio(self) -> float | None:
        return safe_ratio(self.covered, self.total)


class CompetencyQuestionOutcome(str, Enum):
    ANSWERED_TRACEABLE = "ANSWERED_TRACEABLE"
    ANSWERED_WITH_LIMITATIONS = "ANSWERED_WITH_LIMITATIONS"
    INCONCLUSIVE = "INCONCLUSIVE"
    GAP = "GAP"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class CompetencyQuestionCounts:
    answered_traceable: int = 0
    answered_with_limitations: int = 0
    inconclusive: int = 0
    gap: int = 0
    not_applicable: int = 0

    def __post_init__(self) -> None:
        values = asdict(self).values()
        if any(value < 0 for value in values):
            raise ValueError("competency-question counts must be >= 0")

    @property
    def applicable(self) -> int:
        return (
            self.answered_traceable
            + self.answered_with_limitations
            + self.inconclusive
            + self.gap
        )

    @property
    def traceable_rate(self) -> float | None:
        return safe_ratio(self.answered_traceable, self.applicable)

    @property
    def coverage_rate(self) -> float | None:
        return safe_ratio(
            self.answered_traceable + self.answered_with_limitations,
            self.applicable,
        )

    @property
    def gap_rate(self) -> float | None:
        return safe_ratio(self.gap, self.applicable)


@dataclass(frozen=True, slots=True)
class ReuseCounts:
    reused_verified_objects: int = 0
    newly_created_objects: int = 0
    reprocessed_objects: int = 0
    processed_objects: int = 0

    def __post_init__(self) -> None:
        values = asdict(self).values()
        if any(value < 0 for value in values):
            raise ValueError("reuse counts must be >= 0")
        if self.reprocessed_objects > self.processed_objects:
            raise ValueError("reprocessed_objects cannot exceed processed_objects")

    @property
    def reuse_ratio(self) -> float | None:
        return safe_ratio(
            self.reused_verified_objects,
            self.reused_verified_objects + self.newly_created_objects,
        )

    @property
    def rework_ratio(self) -> float | None:
        return safe_ratio(self.reprocessed_objects, self.processed_objects)


@dataclass(frozen=True, slots=True)
class ConstraintCounts:
    objects_validated: int = 0
    objects_conformant: int = 0
    violations_total: int = 0

    def __post_init__(self) -> None:
        if min(self.objects_validated, self.objects_conformant, self.violations_total) < 0:
            raise ValueError("constraint counts must be >= 0")
        if self.objects_conformant > self.objects_validated:
            raise ValueError("objects_conformant cannot exceed objects_validated")

    @property
    def conformance(self) -> float | None:
        return safe_ratio(self.objects_conformant, self.objects_validated)


@dataclass(frozen=True, slots=True)
class MetricProvenance:
    metric_id: str
    metric_version: str
    run_id: str
    corpus_id: str
    method_version: str
    timestamp: str
    gold_set_id: str | None = None
    review_policy_version: str | None = None

    def __post_init__(self) -> None:
        required = (
            self.metric_id,
            self.metric_version,
            self.run_id,
            self.corpus_id,
            self.method_version,
            self.timestamp,
        )
        if any(not value.strip() for value in required):
            raise ValueError("metric provenance identity fields are required")


@dataclass(frozen=True, slots=True)
class KnowledgeQualitySnapshot:
    """Multidimensional snapshot; intentionally has no composite quality score."""

    provenance: MetricProvenance
    lineage_coverage: CoverageCounts
    locator_coverage: CoverageCounts
    constraint_counts: ConstraintCounts
    competency_questions: CompetencyQuestionCounts
    reuse: ReuseCounts
    extraction: ConfusionCounts | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance": asdict(self.provenance),
            "lineage_coverage": {
                **asdict(self.lineage_coverage),
                "ratio": self.lineage_coverage.ratio,
            },
            "locator_coverage": {
                **asdict(self.locator_coverage),
                "ratio": self.locator_coverage.ratio,
            },
            "constraint_counts": {
                **asdict(self.constraint_counts),
                "conformance": self.constraint_counts.conformance,
            },
            "competency_questions": {
                **asdict(self.competency_questions),
                "applicable": self.competency_questions.applicable,
                "traceable_rate": self.competency_questions.traceable_rate,
                "coverage_rate": self.competency_questions.coverage_rate,
                "gap_rate": self.competency_questions.gap_rate,
            },
            "reuse": {
                **asdict(self.reuse),
                "reuse_ratio": self.reuse.reuse_ratio,
                "rework_ratio": self.reuse.rework_ratio,
            },
            "extraction": self.extraction.to_dict() if self.extraction else None,
        }
