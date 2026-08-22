from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REVIEW = STORE_ROOT / "review" / "batch_review_manifest.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D4_D5_ARTICLE_POINT_NORMALIZATION.json"
AUDIT = STORE_ROOT / "review" / "d4_d5_normalization_audit.jsonl"
TARGET_DOCUMENT_ID = "DOC-RU-FZ-152-2006"
NORMALIZER_VERSION = "article-point-parent-v1"
_POINT_TITLE_RE = re.compile(r"^Пункт\s+(.+?)\s*$", re.IGNORECASE)
_CHUNK_INDEX_RE = re.compile(r"/chunk:(\d+)$")


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]
    return f"{prefix}-{digest}"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def normalize_article_point_hierarchy(
    nodes: list[dict[str, object]],
    chunks: list[dict[str, object]],
    *,
    document_id: str,
    version_id: str,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Normalize federal-law numbered points under their containing article.

    The preliminary parser emits nodes in source order. For an article-based
    federal law, a numbered point after an ARTICLE and before the next
    ARTICLE/CHAPTER/SECTION belongs to that article. Numeric nodes occurring
    before the first article are treated as surrounding-page noise and are
    excluded from D4/D5 projection while the exact acquired HTML and extracted
    text remain unchanged.
    """

    current_article: dict[str, object] | None = None
    point_occurrences: Counter[tuple[str, str]] = Counter()
    old_to_new_node_id: dict[str, str] = {}
    old_to_new_locator: dict[str, str] = {}
    removed_node_ids: set[str] = set()
    normalized_nodes: list[dict[str, object]] = []
    reparented_points = 0
    removed_pre_article_points = 0

    for source_node in nodes:
        node = dict(source_node)
        node_type = str(node.get("node_type", ""))

        if node_type in {"CHAPTER", "SECTION"}:
            current_article = None
            normalized_nodes.append(node)
            continue

        if node_type == "ARTICLE":
            current_article = node
            normalized_nodes.append(node)
            continue

        if node_type != "POINT":
            normalized_nodes.append(node)
            continue

        old_node_id = str(node["node_id"])
        if current_article is None:
            removed_node_ids.add(old_node_id)
            removed_pre_article_points += 1
            continue

        title = str(node.get("title", ""))
        match = _POINT_TITLE_RE.match(title)
        if not match:
            raise ValueError(f"cannot recover point number from title: {title!r}")
        point_number = match.group(1).strip()
        article_locator = str(current_article["locator"])
        occurrence_key = (article_locator, point_number)
        point_occurrences[occurrence_key] += 1
        occurrence = point_occurrences[occurrence_key]
        new_locator = f"{article_locator}/point:{point_number}"
        if occurrence > 1:
            new_locator += f"#{occurrence}"

        text = str(node.get("text", ""))
        content = f"{title}\n{text}".strip()
        new_node_id = _stable_id("STR", document_id, version_id, new_locator, content)
        old_to_new_node_id[old_node_id] = new_node_id
        old_to_new_locator[str(node.get("locator", ""))] = new_locator

        if node.get("parent_node_id") != current_article["node_id"] or node.get("locator") != new_locator:
            reparented_points += 1
        node["parent_node_id"] = current_article["node_id"]
        node["locator"] = new_locator
        node["node_id"] = new_node_id
        normalized_nodes.append(node)

    normalized_node_by_id = {str(node["node_id"]): node for node in normalized_nodes}
    normalized_chunks: list[dict[str, object]] = []
    rewritten_chunks = 0
    removed_noise_chunks = 0

    for source_chunk in chunks:
        chunk = dict(source_chunk)
        old_structure_node_id = str(chunk.get("structure_node_id", ""))
        if old_structure_node_id in removed_node_ids:
            removed_noise_chunks += 1
            continue

        new_structure_node_id = old_to_new_node_id.get(old_structure_node_id)
        if new_structure_node_id is None:
            normalized_chunks.append(chunk)
            continue

        target_node = normalized_node_by_id[new_structure_node_id]
        old_chunk_locator = str(chunk.get("locator", ""))
        chunk_match = _CHUNK_INDEX_RE.search(old_chunk_locator)
        if not chunk_match:
            raise ValueError(f"cannot recover chunk index from locator: {old_chunk_locator!r}")
        chunk_index = chunk_match.group(1)
        new_chunk_locator = f"{target_node['locator']}/chunk:{chunk_index}"
        text = str(chunk.get("text", ""))
        chunk["structure_node_id"] = new_structure_node_id
        chunk["locator"] = new_chunk_locator
        chunk["chunk_id"] = _stable_id("CHK", document_id, version_id, new_chunk_locator, text)
        normalized_chunks.append(chunk)
        rewritten_chunks += 1

    node_by_id = {str(node["node_id"]): node for node in normalized_nodes}
    points = [node for node in normalized_nodes if node.get("node_type") == "POINT"]
    points_outside_articles = sum(
        1
        for node in points
        if node_by_id.get(str(node.get("parent_node_id")), {}).get("node_type") != "ARTICLE"
    )
    locator_counts = Counter(str(node.get("locator")) for node in normalized_nodes)
    duplicate_locators = sorted(locator for locator, count in locator_counts.items() if count > 1)
    missing_chunk_nodes = sum(
        1 for chunk in normalized_chunks if str(chunk.get("structure_node_id")) not in node_by_id
    )

    stats: dict[str, object] = {
        "normalizer_version": NORMALIZER_VERSION,
        "reparented_points": reparented_points,
        "removed_pre_article_points": removed_pre_article_points,
        "rewritten_chunks": rewritten_chunks,
        "removed_noise_chunks": removed_noise_chunks,
        "points_outside_articles_after": points_outside_articles,
        "duplicate_locators_after": duplicate_locators,
        "chunks_with_missing_node_after": missing_chunk_nodes,
        "semantic_extraction_performed": False,
    }
    if points_outside_articles or duplicate_locators or missing_chunk_nodes:
        raise ValueError(f"normalization invariant failed: {stats}")

    return normalized_nodes, normalized_chunks, stats


def main() -> int:
    if not REVIEW.is_file():
        print(f"REVIEW_MISSING: {REVIEW}")
        return 2

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    target = next(
        (item for item in review.get("documents", []) if item.get("document_id") == TARGET_DOCUMENT_ID),
        None,
    )
    if not target or target.get("status") != "READY_D5":
        print("TARGET_NOT_READY_D5: run RUN_PDN_OFFICIAL_SOURCE_PACK_D4_D5.cmd first")
        return 2

    structure_rel = target.get("structure_path")
    chunks_rel = target.get("chunks_path")
    manifest_rel = target.get("manifest_path")
    version_id = target.get("version_id")
    if not structure_rel or not chunks_rel or not manifest_rel or not version_id:
        print("NORMALIZATION_INPUT_INCOMPLETE")
        return 2

    structure_path = STORE_ROOT / str(structure_rel)
    chunks_path = STORE_ROOT / str(chunks_rel)
    manifest_path = STORE_ROOT / str(manifest_rel)
    if not structure_path.is_file() or not chunks_path.is_file() or not manifest_path.is_file():
        print("NORMALIZATION_INPUT_FILES_MISSING")
        return 2

    before_structure = structure_path.read_bytes()
    before_chunks = chunks_path.read_bytes()
    nodes = _read_jsonl(structure_path)
    chunks = _read_jsonl(chunks_path)

    backup_structure = structure_path.with_name("structure.pre_article_point_parent_v1.jsonl")
    backup_chunks = chunks_path.with_name("chunks.pre_article_point_parent_v1.jsonl")
    shutil.copyfile(structure_path, backup_structure)
    shutil.copyfile(chunks_path, backup_chunks)

    try:
        normalized_nodes, normalized_chunks, stats = normalize_article_point_hierarchy(
            nodes,
            chunks,
            document_id=TARGET_DOCUMENT_ID,
            version_id=str(version_id),
        )
    except (KeyError, ValueError) as exc:
        print(f"NORMALIZATION_FAILED: {exc}")
        return 2

    _write_jsonl(structure_path, normalized_nodes)
    _write_jsonl(chunks_path, normalized_chunks)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["structure_nodes"] = len(normalized_nodes)
    manifest["chunks"] = len(normalized_chunks)
    manifest["structure_normalizer_version"] = NORMALIZER_VERSION
    manifest["structure_normalization"] = stats
    manifest["semantic_extraction_performed"] = False
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    after_structure = structure_path.read_bytes()
    after_chunks = chunks_path.read_bytes()
    result = {
        "record_type": "D4_D5_STRUCTURE_NORMALIZATION",
        "document_id": TARGET_DOCUMENT_ID,
        "version_id": str(version_id),
        "normalizer_version": NORMALIZER_VERSION,
        "structure_sha256_before": _sha256_bytes(before_structure),
        "structure_sha256_after": _sha256_bytes(after_structure),
        "chunks_sha256_before": _sha256_bytes(before_chunks),
        "chunks_sha256_after": _sha256_bytes(after_chunks),
        "structure_nodes_before": len(nodes),
        "structure_nodes_after": len(normalized_nodes),
        "chunks_before": len(chunks),
        "chunks_after": len(normalized_chunks),
        "backup_structure": backup_structure.relative_to(STORE_ROOT).as_posix(),
        "backup_chunks": backup_chunks.relative_to(STORE_ROOT).as_posix(),
        **stats,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
