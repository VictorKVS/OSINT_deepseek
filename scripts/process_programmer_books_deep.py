from __future__ import annotations

import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import process_programming_kb_sources as source_processor  # noqa: E402
from father_osint.architecture_book_analyst import ArchitectureBookAnalyst  # noqa: E402
from father_osint.book_corpus import BookCorpusBuilder, BookSource  # noqa: E402

DATA_ROOT = ROOT / "data" / "programming_kb_sources"
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
DETAIL_ROOT = REPORT_ROOT / "deep_book_analysis"
LATEST = REPORT_ROOT / "LATEST_PROGRAMMER_BOOK_DEEP_ANALYSIS.json"
AGGREGATE = REPORT_ROOT / "PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def analyze_one(meta_path: Path) -> dict[str, Any]:
    started = time.perf_counter()
    meta = load_json(meta_path)
    target_id = str(meta.get("target_id") or meta_path.parent.name)
    local_ref = str(meta.get("local_path") or "").strip()
    local_path = ROOT / local_ref if local_ref else Path()

    if not local_ref or not local_path.is_file():
        return {
            "target_id": target_id,
            "status": "SOURCE_MISSING",
            "local_path": local_ref or None,
            "seconds": time.perf_counter() - started,
        }

    actual_sha = source_processor.sha256_file(local_path)
    expected_sha = str(meta.get("sha256") or "").strip().lower()
    if expected_sha and expected_sha != actual_sha:
        return {
            "target_id": target_id,
            "status": "SHA_MISMATCH",
            "local_path": local_ref,
            "expected_sha256": expected_sha,
            "actual_sha256": actual_sha,
            "seconds": time.perf_counter() - started,
        }

    try:
        text, extractor = source_processor.extract_text(local_path)
    except Exception as exc:
        return {
            "target_id": target_id,
            "status": "PARSER_GAP",
            "local_path": local_ref,
            "source_sha256": actual_sha,
            "error": f"{type(exc).__name__}: {exc}",
            "seconds": time.perf_counter() - started,
        }

    normalized = text.replace("\x00", "").strip()
    if len(normalized) < 100:
        return {
            "target_id": target_id,
            "status": "TEXT_TOO_SMALL",
            "local_path": local_ref,
            "source_sha256": actual_sha,
            "extractor": extractor,
            "characters": len(normalized),
            "seconds": time.perf_counter() - started,
        }

    source_language = str(meta.get("source_language") or "en")
    source = BookSource(
        title=str(meta.get("title") or target_id),
        authors=source_processor.author_list(meta.get("author")),
        source_language=source_language,
        target_language=source_language,
        edition=str(meta.get("edition")) if meta.get("edition") is not None else None,
        isbn=str(meta.get("isbn")) if meta.get("isbn") is not None else None,
        source_locator=str(meta.get("source_locator") or meta.get("resolved_url") or local_ref),
        source_sha256=actual_sha,
        rights_basis=str(meta.get("rights_basis") or "UNKNOWN_REVIEW_REQUIRED"),
        source_status="EXACT_BYTES_ACQUIRED",
        book_id=target_id,
    )

    corpus = BookCorpusBuilder().build(source, normalized)
    identity = {unit.unit_id: unit.source_text for unit in corpus.translation_units}
    corpus.apply_translations(identity, method="IDENTITY_SOURCE_LANGUAGE")
    corpus.build_semantic_structure()
    package = corpus.to_material_package(task_id=f"programmer-book-deep:{target_id}")
    analysis = ArchitectureBookAnalyst().analyze(package)

    detail = analysis.to_dict()
    detail["source"] = {
        "target_id": target_id,
        "title": source.title,
        "authors": source.authors,
        "source_language": source.source_language,
        "edition": source.edition,
        "isbn": source.isbn,
        "local_path": local_ref,
        "source_locator": source.source_locator,
        "source_sha256": actual_sha,
        "rights_basis": source.rights_basis,
        "extractor": extractor,
        "characters": len(normalized),
        "translation_units": corpus.counters["translation_units"],
        "semantic_units": corpus.counters["semantic_units"],
    }
    detail["kb_auto_promotion"] = False
    detail["review_gate"] = "MAIN_ANALYST_REVIEW_REQUIRED"

    DETAIL_ROOT.mkdir(parents=True, exist_ok=True)
    detail_path = DETAIL_ROOT / f"{target_id}.json"
    detail_path.write_text(
        json.dumps(detail, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    counters = analysis.counters
    return {
        "target_id": target_id,
        "status": "ANALYZED_REVIEW_REQUIRED",
        "title": source.title,
        "source_sha256": actual_sha,
        "local_path": local_ref,
        "extractor": extractor,
        "characters": len(normalized),
        "translation_units": corpus.counters["translation_units"],
        "semantic_units": corpus.counters["semantic_units"],
        "candidates_total": counters.get("candidates", 0),
        "candidate_type_counts": {
            key: value
            for key, value in counters.items()
            if key not in {"materials", "candidates"}
        },
        "detail_report": detail_path.relative_to(ROOT).as_posix(),
        "seconds": time.perf_counter() - started,
        "candidates": [candidate.to_dict() for candidate in analysis.candidates],
    }


def main() -> int:
    started = time.perf_counter()
    metas = sorted(DATA_ROOT.glob("*/source.json")) if DATA_ROOT.exists() else []
    results = [analyze_one(path) for path in metas]

    aggregate_candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    type_counts: Counter[str] = Counter()

    for row in results:
        target_id = str(row.get("target_id") or "")
        source_sha = str(row.get("source_sha256") or "")
        for candidate in row.pop("candidates", []) or []:
            candidate_type = str(candidate.get("candidate_type") or "UNKNOWN")
            statement = str(candidate.get("statement") or "")
            key = (candidate_type, _norm(statement), source_sha)
            if key in seen:
                continue
            seen.add(key)
            enriched = {
                **candidate,
                "target_id": target_id,
                "source_sha256": source_sha,
                "kb_auto_promotion": False,
                "review_status": "NEEDS_REVIEW",
            }
            aggregate_candidates.append(enriched)
            type_counts[candidate_type] += 1

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    aggregate_payload = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES",
        "knowledge_base_id": "PROGRAMMING_KB",
        "state": "REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "candidates_total": len(aggregate_candidates),
        "candidate_type_counts": dict(sorted(type_counts.items())),
        "candidates": aggregate_candidates,
    }
    AGGREGATE.write_text(
        json.dumps(aggregate_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    analyzed = sum(row.get("status") == "ANALYZED_REVIEW_REQUIRED" for row in results)
    parser_gaps = sum(row.get("status") == "PARSER_GAP" for row in results)
    missing = sum(row.get("status") == "SOURCE_MISSING" for row in results)
    integrity_failures = sum(row.get("status") == "SHA_MISMATCH" for row in results)
    too_small = sum(row.get("status") == "TEXT_TOO_SMALL" for row in results)
    elapsed = time.perf_counter() - started

    if analyzed > 0 and integrity_failures == 0:
        status = "PASS" if not (parser_gaps or missing or too_small) else "PASS_WITH_GAPS"
    else:
        status = "NO_PROCESSABLE_SOURCES" if analyzed == 0 and integrity_failures == 0 else "FAIL"

    summary = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_DEEP_ANALYSIS_RUN",
        "status": status,
        "sources_discovered_total": len(metas),
        "analyzed_total": analyzed,
        "source_missing_total": missing,
        "parser_gap_total": parser_gaps,
        "text_too_small_total": too_small,
        "integrity_failure_total": integrity_failures,
        "candidates_total": len(aggregate_candidates),
        "candidate_type_counts": dict(sorted(type_counts.items())),
        "kb_auto_promotion": False,
        "review_gate": "MAIN_ANALYST_REVIEW_REQUIRED",
        "aggregate_candidates": AGGREGATE.relative_to(ROOT).as_posix(),
        "elapsed_seconds": elapsed,
        "throughput_sources_per_second": analyzed / elapsed if elapsed > 0 else 0.0,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "results": results,
    }
    LATEST.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    compact = {key: value for key, value in summary.items() if key != "results"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Candidates: {AGGREGATE.relative_to(ROOT).as_posix()}")
    print(f"Report: {LATEST.relative_to(ROOT).as_posix()}")
    return 0 if status in {"PASS", "PASS_WITH_GAPS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
