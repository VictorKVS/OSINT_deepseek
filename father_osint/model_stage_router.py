from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class ModelCandidate:
    model_id: str
    capability: str
    quality_score: float
    eligible: bool = True
    role: str = "CHALLENGER"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StagePolicy:
    stage_id: str
    capability: str
    semantic: bool = True
    canary_fraction: float = 0.0
    human_review_on_close_margin: bool = False
    close_margin: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.canary_fraction <= 1.0:
            raise ValueError("canary_fraction must be in [0, 1]")
        if self.close_margin < 0:
            raise ValueError("close_margin must be non-negative")


@dataclass(slots=True)
class StageDecision:
    stage_id: str
    champion: ModelCandidate | None
    challengers: list[ModelCandidate]
    human_review_required: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "champion": self.champion.to_dict() if self.champion else None,
            "challengers": [item.to_dict() for item in self.challengers],
            "human_review_required": self.human_review_required,
            "reason": self.reason,
        }


class ModelStageRouter:
    """Deterministic control plane for semantic model stages.

    The router never evaluates semantic truth itself. It only selects eligible
    candidates by capability/quality metadata and decides reproducible canary
    participation. Evidence and promotion gates remain outside the model output.
    """

    def decide(
        self,
        *,
        policy: StagePolicy,
        candidates: Iterable[ModelCandidate],
        work_item_id: str,
        max_challengers: int = 1,
    ) -> StageDecision:
        if not policy.semantic:
            return StageDecision(
                stage_id=policy.stage_id,
                champion=None,
                challengers=[],
                human_review_required=False,
                reason="DETERMINISTIC_STAGE",
            )

        suitable = [
            item
            for item in candidates
            if item.eligible and item.capability == policy.capability
        ]
        suitable.sort(key=lambda item: (item.quality_score, item.model_id), reverse=True)

        if not suitable:
            return StageDecision(
                stage_id=policy.stage_id,
                champion=None,
                challengers=[],
                human_review_required=True,
                reason="NO_ELIGIBLE_MODEL",
            )

        champion = suitable[0]
        challengers: list[ModelCandidate] = []
        if (
            max_challengers > 0
            and len(suitable) > 1
            and self._is_canary(work_item_id, policy.stage_id, policy.canary_fraction)
        ):
            challengers = suitable[1 : 1 + max_challengers]

        review = False
        reason = "CHAMPION_SELECTED"
        if policy.human_review_on_close_margin and len(suitable) > 1:
            margin = champion.quality_score - suitable[1].quality_score
            if margin < policy.close_margin:
                review = True
                reason = "CLOSE_MARGIN_HUMAN_REVIEW"

        return StageDecision(
            stage_id=policy.stage_id,
            champion=champion,
            challengers=challengers,
            human_review_required=review,
            reason=reason,
        )

    @staticmethod
    def _is_canary(work_item_id: str, stage_id: str, fraction: float) -> bool:
        if fraction <= 0.0:
            return False
        if fraction >= 1.0:
            return True
        digest = hashlib.sha256(f"{stage_id}\x1f{work_item_id}".encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:8], "big") / float(2**64 - 1)
        return bucket < fraction
