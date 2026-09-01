from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "config" / "architect_telegram_acquisition_profile.json"
DEFAULT_REPORT = REPO_ROOT / "reports" / "architect_telegram" / "LATEST_ARCHITECT_TELEGRAM_RUN.json"
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}


@dataclass(slots=True)
class SearchTarget:
    target_id: str
    query: str
    kind: str
    lesson_number: int | None = None
    lesson_title: str | None = None
    local_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "query": self.query,
            "kind": self.kind,
            "lesson_number": self.lesson_number,
            "lesson_title": self.lesson_title,
            "local_path": self.local_path,
        }


@dataclass(slots=True)
class Candidate:
    key: str
    message: Any
    chat_id: str
    message_id: int
    chat_title: str | None
    chat_username: str | None
    message_date: str | None
    source_url: str | None
    file_name: str
    extension: str
    mime_type: str | None
    file_size: int | None
    matched_target_ids: list[str] = field(default_factory=list)
    matched_queries: list[str] = field(default_factory=list)


def _load_profile() -> dict[str, Any]:
    return json.loads(PROFILE.read_text(encoding="utf-8"))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_name(value: str, *, fallback: str = "item") -> str:
    value = re.sub(r"[^0-9A-Za-zА-Яа-яЁё._ -]+", "_", value).strip(" ._")
    value = re.sub(r"\s+", "_", value)
    return value[:140] or fallback


def _bounded_files(root: Path, max_depth: int):
    root = root.resolve()
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        try:
            depth = len(current_path.relative_to(root).parts)
        except ValueError:
            continue
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS and not name.startswith(".")]
        if depth >= max_depth:
            dirs[:] = []
        for name in files:
            yield current_path / name


