from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .models import MaterialPackage, ResearchTask


@dataclass(slots=True)
class Analysis:
    task_id: str
    summary: str
    findings: list[str] = field(default_factory=list)
    candidates: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    follow_up_task: ResearchTask | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.follow_up_task is not None:
            data["follow_up_task"] = self.follow_up_task.to_dict()
        return data


class SimpleAnalyst:
    """Small deterministic DEV analyst used to validate the OSINT→Analyst loop.

    This is intentionally not the future LLM analyst. It only proves the handoff,
    gap detection and follow-up task cycle while the project is under development.
    """

    def analyze(self, task: ResearchTask, package: MaterialPackage) -> Analysis:
        findings: list[str] = []
        candidates: list[str] = []

        for material in package.materials:
            text = (material.raw_text or "").strip()
            findings.append(f"[{material.source_type}] {material.title}: {text[:240]}")
            candidate = material.metadata.get("candidate")
            if candidate and candidate not in candidates:
                candidates.append(str(candidate))

        gaps: list[str] = []
        requested = set(task.source_types)
        present = {m.source_type for m in package.materials}
        missing = sorted(requested - present)
        if missing:
            gaps.append(f"No materials collected from: {', '.join(missing)}")
        if package.collection_errors:
            gaps.extend(package.collection_errors)
        if not package.materials:
            gaps.append("No material available for analysis")

        follow_up = None
        if gaps:
            follow_up = ResearchTask(
                question=task.question,
                topics=task.topics,
                source_types=missing or task.source_types,
                date_from=task.date_from,
                date_to=task.date_to,
                max_items=task.max_items,
                depth=task.depth,
                requested_by="analyst_follow_up",
                stop_when_enough="fill identified evidence gaps",
            )

        summary = (
            f"Collected {len(package.materials)} material(s); "
            f"identified {len(candidates)} explicit candidate(s); "
            f"gaps={len(gaps)}."
        )

        return Analysis(
            task_id=task.task_id,
            summary=summary,
            findings=findings,
            candidates=candidates,
            gaps=gaps,
            follow_up_task=follow_up,
        )
