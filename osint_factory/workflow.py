from __future__ import annotations

from dataclasses import dataclass, field

from .models import CaseState, utc_now_iso


_TRANSITIONS = {
    CaseState.NEW: {CaseState.LEGAL_GATE},
    CaseState.LEGAL_GATE: {CaseState.IDENTITY_LOCK},
    CaseState.IDENTITY_LOCK: {CaseState.PLANNED},
    CaseState.PLANNED: {CaseState.COLLECTING},
    CaseState.COLLECTING: {CaseState.NORMALIZING},
    CaseState.NORMALIZING: {CaseState.ANALYZING},
    CaseState.ANALYZING: {CaseState.RED_TEAM},
    CaseState.RED_TEAM: {CaseState.REVIEW},
    CaseState.REVIEW: {CaseState.DECISION},
    CaseState.DECISION: {CaseState.MONITORING, CaseState.CLOSED},
    CaseState.MONITORING: {CaseState.REVIEW, CaseState.CLOSED},
    CaseState.CLOSED: set(),
}


@dataclass(slots=True)
class FactoryWorkflow:
    case_id: str
    state: CaseState = CaseState.NEW
    history: list[dict[str, str]] = field(default_factory=list)

    def transition(self, new_state: CaseState, *, actor: str, reason: str) -> None:
        if new_state not in _TRANSITIONS[self.state]:
            raise ValueError(f"invalid transition {self.state.value} -> {new_state.value}")
        if not actor.strip() or not reason.strip():
            raise ValueError("actor and reason are required")
        self.history.append(
            {
                "from": self.state.value,
                "to": new_state.value,
                "actor": actor,
                "reason": reason,
                "at_utc": utc_now_iso(),
            }
        )
        self.state = new_state
