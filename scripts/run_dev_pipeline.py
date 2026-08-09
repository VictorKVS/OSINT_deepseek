from pathlib import Path

from father_osint.agent import OSINTAgent
from father_osint.analysis import SimpleAnalyst
from father_osint.collectors.dev import FixtureCollector
from father_osint.models import ResearchTask
from father_osint.review_pipeline import DevReviewPipeline
from father_osint.socrates import SimpleSocrates
from father_osint.storage import MaterialStore


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    store = MaterialStore(root / "data" / "osint_dev_pipeline")

    agent = OSINTAgent(
        store,
        collectors=[
            FixtureCollector("telegram_dev", "telegram", root / "data" / "dev" / "telegram_fixture.json"),
            FixtureCollector("github_dev", "github", root / "data" / "dev" / "github_fixture.json"),
        ],
    )

    task = ResearchTask(
        question="Find Telegram transport candidates for FATHER OSINT",
        topics=["TDLib", "MTProto", "Telegram transport"],
        source_types=["telegram", "github"],
        depth="FAST",
        max_items=20,
        requested_by="analyst_dev",
    )

    result = DevReviewPipeline(
        osint_agent=agent,
        analyst=SimpleAnalyst(),
        socrates=SimpleSocrates(),
        max_cycles=3,
    ).run(task)

    print(f"pipeline_stop={result.stop_reason}")
    print(f"cycles={len(result.cycles)}")
    print()

    for cycle in result.cycles:
        print(f"=== cycle {cycle.number} ===")
        print(f"task={cycle.task.question}")
        print(f"sources={','.join(cycle.task.source_types)}")
        print(f"materials={len(cycle.package.materials)}")
        print(f"package_stop={cycle.package.stop_reason}")
        print(f"analysis={cycle.analysis.summary}")
        print(f"socrates={cycle.review.status}")
        if cycle.analysis.candidates:
            print(f"candidates={', '.join(cycle.analysis.candidates)}")
        if cycle.analysis.gaps:
            print("gaps:")
            for gap in cycle.analysis.gaps:
                print(f"  - {gap}")
        if cycle.review.reasons:
            print("review_reasons:")
            for reason in cycle.review.reasons:
                print(f"  - {reason}")
        print()


if __name__ == "__main__":
    main()
