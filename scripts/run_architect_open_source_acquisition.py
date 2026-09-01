from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "config" / "architect_open_source_pack.json"
REPORT = ROOT / "reports" / "architect_open_sources" / "LATEST_ARCHITECT_OPEN_SOURCE_ACQUISITION.json"
UA = "Mozilla/5.0 FATHER-OSINT/1.0"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value)


def safe_file_name(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "index"
    path = path.replace("/", "__")
    if not path.endswith((".html", ".htm")):
        path += ".html"
    return path[:220]


def fetch_url(url: str, timeout: int = 30) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    with urlopen(request, timeout=timeout) as response:
        data = response.read()
        final_url = response.geturl()
        return data, final_url


def crawl_web_book(source: dict[str, Any], target: Path, max_pages: int, delay: float) -> dict[str, Any]:
    target.mkdir(parents=True, exist_ok=True)
    root_url = str(source["root_url"])
    allowed_prefix = str(source["allowed_prefix"])
    queue: deque[str] = deque([root_url])
    seen: set[str] = set()
    pages: list[dict[str, Any]] = []
    errors: list[str] = []

    while queue and len(seen) < max_pages:
        url = queue.popleft()
        if url in seen or not url.startswith(allowed_prefix):
            continue
        seen.add(url)
        try:
            data, final_url = fetch_url(url)
            digest = sha256_bytes(data)
            name = safe_file_name(final_url)
            path = target / name
            path.write_bytes(data)
            pages.append({
                "url": url,
                "final_url": final_url,
                "local_path": str(path),
                "sha256": digest,
                "byte_length": len(data),
            })
            content_type_text = data.decode("utf-8", errors="ignore")
            parser = LinkParser()
            parser.feed(content_type_text)
            for href in parser.links:
                absolute = urljoin(final_url, href).split("#", 1)[0]
                if absolute.startswith(allowed_prefix) and absolute not in seen:
                    queue.append(absolute)
            time.sleep(delay)
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")

    manifest = {
        "source_id": source["source_id"],
        "title": source["title"],
        "source_type": source["source_type"],
        "root_url": root_url,
        "pages_total": len(pages),
        "errors_total": len(errors),
        "pages": pages,
        "errors": errors,
        "kb_auto_promotion": False,
    }
    (target / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def acquire_git_repo(source: dict[str, Any], target: Path) -> dict[str, Any]:
    repo_url = str(source["repo_url"])
    errors: list[str] = []
    status = "PASS"
    if target.exists() and (target / ".git").exists():
        proc = subprocess.run(["git", "-C", str(target), "pull", "--ff-only"], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            status = "PASS_WITH_ERRORS"
            errors.append(proc.stderr.strip() or proc.stdout.strip())
    elif target.exists() and any(target.iterdir()):
        status = "PASS_WITH_ERRORS"
        errors.append("target directory exists and is non-empty but is not a git repository")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run(["git", "clone", "--depth", "1", repo_url, str(target)], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            status = "FAILED"
            errors.append(proc.stderr.strip() or proc.stdout.strip())

    files: list[dict[str, Any]] = []
    if target.exists():
        for path in target.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            try:
                data = path.read_bytes()
            except OSError:
                continue
            files.append({
                "local_path": str(path),
                "relative_path": path.relative_to(target).as_posix(),
                "sha256": sha256_bytes(data),
                "byte_length": len(data),
            })
    manifest = {
        "source_id": source["source_id"],
        "title": source["title"],
        "source_type": source["source_type"],
        "repo_url": repo_url,
        "status": status,
        "files_total": len(files),
        "files": files,
        "errors_total": len(errors),
        "errors": errors,
        "kb_auto_promotion": False,
    }
    if target.exists():
        (target / "father_source_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire official/author-published open architecture books and SRE sources.")
    parser.add_argument("--library-root", default=None)
    args = parser.parse_args()

    pack = load_json(PACK)
    library_root = Path(args.library_root or pack["default_library_root"])
    library_root.mkdir(parents=True, exist_ok=True)
    policy = pack["policy"]
    results: list[dict[str, Any]] = []

    for source in pack["sources"]:
        target = library_root / str(source["target_dir"])
        if source["source_type"] == "WEB_BOOK":
            result = crawl_web_book(
                source,
                target,
                int(policy["max_pages_per_web_book"]),
                float(policy["request_delay_seconds"]),
            )
            result["status"] = "PASS" if result["errors_total"] == 0 and result["pages_total"] > 0 else "PASS_WITH_ERRORS" if result["pages_total"] > 0 else "FAILED"
        else:
            result = acquire_git_repo(source, target)
        results.append(result)

    report = {
        "record_type": "ARCHITECT_OPEN_SOURCE_ACQUISITION_RUN",
        "schema_version": "1.0",
        "library_root": str(library_root),
        "sources_total": len(results),
        "sources_passed_total": sum(r.get("status") == "PASS" for r in results),
        "sources_with_errors_total": sum(r.get("status") == "PASS_WITH_ERRORS" for r in results),
        "sources_failed_total": sum(r.get("status") == "FAILED" for r in results),
        "policy": policy,
        "results": results,
        "kb_auto_promotion": False,
    }
    report["status"] = "PASS" if report["sources_failed_total"] == 0 else "PASS_WITH_GAPS"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    compact = {k: report[k] for k in ["status", "library_root", "sources_total", "sources_passed_total", "sources_with_errors_total", "sources_failed_total"]}
    compact["report"] = REPORT.relative_to(ROOT).as_posix()
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0 if report["status"] in {"PASS", "PASS_WITH_GAPS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
