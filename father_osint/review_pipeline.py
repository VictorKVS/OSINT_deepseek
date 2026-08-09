from __future__ import annotations

from dataclasses import dataclass, field

from .agent import OSINTAgent
from .analysis import Analysis, SimpleAnalyst
from .models import MaterialPackage, ResearchTask
from .socrates import SimpleSocrates, SocratesReview


@dataclass(slots=True)
class ReviewCycle:
    number: int
    task: ResearchTask
    package: MaterialPackage
    evidence_package: MaterialPackage
    analysis: Analysis
    review: SocratesReview


@dataclass(slots=True)
class ReviewPipelineResult:
    cycles: list[ReviewCycle] = field(default_factory=list)
    stop_reason: str = "completed"

    @property
    def final_review(self) -> SocratesReview | None:
        return self.cycles[-1].review if self.cycles else None

    @property
    def final_evidence_package(self) -> MaterialPackage | None:
        return self.cycles[-1].evidence_package if self.cycles else None


class DevReviewPipeline:
    """Bounded DEV loop with cumulative evidence across follow-up cycles.

    Each cycle keeps its own collection package for audit. Analyst and Socrates
    review a cumulative evidence package so material acquired in an earlier cycle
    is not forgotten when a follow-up task targets only a missing source type.
    """

    def __init__(
        self,
        osint_agent: OSINTAgent,
        analyst: SimpleAnalyst | None = None,
        socrates: SimpleSocrates | None = None,
        max_cycles: int = 3,
    ) -> None:
        if max_cycles <= 0:
            raise ValueError("max_cycles must be > 0")
        self.osint_agent = osint_agent
        self.analyst = analyst or SimpleAnalyst()
        self.socrates = socrates or SimpleSocrates()
        self.max_cycles = max_cycles

    def run(self, initial_task: ResearchTask) -> ReviewPipelineResult:
        result = ReviewPipelineResult()
        task = initial_task
        cumulative_materials = []
        cumulative_errors: list[str] = []
        cumulative_payloads_reused = 0

        for cycle_number in range(1, self.max_cycles + 1):
            package = self.osint_agent.run(task)
            cumulative_materials.extend(package.materials)
            cumulative_errors.extend(package.collection_errors)
            cumulative_payloads_reused += package.payloads_reused

            evidence_package = MaterialPackage(
                task_id=initial_task.task_id,
                materials=list(cumulative_materials),
                payloads_reused=cumulative_payloads_reused,
                collection_errors=list(cumulative_errors),
                notes="Cumulative DEV evidence across review cycles",
                stop_reason=package.stop_reason,
            )

            # Coverage is assessed against the original research request, not only
            # against the narrowed follow-up task.
            analysis = self.analyst.analyze(initial_task, evidence_package)
            review = self.socrates.review(initial_task, evidence_package, analysis)

            result.cycles.append(
                ReviewCycle(
                    number=cycle_number,
                    task=task,
                    package=package,
                    evidence_package=evidence_package,
                    analysis=analysis,
                    review=review,
                )
            )

            if review.follow_up_task is not None:
                task = review.follow_up_task
                continue

            if analysis.follow_up_task is not None:
                task = analysis.follow_up_task
                continue

            result.stop_reason = "review_passed" if review.status == "PASS" else "review_stopped"
            return result

        result.stop_reason = "max_cycles_reached"
        return result
