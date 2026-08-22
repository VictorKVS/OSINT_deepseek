from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REVIEW = STORE_ROOT / "review" / "batch_review_manifest.json"
REPORT_JSON = REPO_ROOT / "reports" / "pdn_live" / "D4_D5_STRUCTURE_QUALITY.json"
REPORT_MD = REPO_ROOT / "reports" / "pdn_live" / "D4_D5_STRUCTURE_QUALITY.md"
TARGETS = {
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
}


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    if not REVIEW.is_file():
        print(f"REVIEW_MISSING: {REVIEW}")
        return 2

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    documents = [item for item in review.get("documents", []) if item.get("document_id") in TARGETS]
    if len(documents) != len(TARGETS):
        print("QUALITY_INPUT_INCOMPLETE: expected four bounded Source Pack documents")
        return 2

    results: list[dict[str, object]] = []
    hard_failures = 0

    for item in documents:
        document_id = str(item["document_id"])
        structure_rel = item.get("structure_path")
        chunks_rel = item.get("chunks_path")
        if not structure_rel or not chunks_rel:
            results.append({
                "document_id": document_id,
                "status": "QUALITY_INPUT_MISSING",
                "semantic_extraction_performed": False,
            })
            hard_failures += 1
            continue

        structure_path = STORE_ROOT / str(structure_rel)
        chunks_path = STORE_ROOT / str(chunks_rel)
        nodes = _read_jsonl(structure_path)
        chunks = _read_jsonl(chunks_path)

        node_by_id = {str(node["node_id"]): node for node in nodes}
        node_types = Counter(str(node.get("node_type")) for node in nodes)
        locators = [str(node.get("locator")) for node in nodes]
        locator_counts = Counter(locators)
        duplicate_locators = sorted(locator for locator, count in locator_counts.items() if count > 1)

        orphan_nodes = [
            node
            for node in nodes
            if node.get("parent_node_id") is not None
            and str(node.get("parent_node_id")) not in node_by_id
        ]
        body_fallback_count = node_types.get("BODY", 0)

        points = [node for node in nodes if node.get("node_type") == "POINT"]
        point_parent_types = Counter(
            str(node_by_id.get(str(node.get("parent_node_id")), {}).get("node_type", "MISSING"))
            for node in points
        )

        article_points_outside_articles = 0
        if document_id == "DOC-RU-FZ-152-2006":
            article_points_outside_articles = sum(
                1
                for node in points
                if node_by_id.get(str(node.get("parent_node_id")), {}).get("node_type") != "ARTICLE"
            )

        chunk_node_ids = {str(chunk.get("structure_node_id")) for chunk in chunks}
        chunks_with_missing_node = sum(1 for node_id in chunk_node_ids if node_id not in node_by_id)

        failures: list[str] = []
        if body_fallback_count:
            failures.append("BODY_FALLBACK_PRESENT")
        if orphan_nodes:
            failures.append("ORPHAN_PARENT")
        if duplicate_locators:
            failures.append("DUPLICATE_LOCATOR")
        if chunks_with_missing_node:
            failures.append("CHUNK_PARENT_MISSING")
        if document_id == "DOC-RU-FZ-152-2006" and article_points_outside_articles:
            failures.append("ARTICLE_POINTS_OUTSIDE_ARTICLES")
        if not chunks:
            failures.append("ZERO_CHUNKS")

        status = "QUALITY_PASS" if not failures else "QUALITY_FAIL"
        if failures:
            hard_failures += 1

        results.append({
            "document_id": document_id,
            "status": status,
            "node_type_counts": dict(sorted(node_types.items())),
            "structure_nodes": len(nodes),
            "chunks": len(chunks),
            "point_parent_types": dict(sorted(point_parent_types.items())),
            "orphan_parent_count": len(orphan_nodes),
            "duplicate_locator_count": len(duplicate_locators),
            "duplicate_locators": duplicate_locators[:20],
            "body_fallback_count": body_fallback_count,
            "chunks_with_missing_node": chunks_with_missing_node,
            "article_points_outside_articles": article_points_outside_articles,
            "failures": failures,
            "semantic_extraction_performed": False,
        })

    summary = {
        "record_type": "D4_D5_STRUCTURE_QUALITY",
        "targets": len(TARGETS),
        "quality_pass": sum(item["status"] == "QUALITY_PASS" for item in results),
        "quality_fail": sum(item["status"] == "QUALITY_FAIL" for item in results),
        "quality_input_missing": sum(item["status"] == "QUALITY_INPUT_MISSING" for item in results),
        "semantic_extraction_performed": False,
        "promotion_to_d6_allowed": hard_failures == 0,
    }

    payload = {"summary": summary, "documents": results}
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# PDn D4-D5 structure quality",
        "",
        "This is a structural lineage gate only; no semantic/fact extraction is performed.",
        "",
        f"- targets: {summary['targets']}",
        f"- quality pass: {summary['quality_pass']}",
        f"- quality fail: {summary['quality_fail']}",
        f"- D6 promotion allowed: **{str(summary['promotion_to_d6_allowed']).lower()}**",
        "",
        "| Document | Status | Nodes | Chunks | BODY | Orphans | Duplicate locators | Article points outside articles |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in results:
        lines.append(
            f"| `{item['document_id']}` | {item['status']} | {item.get('structure_nodes', '—')} | "
            f"{item.get('chunks', '—')} | {item.get('body_fallback_count', '—')} | "
            f"{item.get('orphan_parent_count', '—')} | {item.get('duplicate_locator_count', '—')} | "
            f"{item.get('article_points_outside_articles', '—')} |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if hard_failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
