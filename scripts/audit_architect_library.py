from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "architect_library_recommendation_catalog.json"
REPORT_DIR = ROOT / "reports" / "architect_library"
REPORT_JSON = REPORT_DIR / "LATEST_ARCHITECT_LIBRARY_AUDIT.json"
REPORT_MD = REPORT_DIR / "ARCHITECT_LIBRARY_GAPS.md"
REPORT_TSV = REPORT_DIR / "ARCHITECT_LIBRARY_FILES.tsv"
DEFAULT_LIBRARY = Path("G:/1/OTUS/Библиотека")
SUPPORTED = {".pdf", ".epub", ".djvu", ".mobi", ".azw3", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md"}
STOP = {"the","and","for","with","from","into","of","to","a","an","in","on","by","as","at","or","it","up"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str) -> str:
    value = value.casefold().replace("ё", "е")
    value = re.sub(r"[^0-9a-zа-я]+", " ", value)
    return " ".join(value.split())


def tokens(value: str) -> list[str]:
    return [x for x in norm(value).split() if len(x) >= 3 and x not in STOP]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sample_text(path: Path, limit: int = 50000) -> str:
    ext = path.suffix.lower()
    try:
        if ext in {".txt", ".md", ".rtf"}:
            return path.read_text(encoding="utf-8", errors="ignore")[:limit]
        if ext == ".pdf":
            try:
                from pypdf import PdfReader  # type: ignore
                reader = PdfReader(str(path))
                meta = reader.metadata or {}
                parts = [str(getattr(meta, "title", "") or ""), str(getattr(meta, "author", "") or "")]
                chars = 0
                for page in reader.pages[:6]:
                    text = page.extract_text() or ""
                    parts.append(text)
                    chars += len(text)
                    if chars >= limit:
                        break
                return "\n".join(parts)[:limit]
            except Exception:
                return ""
        if ext in {".docx", ".odt", ".epub"}:
            with zipfile.ZipFile(path) as zf:
                out: list[str] = []
                size = 0
                for name in zf.namelist():
                    low = name.lower()
                    if not low.endswith((".xml", ".xhtml", ".html", ".opf")):
                        continue
                    try:
                        text = zf.read(name).decode("utf-8", errors="ignore")
                    except Exception:
                        continue
                    text = re.sub(r"<[^>]+>", " ", text)
                    out.append(text)
                    size += len(text)
                    if size >= limit:
                        break
                return "\n".join(out)[:limit]
    except Exception:
        return ""
    return ""


def match_target(target: dict[str, Any], haystack: str, filename_haystack: str) -> tuple[bool, float]:
    title = str(target.get("title") or "")
    author = str(target.get("author") or "")
    tt = tokens(title)
    at = tokens(author)
    if not tt:
        return False, 0.0
    title_hits = sum(1 for t in tt if t in haystack)
    author_hits = sum(1 for t in at if t in haystack)
    title_ratio = title_hits / len(tt)
    exact_in_name = norm(title) in filename_haystack

    if len(tt) <= 2:
        matched = exact_in_name or (title_hits == len(tt) and author_hits >= 1)
    else:
        matched = exact_in_name or (title_hits >= 2 and title_ratio >= 0.60 and (author_hits >= 1 or title_ratio >= 0.80))
    score = round(title_ratio * 0.8 + min(author_hits, 2) * 0.1, 4)
    return matched, score


def scan_library(library: Path, catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(p for p in library.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED):
        try:
            digest = sha256_file(path)
            byte_length = path.stat().st_size
        except OSError as exc:
            rows.append({"path": str(path), "status": "READ_FAILED", "error": str(exc)})
            continue
        text = sample_text(path)
        hay = norm(path.stem + "\n" + text)
        fname = norm(path.stem)
        matches = []
        for target in catalog:
            ok, score = match_target(target, hay, fname)
            if ok:
                matches.append({"catalog_id": target["id"], "title": target["title"], "domain": target["domain"], "priority": target["priority"], "score": score})
        matches.sort(key=lambda x: (x["score"], x["priority"] == "P0"), reverse=True)
        rows.append({
            "status": "OK",
            "path": path.relative_to(library).as_posix(),
            "file_name": path.name,
            "extension": path.suffix.lower(),
            "byte_length": byte_length,
            "sha256": digest,
            "sample_text_chars": len(text),
            "catalog_matches": matches[:5],
            "best_catalog_id": matches[0]["catalog_id"] if matches else None,
            "best_title": matches[0]["title"] if matches else None,
            "best_domain": matches[0]["domain"] if matches else None,
            "match_score": matches[0]["score"] if matches else None,
        })
    return rows


def render_md(report: dict[str, Any]) -> str:
    lines = [
        "# Architect Library Gap Audit",
        "",
        f"Library: `{report['library_root']}`",
        "",
        f"- Files scanned: **{report['files_total']}**",
        f"- Unique SHA-256: **{report['unique_sha256_total']}**",
        f"- Exact duplicate files: **{report['duplicate_files_total']}**",
        f"- Catalog targets covered: **{report['catalog_found_total']} / {report['catalog_total']}**",
        f"- Missing P0: **{report['missing_p0_total']}**",
        f"- Missing P1: **{report['missing_p1_total']}**",
        "",
        "## Coverage by competency",
        "",
        "| Domain | Found | Target | Coverage |",
        "|---|---:|---:|---:|",
    ]
    for domain, row in report["domain_coverage"].items():
        lines.append(f"| {domain} | {row['found']} | {row['target']} | {row['coverage_pct']:.1f}% |")
    lines += ["", "## P0 — recommended gaps", "", "| Title | Author | Domain |", "|---|---|---|"]
    for row in report["missing_p0"]:
        lines.append(f"| {row['title']} | {row['author']} | {row['domain']} |")
    lines += ["", "## P1 — second layer", "", "| Title | Author | Domain |", "|---|---|---|"]
    for row in report["missing_p1"]:
        lines.append(f"| {row['title']} | {row['author']} | {row['domain']} |")
    lines += ["", "## Exact duplicates", ""]
    if report["duplicate_groups"]:
        for group in report["duplicate_groups"]:
            lines.append(f"- `{group['sha256']}`")
            for path in group["paths"]:
                lines.append(f"  - `{path}`")
    else:
        lines.append("No exact SHA-256 duplicates detected.")
    lines += ["", "## Unmatched local files", ""]
    for row in report["unmatched_files"][:100]:
        lines.append(f"- `{row['path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the exact local OTUS architect library and compute competency/book gaps.")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY))
    args = parser.parse_args()
    library = Path(args.library).expanduser().resolve()
    if not library.is_dir():
        print(json.dumps({"status": "LIBRARY_NOT_FOUND", "library": str(library)}, ensure_ascii=False, indent=2))
        return 2

    catalog_payload = load_json(CATALOG)
    catalog = list(catalog_payload.get("targets") or [])
    rows = scan_library(library, catalog)
    good = [r for r in rows if r.get("status") == "OK"]

    by_sha: dict[str, list[str]] = defaultdict(list)
    for row in good:
        by_sha[str(row["sha256"])].append(str(row["path"]))
    duplicate_groups = [{"sha256": sha, "paths": paths} for sha, paths in by_sha.items() if len(paths) > 1]

    found_ids: set[str] = set()
    for row in good:
        for match in row.get("catalog_matches") or []:
            if float(match.get("score") or 0) >= 0.60:
                found_ids.add(str(match["catalog_id"]))

    missing = [row for row in catalog if str(row["id"]) not in found_ids]
    missing_p0 = [row for row in missing if row.get("priority") == "P0"]
    missing_p1 = [row for row in missing if row.get("priority") == "P1"]

    target_count = Counter(str(r["domain"]) for r in catalog)
    found_domain_ids: dict[str, set[str]] = defaultdict(set)
    id_to_target = {str(r["id"]): r for r in catalog}
    for cid in found_ids:
        target = id_to_target.get(cid)
        if target:
            found_domain_ids[str(target["domain"])].add(cid)
    domain_coverage = {}
    for domain in sorted(target_count):
        target_total = target_count[domain]
        found_total = len(found_domain_ids.get(domain, set()))
        domain_coverage[domain] = {"found": found_total, "target": target_total, "coverage_pct": (found_total / target_total * 100.0) if target_total else 0.0}

    unmatched = [row for row in good if not row.get("catalog_matches")]
    ext_counts = Counter(str(row.get("extension") or "") for row in good)

    report = {
        "schema_version": "1.0",
        "record_type": "ARCHITECT_LIBRARY_GAP_AUDIT",
        "status": "PASS",
        "library_root": str(library),
        "files_total": len(good),
        "read_failed_total": len(rows) - len(good),
        "extension_counts": dict(sorted(ext_counts.items())),
        "unique_sha256_total": len(by_sha),
        "duplicate_groups_total": len(duplicate_groups),
        "duplicate_files_total": sum(len(g["paths"]) - 1 for g in duplicate_groups),
        "duplicate_groups": duplicate_groups,
        "catalog_total": len(catalog),
        "catalog_found_total": len(found_ids),
        "catalog_missing_total": len(missing),
        "missing_p0_total": len(missing_p0),
        "missing_p1_total": len(missing_p1),
        "found_catalog_ids": sorted(found_ids),
        "missing_p0": missing_p0,
        "missing_p1": missing_p1,
        "domain_coverage": domain_coverage,
        "unmatched_files_total": len(unmatched),
        "unmatched_files": unmatched,
        "files": rows,
        "source_files_modified": False,
        "kb_auto_promotion": False
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render_md(report), encoding="utf-8")
    lines = ["path\textension\tbytes\tsha256\tbest_catalog_id\tbest_title\tbest_domain\tmatch_score"]
    for row in good:
        vals = [row.get("path"), row.get("extension"), row.get("byte_length"), row.get("sha256"), row.get("best_catalog_id"), row.get("best_title"), row.get("best_domain"), row.get("match_score")]
        lines.append("\t".join("" if v is None else str(v).replace("\t", " ").replace("\n", " ") for v in vals))
    REPORT_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")

    compact = {
        "status": report["status"],
        "library_root": report["library_root"],
        "files_total": report["files_total"],
        "extension_counts": report["extension_counts"],
        "unique_sha256_total": report["unique_sha256_total"],
        "duplicate_files_total": report["duplicate_files_total"],
        "catalog_total": report["catalog_total"],
        "catalog_found_total": report["catalog_found_total"],
        "catalog_missing_total": report["catalog_missing_total"],
        "missing_p0_total": report["missing_p0_total"],
        "missing_p1_total": report["missing_p1_total"],
        "unmatched_files_total": report["unmatched_files_total"],
        "domain_coverage": report["domain_coverage"],
        "report_md": REPORT_MD.relative_to(ROOT).as_posix(),
        "report_json": REPORT_JSON.relative_to(ROOT).as_posix(),
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
