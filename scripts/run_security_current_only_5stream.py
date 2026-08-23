from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import subprocess
import time
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "config" / "pdn_current_only_registry.json"
OUT_ROOT = REPO_ROOT / "data" / "security_current_only"
RAW_DIR = OUT_ROOT / "raw"
NORMALIZED_DIR = OUT_ROOT / "normalized"
META_DIR = OUT_ROOT / "metadata"
REPORT_DIR = REPO_ROOT / "reports" / "security_current_only"
WORKERS = 5
TIMEOUT_SECONDS = 15
MAX_BYTES = 50 * 1024 * 1024

OFFICIAL_HOSTS = {
    "publication.pravo.gov.ru",
    "pravo.gov.ru",
    "government.ru",
    "rg.ru",
    "www.rg.ru",
    "fstec.ru",
    "www.fstec.ru",
    "fsb.ru",
    "www.fsb.ru",
    "rkn.gov.ru",
    "pd.rkn.gov.ru",
    "minzdrav.gov.ru",
    "digital.gov.ru",
}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text:
            self.parts.append(text)

    def text(self) -> str:
        return "\n".join(self.parts)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return value.strip("._") or "document"


def _is_official(url: str) -> bool:
    host = (urlparse(url).hostname or "").casefold().rstrip(".")
    return any(host == allowed or host.endswith("." + allowed) for allowed in OFFICIAL_HOSTS)


