from __future__ import annotations

from dataclasses import dataclass

from .models import CaseIntake, FactoryJob


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason_codes: tuple[str, ...]


class PassiveDueDiligencePolicy:
    """V1 policy gate: public/passive only, no free-form commands."""

    prohibited_tokens = {
        "AUTH_BYPASS",
        "CREDENTIAL_ATTACK",
        "EXPLOITATION",
        "PHISHING_DELIVERY",
        "UNRESTRICTED_SHELL",
    }

    def evaluate(self, intake: CaseIntake, job: FactoryJob) -> PolicyDecision:
        reasons: list[str] = []
        if intake.active_actions_allowed or job.active_actions_allowed:
            reasons.append("ACTIVE_ACTION_FORBIDDEN_IN_FACTORY_V1")
        if not job.passive_public_only:
            reasons.append("JOB_NOT_PASSIVE_PUBLIC")
        if not intake.legal_basis_or_usage_note.strip():
            reasons.append("LEGAL_BASIS_MISSING")
        if not intake.purpose.strip():
            reasons.append("PURPOSE_MISSING")
        if self.prohibited_tokens - set(intake.prohibited_methods):
            reasons.append("PROHIBITED_METHOD_DENYLIST_INCOMPLETE")
        return PolicyDecision(allowed=not reasons, reason_codes=tuple(reasons or ["PASSIVE_PUBLIC_ALLOWED"]))
