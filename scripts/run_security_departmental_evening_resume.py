from __future__ import annotations

import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import run_security_current_only_5stream_v2 as bulk
import run_security_departmental_5stream as departmental
import run_security_departmental_candidate_d4_d9 as shadow

QUEUE_FILE = REPO_ROOT / "config" / "security_departmental_acquisition_map.json"
REPORT_DIR = REPO_ROOT / "reports" / "security_current_only"
RESUME_QUEUE = REPORT_DIR / "_RUNTIME_DEPARTMENTAL_RESUME_QUEUE.json"
FINAL_REPORT = REPORT_DIR / "LATEST_DEPARTMENTAL_EVENING_RESUME.json"
WORKERS = 5
PREFLIGHT_TIMEOUT_SECONDS = 8.0


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").casefold().rstrip(".")


def _fetch_small(url: str) -> dict[str, object]:
    started = time.perf_counter()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "FATHER-KnowledgeFactory/0.4",
            "Range": "bytes=0-4095",
            "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=PREFLIGHT_TIMEOUT_SECONDS) as response:
            sample = response.read(4096)
            return {
                "status": "AVAILABLE",
                "http_status": int(getattr(response, "status", 200) or 200),
                "final_url": response.geturl(),
                "content_type": response.headers.get("Content-Type"),
                "sample_bytes": len(sample),
                "seconds": time.perf_counter() - started,
            }
    except Exception as exc:
        return {
            "status": "DEGRADED",
            "error": f"{type(exc).__name__}: {exc}",
            "seconds": time.perf_counter() - started,
        }


def _probe_pravo(documents: list[dict[str, object]]) -> dict[str, object]:
    urls = [
        str(row.get("official_source_url") or "").strip()
        for row in documents
        if _host(str(row.get("official_source_url") or "")) == "publication.pravo.gov.ru"
    ]
    urls = [url for url in urls if url][:3]
    attempts = [{"url": url, **_fetch_small(url)} for url in urls]
    available = sum(row.get("status") == "AVAILABLE" for row in attempts)
    return {
        "host": "publication.pravo.gov.ru",
        "status": "AVAILABLE" if available else "DEGRADED",
        "attempts_total": len(attempts),
        "available_attempts": available,
        "attempts": attempts,
    }


def _probe_a2_one(doc: dict[str, object]) -> dict[str, object]:
    document_id = str(doc.get("document_id") or "").strip()
    url = str(doc.get("status_reference_url") or "").strip()
    if not url or not bulk._working_reference_allowed(url):
        return {"document_id": document_id, "status": "NO_A2_ROUTE", "url": url or None}
    started = time.perf_counter()
    errors: list[str] = []
    data = b""
    mime = None
    final_url = url
    transport = None
    try:
        data, mime, final_url = bulk.base._fetch_urllib(url)
        transport = "urllib-reference"
    except Exception as exc:
        errors.append(f"urllib: {type(exc).__name__}: {exc}")
        try:
            data, mime, final_url = bulk.base._fetch_curl(url)
            transport = "curl-reference"
        except Exception as exc2:
            errors.append(f"curl: {type(exc2).__name__}: {exc2}")
            return {
                "document_id": document_id,
                "url": url,
                "status": "FETCH_FAILED",
                "errors": errors,
                "seconds": time.perf_counter() - started,
            }
    normalized, normalization = bulk.base._normalize(data, mime, final_url)
    passed, reason = bulk._reference_content_quality(normalized)
    return {
        "document_id": document_id,
        "url": url,
        "final_url": final_url,
        "transport": transport,
        "status": "CONTENT_QUALITY_PASS" if passed else "CONTENT_QUALITY_BLOCKED",
        "content_quality_pass": passed,
        "content_quality_reason": reason,
        "bytes": len(data),
        "normalized_chars": len((normalized or "").strip()),
        "normalization": normalization,
        "seconds": time.perf_counter() - started,
    }


