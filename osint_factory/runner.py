from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from .adapters import AdapterRegistry
from .models import CaseIntake, FactoryPlan, JobResult, JobState, utc_now_iso
from .policy import PassiveDueDiligencePolicy


@dataclass(slots=True)
class FactoryRunResult:
    case_id: str
    plan_id: str
    results: list[JobResult]
    workers: int
    started_at_utc: str
    finished_at_utc: str


class ParallelFactoryRunner:
    def __init__(
        self,
        registry: AdapterRegistry,
        policy: PassiveDueDiligencePolicy | None = None,
        *,
        max_workers: int = 5,
    ) -> None:
        if max_workers <= 0:
            raise ValueError("max_workers must be > 0")
        self.registry = registry
        self.policy = policy or PassiveDueDiligencePolicy()
        self.max_workers = max_workers

    def run(self, intake: CaseIntake, plan: FactoryPlan) -> FactoryRunResult:
        started = utc_now_iso()
        indexed_results: dict[int, JobResult] = {}
        futures = {}
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="osint-factory") as pool:
            for index, job in enumerate(plan.jobs):
                decision = self.policy.evaluate(intake, job)
                if not decision.allowed:
                    indexed_results[index] = JobResult(
                        case_id=job.case_id,
                        job_id=job.job_id,
                        source_family=job.source_family,
                        state=JobState.BLOCKED,
                        limitations=list(decision.reason_codes),
                    )
                    continue
                adapter = self.registry.get(job.source_family)
                if adapter is None:
                    indexed_results[index] = JobResult(
                        case_id=job.case_id,
                        job_id=job.job_id,
                        source_family=job.source_family,
                        state=JobState.BLOCKED,
                        limitations=["ADAPTER_NOT_CONNECTED"],
                    )
                    continue
                futures[pool.submit(adapter.run, job)] = index

            for future in as_completed(futures):
                index = futures[future]
                job = plan.jobs[index]
                try:
                    indexed_results[index] = future.result()
                except Exception as exc:
                    indexed_results[index] = JobResult(
                        case_id=job.case_id,
                        job_id=job.job_id,
                        source_family=job.source_family,
                        state=JobState.ERROR,
                        error=f"{type(exc).__name__}: {exc}",
                        limitations=["Adapter failure was isolated from other jobs"],
                    )

        ordered = [indexed_results[index] for index in range(len(plan.jobs))]
        return FactoryRunResult(
            case_id=intake.case_id,
            plan_id=plan.plan_id,
            results=ordered,
            workers=self.max_workers,
            started_at_utc=started,
            finished_at_utc=utc_now_iso(),
        )
