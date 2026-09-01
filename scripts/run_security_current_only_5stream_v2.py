from __future__ import annotations

import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import run_security_current_only_5stream as base

REGISTRY = REPO_ROOT / "config" / "pdn_current_only_registry.json"
REPORT_DIR = REPO_ROOT / "reports" / "security_current_only"
OUT_ROOT = REPO_ROOT / "data" / "security_current_only"
WORKING_RAW_DIR = OUT_ROOT / "working_raw"
WORKING_NORMALIZED_DIR = OUT_ROOT / "working_normalized"
WORKING_META_DIR = OUT_ROOT / "working_metadata"
WORKERS = 5

OFFICIAL_ROUTE_OVERRIDES: dict[str, list[str]] = {
    "DOC-RU-PP-687-2008": ["https://government.ru/docs/all/65436/"],
    "DOC-RU-RKN-178-2022": ["https://publication.pravo.gov.ru/document/0001202211290004"],
    "DOC-RU-RKN-179-2022": ["https://publication.pravo.gov.ru/document/0001202211290008"],
    "DOC-RU-RKN-180-2022": ["https://publication.pravo.gov.ru/document/0001202212150022"],
    "DOC-RU-RKN-187-2022": ["https://publication.pravo.gov.ru/document/0001202212280052"],
    "DOC-RU-FSTEC-137-2026": ["https://publication.pravo.gov.ru/document/0001202608110006"],
    "DOC-RU-FZ-149-2006": ["https://government.ru/docs/all/98199/"],
    "DOC-RU-FZ-323-2011": ["https://government.ru/docs/all/100186/"],
}

WORKING_REFERENCE_HOSTS = {
    "minjust.consultant.ru",
    "www.consultant.ru",
    "consultant.ru",
    "normativ.kontur.ru",
    "www.garant.ru",
    "garant.ru",
}

