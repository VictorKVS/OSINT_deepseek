from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from threading import Lock
from time import perf_counter
from .models import (
    CheckResult,
    FactoryRun,
    FactoryRunSummary,
    Outcome,
    ScreeningPlan,
    ScreeningRequest,
    WorkItem,
    WorkState,
    utc_now_iso,
)
from .profiles import CHECK_BY_CODE
from .registry import AdapterPayload, AdapterRegistry, ScreeningAdapter


ALLOWED_SAFETY_CLASSES = {
    "FIXTURE_ONLY",
    "POLICY_GATE",
    "LOCAL_READ_ONLY",
    "PASSIVE_PUBLIC",
    "PUBLIC_READ_ONLY",
    "MANUAL_REVIEW",
}

BAD_DEPENDENCY_OUTCOMES = {
    Outcome.BLOCKED_NO_ADAPTER,
    Outcome.BLOCKED_POLICY,
    Outcome.BLOCKED_MISSING_IDENTIFIER,
    Outcome.ERROR,
}


class ScreeningFactoryRunner:
    """Executes a plan by dependency waves and isolates adapter failures.

    The runner is an orchestration layer. It does not turn tool output into facts,
    does not execute arbitrary shell strings, and records missing adapters as gaps.
    """

    def __init__(self, registry: AdapterRegistry, *, max_workers: int = 5) -> None:
        if max_workers <= 0:
            raise ValueError("max_workers must be > 0")
        self.registry = registry
        self.max_workers = max_workers
        self._active = 0
        self._peak = 0
        self._counter_lock = Lock()

    def run(self, request: ScreeningRequest, plan: ScreeningPlan) -> FactoryRun:
        if request.request_id != plan.request_id or request.case_id != plan.case_id:
            raise ValueError("request/plan lineage mismatch")

        started_iso = utc_now_iso()
        started_perf = perf_counter()
        result_by_code: dict[str, CheckResult] = {}
        results: list[CheckResult] = []

        waves = sorted({item.wave for item in plan.work_items})
        for wave in waves:
            items = [item for item in plan.work_items if item.wave == wave]
            runnable: list[WorkItem] = []
            for item in items:
                if item.state == WorkState.BLOCKED:
                    result = self._blocked_missing_identifier(request, item)
                    result_by_code[item.check_code] = result
                    results.append(result)
                    continue
                bad_dependencies = [
                    code for code in item.dependencies
                    if code not in result_by_code or result_by_code[code].outcome in BAD_DEPENDENCY_OUTCOMES
                ]
                if bad_dependencies:
                    item.state = WorkState.BLOCKED
                    item.blocked_reason = "Blocking dependency not completed: " + ", ".join(bad_dependencies)
                    result = CheckResult(
                        request_id=request.request_id,
                        work_item_id=item.work_item_id,
                        check_code=item.check_code,
                        outcome=Outcome.BLOCKED_POLICY,
                        adapter_id=None,
                        limitations=[item.blocked_reason],
                        next_actions=["Resolve dependency and re-plan the affected checks"],
                    )
                    result_by_code[item.check_code] = result
                    results.append(result)
                else:
                    item.state = WorkState.READY
                    runnable.append(item)

            if runnable:
                with ThreadPoolExecutor(max_workers=min(self.max_workers, len(runnable))) as pool:
                    future_map = {
                        pool.submit(self._execute_work_item, request, item): item
                        for item in runnable
                    }
                    for future in as_completed(future_map):
                        item = future_map[future]
                        try:
                            result = future.result()
                        except Exception as exc:  # defensive isolation around worker wrapper
                            item.state = WorkState.FAILED
                            result = CheckResult(
                                request_id=request.request_id,
                                work_item_id=item.work_item_id,
                                check_code=item.check_code,
                                outcome=Outcome.ERROR,
                                adapter_id=None,
                                limitations=[f"Unhandled worker error: {type(exc).__name__}: {exc}"],
                                next_actions=["Inspect worker log and retry with the same immutable input"],
                            )
                        result_by_code[item.check_code] = result
                        results.append(result)

        results.sort(key=lambda result: next(
            index for index, item in enumerate(plan.work_items) if item.check_code == result.check_code
        ))
        duration_ms = int((perf_counter() - started_perf) * 1000)
        finished_iso = utc_now_iso()
        counts = Counter(result.outcome.value for result in results)
        stream_by_code = {item.check_code: item.stream.value for item in plan.work_items}
        stream_counts = Counter(stream_by_code[result.check_code] for result in results)

        blocking_gaps = list(plan.missing_identity_anchors)
        for result in results:
            definition = CHECK_BY_CODE[result.check_code]
            if definition.criticality == "BLOCKING" and result.outcome in {
                Outcome.CONFLICT,
                Outcome.BLOCKED_NO_ADAPTER,
                Outcome.BLOCKED_POLICY,
                Outcome.BLOCKED_MISSING_IDENTIFIER,
                Outcome.ERROR,
            }:
                blocking_gaps.append(f"{result.check_code}: {result.outcome.value}")
            if definition.criticality == "BLOCKING" and result.human_review_required:
                blocking_gaps.append(f"{result.check_code}: human review required")

        summary = FactoryRunSummary(
            total=len(results),
            counts_by_outcome=dict(sorted(counts.items())),
            counts_by_stream=dict(sorted(stream_counts.items())),
            started_at_utc=started_iso,
            finished_at_utc=finished_iso,
            duration_ms=duration_ms,
            peak_parallelism=self._peak,
            report_ready=not blocking_gaps,
            blocking_gaps=list(dict.fromkeys(blocking_gaps)),
        )
        return FactoryRun(request=request, plan=plan, results=results, summary=summary)

    def _execute_work_item(self, request: ScreeningRequest, item: WorkItem) -> CheckResult:
        with self._counter_lock:
            self._active += 1
            self._peak = max(self._peak, self._active)
        started_iso = utc_now_iso()
        started_perf = perf_counter()
        item.state = WorkState.RUNNING
        try:
            adapters = self.registry.for_check(item.check_code)
            if not adapters:
                item.state = WorkState.BLOCKED
                return CheckResult(
                    request_id=request.request_id,
                    work_item_id=item.work_item_id,
                    check_code=item.check_code,
                    outcome=Outcome.BLOCKED_NO_ADAPTER,
                    adapter_id=None,
                    limitations=["No approved adapter is connected for this check"],
                    next_actions=["Connect, test and approve at least one source adapter"],
                    started_at_utc=started_iso,
                    finished_at_utc=utc_now_iso(),
                    duration_ms=int((perf_counter() - started_perf) * 1000),
                )

            approved: list[ScreeningAdapter] = []
            blocked_adapter_ids: list[str] = []
            for adapter in adapters:
                if adapter.descriptor.safety_class in ALLOWED_SAFETY_CLASSES:
                    approved.append(adapter)
                else:
                    blocked_adapter_ids.append(adapter.descriptor.adapter_id)
            if not approved:
                item.state = WorkState.BLOCKED
                return CheckResult(
                    request_id=request.request_id,
                    work_item_id=item.work_item_id,
                    check_code=item.check_code,
                    outcome=Outcome.BLOCKED_POLICY,
                    adapter_id=",".join(blocked_adapter_ids) or None,
                    limitations=["All available adapters are outside the passive screening safety policy"],
                    next_actions=["Use a separately authorized assessment workflow"],
                    started_at_utc=started_iso,
                    finished_at_utc=utc_now_iso(),
                    duration_ms=int((perf_counter() - started_perf) * 1000),
                )

            payloads: list[tuple[str, AdapterPayload]] = []
            errors: list[str] = []
            for adapter in approved:
                try:
                    payloads.append((adapter.descriptor.adapter_id, adapter.run(request, item)))
                except Exception as exc:
                    errors.append(f"{adapter.descriptor.adapter_id}: {type(exc).__name__}: {exc}")

            result = self._merge_payloads(request, item, payloads, errors)
            item.state = WorkState.FAILED if result.outcome == Outcome.ERROR else WorkState.COMPLETED
            result.started_at_utc = started_iso
            result.finished_at_utc = utc_now_iso()
            result.duration_ms = int((perf_counter() - started_perf) * 1000)
            return result
        finally:
            with self._counter_lock:
                self._active -= 1

    @staticmethod
    def _merge_payloads(
        request: ScreeningRequest,
        item: WorkItem,
        payloads: list[tuple[str, AdapterPayload]],
        errors: list[str],
    ) -> CheckResult:
        if not payloads:
            return CheckResult(
                request_id=request.request_id,
                work_item_id=item.work_item_id,
                check_code=item.check_code,
                outcome=Outcome.ERROR,
                adapter_id=None,
                limitations=errors or ["No adapter result was produced"],
                next_actions=["Inspect adapter logs and retry"],
            )

        observations = [obs for _, payload in payloads for obs in payload.observations]
        attempts = [attempt for _, payload in payloads for attempt in payload.source_attempts]
        evidence_refs = list(dict.fromkeys(
            ref for _, payload in payloads for ref in payload.evidence_refs
        ))
        limitations = [item for _, payload in payloads for item in payload.limitations] + errors
        conflicts = [item for _, payload in payloads for item in payload.conflicts]
        next_actions = [item for _, payload in payloads for item in payload.next_actions]
        outcomes = [payload.outcome for _, payload in payloads]

        if conflicts or Outcome.CONFLICT in outcomes:
            outcome = Outcome.CONFLICT
        elif observations or Outcome.FOUND in outcomes:
            outcome = Outcome.FOUND
        elif all(outcome == Outcome.NO_HIT_IN_SCOPE for outcome in outcomes):
            outcome = Outcome.NO_HIT_IN_SCOPE
        elif Outcome.ERROR in outcomes:
            outcome = Outcome.ERROR
        elif Outcome.BLOCKED_POLICY in outcomes:
            outcome = Outcome.BLOCKED_POLICY
        else:
            outcome = outcomes[0]

        human_review = any(payload.human_review_required for _, payload in payloads)
        definition = CHECK_BY_CODE[item.check_code]
        if outcome in {Outcome.FOUND, Outcome.CONFLICT} and definition.human_review_if_found:
            human_review = True
        if outcome == Outcome.NO_HIT_IN_SCOPE:
            limitations.append(
                "NO_HIT_IN_SCOPE describes only the attempted sources, time and query scope; it is not proof of absence"
            )

        return CheckResult(
            request_id=request.request_id,
            work_item_id=item.work_item_id,
            check_code=item.check_code,
            outcome=outcome,
            adapter_id=",".join(adapter_id for adapter_id, _ in payloads),
            observations=observations,
            source_attempts=attempts,
            evidence_refs=evidence_refs,
            limitations=list(dict.fromkeys(limitations)),
            conflicts=list(dict.fromkeys(conflicts)),
            next_actions=list(dict.fromkeys(next_actions)),
            human_review_required=human_review,
        )

    @staticmethod
    def _blocked_missing_identifier(request: ScreeningRequest, item: WorkItem) -> CheckResult:
        return CheckResult(
            request_id=request.request_id,
            work_item_id=item.work_item_id,
            check_code=item.check_code,
            outcome=Outcome.BLOCKED_MISSING_IDENTIFIER,
            adapter_id=None,
            limitations=[item.blocked_reason or "Required identity anchor is missing"],
            next_actions=["Obtain a lawful identity anchor or keep the check explicitly unresolved"],
        )
