from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "config" / "programmer_bibliography_targets.json"
ROUTES = ROOT / "config" / "programmer_bibliography_acquisition_registry.json"
POLICY = ROOT / "config" / "programming_kb_source_factory_policy.json"
DATA_ROOT = ROOT / "data" / "programming_kb_sources"
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
REPORT = REPORT_ROOT / "LATEST_OPEN_ACQUISITION.json"

OPEN_ROUTES = {"OFFICIAL_OPEN_WEB", "OFFICIAL_OPEN_PDF", "OFFICIAL_REPOSITORY_DOWNLOAD"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value.strip())
    return out[:120] or "source"


def extension_for(url: str, content_type: str | None) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix in {".pdf", ".html", ".htm", ".txt", ".md", ".epub", ".docx"}:
        return suffix
    if content_type:
        ctype = content_type.split(";", 1)[0].strip().lower()
        if ctype == "application/pdf":
            return ".pdf"
        if ctype in {"text/html", "application/xhtml+xml"}:
            return ".html"
        if ctype.startswith("text/plain"):
            return ".txt"
        guessed = mimetypes.guess_extension(ctype)
        if guessed:
            return guessed
    return ".bin"


def build_open_targets() -> list[dict[str, Any]]:
    targets = load_json(TARGETS)
    routes = load_json(ROUTES)
    target_by_id = {str(row["id"]): row for row in targets.get("targets", [])}
    rows: list[dict[str, Any]] = []
    for route in routes.get("targets", []):
        if route.get("route") not in OPEN_ROUTES:
            continue
        target = target_by_id.get(str(route.get("id")))
        if not target:
            continue
        rows.append({**target, **route})
    rows.sort(key=lambda row: str(row.get("id")))
    return rows


def acquire_one(row: dict[str, Any], *, timeout: int, max_bytes: int) -> dict[str, Any]:
    target_id = str(row["id"])
    url = str(row["official_url"])
    target_dir = DATA_ROOT / target_id
    target_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "FATHER-Knowledge-Factory/1.0 (+research; provenance-preserving)",
            "Accept": "text/html,application/pdf,text/plain,application/xhtml+xml,*/*;q=0.5",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type")
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise RuntimeError(f"source exceeds max_bytes={max_bytes}")
            data = response.read(max_bytes + 1)
            final_url = response.geturl()
        if len(data) > max_bytes:
            raise RuntimeError(f"source exceeds max_bytes={max_bytes}")
        digest = sha256_bytes(data)
        ext = extension_for(final_url, content_type)
        destination = target_dir / f"original{ext}"
        if destination.exists() and sha256_bytes(destination.read_bytes()) == digest:
            status = "REUSED_EXACT"
        else:
            destination.write_bytes(data)
            status = "DOWNLOADED"
        metadata = {
            "schema_version": "1.0",
            "record_type": "PROGRAMMING_KB_SOURCE",
            "target_id": target_id,
            "kind": row.get("kind"),
            "author": row.get("author"),
            "title": row.get("title"),
            "year": row.get("year"),
            "topics": row.get("topics") or [],
            "route": row.get("route"),
            "rights_class": row.get("rights_class"),
            "rights_basis": "OFFICIAL_OPEN_OR_INSTITUTIONAL_SOURCE",
            "source_locator": url,
            "resolved_url": final_url,
            "content_type": content_type,
            "local_path": destination.relative_to(ROOT).as_posix(),
            "sha256": digest,
            "bytes": len(data),
            "source_language": "en",
            "acquisition_status": status,
            "kb_auto_promotion": False,
            "elapsed_seconds": time.perf_counter() - started,
        }
        (target_dir / "source.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return metadata
    except Exception as exc:
        return {
            "record_type": "PROGRAMMING_KB_SOURCE",
            "target_id": target_id,
            "title": row.get("title"),
            "source_locator": url,
            "route": row.get("route"),
            "rights_class": row.get("rights_class"),
            "acquisition_status": "FAILED",
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed_seconds": time.perf_counter() - started,
            "kb_auto_promotion": False,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire official/open Programmer bibliography sources for PROGRAMMING_KB.")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-file-size-mb", type=int, default=100)
    args = parser.parse_args()

    started = time.perf_counter()
    policy = load_json(POLICY)
    rows = build_open_targets()
    errors: list[str] = []
    if policy.get("policy_id") != "FATHER-PROGRAMMING-KB-SOURCE-FACTORY-001":
        errors.append("unexpected source factory policy id")
    if len(rows) < 1:
        errors.append("no official/open targets configured")
    if any(row.get("route") not in OPEN_ROUTES for row in rows):
        errors.append("non-open route leaked into automatic acquisition")
    if args.validate_only:
        payload = {
            "record_type": "PROGRAMMING_KB_OPEN_ACQUISITION_VALIDATION",
            "status": "PASS" if not errors else "FAIL",
            "targets_total": len(rows),
            "target_ids": [row["id"] for row in rows],
            "validation_errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 2

    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    workers = max(1, min(5, int(args.workers)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(
                acquire_one,
                row,
                timeout=max(1, int(args.timeout)),
                max_bytes=max(1, int(args.max_file_size_mb)) * 1024 * 1024,
            )
            for row in rows
        ]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda row: str(row.get("target_id")))

    downloaded = sum(row.get("acquisition_status") == "DOWNLOADED" for row in results)
    reused = sum(row.get("acquisition_status") == "REUSED_EXACT" for row in results)
    failed = sum(row.get("acquisition_status") == "FAILED" for row in results)
    bytes_total = sum(int(row.get("bytes") or 0) for row in results)
    elapsed = time.perf_counter() - started
    summary = {
        "record_type": "PROGRAMMING_KB_OPEN_ACQUISITION",
        "schema_version": "1.0",
        "status": "PASS" if failed == 0 else "PASS_WITH_GAPS" if downloaded + reused > 0 else "FAIL",
        "targets_total": len(results),
        "downloaded_total": downloaded,
        "reused_total": reused,
        "failed_total": failed,
        "bytes_total": bytes_total,
        "workers": workers,
        "elapsed_seconds": elapsed,
        "throughput_sources_per_second": (downloaded + reused) / elapsed if elapsed > 0 else None,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "kb_auto_promotion": False,
        "results": results,
    }
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key != "results"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if summary["status"] in {"PASS", "PASS_WITH_GAPS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
