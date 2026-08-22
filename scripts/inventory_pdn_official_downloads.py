from __future__ import annotations

import hashlib
import json
import mimetypes
from pathlib import Path


TARGETS = {
    "DOC-RU-FZ-152-2006": (("152", "персональ"),),
    "DOC-RU-PP-1119-2012": (("1119",),),
    "DOC-RU-FSTEC-21-2013": (("фстэк", "21"), ("fstec", "21")),
    "DOC-RU-FSB-378-2014": (("фсб", "378"), ("378", "криптограф")),
}


def _norm(value: str) -> str:
    return value.casefold().replace("ё", "е")


def _matches(name: str, alternatives: tuple[tuple[str, ...], ...]) -> bool:
    normalized = _norm(name)
    return any(all(_norm(token) in normalized for token in group) for group in alternatives)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    downloads = Path.home() / "Downloads"
    files = sorted(
        (path for path in downloads.iterdir() if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )[:250]

    results: dict[str, list[dict[str, object]]] = {key: [] for key in TARGETS}
    for path in files:
        for document_id, alternatives in TARGETS.items():
            if not _matches(path.name, alternatives):
                continue
            stat = path.stat()
            mime, _ = mimetypes.guess_type(path.name)
            results[document_id].append({
                "name": path.name,
                "path": str(path),
                "bytes": stat.st_size,
                "sha256": _sha256(path),
                "mime_guess": mime or "application/octet-stream",
                "modified_epoch": int(stat.st_mtime),
                "status": "DOWNLOAD_CANDIDATE_ONLY",
            })

    summary = {
        "record_type": "PDN_OFFICIAL_DOWNLOAD_INVENTORY",
        "downloads": str(downloads),
        "targets": len(TARGETS),
        "targets_with_candidates": sum(bool(items) for items in results.values()),
        "candidate_files": sum(len(items) for items in results.values()),
        "note": "Filename matching identifies candidates only. D3 requires source provenance plus document identity verification from bytes.",
    }
    print(json.dumps({"summary": summary, "documents": results}, ensure_ascii=False, indent=2))
    return 0 if summary["targets_with_candidates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
