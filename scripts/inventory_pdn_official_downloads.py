from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.document_compiler import DocumentCompilerError, extract_visible_text


PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
SESSION = REPO_ROOT / ".runtime" / "pdn_official_source_pack_session.json"
INBOX = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "PDN_OFFICIAL_SOURCE_PACK_D0_D3.json"
SUPPORTED_SUFFIXES = {".html", ".htm"}


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _identity_ok(text: str, markers: list[str]) -> tuple[bool, list[str]]:
    normalized = _norm(text)
    missing = [marker for marker in markers if _norm(marker) not in normalized]
    return not missing, missing


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if not SESSION.is_file():
        print("SESSION_MISSING: run OPEN_PDN_OFFICIAL_SOURCE_PACK.cmd first")
        return 2

    pack = json.loads(PACK.read_text(encoding="utf-8"))
    session = json.loads(SESSION.read_text(encoding="utf-8"))
    started_epoch = int(session["started_epoch"])
    downloads = Path.home() / "Downloads"
    INBOX.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    recent_files = sorted(
        (
            path
            for path in downloads.iterdir()
            if path.is_file()
            and path.suffix.casefold() in SUPPORTED_SUFFIXES
            and int(path.stat().st_mtime) >= started_epoch - 5
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    parsed: list[tuple[Path, bytes, str]] = []
    parse_failed: list[dict[str, object]] = []
    for path in recent_files:
        try:
            data = path.read_bytes()
            text = extract_visible_text(data, "text/html")
            parsed.append((path, data, text))
        except (OSError, DocumentCompilerError, ValueError) as exc:
            parse_failed.append({"name": path.name, "reason": str(exc)})

    documents: list[dict[str, object]] = []
    used_paths: set[Path] = set()
    for item in pack["documents"]:
        document_id = item["document_id"]
        anchor = item["publication_anchor"]
        best: tuple[Path, bytes, str] | None = None
        diagnostics: list[dict[str, object]] = []
        for path, data, text in parsed:
            if path in used_paths:
                continue
            ok, missing = _identity_ok(text, list(item["identity_markers"]))
            if ok:
                best = (path, data, text)
                break
            diagnostics.append({"name": path.name, "missing_markers": missing})

        if best is None:
            documents.append({
                "document_id": document_id,
                "title": item["title"],
                "source_id": anchor["source_id"],
                "source_url": anchor["url"],
                "trust_tier": anchor["trust_tier"],
                "status": "INPUT_PENDING",
                "d0_source_discovered": True,
                "d1_source_verified": True,
                "d2_operator_capture_acquired": False,
                "d3_identity_hash_mime_verified": False,
                "diagnostics": diagnostics[:10],
            })
            continue

        path, data, text = best
        used_paths.add(path)
        sha256 = _sha256(data)
        target = INBOX / f"{document_id}.html"
        shutil.copyfile(path, target)
        copied = target.read_bytes()
        if copied != data:
            raise RuntimeError(f"copied bytes differ for {document_id}")

        documents.append({
            "document_id": document_id,
            "title": item["title"],
            "source_id": anchor["source_id"],
            "source_url": anchor["url"],
            "trust_tier": anchor["trust_tier"],
            "status": "D0_D3_VERIFIED_OPERATOR_CAPTURE",
            "d0_source_discovered": True,
            "d1_source_verified": True,
            "d2_operator_capture_acquired": True,
            "d3_identity_hash_mime_verified": True,
            "source_file": str(path),
            "local_capture": target.relative_to(REPO_ROOT).as_posix(),
            "bytes": len(data),
            "sha256": sha256,
            "mime_type": "text/html",
            "identity_markers": "PASS",
            "semantic_extraction_performed": False,
        })

    verified = sum(item["status"] == "D0_D3_VERIFIED_OPERATOR_CAPTURE" for item in documents)
    summary = {
        "record_type": "PDN_OFFICIAL_SOURCE_PACK_D0_D3_SUMMARY",
        "pack_id": pack["pack_id"],
        "downloads": str(downloads),
        "session_started_epoch": started_epoch,
        "recent_html_candidates": len(recent_files),
        "targets": len(documents),
        "d0_d3_verified": verified,
        "input_pending": len(documents) - verified,
        "parse_failed": len(parse_failed),
        "provenance_rule": "Only HTML saved after the explicit A0 publication session is eligible; identity is verified from captured bytes.",
        "garant_used": False,
    }
    output = {"summary": summary, "documents": documents, "parse_failed_files": parse_failed}
    REPORT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if verified == len(documents) else 2


if __name__ == "__main__":
    raise SystemExit(main())