def _probe_a2(documents: list[dict[str, object]]) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="a2-preflight") as executor:
        futures = [executor.submit(_probe_a2_one, doc) for doc in documents]
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda row: str(row.get("document_id") or ""))
    return {
        "routes_total": len(rows),
        "content_quality_pass": sum(row.get("status") == "CONTENT_QUALITY_PASS" for row in rows),
        "content_quality_blocked": sum(row.get("status") == "CONTENT_QUALITY_BLOCKED" for row in rows),
        "fetch_failed": sum(row.get("status") == "FETCH_FAILED" for row in rows),
        "no_a2_route": sum(row.get("status") == "NO_A2_ROUTE" for row in rows),
        "results": rows,
    }


def _has_full_quality_text(doc: dict[str, object]) -> tuple[bool, str | None]:
    document_id = str(doc.get("document_id") or "").strip()
    if not document_id:
        return False, None
    stem = bulk.base._safe_name(document_id)
    for meta_dir in (bulk.base.META_DIR, bulk.WORKING_META_DIR):
        meta_path = meta_dir / f"{stem}.json"
        meta = _read_json(meta_path, {}) or {}
        if not isinstance(meta, dict):
            continue
        normalized_path = str(meta.get("normalized_path") or "").strip()
        digest = str(meta.get("sha256") or "").strip().lower()
        if (
            meta.get("content_quality_pass") is True
            and normalized_path
            and (REPO_ROOT / normalized_path).is_file()
            and len(digest) == 64
        ):
            return True, meta_path.relative_to(REPO_ROOT).as_posix()
    return False, None


