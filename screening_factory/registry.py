from __future__ import annotations

from dataclasses import dataclass, field
from time import sleep
from typing import Callable, Protocol

from .models import Observation, ObservationClass, Outcome, ScreeningRequest, WorkItem


@dataclass(frozen=True, slots=True)
class AdapterDescriptor:
    adapter_id: str
    title: str
    check_codes: tuple[str, ...]
    execution_profile: str
    safety_class: str
    source_ids: tuple[str, ...]
    version: str = "1.0"
    network_policy: str = "PUBLIC_READ_ONLY"
    enabled: bool = True


@dataclass(slots=True)
class AdapterPayload:
    outcome: Outcome
    observations: list[Observation] = field(default_factory=list)
    source_attempts: list[dict] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    human_review_required: bool = False


class ScreeningAdapter(Protocol):
    descriptor: AdapterDescriptor

    def run(self, request: ScreeningRequest, work_item: WorkItem) -> AdapterPayload:
        ...


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, ScreeningAdapter] = {}

    def register(self, adapter: ScreeningAdapter) -> None:
        adapter_id = adapter.descriptor.adapter_id
        if adapter_id in self._adapters:
            raise ValueError(f"adapter already registered: {adapter_id}")
        self._adapters[adapter_id] = adapter

    def for_check(self, check_code: str) -> list[ScreeningAdapter]:
        return [
            adapter for adapter in self._adapters.values()
            if adapter.descriptor.enabled and check_code in adapter.descriptor.check_codes
        ]

    def descriptors(self) -> list[AdapterDescriptor]:
        return [adapter.descriptor for adapter in self._adapters.values()]


class CallbackAdapter:
    def __init__(
        self,
        descriptor: AdapterDescriptor,
        callback: Callable[[ScreeningRequest, WorkItem], AdapterPayload],
    ) -> None:
        self.descriptor = descriptor
        self._callback = callback

    def run(self, request: ScreeningRequest, work_item: WorkItem) -> AdapterPayload:
        return self._callback(request, work_item)


class SyntheticAdapter:
    """Deterministic adapter used only for fixtures and concurrency tests."""

    def __init__(
        self,
        adapter_id: str,
        check_codes: tuple[str, ...],
        *,
        outcome: Outcome = Outcome.NO_HIT_IN_SCOPE,
        delay_seconds: float = 0.0,
        observation_prefix: str = "Synthetic observation",
    ) -> None:
        self.descriptor = AdapterDescriptor(
            adapter_id=adapter_id,
            title=f"Synthetic adapter {adapter_id}",
            check_codes=check_codes,
            execution_profile="SYNTHETIC",
            safety_class="FIXTURE_ONLY",
            source_ids=(f"SRC-{adapter_id}",),
            version="fixture-v1",
            network_policy="NO_NETWORK",
        )
        self.outcome = outcome
        self.delay_seconds = delay_seconds
        self.observation_prefix = observation_prefix

    def run(self, request: ScreeningRequest, work_item: WorkItem) -> AdapterPayload:
        if self.delay_seconds:
            sleep(self.delay_seconds)
        evidence_ref = f"EVID-{self.descriptor.adapter_id}-{work_item.check_code}"
        source_id = self.descriptor.source_ids[0]
        attempts = [{
            "source_id": source_id,
            "adapter_id": self.descriptor.adapter_id,
            "status": self.outcome.value,
            "scope": "synthetic fixture",
        }]
        if self.outcome == Outcome.FOUND:
            observation = Observation(
                statement=f"{self.observation_prefix}: {work_item.check_code}",
                classification=ObservationClass.DIRECT_OBSERVATION,
                evidence_refs=[evidence_ref],
                source_ids=[source_id],
                limitations=["Synthetic fixture; does not describe a real subject"],
            )
            return AdapterPayload(
                outcome=self.outcome,
                observations=[observation],
                source_attempts=attempts,
                evidence_refs=[evidence_ref],
                human_review_required=True,
            )
        return AdapterPayload(
            outcome=self.outcome,
            source_attempts=attempts,
            limitations=[
                "NO_HIT_IN_SCOPE means no result in this synthetic adapter scope; it is not proof of absence"
            ] if self.outcome == Outcome.NO_HIT_IN_SCOPE else [],
        )
