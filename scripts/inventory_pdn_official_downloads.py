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


def _missing_markers(text: str, markers: list[str]) -> list[str]:
    normalized = _norm(text)
    return [marker for marker in markers if _norm(marker) not in normalized]


def _identity_result(text: str, item: dict[str, object]) -> tuple[bool, list[str], list[str]]:
    primary = list(item.get("primary_identity_markers", []))
    secondary = list(item.get("identity_markers", []))
    if not primary:
        return False, ["PRIMARY_IDENTITY_PROFILE_MISSING"], []
    missing_primary = _missing_markers(text, primary)
    missing_secondary = _missing_markers(text, secondary)
    return not missing_primary and not missing_secondary, missing_primary, missing_secondary


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

    parsed: list[dict[str, object]] = []
    parse_failed: list[dict[str, object]] = []
    for path in recent_files:
        try:
            data = path.read_bytes()
            text = extract_visible_text(data, "text/html")
            parsed.append({"path": path, "data": data, "text": text})
        except (OSError, DocumentCompilerError, ValueError) as exc:
            parse_failed.append({"name": path.name, "reason": str(exc)})

    # Build the entire file -> document match matrix before assigning anything.
    # A capture that passes more than one document identity is ambiguous and is
    # never promoted to D3 merely because the registry happens to be iterated first.
    match_matrix: dict[Path, list[str]] = {}
    identity_diagnostics: dict[tuple[Path, str], dict[str, object]] = {}
    for candidate in parsed:
        path = candidate["path"]
        text = str(candidate["text"])
        assert isinstance(path, Path)
        matched_ids: list[str] = []
        for item in pack["documents"]:
            document_id = str(item["document_id"])
            ok, missing_primary, missing_secondary = _identity_result(text, item)
            identity_diagnostics[(path, document_id)] = {
                "name": path.name,
                "missing_primary_markers": missing_primary,
                "missing_secondary_markers": missing_secondary,
            }
            if ok:
                matched_ids.append(document_id)
        match_matrix[path] = matched_ids

    ambiguous = [
        {"name": path.name, "matched_document_ids": ids}
        for path, ids in match_matrix.items()
        if len(ids) > 1
    ]

    documents: list[dict[str, object]] = []
    used_paths: set[Path] = set()
    for item in pack["documents"]:
        document_id = str(item["document_id"])
        anchor = item["publication_anchor"]
        best: dict[str, object] | None = None
        diagnostics: list[dict[str, object]] = []

        for candidate in parsed:
            path = candidate["path"]
            assert isinstance(path, Path)
            if path in used_paths:
                continue
            matched_ids = match_matrix[path]
            if matched_ids == [document_id]:
                best = candidate
                break
            diagnostic = dict(identity_diagnostics[(path, document_id)])
            if len(matched_ids) > 1:
                diagnostic["status"] = "AMBIGUOUS_IDENTITY"
                diagnostic["matched_document_ids"] = matched_ids
            elif matched_ids and document_id not in matched_ids:
                diagnostic["status"] = "IDENTIFIED_AS_OTHER_DOCUMENT"
                diagnostic["matched_document_ids"] = matched_ids
            else:
                diagnostic["status"] = "IDENTITY_FAILED"
            diagnostics.append(diagnostic)

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
                "identity_profile": "PRIMARY_AND_SECONDARY",
                "diagnostics": diagnostics[:10],
            })
            continue

        path = best["path"]
        data = best["data"]
        assert isinstance(path, Path)
        assert isinstance(data, bytes)
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
            "identity_profile": "PRIMARY_AND_SECONDARY",
            "candidate_match_cardinality": 1,
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
        "ambiguous_candidates": len(ambiguous),
        "identity_rule": "PRIMARY_AND_SECONDARY markers must pass and each capture must identify exactly one target document.",
        "provenance_rule": "Only HTML saved after the explicit A0 publication session is eligible; exact bytes, MIME and SHA-256 are preserved after unique document identity verification.",
        "garant_used": False,
    }
    output = {
        "summary": summary,
        "documents": documents,
        "ambiguous_files": ambiguous,
        "parse_failed_files": parse_failed,
    }
    REPORT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if verified == len(documents) and not ambiguous else 2


if __name__ == "__main__":
    raise SystemExit(main())
