from __future__ import annotations

import hashlib

from .models import (
    CaseIntake,
    Depth,
    FactoryJob,
    FactoryPlan,
    IdentityDecision,
    IdentityStatus,
    JobState,
    Stream,
)
from .profiles import CountryPackRegistry, FactoryProfile


SCREENING_FAMILIES = {
    "RU_FNS_EGRUL_EGRIP",
    "RU_FNS_TRANSPARENT_BUSINESS",
    "RU_FNS_PERSON_COMPANY_PARTICIPATION",
    "HOME_COUNTRY_COMPANY_REGISTRY",
    "COMPANY_DIRECTORSHIP_OWNERSHIP",
    "APPLICABLE_SANCTIONS",
    "UN_SANCTIONS",
    "PUBLIC_OFFICIAL_ACCOUNTS",
    "DOMAIN_RDAP_DNS_TLS",
    "RED_TEAM_IDENTITY",
    "RED_TEAM_NAMESAKE_PERSON",
    "RED_TEAM_TRANSLITERATION",
    "RED_TEAM_SOURCE_INDEPENDENCE",
}


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "|".join(parts)
    return f"{prefix}-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16].upper()


class FactoryPlanner:
    def __init__(self, country_packs: CountryPackRegistry | None = None) -> None:
        self.country_packs = country_packs or CountryPackRegistry()

    def build(
        self,
        intake: CaseIntake,
        profile: FactoryProfile,
        identity: IdentityDecision,
    ) -> FactoryPlan:
        if identity.status != IdentityStatus.LOCKED or not identity.entity_key:
            raise ValueError("Identity Lock must pass before factory planning")
        if profile.country_pack_required:
            if not intake.country_pack_id:
                raise ValueError("international profile requires country_pack_id")
            self.country_packs.get(intake.country_pack_id)

        source_pairs: list[tuple[Stream, str]] = []
        for stream, families in profile.streams.items():
            for family in families:
                if intake.depth == Depth.SCREENING and family not in SCREENING_FAMILIES:
                    continue
                source_pairs.append((stream, family))

        if intake.depth == Depth.ENHANCED:
            for family in profile.enhanced_source_families:
                source_pairs.append((self._enhanced_stream(family), family))

        # All five streams must be represented, even in SCREENING.
        represented = {stream for stream, _ in source_pairs}
        for stream in Stream:
            if stream not in represented:
                source_pairs.append((stream, f"SCREENING_PLACEHOLDER_{stream.value}"))

        jobs = [
            FactoryJob(
                case_id=intake.case_id,
                job_id=_stable_id("JOB", intake.case_id, stream.value, family),
                profile_id=intake.profile_id,
                stream=stream,
                source_family=family,
                state=JobState.PLANNED,
                priority=index + 1,
                country_pack_id=intake.country_pack_id,
                input_refs=[identity.entity_key],
            )
            for index, (stream, family) in enumerate(source_pairs)
        ]
        plan_id = _stable_id("PLAN", intake.case_id, intake.profile_id.value, intake.depth.value)
        return FactoryPlan(
            case_id=intake.case_id,
            profile_id=intake.profile_id,
            identity_ref=identity.entity_key,
            country_pack_id=intake.country_pack_id,
            jobs=jobs,
            stop_conditions=[
                "all mandatory source families have a terminal reviewed status",
                "no blocking identity conflict remains",
                "high-impact claims have primary or independent support",
                "Red Team review has no blocking alternative explanation",
                "further collection has low marginal value or approved budget is exhausted",
            ],
            human_approval_required=intake.depth in {Depth.STANDARD, Depth.ENHANCED},
            plan_id=plan_id,
        )

    @staticmethod
    def _enhanced_stream(source_family: str) -> Stream:
        if "MEDIA" in source_family or "LITIGATION" in source_family:
            return Stream.LEGAL_SANCTIONS_ADVERSE
        if "TRADEMARK" in source_family or "OPERATIONS" in source_family:
            return Stream.BUSINESS_FINANCIAL_OPERATIONS
        if "CROSS_CASE" in source_family:
            return Stream.RED_TEAM_SOURCE_QUALITY
        return Stream.ENTITY_REGISTRY