def _fetch_urllib(url: str) -> tuple[bytes, str | None, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "FATHER-KnowledgeFactory/0.2"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise RuntimeError(f"artifact exceeds {MAX_BYTES} bytes")
        mime = response.headers.get_content_type() if response.headers else None
        return data, mime, response.geturl()


def _fetch_curl(url: str) -> tuple[bytes, str | None, str]:
    curl = shutil.which("curl")
    if not curl:
        raise RuntimeError("curl unavailable")
    proc = subprocess.run(
        [curl, "-L", "--fail", "--silent", "--show-error", "--max-time", str(TIMEOUT_SECONDS), url],
        capture_output=True,
        timeout=TIMEOUT_SECONDS + 5,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip() or f"curl exit {proc.returncode}")
    if len(proc.stdout) > MAX_BYTES:
        raise RuntimeError(f"artifact exceeds {MAX_BYTES} bytes")
    return proc.stdout, None, url


def _fetch(url: str) -> tuple[bytes, str | None, str, str]:
    errors: list[str] = []
    for name, func in (("urllib", _fetch_urllib), ("curl", _fetch_curl)):
        try:
            data, mime, final_url = func(url)
            if not data:
                raise RuntimeError("empty response")
            if not _is_official(final_url):
                raise RuntimeError(f"redirected off official allowlist: {final_url}")
            return data, mime, final_url, name
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
    raise RuntimeError("; ".join(errors))


def _decode_text(data: bytes) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp1251"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _normalize_html(data: bytes) -> str:
    parser = _TextExtractor()
    parser.feed(_decode_text(data))
    return parser.text()


def _normalize_docx_or_odt(data: bytes) -> str | None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = set(archive.namelist())
            target = "word/document.xml" if "word/document.xml" in names else "content.xml" if "content.xml" in names else None
            if not target:
                return None
            xml = archive.read(target).decode("utf-8", errors="replace")
            return "\n".join(part for part in re.sub(r"<[^>]+>", "\n", xml).splitlines() if part.strip())
    except zipfile.BadZipFile:
        return None


def _normalize_pdf(data: bytes) -> str | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n\n".join((page.extract_text() or "").strip() for page in reader.pages if (page.extract_text() or "").strip())
    except Exception:
        return None


def _normalize(data: bytes, mime: str | None, final_url: str) -> tuple[str | None, str]:
    lower_mime = (mime or "").casefold()
    lower_path = urlparse(final_url).path.casefold()
    if "html" in lower_mime or lower_path.endswith((".html", ".htm")):
        return _normalize_html(data), "HTML_TEXT"
    if "xml" in lower_mime or lower_path.endswith(".xml"):
        return _decode_text(data), "XML_TEXT"
    if "json" in lower_mime or lower_path.endswith(".json"):
        return _decode_text(data), "JSON_TEXT"
    if lower_path.endswith((".docx", ".odt")):
        text = _normalize_docx_or_odt(data)
        return text, "OFFICE_TEXT" if text else "RAW_ONLY_OFFICE_EXTRACT_FAILED"
    if "pdf" in lower_mime or lower_path.endswith(".pdf") or data.startswith(b"%PDF"):
        text = _normalize_pdf(data)
        return text, "PDF_TEXT" if text else "RAW_ONLY_PDF_EXTRACTOR_UNAVAILABLE"
    if lower_mime.startswith("text/"):
        return _decode_text(data), "PLAIN_TEXT"
    return None, "RAW_ONLY_UNKNOWN_FORMAT"


def _process_document(doc: dict[str, object]) -> dict[str, object]:
    started = time.perf_counter()
    document_id = str(doc.get("document_id") or "").strip()
    url = str(doc.get("official_source_url") or "").strip()
    result: dict[str, object] = {
        "document_id": document_id,
        "title": doc.get("title"),
        "started_at": _utc_now(),
        "legal_status": doc.get("legal_status"),
        "source_url": url or None,
    }

    if not url:
        result.update(status="SOURCE_URL_REQUIRED", seconds=time.perf_counter() - started)
        return result
    if not _is_official(url):
        result.update(status="REFERENCE_ONLY_NOT_ACQUIRED", seconds=time.perf_counter() - started)
        return result

    try:
        data, mime, final_url, transport = _fetch(url)
        digest = hashlib.sha256(data).hexdigest()
        stem = _safe_name(document_id)
        raw_path = RAW_DIR / f"{stem}__{digest}.bin"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        if not raw_path.exists():
            raw_path.write_bytes(data)
        if hashlib.sha256(raw_path.read_bytes()).hexdigest() != digest:
            raise RuntimeError("post-write SHA-256 mismatch")

        normalized, normalization = _normalize(data, mime, final_url)
        normalized_path: Path | None = None
        if normalized is not None and normalized.strip():
            normalized_path = NORMALIZED_DIR / f"{stem}__{digest}.txt"
            normalized_path.parent.mkdir(parents=True, exist_ok=True)
            normalized_path.write_text(normalized.strip() + "\n", encoding="utf-8")

        result.update(
            status="NORMALIZED" if normalized_path else "ACQUIRED_RAW",
            final_url=final_url,
            transport=transport,
            mime_type=mime,
            byte_length=len(data),
            sha256=digest,
            raw_path=raw_path.relative_to(REPO_ROOT).as_posix(),
            normalized_path=normalized_path.relative_to(REPO_ROOT).as_posix() if normalized_path else None,
            normalization=normalization,
            seconds=time.perf_counter() - started,
        )
    except Exception as exc:
        result.update(status="FAILED", error=f"{type(exc).__name__}: {exc}", seconds=time.perf_counter() - started)

    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / f"{_safe_name(document_id)}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    started = time.perf_counter()
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    documents = list(payload.get("documents") or [])
    queue = [
        doc for doc in documents
        if isinstance(doc, dict) and str(doc.get("download_status") or "") != "LOCAL_A0_AVAILABLE"
    ]

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="security-kb") as executor:
        futures = {executor.submit(_process_document, doc): doc for doc in queue}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"[{result.get('status')}] {result.get('document_id')} {result.get('sha256') or ''}")

    results.sort(key=lambda row: str(row.get("document_id") or ""))
    total_seconds = time.perf_counter() - started
    acquired = sum(row.get("status") in {"NORMALIZED", "ACQUIRED_RAW"} for row in results)
    normalized = sum(row.get("status") == "NORMALIZED" for row in results)
    failed = sum(row.get("status") == "FAILED" for row in results)
    source_needed = sum(row.get("status") == "SOURCE_URL_REQUIRED" for row in results)
    reference_only = sum(row.get("status") == "REFERENCE_ONLY_NOT_ACQUIRED" for row in results)

    summary = {
        "record_type": "SECURITY_CURRENT_ONLY_5STREAM_RUN",
        "observed_at": _utc_now(),
        "workers": WORKERS,
        "registry": REGISTRY.relative_to(REPO_ROOT).as_posix(),
        "registry_documents_total": len(documents),
        "queue_total": len(queue),
        "acquired_total": acquired,
        "normalized_total": normalized,
        "failed_total": failed,
        "source_url_required_total": source_needed,
        "reference_only_total": reference_only,
        "throughput_docs_per_second": acquired / total_seconds if total_seconds > 0 else 0.0,
        "speedup_vs_1_stream_pct": None,
        "speedup_note": "No 1-stream baseline is claimed until measured on the same queue and workstation.",
        "total_seconds": total_seconds,
        "results": results,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "LATEST_5STREAM_RUN.json"
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
