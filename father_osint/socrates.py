from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .analysis import Analysis
from .models import MaterialPackage, ResearchTask


@dataclass(slots=True)
class SocratesReview:
    task_id: str
    status: str
    issues: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    follow_up_task: ResearchTask | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.follow_up_task is not None:
            data["follow_up_task"] = self.follow_up_task.to_dict()
        return data


class SimpleSocrates:
    """Minimal deterministic DEV reviewer.

    It does not try to prove truth. It only checks whether the Analyst has enough
    sourced material, whether obvious collection gaps remain, and whether a
    follow-up collection request is justified.
    """

    def review(
        self,
        task: ResearchTask,
        package: MaterialPackage,
        analysis: Analysis,
    ) -> SocratesReview:
        issues: list[str] = []
        questions: list[str] = []

        if not package.materials:
            issues.append("No source material supports the analysis")

        if analysis.gaps:
            issues.extend(f"Analyst gap: {gap}" for gap in analysis.gaps)

        if analysis.findings and not package.materials:
            issues.append("Findings exist without collected materials")

        requested = set(task.source_types)
        present = {m.source_type for m in package.materials}
        missing = sorted(requested - present)
        if missing:
            questions.append(f"Can OSINT collect missing source types: {', '.join(missing)}?")

        follow_up = None
        if missing:
            follow_up = ResearchTask(
                question=task.question,
                topics=task.topics,
                source_types=missing,
                date_from=task.date_from,
                date_to=task.date_to,
                max_items=task.max_items,
                depth=task.depth,
                requested_by="socrates_follow_up",
                stop_when_enough="collect material for missing source types",
            )
        elif not package.materials:
            follow_up = ResearchTask(
                question=task.question,
                topics=task.topics,
                source_types=task.source_types,
                date_from=task.date_from,
                date_to=task.date_to,
                max_items=task.max_items,
                depth=task.depth,
                requested_by="socrates_follow_up",
                stop_when_enough="obtain at least one relevant source material",
            )

        status = "PASS" if not issues else "RESEARCH_MORE"
        return SocratesReview(
            task_id=task.task_id,
            status=status,
            issues=issues,
            questions=questions,
            follow_up_task=follow_up,
        )
