from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from father_osint.agent import OSINTAgent
from father_osint.collectors.dev import FixtureCollector
from father_osint.models import ResearchTask
from father_osint.storage import MaterialStore


def main() -> None:
    root = ROOT
    store = MaterialStore(root / "data" / "osint_dev")

    agent = OSINTAgent(
        store,
        collectors=[
            FixtureCollector("telegram_dev", "telegram", root / "data" / "dev" / "telegram_fixture.json"),
            FixtureCollector("github_dev", "github", root / "data" / "dev" / "github_fixture.json"),
        ],
    )

    task = ResearchTask(
        question="Telegram",
        topics=["TDLib", "MTProto"],
        source_types=["telegram", "github"],
        depth="FAST",
        max_items=20,
        requested_by="analyst_dev",
    )

    package = agent.run(task)

    print(f"task_id={package.task_id}")
    print(f"materials={len(package.materials)}")
    print(f"duplicates_skipped={package.duplicates_skipped}")
    print(f"errors={len(package.collection_errors)}")
    print(f"stop_reason={package.stop_reason}")
    print()

    for material in package.materials:
        print(f"[{material.source_type}] {material.title}")
        print(f"  {material.source_locator}")
        print(f"  {material.raw_text}")


if __name__ == "__main__":
    main()
