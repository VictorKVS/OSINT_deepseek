from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Protocol

from .models import FactoryJob, JobResult, JobState, Observation, utc_now_iso


class SourceAdapter(Protocol):
    source_family: str

    def run(self, job: FactoryJob) -> JobResult: ...


@dataclass(slots=True)
class SyntheticSourceAdapter:
    source_family: str
    outcome: JobState = JobState.NO_HIT
    values: tuple[str, ...] = ()
    delay_ms: int = 0

    def run(self, job: FactoryJob) -> JobResult:
        started = utc_now_iso()
        start_ns = time.perf_counter_ns()
        if self.delay_ms:
            time.sleep(self.delay_ms / 1000)
        observations: list[Observation] = []
        if self.outcome == JobState.FOUND:
            for value in self.values:
                digest = hashlib.sha256(
                    f"{job.job_id}|{self.source_family}|{value}".encode("utf-8")
                ).hexdigest()
                observations.append(
                    Observation(
                        observation_id=f"OBS-{digest[:16].upper()}",
                        case_id=job.case_id,
                        job_id=job.job_id,
                        source_family=self.source_family,
                        observation_type="SOURCE_CLAIM_CANDIDATE",
                        normalized_value=value.strip(),
                        source_ref=f"synthetic://{self.source_family}/{job.job_id}",
                        capture_sha256=digest,
                        limitations=["Synthetic adapter output is not a verified fact"],
                    )
                )
        duration_ms = max(0, int((time.perf_counter_ns() - start_ns) / 1_000_000))
        no_hit_note = None
        if self.outcome == JobState.NO_HIT:
            no_hit_note = (
                f"No result in synthetic source family {self.source_family} for this exact job input; "
                "this does not prove absence of the underlying fact."
            )
        return JobResult(
            case_id=job.case_id,
            job_id=job.job_id,
            source_family=self.source_family,
            state=self.outcome,
            observations=observations,
            scoped_no_hit_note=no_hit_note,
            limitations=["Fixture-only adapter"],
            duration_ms=duration_ms,
            started_at_utc=started,
            finished_at_utc=utc_now_iso(),
        )


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, SourceAdapter] = {}

    def register(self, adapter: SourceAdapter) -> None:
        if adapter.source_family in self._adapters:
            raise ValueError(f"adapter already registered: {adapter.source_family}")
        self._adapters[adapter.source_family] = adapter

    def get(self, source_family: str) -> SourceAdapter | None:
        return self._adapters.get(source_family)

    def registered_families(self) -> list[str]:
        return sorted(self._adapters)
