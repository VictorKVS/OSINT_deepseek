from __future__ import annotations

import hashlib
import json
import mimetypes
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import run_security_current_only_5stream as base  # noqa: E402
import run_security_official_master_download as master  # noqa: E402

INBOX = ROOT / "_MANUAL_OFFICIAL_INBOX"
PLAN = ROOT / "config" / "security_official_master_download_plan.json"
REPORT = ROOT / "reports" / "security_current_only" / "LATEST_MANUAL_OFFICIAL_IMPORT.json"
CHECKLIST = INBOX / "MANUAL_DOWNLOAD_CHECKLIST.tsv"
SUPPORTED = {".pdf", ".html", ".htm", ".docx", ".odt", ".xml", ".json", ".txt"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def document_index() -> dict[str, dict[str, Any]]:
    plan = load_json(PLAN)
    docs, _ = master.merge_plan(plan)
    return {str(row.get("document_id") or ""): row for row in docs if str(row.get("document_id") or "")}


def infer_document_id(path: Path, known_ids: set[str]) -> str | None:
    stem = path.stem
    for document_id in sorted(known_ids, key=len, reverse=True):
        if stem == document_id or stem.startswith(document_id + "__") or stem.startswith(document_id + "_"):
            return document_id
    return None


def sidecar_url(path: Path) -> str | None:
    candidates = [
        path.with_suffix(path.suffix + ".source.txt"),
        path.with_name(path.stem + ".source.txt"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            value = candidate.read_text(encoding="utf-8", errors="ignore").strip()
            if value:
                return value.splitlines()[0].strip()
    return None


def detect_mime(path: Path, data: bytes) -> str:
    if data.startswith(b"%PDF-"):
        return "application/pdf"
    if data.startswith(b"PK\x03\x04") and path.suffix.lower() == ".docx":
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def write_checklist(docs: dict[str, dict[str, Any]]) -> None:
    latest_master = ROOT / "reports" / "security_current_only" / "LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json"
    unresolved: set[str] | None = None
    if latest_master.is_file():
        try:
            payload = load_json(latest_master)
            unresolved = {
                str(row.get("document_id") or "")
                for row in payload.get("results", []) or []
                if isinstance(row, dict) and row.get("status") in {"FAILED", "NEED_OFFICIAL_SOURCE"}
            }
        except Exception:
            unresolved = None

    lines = ["document_id\ttitle\tofficial_source_url\tlocal_target_name\tstatus"]
    for did, row in sorted(docs.items()):
        if unresolved is not None and did not in unresolved:
            continue
        title = str(row.get("title") or "").replace("\t", " ").replace("\n", " ")
        url = str(row.get("official_source_url") or "")
        lines.append(f"{did}\t{title}\t{url}\t{did}.pdf\tDOWNLOAD_MANUALLY")
    INBOX.mkdir(parents=True, exist_ok=True)
    CHECKLIST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def import_one(path: Path, doc: dict[str, Any]) -> dict[str, Any]:
    did = str(doc.get("document_id") or "")
    data = path.read_bytes()
    if not data:
        return {"document_id": did, "status": "REJECTED_EMPTY", "file": path.name}

    digest = sha256_bytes(data)
    mime = detect_mime(path, data)
    source_url = sidecar_url(path)
    raw_path = base.RAW_DIR / f"{base._safe_name(did)}__{digest}.bin"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if not raw_path.exists():
        raw_path.write_bytes(data)
    if sha256_bytes(raw_path.read_bytes()) != digest:
        return {"document_id": did, "status": "FAILED_POST_WRITE_SHA", "file": path.name}

    normalized, normalization = base._normalize(data, mime, path.name)
    normalized_path: Path | None = None
    if normalized and normalized.strip():
        normalized_path = base.NORMALIZED_DIR / f"{base._safe_name(did)}__{digest}.txt"
        normalized_path.parent.mkdir(parents=True, exist_ok=True)
        normalized_path.write_text(normalized.strip() + "\n", encoding="utf-8")

    expected_url = str(doc.get("official_source_url") or "").strip() or None
    provenance_status = "COMPLETE" if source_url else "SOURCE_URL_MISSING"
    identity_status = "MANUAL_IDENTITY_REVIEW_REQUIRED"
    if normalized:
        title = str(doc.get("title") or "")
        numeric_tokens = re.findall(r"\b\d{2,4}\b", title)
        if numeric_tokens and any(token in normalized for token in numeric_tokens):
            identity_status = "PROVISIONAL_NUMBER_MARKER_MATCH_NEEDS_REVIEW"

    meta = {
        "schema_version": "1.0",
        "record_type": "MANUAL_OFFICIAL_DOCUMENT_IMPORT",
        "document_id": did,
        "title": doc.get("title"),
        "domain": doc.get("domain"),
        "legal_status": doc.get("legal_status"),
        "status": "NORMALIZED" if normalized_path else "ACQUIRED_RAW",
        "transport": "MANUAL_BROWSER_DOWNLOAD",
        "execution_environment_id": "LOCAL_WINDOWS_MANUAL_BROWSER",
        "manual_original_file_name": path.name,
        "source_url": source_url,
        "expected_official_source_url": expected_url,
        "provenance_status": provenance_status,
        "mime_type": mime,
        "byte_length": len(data),
        "sha256": digest,
        "raw_path": raw_path.relative_to(ROOT).as_posix(),
        "normalized_path": normalized_path.relative_to(ROOT).as_posix() if normalized_path else None,
        "normalization": normalization,
        "identity_status": identity_status,
        "document_identity_confirmed": False,
        "currentness_verified": False,
        "legal_truth_eligible": False,
        "kb_auto_promotion": False,
        "imported_at": utc_now(),
    }
    meta_path = base.META_DIR / f"{base._safe_name(did)}.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "document_id": did,
        "status": "IMPORTED_REVIEW_REQUIRED",
        "sha256": digest,
        "byte_length": len(data),
        "mime_type": mime,
        "provenance_status": provenance_status,
        "identity_status": identity_status,
        "raw_path": meta["raw_path"],
        "metadata_path": meta_path.relative_to(ROOT).as_posix(),
    }


def main() -> int:
    docs = document_index()
    INBOX.mkdir(parents=True, exist_ok=True)
    write_checklist(docs)

    results: list[dict[str, Any]] = []
    ignored: list[str] = []
    for path in sorted(INBOX.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        did = infer_document_id(path, set(docs))
        if not did:
            ignored.append(path.name)
            continue
        results.append(import_one(path, docs[did]))

    imported = sum(row.get("status") == "IMPORTED_REVIEW_REQUIRED" for row in results)
    source_url_missing = sum(row.get("provenance_status") == "SOURCE_URL_MISSING" for row in results)
    failed = len(results) - imported
    summary = {
        "record_type": "SECURITY_OFFICIAL_MANUAL_INBOX_IMPORT",
        "schema_version": "1.0",
        "status": "PASS" if imported and failed == 0 else "PASS_WITH_GAPS" if imported else "NO_IMPORTABLE_FILES",
        "inbox": INBOX.relative_to(ROOT).as_posix(),
        "checklist": CHECKLIST.relative_to(ROOT).as_posix(),
        "files_seen_total": len(results) + len(ignored),
        "imported_total": imported,
        "failed_total": failed,
        "source_url_missing_total": source_url_missing,
        "ignored_unmatched_files": ignored,
        "document_identity_confirmed": False,
        "legal_truth_eligible": False,
        "kb_auto_promotion": False,
        "results": results,
        "observed_at": utc_now(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "results"}, ensure_ascii=False, indent=2))
    print(f"Checklist: {CHECKLIST.relative_to(ROOT).as_posix()}")
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if imported or not results else 2


if __name__ == "__main__":
    raise SystemExit(main())
