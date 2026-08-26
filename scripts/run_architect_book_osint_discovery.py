from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "architect_book_acquisition_registry.json"
REPORT = ROOT / "reports" / "architect_books" / "LATEST_ARCHITECT_BOOK_OSINT_DISCOVERY.json"
SUPPORTED = {".pdf", ".epub", ".djvu", ".mobi", ".azw3", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str) -> str:
    value = value.casefold().replace("ё", "е")
    value = re.sub(r"[^0-9a-zа-я]+", " ", value)
    return " ".join(value.split())


def title_tokens(row: dict[str, Any]) -> list[str]:
    title = norm(str(row.get("title") or ""))
    author = norm(str(row.get("author") or ""))
    tokens = [t for t in title.split() if len(t) >= 4]
    author_tokens = [t for t in author.split() if len(t) >= 4]
    return tokens[:6] + author_tokens[:3]


def local_roots(explicit: str | None) -> list[Path]:
    roots = []
    raw = explicit or os.environ.get("ARCHITECT_BOOK_LOCAL_ROOTS") or ""
    for part in raw.split(os.pathsep):
        if part.strip():
            roots.append(Path(part.strip()).expanduser())
    roots += [Path.home() / "Downloads", Path("G:/1/OTUS"), ROOT / "data" / "architect_telegram_downloads", ROOT / "_LOCAL_DOWNLOADS_KB_INTAKE"]
    out, seen = [], set()
    for p in roots:
        key = str(p).casefold()
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def scan_files(roots: list[Path], max_files: int = 20000) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.exists() or not root.is_dir():
            continue
        try:
            for p in root.rglob("*"):
                if len(files) >= max_files:
                    return files
                if p.is_file() and p.suffix.lower() in SUPPORTED:
                    files.append(p)
        except (OSError, PermissionError):
            continue
    return files


def match_local(row: dict[str, Any], files: list[Path]) -> list[str]:
    tokens = title_tokens(row)
    matches = []
    for p in files:
        name = norm(p.stem)
        score = sum(1 for t in tokens if t in name)
        title_only = [t for t in norm(str(row.get("title") or "")).split() if len(t) >= 4]
        title_hits = sum(1 for t in title_only if t in name)
        if (title_only and title_hits >= max(2, min(4, len(title_only)))) or score >= 4:
            matches.append(str(p))
    return matches[:10]


async def search_telegram(missing: list[dict[str, Any]], search_limit: int, streams: int) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required") from exc

    api_id = int(os.environ["TELEGRAM_API_ID"])
    api_hash = os.environ["TELEGRAM_API_HASH"]
    session_raw = os.environ.get("TELEGRAM_SESSION_PATH") or str(ROOT / "legacy" / "telegram" / "reader_session")
    client = TelegramClient(session_raw, api_id, api_hash)
    sem = asyncio.Semaphore(max(1, min(5, streams)))
    results: list[dict[str, Any]] = []
    errors: list[str] = []

    async def one(book: dict[str, Any], query: str) -> None:
        async with sem:
            try:
                async for message in client.iter_messages(None, search=query, limit=search_limit):
                    file_obj = getattr(message, "file", None)
                    if file_obj is None:
                        continue
                    name = str(getattr(file_obj, "name", None) or "")
                    ext = str(getattr(file_obj, "ext", None) or Path(name).suffix or "").lower()
                    if ext not in SUPPORTED:
                        continue
                    size = getattr(file_obj, "size", None)
                    chat = None
                    try:
                        chat = await message.get_chat()
                    except Exception:
                        pass
                    username = str(getattr(chat, "username", None) or "") if chat else ""
                    mid = int(getattr(message, "id", 0) or 0)
                    results.append({
                        "book_id": book["book_id"],
                        "title": book["title"],
                        "rights_class": book["rights_class"],
                        "query": query,
                        "file_name": name,
                        "extension": ext,
                        "file_size": int(size) if isinstance(size, int) else None,
                        "chat_title": str(getattr(chat, "title", None) or getattr(chat, "first_name", None) or "") if chat else None,
                        "chat_username": username or None,
                        "message_id": mid,
                        "source_url": f"https://t.me/{username}/{mid}" if username and mid else None,
                        "action": "DISCOVERY_ONLY" if book["rights_class"] == "COMMERCIAL" else "OPEN_SOURCE_CANDIDATE_REVIEW",
                    })
            except Exception as exc:
                errors.append(f"{book['book_id']}:{query}: {type(exc).__name__}: {exc}")

    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized")
        tasks = []
        for book in missing:
            for query in book.get("queries") or [book.get("title")]:
                tasks.append(asyncio.create_task(one(book, str(query))))
        if tasks:
            await asyncio.gather(*tasks)
    finally:
        await client.disconnect()

    unique: dict[tuple[str, str, int], dict[str, Any]] = {}
    for row in results:
        key = (str(row["book_id"]), str(row.get("chat_username") or row.get("chat_title") or ""), int(row.get("message_id") or 0))
        unique[key] = row
    return list(unique.values()), errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Find which architect books are already local and discover Telegram candidates only for missing titles.")
    parser.add_argument("--local-roots", default=None)
    parser.add_argument("--search-limit", type=int, default=20)
    parser.add_argument("--search-streams", type=int, default=5)
    parser.add_argument("--local-only", action="store_true")
    args = parser.parse_args()

    registry = load_json(REGISTRY)
    roots = local_roots(args.local_roots)
    files = scan_files(roots)
    found, missing = [], []
    for row in registry.get("targets") or []:
        matches = match_local(row, files)
        record = {**row, "local_matches": matches, "status": "FOUND_LOCAL" if matches else "MISSING_LOCAL"}
        (found if matches else missing).append(record)

    candidates, errors = ([], [])
    if missing and not args.local_only:
        candidates, errors = asyncio.run(search_telegram(missing, args.search_limit, args.search_streams))

    by_book: dict[str, int] = {}
    for row in candidates:
        by_book[row["book_id"]] = by_book.get(row["book_id"], 0) + 1

    report = {
        "record_type": "ARCHITECT_BOOK_OSINT_DISCOVERY_RUN",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "PASS_WITH_ERRORS",
        "registry": REGISTRY.relative_to(ROOT).as_posix(),
        "local_roots_checked": [str(p) for p in roots],
        "local_files_scanned_total": len(files),
        "books_total": len(found) + len(missing),
        "found_local_total": len(found),
        "missing_local_total": len(missing),
        "found_local": found,
        "missing_local": missing,
        "osint_candidates_total": len(candidates),
        "osint_candidates_by_book": by_book,
        "osint_candidates": candidates,
        "errors_total": len(errors),
        "errors": errors,
        "policy": registry.get("policy"),
        "kb_auto_promotion": False
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {k: report[k] for k in ["status","local_files_scanned_total","books_total","found_local_total","missing_local_total","osint_candidates_total","osint_candidates_by_book","errors_total"]}
    compact["report"] = REPORT.relative_to(ROOT).as_posix()
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0 if report["status"] in {"PASS", "PASS_WITH_ERRORS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
