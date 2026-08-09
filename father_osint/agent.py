from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from .models import Material, MaterialPackage, ResearchTask
from .storage import MaterialStore


class Collector(Protocol):
    name: str
    source_types: set[str]

    def collect(self, task: ResearchTask) -> Iterable[Material]:
        """Yield materials found for the research task."""
        ...


class OSINTAgent:
    """Read/collect worker for the FATHER Knowledge Factory.

    The agent intentionally does not analyze or promote knowledge. It coordinates
    source collectors, stores provenance-rich materials, skips obvious duplicates,
    and returns a package to Analyst.
    """

    def __init__(self, store: MaterialStore, collectors: Iterable[Collector] = ()) -> None:
        self.store = store
        self.collectors = list(collectors)

    def register(self, collector: Collector) -> None:
        self.collectors.append(collector)

    def run(self, task: ResearchTask) -> MaterialPackage:
        self.store.save_task(task)
        package = MaterialPackage(task_id=task.task_id)

        eligible = [
            collector
            for collector in self.collectors
            if collector.source_types.intersection(task.source_types)
        ]

        if not eligible:
            package.stop_reason = "no_eligible_collectors"
            package.collection_errors.append(
                f"No collector registered for source types: {', '.join(task.source_types)}"
            )
            self.store.save_package(package)
            return package

        for collector in eligible:
            try:
                for material in collector.collect(task):
                    if len(package.materials) >= task.max_items:
                        package.stop_reason = "max_items_reached"
                        self.store.save_package(package)
                        return package

                    if self.store.save_material(material):
                        package.materials.append(material)
                    else:
                        package.duplicates_skipped += 1
            except Exception as exc:  # collector isolation is intentional at the orchestration boundary
                package.collection_errors.append(f"{collector.name}: {type(exc).__name__}: {exc}")

        if package.collection_errors and not package.materials:
            package.stop_reason = "collection_failed"
        elif len(package.materials) >= task.max_items:
            package.stop_reason = "max_items_reached"
        else:
            package.stop_reason = "collectors_exhausted"

        self.store.save_package(package)
        return package
