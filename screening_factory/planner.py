from __future__ import annotations

from .models import (
    CheckDefinition,
    CheckStage,
    ScreeningPlan,
    ScreeningRequest,
    Subject,
    WorkItem,
    WorkState,
)
from .profiles import CHECK_BY_CODE, checks_for_profile, profile_for


class ScreeningPolicyError(ValueError):
    pass


STAGE_BASE_WAVE = {
    CheckStage.ADMISSION: 0,
    CheckStage.IDENTIFY: 10,
    CheckStage.EXPAND: 20,
    CheckStage.ASSESS: 30,
    CheckStage.REVIEW: 40,
}


def _anchor_available(subject: Subject, anchor: str) -> bool:
    if anchor == "dob":
        return bool(subject.date_of_birth)
    if anchor == "name_region":
        return bool(subject.display_name and subject.known_regions)
    if anchor == "name_country":
        return bool(subject.display_name and subject.country_code and subject.country_code != "ZZ")
    return bool(subject.identifiers.get(anchor))


def _strong_identity_gaps(subject: Subject) -> list[str]:
    if subject.kind.value == "LEGAL_ENTITY":
        strong = {"inn", "ogrn", "registration_number", "tax_id", "lei", "eori"}
        if any(subject.identifiers.get(key) for key in strong):
            return []
        return ["No strong registration/tax identifier; exact-name resolution and namesake review are mandatory"]

    strong_person = {
        "inn", "snils_masked", "national_id_masked", "passport_masked", "professional_id",
    }
    gaps: list[str] = []
    if not subject.date_of_birth:
        gaps.append("Date of birth is absent")
    if not any(subject.identifiers.get(key) for key in strong_person):
        gaps.append("No strong lawful person identifier is supplied")
    return gaps


class ScreeningPlanner:
    """Builds a deterministic, reviewable screening production plan.

    The planner never performs collection and never promotes a match into a fact.
    It only selects checks, exposes missing anchors and creates ordered work items.
    """

    algorithm_version = "screening-planner-m3-v1"

    def build(self, request: ScreeningRequest) -> ScreeningPlan:
        if request.active_actions_allowed:
            raise ScreeningPolicyError(
                "The screening factory is passive/public-data only; active actions require a separate assessment case type"
            )
        if not request.allowed_source_classes:
            raise ScreeningPolicyError("At least one allowed source class is required")

        profile = profile_for(request.subject.kind, request.jurisdiction_scope)
        selected = [item for item in checks_for_profile(profile) if item.applies_to(request)]
        selected_by_code = {item.code: item for item in selected}

        # Dependencies needed by a selected check are pulled in when applicable.
        changed = True
        while changed:
            changed = False
            for item in list(selected_by_code.values()):
                for dep_code in item.dependencies:
                    dep = CHECK_BY_CODE[dep_code]
                    if dep.applies_to(request) and dep_code not in selected_by_code:
                        selected_by_code[dep_code] = dep
                        changed = True

        wave_cache: dict[str, int] = {}

        def wave_for(definition: CheckDefinition, stack: tuple[str, ...] = ()) -> int:
            if definition.code in wave_cache:
                return wave_cache[definition.code]
            if definition.code in stack:
                raise ValueError(f"cyclic check dependency: {' -> '.join(stack + (definition.code,))}")
            wave = STAGE_BASE_WAVE[definition.stage]
            for dep_code in definition.dependencies:
                dep = selected_by_code.get(dep_code)
                if dep is not None:
                    wave = max(wave, wave_for(dep, stack + (definition.code,)) + 1)
            wave_cache[definition.code] = wave
            return wave

        work_items: list[WorkItem] = []
        for definition in selected_by_code.values():
            missing_required = [
                anchor for anchor in definition.required_identifiers_any
                if not _anchor_available(request.subject, anchor)
            ]
            all_required_missing = bool(definition.required_identifiers_any) and len(missing_required) == len(
                definition.required_identifiers_any
            )
            state = WorkState.BLOCKED if all_required_missing else WorkState.PLANNED
            blocked_reason = None
            if all_required_missing:
                blocked_reason = (
                    "At least one identity anchor is required: "
                    + ", ".join(definition.required_identifiers_any)
                )
            work_items.append(
                WorkItem(
                    request_id=request.request_id,
                    check_code=definition.code,
                    title_ru=definition.title_ru,
                    stream=definition.stream,
                    stage=definition.stage,
                    wave=wave_for(definition),
                    dependencies=[code for code in definition.dependencies if code in selected_by_code],
                    source_families=list(definition.source_families),
                    capabilities=list(definition.capabilities),
                    state=state,
                    blocked_reason=blocked_reason,
                )
            )

        work_items.sort(key=lambda item: (item.wave, item.stream.value, item.check_code))
        missing_identity = _strong_identity_gaps(request.subject)

        human_gates = [
            "Exact identity/namesake review before joining person or organization candidates",
            "Official-list confirmation and analyst review for every sanctions/PEP match",
            "Court/enforcement findings require exact subject identity and procedural status",
            "Adverse media remains SOURCE_CLAIM until independently corroborated",
            "Beneficial ownership/control inference requires explicit evidence and human approval",
            "No final negative decision while a blocking identity conflict remains unresolved",
            "Public export requires minimization and source-by-source publication review",
        ]
        stop_conditions = [
            "All blocking checks have terminal outcomes and provenance-preserved source attempts",
            "Required sufficiency for the selected depth has been reached",
            "No unresolved critical sanctions or identity collision remains",
            "Additional collection has low marginal value and gaps are explicitly recorded",
            "Legal/access policy blocks further collection",
        ]
        coverage_domains = [
            "identity", "registration_and_roles", "sanctions_and_pep", "courts_and_enforcement",
            "insolvency_and_finance", "procurement_and_licenses", "digital_footprint",
            "adverse_media", "source_independence", "contradictions_and_gaps",
        ]

        return ScreeningPlan(
            request_id=request.request_id,
            case_id=request.case_id,
            subject_id=request.subject.subject_id,
            profile_id=profile.profile_id,
            depth=request.depth,
            risk_tier=request.risk_tier,
            source_pack_ids=list(profile.source_pack_ids),
            work_items=work_items,
            missing_identity_anchors=missing_identity,
            stop_conditions=stop_conditions,
            human_review_gates=human_gates,
            coverage_domains=coverage_domains,
        )
