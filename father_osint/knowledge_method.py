from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .knowledge_quality import CompetencyQuestionOutcome


class KnowledgeObjectType(str, Enum):
    TERM_MENTION = "TERM_MENTION"
    CONCEPT = "CONCEPT"
    DEFINITION = "DEFINITION"
    ENTITY = "ENTITY"
    FACT = "FACT"
    REQUIREMENT = "REQUIREMENT"
    RULE = "RULE"
    CLAIM = "CLAIM"
    HYPOTHESIS = "HYPOTHESIS"
    OPINION = "OPINION"
    METHOD = "METHOD"
    CONTROL = "CONTROL"
    GAP = "GAP"
    CONFLICT_CANDIDATE = "CONFLICT_CANDIDATE"
    REVIEW_DECISION = "REVIEW_DECISION"


@dataclass(frozen=True, slots=True)
class CompetencyQuestion:
    question: str
    expected_answer_types: tuple[KnowledgeObjectType, ...]
    cq_id: str = field(default_factory=lambda: f"CQ-{uuid4()}")
    minimum_evidence_types: tuple[str, ...] = ()
    required_relation_types: tuple[str, ...] = ()
    allowed_outcomes: tuple[CompetencyQuestionOutcome, ...] = (
        CompetencyQuestionOutcome.ANSWERED_TRACEABLE,
        CompetencyQuestionOutcome.ANSWERED_WITH_LIMITATIONS,
        CompetencyQuestionOutcome.INCONCLUSIVE,
        CompetencyQuestionOutcome.GAP,
        CompetencyQuestionOutcome.NOT_APPLICABLE,
    )
    forbidden_shortcuts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.cq_id.startswith("CQ-"):
            raise ValueError("competency question id must start with CQ-")
        if not self.question.strip():
            raise ValueError("competency question text is required")
        if not self.expected_answer_types:
            raise ValueError("competency question requires at least one expected answer type")
        if not self.allowed_outcomes:
            raise ValueError("competency question requires allowed outcomes")

    def to_dict(self) -> dict[str, Any]:
        return {
            "cq_id": self.cq_id,
            "question": self.question,
            "expected_answer_types": [value.value for value in self.expected_answer_types],
            "minimum_evidence_types": list(self.minimum_evidence_types),
            "required_relation_types": list(self.required_relation_types),
            "allowed_outcomes": [value.value for value in self.allowed_outcomes],
            "forbidden_shortcuts": list(self.forbidden_shortcuts),
        }


@dataclass(frozen=True, slots=True)
class KnowledgeScope:
    domain: str
    material_profiles: tuple[str, ...]
    competency_questions: tuple[CompetencyQuestion, ...]
    intended_uses: tuple[str, ...]
    review_authority: str
    scope_id: str = field(default_factory=lambda: f"KS-{uuid4()}")
    out_of_scope_questions: tuple[str, ...] = ()
    required_source_classes: tuple[str, ...] = ()
    vocabularies_to_check: tuple[str, ...] = ()
    forbidden_implicit_casts: tuple[str, ...] = (
        "HYPOTHESIS->FACT",
        "CLAIM->FACT",
        "OPINION->FACT",
    )
    freshness_policy: str | None = None
    method_version: str = "knowledge-engineering-v1"

    def __post_init__(self) -> None:
        if not self.scope_id.startswith("KS-"):
            raise ValueError("knowledge scope id must start with KS-")
        if not self.domain.strip():
            raise ValueError("knowledge scope domain is required")
        if not self.material_profiles:
            raise ValueError("knowledge scope requires at least one material profile")
        if not self.intended_uses:
            raise ValueError("knowledge scope requires at least one intended use")
        if not self.review_authority.strip():
            raise ValueError("knowledge scope review authority is required")
        if not self.method_version.strip():
            raise ValueError("knowledge scope method_version is required")

        cq_ids = [item.cq_id for item in self.competency_questions]
        if len(set(cq_ids)) != len(cq_ids):
            raise ValueError("competency question ids must be unique within a scope")

    @property
    def semantic_entry_ready(self) -> bool:
        return bool(self.competency_questions)

    def require_semantic_entry_ready(self) -> None:
        if not self.competency_questions:
            raise ValueError("D6+ semantic processing requires at least one competency question")

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "domain": self.domain,
            "material_profiles": list(self.material_profiles),
            "competency_questions": [item.to_dict() for item in self.competency_questions],
            "intended_uses": list(self.intended_uses),
            "review_authority": self.review_authority,
            "out_of_scope_questions": list(self.out_of_scope_questions),
            "required_source_classes": list(self.required_source_classes),
            "vocabularies_to_check": list(self.vocabularies_to_check),
            "forbidden_implicit_casts": list(self.forbidden_implicit_casts),
            "freshness_policy": self.freshness_policy,
            "method_version": self.method_version,
        }


@dataclass(frozen=True, slots=True)
class CompetencyQuestionResult:
    cq_id: str
    outcome: CompetencyQuestionOutcome
    answer_object_ids: tuple[str, ...] = ()
    evidence_object_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.cq_id.startswith("CQ-"):
            raise ValueError("competency question result requires CQ-* id")
        if self.outcome == CompetencyQuestionOutcome.ANSWERED_TRACEABLE:
            if not self.answer_object_ids or not self.evidence_object_ids:
                raise ValueError("ANSWERED_TRACEABLE requires answer and evidence object ids")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["outcome"] = self.outcome.value
        return data