def _build_resume_queue(payload: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    documents = [row for row in payload.get("documents", []) if isinstance(row, dict)]
    targets: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    for doc in documents:
        complete, evidence = _has_full_quality_text(doc)
        if complete:
            skipped.append({
                "document_id": doc.get("document_id"),
                "reason": "FULL_QUALITY_TEXT_ALREADY_PRESENT",
                "evidence": evidence,
            })
        else:
            targets.append(doc)
    return targets, skipped


def _run_shadow_pass_only() -> dict[str, object]:
    acquisition = _read_json(departmental.REPORT, {}) or {}
    source_rows = [row for row in acquisition.get("results", []) if isinstance(row, dict)]
    targets = [
        row
        for row in source_rows
        if row.get("content_quality_pass") is True
        and str(row.get("status") or "") in {"NORMALIZED", "WORKING_COPY_NORMALIZED"}
        and str(row.get("normalized_path") or "").strip()
    ]
    excluded = [
        row for row in source_rows
        if row not in targets
    ]

    started = time.perf_counter()
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="dept-d4-d9") as executor:
        futures = [executor.submit(shadow._process, row) for row in targets]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"[SHADOW {result.get('status')}] {result.get('document_id')} "
                f"requirements={result.get('requirements', 0)} entities={result.get('entities', 0)}"
            )

    results.sort(key=lambda item: str(item.get("document_id") or ""))
    total_seconds = time.perf_counter() - started
    ready = sum(item.get("status") == "READY_D9_SHADOW_CANDIDATE" for item in results)
    failed = len(results) - ready
    summary = {
        "record_type": "SECURITY_DEPARTMENTAL_D4_D9_CANDIDATE_SUMMARY",
        "schema_version": "1.2",
        "observed_at": _utc_now(),
        "workers": WORKERS,
        "input_report": departmental.REPORT.relative_to(REPO_ROOT).as_posix(),
        "input_results_total": len(source_rows),
        "targets_total": len(targets),
        "excluded_non_pass_total": len(excluded),
        "ready_d9_shadow_candidates": ready,
        "failed_total": failed,
        "structure_nodes": sum(int(item.get("structure_nodes") or 0) for item in results),
        "chunks": sum(int(item.get("chunks") or 0) for item in results),
        "terms": sum(int(item.get("terms") or 0) for item in results),
        "definitions": sum(int(item.get("definitions") or 0) for item in results),
        "requirements": sum(int(item.get("requirements") or 0) for item in results),
        "entities": sum(int(item.get("entities") or 0) for item in results),
        "throughput_docs_per_second": ready / total_seconds if total_seconds > 0 else 0.0,
        "official_pipeline_advanced": False,
        "currentness_verified": False,
        "legal_truth_promoted": False,
        "kb_promotion_allowed": False,
        "review_required": True,
        "total_seconds": total_seconds,
        "results": results,
    }
    shadow.REPORT.parent.mkdir(parents=True, exist_ok=True)
    shadow.REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    started = time.perf_counter()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    queue_payload = _read_json(QUEUE_FILE, {}) or {}
    all_documents = [row for row in queue_payload.get("documents", []) if isinstance(row, dict)]

    print("[1/4] Preflight publication.pravo.gov.ru")
    pravo = _probe_pravo(all_documents)
    print(json.dumps(pravo, ensure_ascii=False, indent=2))

    print("[2/4] Preflight A2 reference content quality")
    a2 = _probe_a2(all_documents)
    print(json.dumps({k: v for k, v in a2.items() if k != "results"}, ensure_ascii=False, indent=2))

    targets, skipped = _build_resume_queue(queue_payload)
    resume_payload = {
        **queue_payload,
        "queue_id": f"{queue_payload.get('queue_id', 'SECURITY-DEPARTMENTAL')}-EVENING-RESUME",
        "resume_observed_at": _utc_now(),
        "documents": targets,
        "skipped_full_quality": skipped,
    }
    RESUME_QUEUE.write_text(json.dumps(resume_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"[3/4] Departmental acquisition: workers={WORKERS} targets={len(targets)} skipped_full_quality={len(skipped)}")
    original_queue = departmental.QUEUE_FILE
    try:
        departmental.QUEUE_FILE = RESUME_QUEUE
        acquisition_rc = departmental.main()
    finally:
        departmental.QUEUE_FILE = original_queue
    acquisition = _read_json(departmental.REPORT, {}) or {}

    print("[4/4] Shadow D4-D9 for content-quality PASS only")
    shadow_summary = _run_shadow_pass_only()

    official_acquired = int(acquisition.get("official_acquired_total") or 0)
    working_acquired = int(acquisition.get("working_copy_acquired_total") or 0)
    official_normalized = int(acquisition.get("official_normalized_total") or 0)
    working_normalized = int(acquisition.get("working_copy_normalized_total") or 0)
    content_blocked = int(acquisition.get("working_copy_content_blocked_total") or 0)
    downloaded = official_acquired + working_acquired
    normalized = official_normalized + working_normalized
    acquisition_seconds = float(acquisition.get("total_seconds") or 0.0)

    final = {
        "record_type": "SECURITY_DEPARTMENTAL_EVENING_RESUME",
        "schema_version": "1.0",
        "observed_at": _utc_now(),
        "workers": WORKERS,
        "source_queue_total": len(all_documents),
        "resume_queue_total": len(targets),
        "skipped_full_quality_total": len(skipped),
        "preflight": {
            "publication_pravo": pravo,
            "a2": a2,
        },
        "downloaded": downloaded,
        "official_downloaded": official_acquired,
        "a2_downloaded": working_acquired,
        "normalized": normalized,
        "content_blocked": content_blocked,
        "unresolved": int(acquisition.get("unresolved_total") or 0),
        "requirements": int(shadow_summary.get("requirements") or 0),
        "entities": int(shadow_summary.get("entities") or 0),
        "shadow_ready_documents": int(shadow_summary.get("ready_d9_shadow_candidates") or 0),
        "acquisition_throughput_operational_docs_per_second": float(acquisition.get("throughput_operational_docs_per_second") or 0.0),
        "acquisition_throughput_downloaded_docs_per_second": downloaded / acquisition_seconds if acquisition_seconds > 0 else 0.0,
        "shadow_throughput_docs_per_second": float(shadow_summary.get("throughput_docs_per_second") or 0.0),
        "acquisition_seconds": acquisition_seconds,
        "shadow_seconds": float(shadow_summary.get("total_seconds") or 0.0),
        "wall_seconds": time.perf_counter() - started,
        "current_promotions": 0,
        "currentness_verified": False,
        "kb_promotion_allowed": False,
        "legal_truth_policy": "No CURRENT promotion in this run. Exact official bytes and SHA-256 establish evidence identity only; amendment/replacement chain verification remains mandatory before CURRENT.",
        "acquisition_exit_code": acquisition_rc,
        "reports": {
            "acquisition": departmental.REPORT.relative_to(REPO_ROOT).as_posix(),
            "shadow_d4_d9": shadow.REPORT.relative_to(REPO_ROOT).as_posix(),
        },
    }
    FINAL_REPORT.write_text(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
