from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.benchmark_152_prebuilt_mcp_db import DB_PATH
from scripts.benchmark_152_reuse import TARGET_ID, TARGET_NUMBER, TARGET_TITLE_MARKER, _compare, _father_reference

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REVIEW = STORE_ROOT / "review" / "batch_review_manifest.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "AUDIT_152_PREBUILT_DB_SEMANTICS.json"
HOT_ITERATIONS = 100
ARTICLE_LOCATOR_RE = re.compile(r"(?:^|/)article:(\d+(?:\.\d+)?)", re.IGNORECASE)
ARTICLE_VALUE_RE = re.compile(r"(\d+(?:\.\d+)?)")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _father_articles() -> tuple[dict[str, str], dict[str, object]]:
    if not REVIEW.is_file():
        raise RuntimeError("FATHER review manifest missing")
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    item = next((x for x in review.get("documents", []) if x.get("document_id") == TARGET_ID), None)
    if not item:
        raise RuntimeError("152-ФЗ missing from FATHER review manifest")
    chunks_path = STORE_ROOT / str(item.get("chunks_path") or "")
    if not chunks_path.is_file():
        raise RuntimeError(f"FATHER chunks missing: {chunks_path}")
    grouped: dict[str, list[str]] = defaultdict(list)
    for chunk in _read_jsonl(chunks_path):
        locator = str(chunk.get("locator") or "")
        match = ARTICLE_LOCATOR_RE.search(locator)
        if not match:
            continue
        text = str(chunk.get("text") or "").strip()
        if text:
            grouped[match.group(1)].append(text)
    articles = {key: "\n".join(values) for key, values in grouped.items()}
    return articles, {
        "chunks_path": str(item.get("chunks_path")),
        "artifact_sha256": item.get("artifact_sha256"),
        "version_id": item.get("version_id"),
        "article_keys": sorted(articles, key=lambda x: [int(p) for p in x.split('.')]),
    }


def _normalize_article(value: object) -> str | None:
    match = ARTICLE_VALUE_RE.search(str(value or ""))
    return match.group(1) if match else None


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * p))
    return ordered[index]


def _hot_query(conn: sqlite3.Connection, law_id: str) -> tuple[float, int]:
    started = time.perf_counter()
    rows = conn.execute(
        "SELECT article, title, content, provision_ref, order_index "
        "FROM provisions WHERE law_id = ? ORDER BY order_index, id",
        (law_id,),
    ).fetchall()
    return time.perf_counter() - started, len(rows)


