from __future__ import annotations

from dataclasses import dataclass

ACCESS_CLASSES = {
    "PUBLIC",
    "PUBLIC_WITH_PERSONAL_DATA",
    "AUTHORIZED_INTERNAL",
    "RESTRICTED",
    "PROHIBITED",
}
SAFETY_CLASSES = {"PASSIVE_PUBLIC", "ACTIVE_AUTHORIZED", "RESTRICTED_FORENSIC", "PROHIBITED"}
NETWORK_POLICIES = {"NO_NETWORK", "INTERNET_READ_ONLY", "ALLOWLIST_ONLY", "AUTHORIZED_TARGET_SCOPE"}
REPUBLICATION_STATUSES = {"ALLOWED", "METADATA_ONLY", "REDACTED_ONLY", "PROHIBITED", "UNKNOWN"}

_ACCESS_RANK = {
    "PUBLIC": 0,
    "PUBLIC_WITH_PERSONAL_DATA": 1,
    "AUTHORIZED_INTERNAL": 2,
    "RESTRICTED": 3,
    "PROHIBITED": 4,
}


class PolicyError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    decision: str
    reason_codes: tuple[str, ...]
    human_approval_required: bool = False


def validate_access_class(value: str) -> str:
    value = value.upper()
    if value not in ACCESS_CLASSES:
        raise PolicyError(f"unsupported access class: {value}")
    return value


def strictest_access_class(*values: str) -> str:
    checked = [validate_access_class(value) for value in values]
    return max(checked, key=_ACCESS_RANK.__getitem__) if checked else "PUBLIC"


def authorize_transform(
    *,
    case_active_actions_allowed: bool,
    safety_class: str,
    network_policy: str,
    access_class: str,
    human_approval_obtained: bool = False,
) -> PolicyDecision:
    safety_class = safety_class.upper()
    network_policy = network_policy.upper()
    access_class = validate_access_class(access_class)
    if safety_class not in SAFETY_CLASSES:
        raise PolicyError(f"unsupported safety class: {safety_class}")
    if network_policy not in NETWORK_POLICIES:
        raise PolicyError(f"unsupported network policy: {network_policy}")
    if access_class == "PROHIBITED" or safety_class == "PROHIBITED":
        return PolicyDecision("DENY", ("PROHIBITED_CLASS",))
    if safety_class == "PASSIVE_PUBLIC":
        if access_class not in {"PUBLIC", "PUBLIC_WITH_PERSONAL_DATA"}:
            return PolicyDecision("DENY", ("PASSIVE_PUBLIC_DATA_BOUNDARY",))
        return PolicyDecision("ALLOW", ("PASSIVE_PUBLIC_SCOPE",))
    if safety_class == "ACTIVE_AUTHORIZED":
        if not case_active_actions_allowed:
            return PolicyDecision("DENY", ("ACTIVE_ACTIONS_OUT_OF_SCOPE",), True)
        if not human_approval_obtained:
            return PolicyDecision("REQUIRE_APPROVAL", ("WRITTEN_SCOPE_AND_HUMAN_APPROVAL_REQUIRED",), True)
        return PolicyDecision("ALLOW", ("ACTIVE_SCOPE_APPROVED",), True)
    if safety_class == "RESTRICTED_FORENSIC":
        if access_class != "RESTRICTED":
            return PolicyDecision("DENY", ("FORENSIC_RESTRICTED_ENVIRONMENT_REQUIRED",), True)
        if not human_approval_obtained:
            return PolicyDecision("REQUIRE_APPROVAL", ("FORENSIC_APPROVAL_REQUIRED",), True)
        return PolicyDecision("ALLOW", ("FORENSIC_SCOPE_APPROVED",), True)
    return PolicyDecision("DENY", ("DEFAULT_DENY",))


def authorize_public_export(
    *,
    access_class: str,
    republication_status: str,
    contains_personal_data: bool,
    redacted: bool,
    evidence_trace_complete: bool,
    human_reviewed: bool,
) -> PolicyDecision:
    access_class = validate_access_class(access_class)
    republication_status = republication_status.upper()
    if republication_status not in REPUBLICATION_STATUSES:
        raise PolicyError(f"unsupported republication status: {republication_status}")
    reasons: list[str] = []
    if access_class in {"AUTHORIZED_INTERNAL", "RESTRICTED", "PROHIBITED"}:
        reasons.append("ACCESS_CLASS_BLOCKS_PUBLIC_EXPORT")
    if republication_status in {"PROHIBITED", "UNKNOWN"}:
        reasons.append("REPUBLICATION_NOT_ALLOWED")
    if contains_personal_data and not redacted:
        reasons.append("UNREDACTED_PERSONAL_DATA")
    if not evidence_trace_complete:
        reasons.append("INCOMPLETE_EVIDENCE_TRACE")
    if not human_reviewed:
        reasons.append("HUMAN_REVIEW_REQUIRED")
    return PolicyDecision("DENY" if reasons else "ALLOW", tuple(reasons or ["PUBLIC_EXPORT_GATES_PASSED"]))
