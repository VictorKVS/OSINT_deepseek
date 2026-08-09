from __future__ import annotations

from dataclasses import dataclass, field

from .agent import OSINTAgent
from .analysis import Analysis, SimpleAnalyst
from .models import MaterialPackage, ResearchTask


@dataclass(slots=True)
class PipelineCycle:
    number: int
    task: ResearchTask
    package: MaterialPackage
    analysis: Analysis


@dataclass(slots=True)
class PipelineResult:
    cycles: list[PipelineCycle] = field(default_factory=list)
    stop_reason: str = "completed"

    @property
    def final_analysis(self) -> Analysis | None:
        return self.cycles[-1].analysis if self.cycles else None


class DevResearchPipeline:
    """Bounded DEV loop: OSINT -> Analyst -> optional follow-up OSINT.

    The loop is intentionally small. It validates handoffs and stop conditions
    without introducing Socrates, Knowledge Gate, LLM orchestration, or battle
    collectors during project development.
    """

    def __init__(
        self,
        osint_agent: OSINTAgent,
        analyst: SimpleAnalyst | None = None,
        max_cycles: int = 3,
    ) -> None:
        if max_cycles <= 0:
            raise ValueError("max_cycles must be > 0")
        self.osint_agent = osint_agent
        self.analyst = analyst or SimpleAnalyst()
        self.max_cycles = max_cycles

    def run(self, initial_task: ResearchTask) -> PipelineResult:
        result = PipelineResult()
        task = initial_task

        for cycle_number in range(1, self.max_cycles + 1):
            package = self.osint_agent.run(task)
            analysis = self.analyst.analyze(task, package)
            result.cycles.append(
                PipelineCycle(
                    number=cycle_number,
                    task=task,
                    package=package,
                    analysis=analysis,
                )
            )

            if analysis.follow_up_task is None:
                result.stop_reason = "analyst_satisfied"
                return result

            task = analysis.follow_up_task

        result.stop_reason = "max_cycles_reached"
        return result
