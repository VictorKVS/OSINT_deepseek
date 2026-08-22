from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.knowledge_factory_store import KnowledgeFactoryStore
from father_osint.pdn_batch import PdnOfficialBatchRunner, load_registry


DEFAULT_REGISTRY = REPO_ROOT / "config" / "pdn_official_documents.json"
DEFAULT_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download approved official PDn documents by registry and prepare D0-D5 review package"
    )
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--max-chunk-chars", type=int, default=2400)
    args = parser.parse_args()

    registry = load_registry(args.registry)
    store = KnowledgeFactoryStore(args.root)
    result = PdnOfficialBatchRunner(
        store,
        max_chunk_chars=args.max_chunk_chars,
    ).run(registry)

    payload = {
        "registry_id": result.registry_id,
        "counters": result.counters,
        "review_json": result.review_json_path,
        "review_md": result.review_md_path,
        "store_root": str(store.root),
        "documents": [item.to_dict() for item in result.results],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    hard_failures = (
        result.counters["acquisition_failed"]
        + result.counters["acquisition_blocked"]
        + result.counters["compile_failed"]
    )
    return 2 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
