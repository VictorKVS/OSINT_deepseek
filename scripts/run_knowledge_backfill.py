from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from father_osint.knowledge_analyst import DeterministicKnowledgeAnalyst
from father_osint.models import Material, MaterialPackage
from father_osint.storage import MaterialStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a traceable knowledge bundle from materials already stored by FATHER OSINT."
    )
    parser.add_argument(
        "--store-root",
        default=str(ROOT / "data" / "osint"),
        help="MaterialStore root containing materials.jsonl and raw/.",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "data" / "knowledge" / "backfill.bundle.json"),
        help="Destination JSON knowledge bundle.",
    )
    parser.add_argument(
        "--task-id",
        default="knowledge-backfill",
        help="Synthetic task ID used for an offline corpus backfill.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    store = MaterialStore(args.store_root)
    rows = list(store.iter_materials())
    materials = [Material(**row) for row in rows]

    package = MaterialPackage(
        task_id=args.task_id,
        materials=materials,
        notes="offline knowledge extraction from previously acquired OSINT materials",
        stop_reason="backfill",
    )
    bundle = DeterministicKnowledgeAnalyst().analyze(package)
    output = bundle.write_json(args.output)

    print(f"materials={bundle.counters.get('materials', 0)}")
    print(f"chunks={bundle.counters.get('chunks', 0)}")
    print(f"claims={bundle.counters.get('CLAIM_CANDIDATE', 0)}")
    print(f"definitions={bundle.counters.get('DEFINITION_CANDIDATE', 0)}")
    print(f"requirements={bundle.counters.get('REQUIREMENT_CANDIDATE', 0)}")
    print(f"entities={bundle.counters.get('ENTITY_CANDIDATE', 0)}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
