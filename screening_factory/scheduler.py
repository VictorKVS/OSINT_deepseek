from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .models import RiskTier


DEFAULT_RECHECK_DAYS = {
    RiskTier.LOW: 365,
    RiskTier.MEDIUM: 180,
    RiskTier.HIGH: 90,
    RiskTier.CRITICAL: 30,
}


@dataclass(frozen=True, slots=True)
class RecheckDecision:
    next_due_at_utc: str
    interval_days: int
    reason: str
    event_triggered: bool


class RecheckScheduler:
    """Operational default scheduler, not a statement of a legal deadline."""

    def next_due(
        self,
        completed_at_utc: str,
        risk_tier: RiskTier,
        *,
        unresolved_blocking_gap: bool = False,
        material_event: bool = False,
    ) -> RecheckDecision:
        completed = datetime.fromisoformat(completed_at_utc.replace("Z", "+00:00"))
        if completed.tzinfo is None:
            completed = completed.replace(tzinfo=timezone.utc)
        if material_event:
            return RecheckDecision(
                next_due_at_utc=completed.astimezone(timezone.utc).isoformat(),
                interval_days=0,
                reason="Material event requires immediate event-driven re-screening",
                event_triggered=True,
            )
        interval = DEFAULT_RECHECK_DAYS[risk_tier]
        if unresolved_blocking_gap:
            interval = min(interval, 14)
            reason = "Blocking gap remains; shortened operational review interval"
        else:
            reason = f"Default operational interval for {risk_tier.value} risk"
        due = completed.astimezone(timezone.utc) + timedelta(days=interval)
        return RecheckDecision(
            next_due_at_utc=due.isoformat(),
            interval_days=interval,
            reason=reason,
            event_triggered=False,
        )
