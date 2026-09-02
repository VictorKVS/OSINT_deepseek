from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files
from typing import Any

from .models import ProfileId, Stream


@dataclass(frozen=True, slots=True)
class FactoryProfile:
    profile_id: ProfileId
    subject_type: str
    jurisdiction_group: str
    country_pack_required: bool
    minimum_identity: dict[str, list[str]]
    streams: dict[Stream, list[str]]
    enhanced_source_families: list[str]
    hard_rules: list[str]


class ProfileRegistry:
    def __init__(self) -> None:
        payload = json.loads(
            files("osint_factory.data").joinpath("profiles.json").read_text(encoding="utf-8")
        )
        self._profiles: dict[ProfileId, FactoryProfile] = {}
        for raw_id, raw in payload["profiles"].items():
            profile_id = ProfileId(raw_id)
            self._profiles[profile_id] = FactoryProfile(
                profile_id=profile_id,
                subject_type=raw["subject_type"],
                jurisdiction_group=raw["jurisdiction_group"],
                country_pack_required=bool(raw["country_pack_required"]),
                minimum_identity={key: list(value) for key, value in raw["minimum_identity"].items()},
                streams={Stream(key): list(value) for key, value in raw["streams"].items()},
                enhanced_source_families=list(raw.get("enhanced_source_families", [])),
                hard_rules=list(raw.get("hard_rules", [])),
            )

    def get(self, profile_id: ProfileId) -> FactoryProfile:
        return self._profiles[profile_id]

    def all(self) -> list[FactoryProfile]:
        return list(self._profiles.values())


class CountryPackRegistry:
    def __init__(self) -> None:
        payload = json.loads(
            files("osint_factory.data").joinpath("country_packs.json").read_text(encoding="utf-8")
        )
        self._packs: dict[str, dict[str, Any]] = {
            key: dict(value) for key, value in payload["country_packs"].items()
        }

    def get(self, pack_id: str) -> dict[str, Any]:
        try:
            return self._packs[pack_id]
        except KeyError as exc:
            raise KeyError(f"unknown country pack: {pack_id}") from exc

    def all_ids(self) -> list[str]:
        return sorted(self._packs)
