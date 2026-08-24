from __future__ import annotations

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGETS_PATH = REPO_ROOT / "config" / "programmer_bibliography_targets.json"
ARCHITECT_PROFILE = REPO_ROOT / "config" / "architect_telegram_acquisition_profile.json"
REPORT_PATH = REPO_ROOT / "reports" / "team_role_telegram" / "LATEST_PROGRAMMER_BIBLIOGRAPHY_PROBE.json"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize(text: str) -> list[str]:
    text = re.sub(r"[^0-9A-Za-zА-Яа-яЁё]+", " ", text.casefold())
    stop = {"the", "and", "of", "a", "an", "with", "to", "in", "2nd", "3rd", "edition"}
    return [token for token in text.split() if len(token) > 1 and token not in stop]


def _surname_tokens(author: str) -> set[str]:
    chunks = [chunk.strip() for chunk in author.split(";") if chunk.strip()]
    out: set[str] = set()
    for chunk in chunks:
        tokens = _normalize(chunk)
        if tokens:
            out.add(tokens[-1])
    return out


def _score_candidate(target: dict[str, Any], haystack: str) -> float:
    hay = set(_normalize(haystack))
    title_tokens = set(_normalize(str(target.get("title", ""))))
    author_tokens = _surname_tokens(str(target.get("author", "")))
    if not title_tokens:
        return 0.0
    title_overlap = len(title_tokens & hay) / len(title_tokens)
    author_hit = 1.0 if author_tokens and (author_tokens & hay) else 0.0
    # Exact bibliographic title evidence dominates; author surname is supportive.
    return min(1.0, 0.85 * title_overlap + 0.15 * author_hit)


def _load_credentials(profile: dict[str, Any]) -> tuple[int, str, Path]:
    tg = profile["telegram"]
    api_id_raw = os.getenv(str(tg.get("api_id_env", "TELEGRAM_API_ID")), "").strip()
    api_hash = os.getenv(str(tg.get("api_hash_env", "TELEGRAM_API_HASH")), "").strip()
    session_raw = os.getenv(str(tg.get("session_env", "TELEGRAM_SESSION_PATH")), "").strip()
    if not api_id_raw or not api_hash:
        raise RuntimeError("TELEGRAM_API_ID/TELEGRAM_API_HASH are required in the current process")
    try:
        api_id = int(api_id_raw)
    except ValueError as exc:
        raise RuntimeError("TELEGRAM_API_ID must be an integer") from exc
    session = Path(session_raw) if session_raw else (REPO_ROOT / str(tg["default_session_path"]))
    if not session.is_absolute():
        session = REPO_ROOT / session
    return api_id, api_hash, session


@dataclass(slots=True)
class ProbeCandidate:
    key: str
    score: float
    query: str
    chat_id: str
    message_id: int
    chat_title: str | None
    chat_username: str | None
    source_url: str | None
    file_name: str
    extension: str
    mime_type: str | None
    file_size: int | None
    message_date: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 4),
            "query": self.query,
            "chat_id": self.chat_id,
            "message_id": self.message_id,
            "chat_title": self.chat_title,
            "chat_username": self.chat_username,
            "source_url": self.source_url,
            "file_name": self.file_name,
            "extension": self.extension,
            "mime_type": self.mime_type,
            "file_size": self.file_size,
            "message_date": self.message_date,
        }


async def _candidate_from_message(message: Any, query: str, target: dict[str, Any], allowed_exts: set[str]) -> ProbeCandidate | None:
    file_obj = getattr(message, "file", None)
    if file_obj is None:
        return None
    name = str(getattr(file_obj, "name", None) or "").strip()
    ext = str(getattr(file_obj, "ext", None) or "").strip().casefold()
    if name and not ext:
        ext = Path(name).suffix.casefold()
    mime = str(getattr(file_obj, "mime_type", None) or "").strip() or None
    if ext not in allowed_exts:
        return None
    if mime and mime.casefold().startswith(("video/", "audio/", "image/")):
        return None

    body = str(getattr(message, "message", None) or "")
    haystack = f"{name} {body}"
    score = _score_candidate(target, haystack)
    if score <= 0:
        return None

    chat_id = str(getattr(message, "chat_id", None) or "unknown")
    message_id = int(getattr(message, "id", 0) or 0)
    chat_title = None
    username = None
    try:
        chat = await message.get_chat()
        chat_title = str(getattr(chat, "title", None) or getattr(chat, "first_name", None) or "").strip() or None
        username = str(getattr(chat, "username", None) or "").strip() or None
    except Exception:
        pass
    source_url = f"https://t.me/{username}/{message_id}" if username and message_id else None
    date = getattr(message, "date", None)
    date_iso = date.isoformat() if date is not None and hasattr(date, "isoformat") else None
    size_raw = getattr(file_obj, "size", None)
    size = int(size_raw) if isinstance(size_raw, int) else None
    return ProbeCandidate(
        key=f"{chat_id}:{message_id}",
        score=score,
        query=query,
        chat_id=chat_id,
        message_id=message_id,
        chat_title=chat_title,
        chat_username=username,
        source_url=source_url,
        file_name=name or f"telegram_{message_id}{ext or '.bin'}",
        extension=ext,
        mime_type=mime,
        file_size=size,
        message_date=date_iso,
    )