def _resolve_course_root(profile: dict[str, Any], explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    env_value = os.getenv("ARCHITECT_COURSE_ROOT", "").strip()
    if env_value:
        candidates.append(Path(env_value))
    for raw in profile.get("course_root_candidates", []):
        path = Path(str(raw))
        candidates.append(path if path.is_absolute() else (REPO_ROOT / path))
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    attempted = ", ".join(str(path) for path in candidates) or "<none>"
    raise RuntimeError(f"architect course root not found; attempted: {attempted}")


def _normalize_lesson_query(folder_name: str) -> str:
    text = re.sub(r"^\s*\d+\s*[.\-_:]*\s*", "", folder_name).strip()
    text = re.sub(r"\bДЗ\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[^0-9A-Za-zА-Яа-яЁё+.# -]+", " ", text)
    words = [word for word in text.split() if len(word) > 1]
    return " ".join(words[:9]).strip()


def _inventory_lessons(course_root: Path, profile: dict[str, Any]) -> tuple[list[dict[str, Any]], set[str]]:
    inventory_cfg = profile["inventory"]
    pattern = re.compile(str(inventory_cfg["lesson_folder_pattern"]))
    primary_exts = {str(value).casefold() for value in inventory_cfg["primary_source_extensions"]}
    downloadable_exts = {str(value).casefold() for value in inventory_cfg["downloadable_extensions"]}
    max_depth = int(inventory_cfg.get("max_scan_depth", 2))
    lessons: list[dict[str, Any]] = []
    existing_hashes: set[str] = set()

    for folder in sorted((item for item in course_root.iterdir() if item.is_dir()), key=lambda item: item.name.casefold()):
        match = pattern.match(folder.name)
        if not match:
            continue
        number = int(match.group(1))
        primary_files: list[str] = []
        downloadable_files: list[str] = []
        for path in _bounded_files(folder, max_depth):
            ext = path.suffix.casefold()
            if ext in primary_exts:
                primary_files.append(path.relative_to(course_root).as_posix())
            if ext in downloadable_exts:
                downloadable_files.append(path.relative_to(course_root).as_posix())
                try:
                    if path.stat().st_size <= 100 * 1024 * 1024:
                        existing_hashes.add(_sha256_file(path))
                except OSError:
                    pass
        lessons.append(
            {
                "lesson_number": number,
                "folder_name": folder.name,
                "path": folder.relative_to(course_root).as_posix(),
                "query": _normalize_lesson_query(folder.name),
                "primary_source_files": sorted(primary_files),
                "downloadable_source_files": sorted(downloadable_files),
                "has_primary_source": bool(primary_files),
            }
        )
    lessons.sort(key=lambda row: (int(row["lesson_number"]), str(row["folder_name"])))
    return lessons, existing_hashes


def _build_targets(lessons: list[dict[str, Any]], profile: dict[str, Any], *, lessons_only: bool) -> list[SearchTarget]:
    targets: list[SearchTarget] = []
    for lesson in lessons:
        if bool(lesson["has_primary_source"]):
            continue
        query = str(lesson.get("query") or "").strip()
        if not query:
            continue
        number = int(lesson["lesson_number"])
        targets.append(
            SearchTarget(
                target_id=f"LESSON-{number:03d}",
                query=query,
                kind="LESSON_GAP",
                lesson_number=number,
                lesson_title=str(lesson["folder_name"]),
                local_path=str(lesson["path"]),
            )
        )
    if not lessons_only:
        for index, raw in enumerate(profile.get("role_topic_seeds", []), start=1):
            query = str(raw).strip()
            if query:
                targets.append(SearchTarget(target_id=f"ROLE-TOPIC-{index:02d}", query=query, kind="ROLE_TOPIC"))
    max_queries = int(profile["telegram"].get("max_queries", 80))
    return targets[:max_queries]


def _load_credentials(profile: dict[str, Any]) -> tuple[int, str, Path]:
    tg = profile["telegram"]
    api_id_raw = os.getenv(str(tg.get("api_id_env", "TELEGRAM_API_ID")), "").strip()
    api_hash = os.getenv(str(tg.get("api_hash_env", "TELEGRAM_API_HASH")), "").strip()
    session_raw = os.getenv(str(tg.get("session_env", "TELEGRAM_SESSION_PATH")), "").strip()

    if not api_id_raw or not api_hash:
        local_config = REPO_ROOT / "legacy" / "telegram" / "config.yaml"
        if local_config.is_file():
            try:
                import yaml  # type: ignore
            except ImportError:
                yaml = None
            if yaml is not None:
                payload = yaml.safe_load(local_config.read_text(encoding="utf-8")) or {}
                telegram = payload.get("telegram", {})
                api_id_raw = api_id_raw or str(telegram.get("api_id") or "").strip()
                api_hash = api_hash or str(telegram.get("api_hash") or "").strip()

    if not api_id_raw or not api_hash:
        raise RuntimeError("TELEGRAM_API_ID/TELEGRAM_API_HASH are required (or legacy/telegram/config.yaml)")
    try:
        api_id = int(api_id_raw)
    except ValueError as exc:
        raise RuntimeError("TELEGRAM_API_ID must be an integer") from exc
    session = Path(session_raw) if session_raw else (REPO_ROOT / str(tg["default_session_path"]))
    if not session.is_absolute():
        session = REPO_ROOT / session
    return api_id, api_hash, session


def _message_file_info(message: Any) -> tuple[str, str, str | None, int | None] | None:
    file_obj = getattr(message, "file", None)
    if file_obj is None:
        return None
    name = str(getattr(file_obj, "name", None) or "").strip()
    ext = str(getattr(file_obj, "ext", None) or "").strip().casefold()
    if name and not ext:
        ext = Path(name).suffix.casefold()
    mime = str(getattr(file_obj, "mime_type", None) or "").strip() or None
    if not ext and mime:
        ext = {
            "application/pdf": ".pdf",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/epub+zip": ".epub",
        }.get(mime.casefold(), "")
    size_raw = getattr(file_obj, "size", None)
    size = int(size_raw) if isinstance(size_raw, int) else None
    if not name:
        message_id = int(getattr(message, "id", 0) or 0)
        name = f"telegram_{message_id}{ext or '.bin'}"
    return name, ext, mime, size


async def _search_target(client: Any, target: SearchTarget, *, limit: int, semaphore: asyncio.Semaphore, errors: list[str]) -> list[tuple[Any, SearchTarget]]:
    async with semaphore:
        rows: list[tuple[Any, SearchTarget]] = []
        attempts = 0
        while True:
            try:
                async for message in client.iter_messages(None, search=target.query, limit=limit):
                    rows.append((message, target))
                return rows
            except Exception as exc:
                if exc.__class__.__name__ != "FloodWaitError" or attempts >= 1:
                    errors.append(f"search:{target.target_id}: {type(exc).__name__}: {exc}")
                    return rows
                seconds = int(getattr(exc, "seconds", 0) or 0)
                if seconds > 30:
                    errors.append(f"search:{target.target_id}: FloodWait {seconds}s above bound")
                    return rows
                attempts += 1
                await asyncio.sleep(seconds)


async def _candidate_from_hit(message: Any, target: SearchTarget, allowed_exts: set[str]) -> Candidate | None:
    info = _message_file_info(message)
    if info is None:
        return None
    file_name, ext, mime, size = info
    if ext.casefold() not in allowed_exts:
        return None
    if mime and mime.casefold().startswith(("video/", "audio/", "image/")):
        return None
    chat_id = str(getattr(message, "chat_id", None) or "unknown")
    chat_title = None
    username = None
    try:
        chat = await message.get_chat()
        chat_title = str(getattr(chat, "title", None) or getattr(chat, "first_name", None) or "").strip() or None
        username = str(getattr(chat, "username", None) or "").strip() or None
    except Exception:
        pass
    message_id = int(getattr(message, "id", 0) or 0)
    date = getattr(message, "date", None)
    date_iso = date.isoformat() if date is not None and hasattr(date, "isoformat") else None
    source_url = f"https://t.me/{username}/{message_id}" if username and message_id else None
    return Candidate(
        key=f"{chat_id}:{message_id}",
        message=message,
        chat_id=chat_id,
        message_id=message_id,
        chat_title=chat_title,
        chat_username=username,
        message_date=date_iso,
        source_url=source_url,
        file_name=file_name,
        extension=ext.casefold(),
        mime_type=mime,
        file_size=size,
        matched_target_ids=[target.target_id],
        matched_queries=[target.query],
    )


def _target_dir_for_candidate(output_root: Path, candidate: Candidate, targets_by_id: dict[str, SearchTarget]) -> Path:
    lesson_target = next((targets_by_id[target_id] for target_id in candidate.matched_target_ids if target_id.startswith("LESSON-") and target_id in targets_by_id), None)
    if lesson_target is not None:
        return output_root / f"lesson_{lesson_target.lesson_number:03d}_{_safe_name(lesson_target.lesson_title or lesson_target.target_id)}"
    return output_root / "role_topics"


def _local_display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


async def _run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter()
    profile = _load_profile()
    course_root = _resolve_course_root(profile, args.course_root)
    lessons, existing_hashes = _inventory_lessons(course_root, profile)
    targets = _build_targets(lessons, profile, lessons_only=args.lessons_only)
    targets_by_id = {target.target_id: target for target in targets}

    output_root = Path(args.output) if args.output else (REPO_ROOT / profile["outputs"]["local_download_root"])
    if not output_root.is_absolute():
        output_root = REPO_ROOT / output_root
    output_root.mkdir(parents=True, exist_ok=True)

    for path in output_root.rglob("*"):
        if path.is_file() and path.name != "manifest.json" and not path.name.endswith(".json"):
            try:
                if path.stat().st_size <= int(profile["telegram"]["max_file_size_mb"]) * 1024 * 1024:
                    existing_hashes.add(_sha256_file(path))
            except OSError:
                pass

    api_id, api_hash, session = _load_credentials(profile)
    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for this local runner; install it into the selected Python environment") from exc

    client = TelegramClient(str(session), api_id, api_hash)
    errors: list[str] = []
    search_hits_total = 0
    skipped_type_total = 0
    skipped_size_total = 0
    downloaded_rows: list[dict[str, Any]] = []
    reused_rows: list[dict[str, Any]] = []
    media_candidates_total = 0
    bytes_downloaded = 0

    allowed_exts = {str(value).casefold() for value in profile["inventory"]["downloadable_extensions"]}
    max_bytes = int(args.max_file_size_mb or profile["telegram"]["max_file_size_mb"]) * 1024 * 1024
    search_limit = int(args.search_limit or profile["telegram"]["search_limit_per_query"])
    search_streams = min(5, max(1, int(args.search_streams or profile["telegram"]["max_search_streams"])))
    download_streams = min(5, max(1, int(args.download_streams or profile["telegram"]["max_download_streams"])))

    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized; authorize the existing local session first")

        search_sem = asyncio.Semaphore(search_streams)
        search_tasks = [
            asyncio.create_task(_search_target(client, target, limit=search_limit, semaphore=search_sem, errors=errors))
            for target in targets
        ]
        raw_hits: list[tuple[Any, SearchTarget]] = []
        for task in asyncio.as_completed(search_tasks):
            rows = await task
            raw_hits.extend(rows)
        search_hits_total = len(raw_hits)

        candidate_map: dict[str, Candidate] = {}
        for message, target in raw_hits:
            info = _message_file_info(message)
            if info is None:
                skipped_type_total += 1
                continue
            _, ext, mime, size = info
            if ext.casefold() not in allowed_exts or (mime and mime.casefold().startswith(("video/", "audio/", "image/"))):
                skipped_type_total += 1
                continue
            if size is not None and size > max_bytes:
                skipped_size_total += 1
                continue
            candidate = await _candidate_from_hit(message, target, allowed_exts)
            if candidate is None:
                skipped_type_total += 1
                continue
            existing = candidate_map.get(candidate.key)
            if existing is None:
                candidate_map[candidate.key] = candidate
            else:
                if target.target_id not in existing.matched_target_ids:
                    existing.matched_target_ids.append(target.target_id)
                if target.query not in existing.matched_queries:
                    existing.matched_queries.append(target.query)
        candidates = list(candidate_map.values())
        media_candidates_total = len(candidates)

        download_sem = asyncio.Semaphore(download_streams)

        async def download_one(candidate: Candidate) -> tuple[str, dict[str, Any]]:
            nonlocal bytes_downloaded
            async with download_sem:
                target_dir = _target_dir_for_candidate(output_root, candidate, targets_by_id)
                target_dir.mkdir(parents=True, exist_ok=True)
                original = _safe_name(candidate.file_name, fallback=f"telegram_{candidate.message_id}{candidate.extension}")
                destination = target_dir / f"{_safe_name(candidate.chat_id)}_{candidate.message_id}_{original}"
                if destination.exists():
                    try:
                        digest = _sha256_file(destination)
                        if digest in existing_hashes:
                            return "REUSED", {
                                "chat_id": candidate.chat_id,
                                "message_id": candidate.message_id,
                                "chat_title": candidate.chat_title,
                                "source_url": candidate.source_url,
                                "file_name": candidate.file_name,
                                "local_path": _local_display_path(destination),
                                "sha256": digest,
                                "matched_target_ids": candidate.matched_target_ids,
                                "matched_queries": candidate.matched_queries,
                                "reason": "existing local Telegram payload",
                            }
                    except OSError:
                        pass
                try:
                    downloaded = await client.download_media(candidate.message, file=str(destination))
                    if not downloaded:
                        raise RuntimeError("download_media returned no path")
                    path = Path(str(downloaded))
                    if not path.is_file():
                        raise RuntimeError(f"downloaded path is not a file: {path}")
                    digest = _sha256_file(path)
                    size = path.stat().st_size
                    common = {
                        "chat_id": candidate.chat_id,
                        "message_id": candidate.message_id,
                        "chat_title": candidate.chat_title,
                        "chat_username": candidate.chat_username,
                        "message_date": candidate.message_date,
                        "source_url": candidate.source_url,
                        "file_name": candidate.file_name,
                        "mime_type": candidate.mime_type,
                        "file_size": size,
                        "sha256": digest,
                        "matched_target_ids": candidate.matched_target_ids,
                        "matched_queries": candidate.matched_queries,
                    }
                    if digest in existing_hashes:
                        try:
                            path.unlink()
                        except OSError:
                            pass
                        return "REUSED", {**common, "local_path": None, "reason": "SHA-256 already exists in course/download corpus"}
                    existing_hashes.add(digest)
                    bytes_downloaded += size
                    return "DOWNLOADED", {**common, "local_path": _local_display_path(path)}
                except Exception as exc:
                    return "ERROR", {
                        "chat_id": candidate.chat_id,
                        "message_id": candidate.message_id,
                        "file_name": candidate.file_name,
                        "matched_target_ids": candidate.matched_target_ids,
                        "error": f"{type(exc).__name__}: {exc}",
                    }

        download_tasks = [asyncio.create_task(download_one(candidate)) for candidate in candidates]
        for task in asyncio.as_completed(download_tasks):
            state, row = await task
            if state == "DOWNLOADED":
                downloaded_rows.append(row)
            elif state == "REUSED":
                reused_rows.append(row)
            else:
                errors.append(f"download:{row.get('chat_id')}:{row.get('message_id')}: {row.get('error')}")
    finally:
        await client.disconnect()

    elapsed = time.perf_counter() - started
    missing = [lesson for lesson in lessons if not bool(lesson["has_primary_source"])]
    report = {
        "record_type": "ARCHITECT_TELEGRAM_ACQUISITION_RUN",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "PASS_WITH_ERRORS",
        "policy": profile["policy"],
        "course_root": str(course_root),
        "session_path": str(session),
        "search_streams": search_streams,
        "download_streams": download_streams,
        "lessons_total": len(lessons),
        "lessons_with_primary_sources": len(lessons) - len(missing),
        "lessons_missing_primary_sources": len(missing),
        "queries_total": len(targets),
        "search_hits_total": search_hits_total,
        "media_candidates_total": media_candidates_total,
        "downloaded_total": len(downloaded_rows),
        "payload_reused_total": len(reused_rows),
        "skipped_type_total": skipped_type_total,
        "skipped_size_total": skipped_size_total,
        "errors_total": len(errors),
        "bytes_downloaded": bytes_downloaded,
        "elapsed_seconds": elapsed,
        "throughput_files_per_second": len(downloaded_rows) / elapsed if elapsed > 0 else 0.0,
        "throughput_megabytes_per_second": (bytes_downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0.0,
        "speedup_vs_1_stream_pct": None,
        "speedup_note": "No 1-stream speedup is claimed until the same target/query set is measured on the same workstation.",
        "kb_auto_promotion": False,
        "lessons": lessons,
        "targets": [target.to_dict() for target in targets],
        "downloads": downloaded_rows,
        "reused": reused_rows,
        "errors": errors,
    }
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search/download remaining Architect materials from Telegram already accessible to the operator account")
    parser.add_argument("--course-root", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--lessons-only", action="store_true", help="Search only missing numbered course lessons; skip general Architect role-topic seeds")
    parser.add_argument("--search-limit", type=int, default=None)
    parser.add_argument("--search-streams", type=int, default=None)
    parser.add_argument("--download-streams", type=int, default=None)
    parser.add_argument("--max-file-size-mb", type=int, default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = asyncio.run(_run(args))
    except Exception as exc:
        report = {
            "record_type": "ARCHITECT_TELEGRAM_ACQUISITION_RUN",
            "schema_version": "1.0",
            "status": "FATAL",
            "error": f"{type(exc).__name__}: {exc}",
            "kb_auto_promotion": False,
        }
    DEFAULT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    compact_keys = (
        "status", "course_root", "search_streams", "download_streams", "lessons_total",
        "lessons_with_primary_sources", "lessons_missing_primary_sources", "queries_total",
        "search_hits_total", "media_candidates_total", "downloaded_total", "payload_reused_total",
        "skipped_type_total", "skipped_size_total", "errors_total", "bytes_downloaded",
        "elapsed_seconds", "throughput_files_per_second", "throughput_megabytes_per_second",
        "speedup_vs_1_stream_pct", "error",
    )
    compact = {key: report.get(key) for key in compact_keys if key in report}
    compact["report"] = DEFAULT_REPORT.relative_to(REPO_ROOT).as_posix()
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0 if report.get("status") in {"PASS", "PASS_WITH_ERRORS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
