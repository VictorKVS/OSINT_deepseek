from __future__ import annotations

import hashlib
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.garant_timeline import parse_garant_timeline_text
from father_osint.legal_core import (
    LegalCoreExtractionError,
    extract_152_fz_core_text,
    is_152_fz_primary_document,
)
from father_osint.odt_extract import OdtExtractionError, extract_odt_text


DOCUMENT_ID = "DOC-RU-FZ-152-2006"
SOURCE_URL = "https://base.garant.ru/12148567/"
DEFAULT_DOWNLOADS = Path.home() / "Downloads"
DEFAULT_ARCHIVE = REPO_ROOT / "data" / "knowledge_factory" / "garant_editions" / DOCUMENT_ID
DEFAULT_REPORT = REPO_ROOT / "reports" / "pdn_timelines"


def _observed_on(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).astimezone().date().isoformat()


def main() -> int:
    downloads = DEFAULT_DOWNLOADS
    archive = DEFAULT_ARCHIVE
    report_dir = DEFAULT_REPORT
    archive.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    candidates = sorted(
        (path for path in downloads.glob("*.odt") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    parse_failed = 0
    identity_failed = 0
    scope_failed = 0
    identity_valid = 0
    by_sha: dict[str, dict[str, object]] = {}
    aliases: defaultdict[str, list[str]] = defaultdict(list)
    full_text_shas: set[str] = set()
    core_text_shas: set[str] = set()

    for path in candidates:
        try:
            data = path.read_bytes()
            text = extract_odt_text(data)
        except (OSError, OdtExtractionError):
            parse_failed += 1
            continue

        if not is_152_fz_primary_document(text):
            identity_failed += 1
            continue

        identity_valid += 1
        try:
            core_text = extract_152_fz_core_text(text)
        except LegalCoreExtractionError:
            scope_failed += 1
            continue

        capture_sha256 = hashlib.sha256(data).hexdigest()
        full_text_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
        core_text_sha256 = hashlib.sha256(core_text.encode("utf-8")).hexdigest()
        full_text_shas.add(full_text_sha256)
        core_text_shas.add(core_text_sha256)
        aliases[capture_sha256].append(path.name)
        if capture_sha256 in by_sha:
            continue

        observed_on = _observed_on(path)
        capture = parse_garant_timeline_text(
            document_id=DOCUMENT_ID,
            source_url=SOURCE_URL,
            observed_on=observed_on,
            text=core_text,
        )
        hints = [item.amendment_date for item in capture.amendment_date_hints]
        destination = archive / f"{capture_sha256}.odt"
        if not destination.exists():
            shutil.copyfile(path, destination)

        by_sha[capture_sha256] = {
            "record_type": "GARANT_EDITION_CAPTURE",
            "document_id": DOCUMENT_ID,
            "source_id": "SRC-RU-GARANT-001",
            "source_url": SOURCE_URL,
            "capture_sha256": capture_sha256,
            "capture_bytes": len(data),
            "extracted_text_sha256": full_text_sha256,
            "core_text_sha256": core_text_sha256,
            "observed_on": observed_on,
            "amendment_hint_count": len(hints),
            "first_amendment_hint": hints[0] if hints else None,
            "latest_amendment_hint": hints[-1] if hints else None,
            "detailed_event_count": len(capture.events),
            "future_edition_signalled": capture.future_edition_signalled,
            "identity_markers": "PASS_PRIMARY_DOCUMENT",
            "scope": "PRIMARY_152_FZ_CORE_ONLY",
            "evidence_state": "A2_WORKING_COPY_ONLY",
            "semantic_text_mirrored": False,
        }

    records = list(by_sha.values())
    for record in records:
        sha = str(record["capture_sha256"])
        record["source_filenames"] = sorted(set(aliases[sha]))

    records.sort(key=lambda item: (str(item.get("latest_amendment_hint") or ""), str(item["capture_sha256"])))
    duplicate_payloads = max(0, identity_valid - scope_failed - len(records))
    unique_full_text = len(full_text_shas)
    unique_core_text = len(core_text_shas)
    semantic_duplicate_captures = max(0, len(records) - unique_full_text)
    core_semantic_duplicate_captures = max(0, len(records) - unique_core_text)

    summary = {
        "record_type": "GARANT_EDITION_INVENTORY_SUMMARY",
        "document_id": DOCUMENT_ID,
        "scanned_odt": len(candidates),
        "identity_valid": identity_valid,
        "unique_captures": len(records),
        "duplicate_content": duplicate_payloads,
        "duplicate_payloads": duplicate_payloads,
        "unique_text_captures": unique_full_text,
        "semantic_duplicate_captures": semantic_duplicate_captures,
        "unique_core_editions": unique_core_text,
        "core_semantic_duplicate_captures": core_semantic_duplicate_captures,
        "identity_failed": identity_failed,
        "scope_failed": scope_failed,
        "parse_failed": parse_failed,
        "semantic_text_mirrored": False,
        "edition_identity_semantics": "capture_sha256 identifies exact downloaded bytes; extracted_text_sha256 identifies full extracted ODT text; core_text_sha256 identifies only the primary 152-FZ legal body",
        "edition_date_semantics": "latest_amendment_hint is navigation metadata from the scoped primary law body, not a proven edition-effective date",
    }

    jsonl = report_dir / "garant_152_edition_inventory.jsonl"
    with jsonl.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n")
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    md = report_dir / "GARANT_152_EDITION_INVENTORY.md"
    lines = [
        "# GARANT 152-FZ edition capture inventory",
        "",
        "Working-copy policy: **GARANT navigates; A0/A1 proves.**",
        "",
        f"- scanned ODT: {summary['scanned_odt']}",
        f"- primary-document identity valid: {summary['identity_valid']}",
        f"- exact unique captures by SHA-256: {summary['unique_captures']}",
        f"- unique full extracted texts: {summary['unique_text_captures']}",
        f"- unique scoped legal-core editions: {summary['unique_core_editions']}",
        f"- exact duplicate payloads: {summary['duplicate_payloads']}",
        f"- full-text semantic duplicates: {summary['semantic_duplicate_captures']}",
        f"- core semantic duplicates: {summary['core_semantic_duplicate_captures']}",
        f"- identity failed: {summary['identity_failed']}",
        f"- scope failed: {summary['scope_failed']}",
        f"- parse failed: {summary['parse_failed']}",
        "- full GARANT semantic text mirrored to Git: **no**",
        "",
        "| # | Capture SHA-256 | Bytes | Core SHA-256 | Amendment hints | Latest hint | Detailed events |",
        "|---:|---|---:|---|---:|---|---:|",
    ]
    for index, record in enumerate(records, start=1):
        lines.append(
            f"| {index} | `{str(record['capture_sha256'])[:16]}…` | {record['capture_bytes']} | "
            f"`{str(record['core_text_sha256'])[:16]}…` | {record['amendment_hint_count']} | "
            f"{record.get('latest_amendment_hint') or '—'} | {record['detailed_event_count']} |"
        )
    lines += [
        "",
        "`latest_amendment_hint` is an A2 navigation hint only. It is not promoted to an official edition-effective date.",
        "`core_text_sha256` is calculated only over the primary 152-FZ legal body; surrounding GARANT material is excluded from semantic edition identity.",
        "Exact ODT bytes are archived only under ignored local `data/knowledge_factory/`; Git receives metadata and hashes only.",
    ]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"summary": summary, "inventory_jsonl": str(jsonl), "inventory_md": str(md), "archive": str(archive)}, ensure_ascii=False, indent=2))
    if scope_failed:
        print("PARTIAL: some primary-document ODT captures failed legal-core scoping and were not promoted to edition inventory.")
    return 0 if records else 2


if __name__ == "__main__":
    raise SystemExit(main())
