from __future__ import annotations

import hashlib
import re

from .models import CaseIntake, IdentityDecision, IdentityStatus, ProfileId
from .profiles import FactoryProfile


_SPACE_RE = re.compile(r"\s+")


def _norm(value: str | None) -> str:
    return _SPACE_RE.sub(" ", (value or "").strip().casefold())


def _entity_key(parts: list[str]) -> str:
    canonical = "|".join(_norm(item) for item in parts if _norm(item))
    return "ENT-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24].upper()


class IdentityLocker:
    """Conservative identity gate. It never merges people or companies."""

    def lock(self, intake: CaseIntake, profile: FactoryProfile) -> IdentityDecision:
        subject = intake.subject
        values = {
            "official_name": subject.official_name,
            "full_name_original": subject.full_name_original,
            "jurisdiction": subject.jurisdiction,
            "registration_or_tax_id": subject.registration_or_tax_id,
            "birth_date_or_year": subject.birth_date_or_year,
            "role_or_employer": subject.role_or_employer,
            "city_or_region": subject.city_or_region,
            "distinguishing_context": subject.distinguishing_context,
            "incorporation_date": subject.incorporation_date,
            "registered_address": subject.registered_address,
            "official_domain": subject.official_domain,
        }
        required = profile.minimum_identity.get("required", [])
        missing = [name for name in required if not _norm(values.get(name))]
        used = [name for name, value in values.items() if _norm(value)]

        conflict_reasons: list[str] = []
        if subject.candidate_count > 1 and not subject.decisive_identifier_present:
            conflict_reasons.append(
                f"{subject.candidate_count} identity candidates remain and no decisive identifier is present"
            )

        if intake.profile_id in {ProfileId.RU_PERSON, ProfileId.INTL_PERSON}:
            distinguishers = [
                subject.birth_date_or_year,
                subject.role_or_employer,
                subject.city_or_region,
                subject.distinguishing_context,
                subject.jurisdiction,
            ]
            if sum(bool(_norm(item)) for item in distinguishers) < 2:
                missing.append("at_least_two_person_distinguishers")

        if conflict_reasons:
            return IdentityDecision(
                case_id=intake.case_id,
                status=IdentityStatus.HOLD_CONFLICT,
                entity_key=None,
                used_identifiers=used,
                missing_identifiers=sorted(set(missing)),
                conflict_reasons=conflict_reasons,
            )
        if missing:
            return IdentityDecision(
                case_id=intake.case_id,
                status=IdentityStatus.HOLD_MISSING_IDENTIFIERS,
                entity_key=None,
                used_identifiers=used,
                missing_identifiers=sorted(set(missing)),
                conflict_reasons=[],
            )

        if intake.profile_id in {ProfileId.RU_ORG, ProfileId.INTL_ORG}:
            key_parts = [
                intake.profile_id.value,
                subject.jurisdiction or "",
                subject.registration_or_tax_id or "",
                subject.official_name or "",
            ]
        else:
            key_parts = [
                intake.profile_id.value,
                subject.full_name_original or "",
                subject.birth_date_or_year or "",
                subject.role_or_employer or subject.distinguishing_context or "",
                subject.jurisdiction or "",
            ]

        return IdentityDecision(
            case_id=intake.case_id,
            status=IdentityStatus.LOCKED,
            entity_key=_entity_key(key_parts),
            used_identifiers=used,
            missing_identifiers=[],
            conflict_reasons=[],
        )
