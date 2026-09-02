from __future__ import annotations

from .models import CoverageAssessment, CoverageStatus, FactoryPlan, JobResult, JobState


TERMINAL_STATES = {
    JobState.FOUND,
    JobState.NO_HIT,
    JobState.BLOCKED,
    JobState.CONFLICT,
    JobState.ERROR,
    JobState.REVIEWED,
    JobState.CANCELLED,
}


class CoverageAssessor:
    def assess(self, plan: FactoryPlan, results: list[JobResult]) -> CoverageAssessment:
        by_job = {item.job_id: item for item in results}
        missing = [job.source_family for job in plan.jobs if job.job_id not in by_job]
        attempted = [by_job[job.job_id] for job in plan.jobs if job.job_id in by_job]
        counts = {state: sum(item.state == state for item in attempted) for state in JobState}

        blocking: list[str] = []
        if missing:
            blocking.append("mandatory source families were not attempted")
        if counts[JobState.CONFLICT]:
            blocking.append("unresolved source or identity conflicts remain")
        if counts[JobState.BLOCKED]:
            blocking.append("one or more mandatory source families are blocked")
        if counts[JobState.ERROR]:
            blocking.append("one or more mandatory source families ended in error")
        nonterminal = [item.job_id for item in attempted if item.state not in TERMINAL_STATES]
        if nonterminal:
            blocking.append("non-terminal jobs remain")

        if counts[JobState.CONFLICT]:
            status = CoverageStatus.HOLD_CONFLICT
        elif counts[JobState.BLOCKED] and not counts[JobState.FOUND]:
            status = CoverageStatus.BLOCKED_BY_POLICY
        elif blocking:
            status = CoverageStatus.HOLD_EVIDENCE_INSUFFICIENT
        else:
            status = CoverageStatus.READY_FOR_HUMAN_REVIEW

        return CoverageAssessment(
            case_id=plan.case_id,
            plan_id=plan.plan_id,
            status=status,
            mandatory_total=len(plan.jobs),
            attempted_total=len(attempted),
            found_total=counts[JobState.FOUND],
            no_hit_total=counts[JobState.NO_HIT],
            blocked_total=counts[JobState.BLOCKED],
            conflict_total=counts[JobState.CONFLICT],
            error_total=counts[JobState.ERROR],
            missing_source_families=missing,
            blocking_reasons=blocking,
            ready_for_human_review=status == CoverageStatus.READY_FOR_HUMAN_REVIEW,
        )
