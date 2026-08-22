from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.artifact_identity import MarkerValidatingFetcher
from father_osint.knowledge_factory_store import KnowledgeFactoryStore
from father_osint.models import utc_now_iso
from father_osint.operator_import import OperatorImportArtifactFetcher
from father_osint.pdn_batch import PdnOfficialBatchRunner, load_registry
from scripts.run_pdn_official_batch import build_marker_map, export_sanitized_review


DEFAULT_REGISTRY = REPO_ROOT / "config" / "pdn_official_documents.json"
DEFAULT_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
DEFAULT_INBOX = REPO_ROOT / "data" / "operator_import" / "pdn_inbox"
DEFAULT_EXPORT = REPO_ROOT / "reports" / "pdn_live"
SUPPORTED_SUFFIXES = (".html", ".htm", ".txt", ".json")


def _resolve_repo_path(value: str | Path) -> Path:
    """Resolve CLI paths consistently on Windows/Linux before relative_to checks."""

    path = Path(value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def discover_files(registry: dict, inbox: Path) -> tuple[dict[str, Path], list[dict[str, object]]]:
    inbox = _resolve_repo_path(inbox)
    files_by_url: dict[str, Path] = {}
    inventory: list[dict[str, object]] = []
    for item in registry["documents"]:
        if not item.get("enabled", False):
            continue
        document_id = item["document_id"]
        source_url = item.get("source_url")
        if not source_url:
            inventory.append({
                "document_id": document_id,
                "status": "SOURCE_URL_MISSING",
                "path": None,
            })
            continue

        candidates = [inbox / f"{document_id}{suffix}" for suffix in SUPPORTED_SUFFIXES]
        existing = [path for path in candidates if path.exists()]
        if len(existing) > 1:
            raise ValueError(
                f"multiple operator files found for {document_id}: "
                + ", ".join(path.name for path in existing)
            )
        if not existing:
            inventory.append({
                "document_id": document_id,
                "status": "FILE_MISSING",
                "path": None,
            })
            continue

        path = existing[0].resolve()
        data = path.read_bytes()
        files_by_url[source_url] = path
        inventory.append({
            "document_id": document_id,
            "status": "FOUND",
            "path": path.relative_to(REPO_ROOT).as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "source_url": source_url,
        })
    return files_by_url, inventory


def append_operator_observations(store: KnowledgeFactoryStore, inventory: list[dict[str, object]], results) -> str:
    path = store.root / "operator_import_observations.jsonl"
    status_by_id = {item.document_id: item.status for item in results}
    reason_by_id = {item.document_id: item.reason for item in results}
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for item in inventory:
            payload = {
                "record_type": "OPERATOR_IMPORT_OBSERVATION",
                "observed_at": utc_now_iso(),
                **item,
                "batch_status": status_by_id.get(str(item["document_id"])),
                "batch_reason": reason_by_id.get(str(item["document_id"]), ""),
                "semantic_extraction_performed": False,
            }
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return path.relative_to(store.root).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import operator-saved official PDn HTML/TXT files through the normal D0-D5 conveyor"
    )
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--inbox", default=str(DEFAULT_INBOX))
    parser.add_argument("--export-review", default=str(DEFAULT_EXPORT))
    parser.add_argument("--max-chunk-chars", type=int, default=2400)
    args = parser.parse_args()

    registry_path = _resolve_repo_path(args.registry)
    inbox = _resolve_repo_path(args.inbox)
    root = _resolve_repo_path(args.root)
    export_review = _resolve_repo_path(args.export_review)

    registry = load_registry(registry_path)
    inbox.mkdir(parents=True, exist_ok=True)
    files_by_url, inventory = discover_files(registry, inbox)

    marker_map = build_marker_map(registry)
    local_fetcher = OperatorImportArtifactFetcher(files_by_url)
    validating_fetcher = MarkerValidatingFetcher(marker_map, inner=local_fetcher)

    store = KnowledgeFactoryStore(root)
    result = PdnOfficialBatchRunner(
        store,
        fetcher=validating_fetcher,
        max_chunk_chars=args.max_chunk_chars,
    ).run(registry)
    exported = export_sanitized_review(store, result, export_review)
    observation_log = append_operator_observations(store, inventory, result.results)

    payload = {
        "registry_id": result.registry_id,
        "mode": "operator_assisted_official_import",
        "inbox": str(inbox),
        "supported_suffixes": list(SUPPORTED_SUFFIXES),
        "inventory": inventory,
        "counters": result.counters,
        "operator_observation_log": observation_log,
        "sanitized_export": exported,
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
