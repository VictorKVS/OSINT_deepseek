from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "_MANUAL_OFFICIAL_INBOX"
ARCHIVE = ROOT / "_MANUAL_OFFICIAL_ARCHIVE"
META_DIR = ROOT / "data" / "security_current_only" / "metadata"
REPORT = ROOT / "reports" / "security_current_only" / "LATEST_MANUAL_OFFICIAL_ORGANIZE.json"
INDEX_JSON = ARCHIVE / "INDEX.json"
INDEX_MD = ARCHIVE / "INDEX.md"

AUTHORITY_MAP = {
    "FZ": "FEDERAL_LAWS",
    "PP": "GOVERNMENT",
    "FSTEC": "FSTEC",
    "FSB": "FSB",
    "RKN": "ROSKOMNADZOR",
    "GOST": "ROSSTANDART_GOST",
    "MINZDRAV": "MINZDRAV",
    "MINTRANS": "MINTRANS",
    "MINPROMTORG": "MINPROMTORG",
    "MINEKONOM": "MINEKONOM",
    "MINENERGO": "MINENERGO",
    "SFR": "SFR",
    "ROSFMON": "ROSMONITORING",
}

DOMAIN_ORDER = [
    "PDN", "KII", "GIS", "SECURE_SOFTWARE_DEVELOPMENT", "SECURE_SDLC",
    "INCIDENTS", "THREAT_MODEL", "CRYPTO", "SECURITY_CORE", "STATIC_ANALYSIS",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def authority_for(document_id: str) -> str:
    parts = document_id.split("-")
    token = parts[2] if len(parts) >= 3 else "OTHER"
    return AUTHORITY_MAP.get(token, "OTHER_AUTHORITIES")


def domain_for(meta: dict[str, Any]) -> str:
    raw = str(meta.get("domain") or meta.get("applicability") or "SECURITY")
    tokens = [item.strip().upper() for item in re.split(r"[,;/|]+", raw) if item.strip()]
    for preferred in DOMAIN_ORDER:
        if preferred in tokens:
            return preferred
    return tokens[0] if tokens else "SECURITY"


def sidecars_for(path: Path) -> list[Path]:
    candidates = [
        path.with_suffix(path.suffix + ".source.txt"),
        path.with_name(path.stem + ".source.txt"),
    ]
    return [candidate for candidate in candidates if candidate.is_file()]


def metadata_for(document_id: str) -> dict[str, Any] | None:
    path = META_DIR / f"{document_id}.json"
    if not path.is_file():
        return None
    try:
        return load_json(path)
    except Exception:
        return None


def organize_one(meta: dict[str, Any]) -> dict[str, Any]:
    did = str(meta.get("document_id") or "")
    original = str(meta.get("manual_original_file_name") or "")
    if not did or not original:
        return {"document_id": did or None, "status": "SKIPPED_NO_MANUAL_ORIGINAL"}

    source = INBOX / original
    if not source.is_file():
        return {"document_id": did, "status": "SKIPPED_SOURCE_ALREADY_MOVED_OR_MISSING", "file": original}

    authority = authority_for(did)
    domain = domain_for(meta)
    target_dir = ARCHIVE / authority / domain / did
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name

    if target.exists():
        if target.read_bytes() == source.read_bytes():
            source.unlink()
            status = "ARCHIVED_DUPLICATE_REMOVED_FROM_INBOX"
        else:
            target = target_dir / f"{source.stem}__duplicate{source.suffix}"
            shutil.move(str(source), str(target))
            status = "ARCHIVED_WITH_NAME_COLLISION"
    else:
        shutil.move(str(source), str(target))
        status = "ARCHIVED"

    moved_sidecars: list[str] = []
    for sidecar in sidecars_for(INBOX / original):
        side_target = target_dir / sidecar.name
        if side_target.exists():
            side_target.unlink()
        shutil.move(str(sidecar), str(side_target))
        moved_sidecars.append(side_target.relative_to(ROOT).as_posix())

    return {
        "document_id": did,
        "status": status,
        "authority": authority,
        "domain": domain,
        "archive_path": target.relative_to(ROOT).as_posix(),
        "sidecars": moved_sidecars,
        "sha256": meta.get("sha256"),
        "source_url": meta.get("source_url"),
        "identity_status": meta.get("identity_status"),
        "legal_truth_eligible": bool(meta.get("legal_truth_eligible")),
    }


def rebuild_index() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not ARCHIVE.exists():
        return rows
    for file in sorted(ARCHIVE.rglob("*")):
        if not file.is_file() or file.name in {"INDEX.json", "INDEX.md"} or file.name.endswith(".source.txt"):
            continue
        parts = file.relative_to(ARCHIVE).parts
        if len(parts) < 4:
            continue
        authority, domain, did = parts[0], parts[1], parts[2]
        meta = metadata_for(did) or {}
        rows.append({
            "document_id": did,
            "authority": authority,
            "domain": domain,
            "file": file.relative_to(ROOT).as_posix(),
            "title": meta.get("title"),
            "sha256": meta.get("sha256"),
            "source_url": meta.get("source_url"),
            "identity_status": meta.get("identity_status"),
            "currentness_verified": bool(meta.get("currentness_verified")),
            "legal_truth_eligible": bool(meta.get("legal_truth_eligible")),
        })
    return rows


def write_indexes(rows: list[dict[str, Any]]) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.write_text(json.dumps({
        "schema_version": "1.0",
        "record_type": "SECURITY_MANUAL_OFFICIAL_ARCHIVE_INDEX",
        "documents_total": len(rows),
        "generated_at": utc_now(),
        "documents": rows,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Security manual official archive",
        "",
        f"Documents: {len(rows)}",
        "",
        "| Authority | Domain | Document ID | Title | Identity | Currentness | Legal truth |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        title = str(row.get("title") or "").replace("|", "/")
        lines.append(
            f"| {row['authority']} | {row['domain']} | {row['document_id']} | {title} | "
            f"{row.get('identity_status') or ''} | {row.get('currentness_verified')} | {row.get('legal_truth_eligible')} |"
        )
    INDEX_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for meta_path in sorted(META_DIR.glob("DOC-RU-*.json")) if META_DIR.exists() else []:
        try:
            meta = load_json(meta_path)
        except Exception:
            continue
        if str(meta.get("transport") or "") != "MANUAL_BROWSER_DOWNLOAD":
            continue
        results.append(organize_one(meta))

    index_rows = rebuild_index()
    write_indexes(index_rows)
    archived = sum(str(row.get("status") or "").startswith("ARCHIVED") for row in results)
    report = {
        "record_type": "SECURITY_MANUAL_OFFICIAL_ARCHIVE_ORGANIZE",
        "schema_version": "1.0",
        "status": "PASS",
        "archived_this_run_total": archived,
        "archive_documents_total": len(index_rows),
        "archive_root": ARCHIVE.relative_to(ROOT).as_posix(),
        "index_json": INDEX_JSON.relative_to(ROOT).as_posix(),
        "index_md": INDEX_MD.relative_to(ROOT).as_posix(),
        "results": results,
        "observed_at": utc_now(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