def main() -> int:
    total_started = time.perf_counter()
    if not DB_PATH.is_file():
        print(f"PREBUILT_DB_MISSING: {DB_PATH}")
        return 2

    father_text, _ = _father_reference()
    father_articles, father_meta = _father_articles()

    conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        integrity_started = time.perf_counter()
        quick_check = conn.execute("PRAGMA quick_check").fetchone()[0]
        integrity_seconds = time.perf_counter() - integrity_started
        if quick_check != "ok":
            raise RuntimeError(f"SQLITE_QUICK_CHECK_FAILED: {quick_check}")

        law = conn.execute(
            "SELECT id, title, identifier, law_type, status, effective_date, publication_date, "
            "source_url, last_amended, last_updated, provision_count "
            "FROM laws WHERE identifier = ? OR title LIKE ? ORDER BY provision_count DESC LIMIT 1",
            (TARGET_NUMBER, f"%{TARGET_TITLE_MARKER}%"),
        ).fetchone()
        if law is None:
            raise RuntimeError("152_FZ_NOT_FOUND_IN_PREBUILT_DB")
        law_payload = dict(law)

        rows = conn.execute(
            "SELECT id, article, title, content, provision_ref, order_index, metadata "
            "FROM provisions WHERE law_id = ? ORDER BY order_index, id",
            (law["id"],),
        ).fetchall()
        if not rows:
            raise RuntimeError("152_FZ_HAS_NO_PROVISIONS_IN_PREBUILT_DB")

        hot_samples: list[float] = []
        hot_rows = 0
        for _ in range(HOT_ITERATIONS):
            elapsed, hot_rows = _hot_query(conn, str(law["id"]))
            hot_samples.append(elapsed)

        exact_hashes = Counter(_sha256_text(str(row["content"] or "")) for row in rows)
        duplicate_content_rows = sum(count - 1 for count in exact_hashes.values() if count > 1)
        duplicate_provision_refs = {
            key: count
            for key, count in Counter(str(row["provision_ref"] or "") for row in rows).items()
            if key and count > 1
        }

        by_article: dict[str, list[str]] = defaultdict(list)
        row_diagnostics: list[dict[str, object]] = []
        for row in rows:
            article_key = _normalize_article(row["article"])
            content = str(row["content"] or "").strip()
            if article_key and content:
                by_article[article_key].append(content)
            row_diagnostics.append({
                "id": row["id"],
                "article_raw": row["article"],
                "article_key": article_key,
                "provision_ref": row["provision_ref"],
                "order_index": row["order_index"],
                "chars": len(content),
                "sha256": _sha256_text(content),
                "title": row["title"],
            })

        article_comparisons: list[dict[str, object]] = []
        for article_key in sorted(set(father_articles) & set(by_article), key=lambda x: [int(p) for p in x.split('.')]):
            external_unique: list[str] = []
            seen: set[str] = set()
            for content in by_article[article_key]:
                digest = _sha256_text(content)
                if digest not in seen:
                    seen.add(digest)
                    external_unique.append(content)
            external_text = "\n".join(external_unique)
            metrics = _compare(father_articles[article_key], external_text)
            article_comparisons.append({
                "article": article_key,
                "external_rows": len(by_article[article_key]),
                "external_unique_rows": len(external_unique),
                "father_chars": len(father_articles[article_key]),
                "external_chars": len(external_text),
                "sequence_ratio": metrics["sequence_ratio"],
                "five_token_shingle_jaccard": metrics["five_token_shingle_jaccard"],
            })

        ratios = [float(item["sequence_ratio"]) for item in article_comparisons]
        high_match = sum(1 for value in ratios if value >= 0.90)
        medium_match = sum(1 for value in ratios if 0.60 <= value < 0.90)
        low_match = sum(1 for value in ratios if value < 0.60)

        full_external_text = "\n".join(str(row["content"] or "") for row in rows if str(row["content"] or "").strip())
        full_metrics = _compare(father_text, full_external_text)
        declared_count = int(law["provision_count"] or 0)
        retrieved_count = len(rows)
        version_scope_mismatch = (
            str(law["status"] or "").casefold() in {"amended", "in_force", "effective"}
            and str(law["last_updated"] or "") > "2006-07-27"
        )

        result = {
            "record_type": "AUDIT_152_PREBUILT_DB_SEMANTICS",
            "target_document_id": TARGET_ID,
            "database": {
                "path": DB_PATH.relative_to(REPO_ROOT).as_posix(),
                "bytes": DB_PATH.stat().st_size,
                "quick_check": quick_check,
                "integrity_check_seconds": integrity_seconds,
            },
            "law": law_payload,
            "father": father_meta,
            "semantic_findings": {
                "declared_provision_count": declared_count,
                "retrieved_provision_rows": retrieved_count,
                "provision_count_consistent": declared_count == retrieved_count,
                "external_article_keys": sorted(by_article, key=lambda x: [int(p) for p in x.split('.')]),
                "father_article_keys": father_meta["article_keys"],
                "matched_article_keys": len(article_comparisons),
                "duplicate_content_rows": duplicate_content_rows,
                "duplicate_provision_refs": duplicate_provision_refs,
                "version_scope_mismatch_with_father_base_publication": version_scope_mismatch,
                "external_status": law["status"],
                "external_last_updated": law["last_updated"],
                "father_reference_scope": "official publication snapshot / base 2006 artifact",
            },
            "whole_document_comparison": full_metrics,
            "article_comparison_summary": {
                "matched_articles": len(article_comparisons),
                "sequence_ratio_median": statistics.median(ratios) if ratios else None,
                "sequence_ratio_p25": _percentile(ratios, 0.25) if ratios else None,
                "sequence_ratio_p75": _percentile(ratios, 0.75) if ratios else None,
                "high_match_ge_0_90": high_match,
                "medium_match_0_60_0_90": medium_match,
                "low_match_lt_0_60": low_match,
            },
            "article_comparisons": article_comparisons,
            "provision_rows": row_diagnostics,
            "hot_path": {
                "iterations": HOT_ITERATIONS,
                "rows_per_query": hot_rows,
                "query_p50_ms": statistics.median(hot_samples) * 1000,
                "query_p95_ms": _percentile(hot_samples, 0.95) * 1000,
                "query_min_ms": min(hot_samples) * 1000,
                "query_max_ms": max(hot_samples) * 1000,
                "integrity_check_excluded_from_hot_path": True,
            },
            "architecture_interpretation": {
                "reference_db_role": "REFERENCE_KB_NOT_A0_PROOF",
                "whole_document_similarity_is_not_a_valid_quality_gate_when_versions_differ": True,
                "integrity_validation_belongs_to_import_hash_boundary_not_every_read": True,
                "next_gate": "decide donor adoption from per-article quality + hot-path latency",
                "legal_truth_promoted": False,
            },
            "total_seconds": time.perf_counter() - total_started,
        }

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()
        print(f"DB_INTEGRITY={quick_check}")
        print(f"PROVISION_COUNT_DECLARED={declared_count}")
        print(f"PROVISION_ROWS_RETRIEVED={retrieved_count}")
        print(f"MATCHED_ARTICLES={len(article_comparisons)}")
        print(f"ARTICLE_SEQUENCE_MEDIAN={statistics.median(ratios) if ratios else 0.0:.6f}")
        print(f"HIGH_MATCH_ARTICLES={high_match}")
        print(f"DUPLICATE_CONTENT_ROWS={duplicate_content_rows}")
        print(f"HOT_QUERY_P50_MS={statistics.median(hot_samples) * 1000:.3f}")
        print(f"HOT_QUERY_P95_MS={_percentile(hot_samples, 0.95) * 1000:.3f}")
        print(f"VERSION_SCOPE_MISMATCH={str(version_scope_mismatch).lower()}")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
