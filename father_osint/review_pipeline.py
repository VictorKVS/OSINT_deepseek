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
    analysis: Analysis
    review: SocratesReview


@dataclass(slots=True)
class ReviewPipelineResult:
    cycles: list[ReviewCycle] = field(default_factory=list)
    stop_reason: str = "completed"

    @property
    def final_review(self) -> SocratesReview | None:
        return self.cycles[-1].review if self.cycles else None


class DevReviewPipeline:
    """Bounded DEV loop: OSINT -> Analyst -> Socrates -> optional follow-up OSINT."""

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

        for cycle_number in range(1, self.max_cycles + 1):
            package = self.osint_agent.run(task)
            analysis = self.analyst.analyze(task, package)
            review = self.socrates.review(task, package, analysis)

            result.cycles.append(
                ReviewCycle(
                    number=cycle_number,
                    task=task,
                    package=package,
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