REFERENCE_CONTENT_BLOCK_MARKERS = (
    "документ в некоммерческой версии консультантплюс доступен по расписанию",
    "этот документ в некоммерческой версии консультантплюс доступен по расписанию",
    "тексты документов всегда доступны в коммерческой версии консультантплюс",
    "вы можете заказать документ на e-mail",
    "откройте документ в системе консультантплюс",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").casefold().rstrip(".")


def _working_reference_allowed(url: str) -> bool:
    host = _host(url)
    return any(host == allowed or host.endswith("." + allowed) for allowed in WORKING_REFERENCE_HOSTS)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = str(value or "").strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _official_routes(doc: dict[str, object]) -> list[str]:
    document_id = str(doc.get("document_id") or "")
    routes: list[str] = []
    configured = str(doc.get("official_source_url") or "").strip()
    if configured and base._is_official(configured):
        routes.append(configured)
    routes.extend(OFFICIAL_ROUTE_OVERRIDES.get(document_id, []))
    return _dedupe(routes)


def _reference_content_quality(normalized: str | None) -> tuple[bool, str]:
    if normalized is None or not normalized.strip():
        return False, "NO_NORMALIZED_TEXT"
    text = normalized.strip()
    folded = text.casefold().replace("ё", "е")
    if any(marker in folded for marker in REFERENCE_CONTENT_BLOCK_MARKERS):
        return False, "REFERENCE_ACCESS_WINDOW_BLOCKED"
    if len(text) < 600:
        return False, "REFERENCE_TEXT_TOO_SHORT"
    legal_anchor = any(
        marker in folded
        for marker in ("приказ", "постановление", "федеральный закон", "распоряжение")
    )
    operative_anchor = any(
        marker in folded
        for marker in ("приказываю", "постановляет", "утвердить", "определить", "в соответствии", "настоящ")
    )
    if not (legal_anchor and operative_anchor):
        return False, "REFERENCE_LEGAL_BODY_NOT_CONFIRMED"
    return True, "PASS"


def _save_working_copy(
    doc: dict[str, object],
    *,
    data: bytes,
    mime: str | None,
    final_url: str,
    transport: str,
    started: float,
    official_attempts: list[dict[str, object]],
) -> dict[str, object]:
    document_id = str(doc.get("document_id") or "").strip()
    digest = hashlib.sha256(data).hexdigest()
    stem = base._safe_name(document_id)
    WORKING_RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = WORKING_RAW_DIR / f"{stem}__{digest}.bin"
    if not raw_path.exists():
        raw_path.write_bytes(data)
    if hashlib.sha256(raw_path.read_bytes()).hexdigest() != digest:
        raise RuntimeError("working-copy post-write SHA-256 mismatch")

    normalized, normalization = base._normalize(data, mime, final_url)
    normalized_path: Path | None = None
    if normalized is not None and normalized.strip():
        WORKING_NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
        normalized_path = WORKING_NORMALIZED_DIR / f"{stem}__{digest}.txt"
        normalized_path.write_text(normalized.strip() + "\n", encoding="utf-8")

    content_quality_pass, content_quality_reason = _reference_content_quality(normalized)
    if normalized_path and content_quality_pass:
        status = "WORKING_COPY_NORMALIZED"
    elif normalized_path:
        status = "WORKING_COPY_CONTENT_BLOCKED"
    else:
        status = "WORKING_COPY_RAW"

    result: dict[str, object] = {
        "document_id": document_id,
        "title": doc.get("title"),
        "started_at": _utc_now(),
        "legal_status": doc.get("legal_status"),
        "status": status,
        "trust_tier": "A2_REFERENCE_WORKING_COPY",
        "legal_truth_eligible": False,
        "kb_promotion_allowed": False,
        "source_url": final_url,
        "transport": transport,
        "mime_type": mime,
        "byte_length": len(data),
        "sha256": digest,
        "raw_path": raw_path.relative_to(REPO_ROOT).as_posix(),
        "normalized_path": normalized_path.relative_to(REPO_ROOT).as_posix() if normalized_path else None,
        "normalization": normalization,
        "content_quality_pass": content_quality_pass,
        "content_quality_reason": content_quality_reason,
        "operationally_available": bool(normalized_path and content_quality_pass),
        "official_attempts": official_attempts,
        "seconds": time.perf_counter() - started,
    }
    WORKING_META_DIR.mkdir(parents=True, exist_ok=True)
    (WORKING_META_DIR / f"{stem}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def _process(doc: dict[str, object]) -> dict[str, object]:
    started = time.perf_counter()
    document_id = str(doc.get("document_id") or "").strip()
    official_attempts: list[dict[str, object]] = []

    for url in _official_routes(doc):
        attempt_started = time.perf_counter()
        try:
            data, mime, final_url, transport = base._fetch(url)
            if not base._is_official(final_url):
                raise RuntimeError(f"redirected off official allowlist: {final_url}")

            digest = hashlib.sha256(data).hexdigest()
            stem = base._safe_name(document_id)
            raw_path = base.RAW_DIR / f"{stem}__{digest}.bin"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            if not raw_path.exists():
                raw_path.write_bytes(data)
            if hashlib.sha256(raw_path.read_bytes()).hexdigest() != digest:
                raise RuntimeError("post-write SHA-256 mismatch")

            normalized, normalization = base._normalize(data, mime, final_url)
            normalized_path: Path | None = None
            if normalized is not None and normalized.strip():
                normalized_path = base.NORMALIZED_DIR / f"{stem}__{digest}.txt"
                normalized_path.parent.mkdir(parents=True, exist_ok=True)
                normalized_path.write_text(normalized.strip() + "\n", encoding="utf-8")

            result: dict[str, object] = {
                "document_id": document_id,
                "title": doc.get("title"),
                "started_at": _utc_now(),
                "legal_status": doc.get("legal_status"),
                "status": "NORMALIZED" if normalized_path else "ACQUIRED_RAW",
                "trust_tier": "A0_A1_OFFICIAL_ROUTE",
                "legal_truth_eligible": True,
                "source_url": final_url,
                "transport": transport,
                "mime_type": mime,
                "byte_length": len(data),
                "sha256": digest,
                "raw_path": raw_path.relative_to(REPO_ROOT).as_posix(),
                "normalized_path": normalized_path.relative_to(REPO_ROOT).as_posix() if normalized_path else None,
                "normalization": normalization,
                "content_quality_pass": True,
                "content_quality_reason": "OFFICIAL_EXACT_BYTES",
                "operationally_available": True,
                "official_attempts": official_attempts,
                "seconds": time.perf_counter() - started,
            }
            base.META_DIR.mkdir(parents=True, exist_ok=True)
            (base.META_DIR / f"{stem}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            return result
        except Exception as exc:
            official_attempts.append(
                {
                    "url": url,
                    "status": "FAILED",
                    "error": f"{type(exc).__name__}: {exc}",
                    "seconds": time.perf_counter() - attempt_started,
                }
            )

    reference_url = str(doc.get("status_reference_url") or "").strip()
    if reference_url and _working_reference_allowed(reference_url):
        try:
            data, mime, final_url = base._fetch_urllib(reference_url)
            if not _working_reference_allowed(final_url):
                raise RuntimeError(f"working reference redirected off allowlist: {final_url}")
            return _save_working_copy(
                doc,
                data=data,
                mime=mime,
                final_url=final_url,
                transport="urllib-reference",
                started=started,
                official_attempts=official_attempts,
            )
        except Exception as urllib_exc:
            try:
                data, mime, final_url = base._fetch_curl(reference_url)
                if not _working_reference_allowed(final_url):
                    raise RuntimeError(f"working reference redirected off allowlist: {final_url}")
                return _save_working_copy(
                    doc,
                    data=data,
                    mime=mime,
                    final_url=final_url,
                    transport="curl-reference",
                    started=started,
                    official_attempts=official_attempts,
                )
            except Exception as curl_exc:
                return {
                    "document_id": document_id,
                    "title": doc.get("title"),
                    "legal_status": doc.get("legal_status"),
                    "status": "UNRESOLVED",
                    "legal_truth_eligible": False,
                    "official_attempts": official_attempts,
                    "reference_url": reference_url,
                    "reference_error": (
                        f"urllib: {type(urllib_exc).__name__}: {urllib_exc}; "
                        f"curl: {type(curl_exc).__name__}: {curl_exc}"
                    ),
                    "seconds": time.perf_counter() - started,
                }

    return {
        "document_id": document_id,
        "title": doc.get("title"),
        "legal_status": doc.get("legal_status"),
        "status": "UNRESOLVED",
        "legal_truth_eligible": False,
        "official_attempts": official_attempts,
        "reason": "no reachable official route and no approved working-reference route",
        "seconds": time.perf_counter() - started,
    }


def main() -> int:
    started = time.perf_counter()
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    documents = list(payload.get("documents") or [])
    queue = [
        doc
        for doc in documents
        if isinstance(doc, dict) and str(doc.get("download_status") or "") != "LOCAL_A0_AVAILABLE"
    ]

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="security-kb-v2") as executor:
        futures = {executor.submit(_process, doc): doc for doc in queue}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"[{result.get('status')}] {result.get('document_id')} {result.get('sha256') or ''}")

    results.sort(key=lambda row: str(row.get("document_id") or ""))
    total_seconds = time.perf_counter() - started
    official_acquired = sum(row.get("status") in {"NORMALIZED", "ACQUIRED_RAW"} for row in results)
    official_normalized = sum(row.get("status") == "NORMALIZED" for row in results)
    working_acquired = sum(row.get("status") in {"WORKING_COPY_NORMALIZED", "WORKING_COPY_RAW", "WORKING_COPY_CONTENT_BLOCKED"} for row in results)
    working_normalized = sum(row.get("status") == "WORKING_COPY_NORMALIZED" for row in results)
    working_content_blocked = sum(row.get("status") == "WORKING_COPY_CONTENT_BLOCKED" for row in results)
    unresolved = sum(row.get("status") == "UNRESOLVED" for row in results)
    completed_operationally = official_acquired + working_normalized

    summary = {
        "record_type": "SECURITY_CURRENT_ONLY_5STREAM_RUN_V2",
        "observed_at": _utc_now(),
        "workers": WORKERS,
        "registry": REGISTRY.relative_to(REPO_ROOT).as_posix(),
        "registry_documents_total": len(documents),
        "queue_total": len(queue),
        "official_acquired_total": official_acquired,
        "official_normalized_total": official_normalized,
        "working_copy_acquired_total": working_acquired,
        "working_copy_normalized_total": working_normalized,
        "working_copy_content_blocked_total": working_content_blocked,
        "operationally_available_total": completed_operationally,
        "unresolved_total": unresolved,
        "official_coverage_ratio": official_acquired / len(queue) if queue else 1.0,
        "operational_coverage_ratio": completed_operationally / len(queue) if queue else 1.0,
        "throughput_operational_docs_per_second": completed_operationally / total_seconds if total_seconds > 0 else 0.0,
        "speedup_vs_1_stream_pct": None,
        "speedup_note": "No 1-stream baseline is claimed until measured on the same queue and workstation.",
        "legal_truth_policy": "Only NORMALIZED/ACQUIRED_RAW from official routes are legal-truth eligible. A2 references must also pass content-quality gating before they are operationally usable.",
        "total_seconds": total_seconds,
        "results": results,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "LATEST_5STREAM_RUN_V2.json"
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if unresolved == 0 and working_content_blocked == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
