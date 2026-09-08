from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .coverage import CoverageAssessor
from .identity import IdentityLocker
from .journal import HashChainJournal
from .models import CaseIntake, CaseState, CoverageAssessment, FactoryPlan, IdentityDecision
from .planner import FactoryPlanner
from .profiles import ProfileRegistry
from .report import MarkdownReportBuilder
from .runner import FactoryRunResult, ParallelFactoryRunner
from .storage import CaseStore
from .workflow import FactoryWorkflow


@dataclass(slots=True)
class FactoryExecution:
    identity: IdentityDecision
    plan: FactoryPlan
    run: FactoryRunResult
    coverage: CoverageAssessment
    report_markdown: str
    journal_valid: bool
    journal_message: str


class DueDiligenceFactory:
    def __init__(
        self,
        runner: ParallelFactoryRunner,
        *,
        store_root: str | Path = "runtime/osint-factory",
    ) -> None:
        self.runner = runner
        self.profiles = ProfileRegistry()
        self.identity_locker = IdentityLocker()
        self.planner = FactoryPlanner()
        self.coverage = CoverageAssessor()
        self.report_builder = MarkdownReportBuilder()
        self.store = CaseStore(store_root)

    def execute(self, intake: CaseIntake) -> FactoryExecution:
        profile = self.profiles.get(intake.profile_id)
        workflow = FactoryWorkflow(intake.case_id)
        journal = HashChainJournal(intake.case_id)

        workflow.transition(CaseState.LEGAL_GATE, actor="FACTORY", reason="intake validated")
        journal.append("LEGAL_GATE_PASSED", "FACTORY", {"profile_id": intake.profile_id.value})
        workflow.transition(CaseState.IDENTITY_LOCK, actor="FACTORY", reason="start identity resolution")

        identity = self.identity_locker.lock(intake, profile)
        journal.append("IDENTITY_DECISION", "FACTORY", identity.to_dict())
        if identity.status.value != "LOCKED":
            raise ValueError(f"factory halted at Identity Lock: {identity.status.value}")

        plan = self.planner.build(intake, profile, identity)
        workflow.transition(CaseState.PLANNED, actor="FACTORY", reason="query plan generated")
        journal.append("PLAN_CREATED", "FACTORY", {"plan_id": plan.plan_id, "jobs": len(plan.jobs)})
        workflow.transition(CaseState.COLLECTING, actor="FACTORY", reason="parallel jobs released")

        run = self.runner.run(intake, plan)
        for item in run.results:
            journal.append(
                "JOB_TERMINAL",
                "WORKER",
                {
                    "job_id": item.job_id,
                    "source_family": item.source_family,
                    "state": item.state.value,
                    "observations": len(item.observations),
                },
            )
        workflow.transition(CaseState.NORMALIZING, actor="FACTORY", reason="job outputs preserved")
        workflow.transition(CaseState.ANALYZING, actor="FACTORY", reason="coverage assessment")
        coverage = self.coverage.assess(plan, run.results)
        journal.append("COVERAGE_ASSESSED", "FACTORY", coverage.to_dict())
        workflow.transition(CaseState.RED_TEAM, actor="FACTORY", reason="red-team stream completed")
        workflow.transition(CaseState.REVIEW, actor="FACTORY", reason="human review required")

        report = self.report_builder.build(intake, identity, plan, run.results, coverage)
        journal.append("REPORT_DRAFTED", "FACTORY", {"human_review_required": True})
        valid, message = journal.verify()

        self.store.write_json(intake.case_id, "00_case_intake.json", intake.to_dict())
        self.store.write_json(intake.case_id, "01_identity_decision.json", identity.to_dict())
        self.store.write_json(intake.case_id, "02_factory_plan.json", plan.to_dict())
        self.store.write_json(
            intake.case_id,
            "03_job_results.json",
            {"results": [item.to_dict() for item in run.results]},
        )
        self.store.write_json(intake.case_id, "04_coverage.json", coverage.to_dict())
        report_path = self.store.case_dir(intake.case_id) / "05_report.md"
        report_path.write_text(report, encoding="utf-8")
        journal.save_jsonl(self.store.case_dir(intake.case_id) / "06_journal.jsonl")

        return FactoryExecution(
            identity=identity,
            plan=plan,
            run=run,
            coverage=coverage,
            report_markdown=report,
            journal_valid=valid,
            journal_message=message,
        )