async def _probe_target(client: Any, target: dict[str, Any], *, semaphore: asyncio.Semaphore, limit: int, max_candidates: int, allowed_exts: set[str]) -> dict[str, Any]:
    candidates: dict[str, ProbeCandidate] = {}
    query_stats: list[dict[str, Any]] = []
    errors: list[str] = []

    async with semaphore:
        for query in target.get("query_variants", []):
            query = str(query).strip()
            if not query:
                continue
            hit_count = 0
            try:
                async for message in client.iter_messages(None, search=query, limit=limit):
                    hit_count += 1
                    candidate = await _candidate_from_message(message, query, target, allowed_exts)
                    if candidate is None:
                        continue
                    previous = candidates.get(candidate.key)
                    if previous is None or candidate.score > previous.score:
                        candidates[candidate.key] = candidate
            except Exception as exc:
                errors.append(f"{query}: {type(exc).__name__}: {exc}")
            query_stats.append({"query": query, "hits": hit_count})

    ranked = sorted(candidates.values(), key=lambda item: (-item.score, item.file_name.casefold()))[:max_candidates]
    best_score = ranked[0].score if ranked else 0.0
    if best_score >= 0.72:
        status = "FOUND_CANDIDATE"
    elif ranked:
        status = "AMBIGUOUS"
    else:
        status = "NOT_FOUND"

    return {
        "id": target["id"],
        "priority": target.get("priority"),
        "kind": target.get("kind"),
        "author": target.get("author"),
        "title": target.get("title"),
        "status": status,
        "best_score": round(best_score, 4),
        "query_stats": query_stats,
        "candidates": [item.to_dict() for item in ranked],
        "errors": errors,
    }


async def _run() -> dict[str, Any]:
    started = time.perf_counter()
    registry = _load_json(TARGETS_PATH)
    profile = _load_json(ARCHITECT_PROFILE)
    policy = registry["policy"]
    api_id, api_hash, session = _load_credentials(profile)

    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for bibliography probe") from exc

    client = TelegramClient(str(session), api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("shared Telethon session is not authorized")
        semaphore = asyncio.Semaphore(min(5, max(1, int(policy.get("max_parallel_streams", 5)))))
        allowed_exts = {str(value).casefold() for value in policy.get("allowed_extensions", [])}
        tasks = [
            asyncio.create_task(
                _probe_target(
                    client,
                    target,
                    semaphore=semaphore,
                    limit=max(1, int(policy.get("max_results_per_query", 20))),
                    max_candidates=max(1, int(policy.get("max_candidates_per_target", 5))),
                    allowed_exts=allowed_exts,
                )
            )
            for target in registry.get("targets", [])
        ]
        rows = [await task for task in asyncio.as_completed(tasks)]
    finally:
        await client.disconnect()

    rows.sort(key=lambda row: row["id"])
    found = sum(1 for row in rows if row["status"] == "FOUND_CANDIDATE")
    ambiguous = sum(1 for row in rows if row["status"] == "AMBIGUOUS")
    not_found = sum(1 for row in rows if row["status"] == "NOT_FOUND")
    errors_total = sum(len(row["errors"]) for row in rows)
    elapsed = time.perf_counter() - started
    report = {
        "record_type": "PROGRAMMER_BIBLIOGRAPHY_TELEGRAM_PROBE",
        "schema_version": "1.0",
        "status": "PASS" if errors_total == 0 else "PASS_WITH_ERRORS",
        "probe_only": True,
        "downloaded_total": 0,
        "targets_total": len(rows),
        "found_candidate_total": found,
        "ambiguous_total": ambiguous,
        "not_found_total": not_found,
        "errors_total": errors_total,
        "availability_ratio": (found / len(rows)) if rows else None,
        "elapsed_seconds": elapsed,
        "speedup_vs_1_stream_pct": None,
        "targets": rows,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    try:
        report = asyncio.run(_run())
    except Exception as exc:
        report = {
            "record_type": "PROGRAMMER_BIBLIOGRAPHY_TELEGRAM_PROBE",
            "status": "FATAL",
            "error": f"{type(exc).__name__}: {exc}",
            "probe_only": True,
            "downloaded_total": 0,
        }
    keys = (
        "status",
        "probe_only",
        "targets_total",
        "found_candidate_total",
        "ambiguous_total",
        "not_found_total",
        "errors_total",
        "availability_ratio",
        "elapsed_seconds",
        "speedup_vs_1_stream_pct",
        "error",
    )
    print(json.dumps({key: report.get(key) for key in keys if key in report}, ensure_ascii=False, indent=2))
    print(f"Report: {REPORT_PATH.relative_to(REPO_ROOT).as_posix()}")
    return 0 if report.get("status") in {"PASS", "PASS_WITH_ERRORS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
