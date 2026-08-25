from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "reports" / "team_role_telegram" / "LATEST_PROGRAMMER_BIBLIOGRAPHY_PROBE.json"
TARGETS = ROOT / "config" / "programmer_bibliography_targets.json"
ROUTES = ROOT / "config" / "programmer_bibliography_acquisition_registry.json"
PROFILE = ROOT / "config" / "architect_telegram_acquisition_profile.json"
DATA_ROOT = ROOT / "data" / "programming_kb_sources"
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
REPORT = REPORT_ROOT / "LATEST_OWNED_TELEGRAM_ACQUISITION.json"
OWNED_ENV = "FATHER_OWNED_BOOK_IDS"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value.strip())
    return out[:140] or "telegram_source"


def owned_ids() -> set[str]:
    return {item.strip().upper() for item in os.getenv(OWNED_ENV, "").split(",") if item.strip()}


def build_queue() -> tuple[list[dict[str, Any]], list[str]]:
    ids = owned_ids()
    if not ids:
        return [], []
    targets = load_json(TARGETS)
    routes = load_json(ROUTES)
    probe = load_json(PROBE)
    target_by_id = {str(row["id"]): row for row in targets.get("targets", [])}
    route_by_id = {str(row["id"]): row for row in routes.get("targets", [])}
    probe_by_id = {str(row["id"]): row for row in probe.get("targets", [])}
    errors: list[str] = []
    queue: list[dict[str, Any]] = []
    for target_id in sorted(ids):
        target = target_by_id.get(target_id)
        route = route_by_id.get(target_id)
        observed = probe_by_id.get(target_id)
        if not target or not route:
            errors.append(f"{target_id}: unknown bibliography id")
            continue
        if target.get("kind") != "BOOK":
            errors.append(f"{target_id}: only BOOK ids may use owned-copy Telegram route")
            continue
        if not observed or observed.get("status") != "FOUND_CANDIDATE":
            errors.append(f"{target_id}: no FOUND_CANDIDATE in latest Telegram probe")
            continue
        candidates = observed.get("candidates") or []
        if not candidates:
            errors.append(f"{target_id}: probe has no candidate payload")
            continue
        candidate = candidates[0]
        queue.append({**target, **route, "candidate": candidate})
    return queue, errors


def load_credentials() -> tuple[int, str, Path]:
    profile = load_json(PROFILE)
    tg = profile["telegram"]
    api_id_raw = os.getenv(str(tg.get("api_id_env", "TELEGRAM_API_ID")), "").strip()
    api_hash = os.getenv(str(tg.get("api_hash_env", "TELEGRAM_API_HASH")), "").strip()
    session_raw = os.getenv(str(tg.get("session_env", "TELEGRAM_SESSION_PATH")), "").strip()
    if not api_id_raw or not api_hash:
        raise RuntimeError("TELEGRAM_API_ID/TELEGRAM_API_HASH are required")
    session = Path(session_raw) if session_raw else (ROOT / str(tg["default_session_path"]))
    if not session.is_absolute():
        session = ROOT / session
    return int(api_id_raw), api_hash, session


async def download_one(client: Any, row: dict[str, Any], semaphore: asyncio.Semaphore, max_bytes: int) -> dict[str, Any]:
    target_id = str(row["id"])
    candidate = row["candidate"]
    started = time.perf_counter()
    async with semaphore:
        try:
            username = str(candidate.get("chat_username") or "").strip()
            chat_id = str(candidate.get("chat_id") or "").strip()
            if username:
                entity_ref: Any = username.lstrip("@")
            else:
                entity_ref = int(chat_id)
            entity = await client.get_entity(entity_ref)
            message = await client.get_messages(entity, ids=int(candidate["message_id"]))
            if message is None or getattr(message, "file", None) is None:
                raise RuntimeError("Telegram candidate message/file is unavailable")
            file_obj = message.file
            size = int(getattr(file_obj, "size", 0) or 0)
            if size and size > max_bytes:
                raise RuntimeError(f"candidate exceeds max_bytes={max_bytes}")
            filename = safe_name(str(getattr(file_obj, "name", None) or candidate.get("file_name") or f"{target_id}.bin"))
            target_dir = DATA_ROOT / target_id
            target_dir.mkdir(parents=True, exist_ok=True)
            destination = target_dir / f"telegram_owned_{filename}"
            downloaded = await client.download_media(message, file=str(destination))
            if not downloaded:
                raise RuntimeError("download_media returned no path")
            path = Path(str(downloaded))
            digest = sha256_file(path)
            source_url = candidate.get("source_url")
            meta = {
                "schema_version": "1.0",
                "record_type": "PROGRAMMING_KB_SOURCE",
                "target_id": target_id,
                "kind": "BOOK",
                "author": row.get("author"),
                "title": row.get("title"),
                "year": row.get("year"),
                "topics": row.get("topics") or [],
                "route": "TELEGRAM_USER_OWNED_OR_AUTHORIZED_COPY",
                "rights_class": row.get("rights_class"),
                "rights_basis": "USER_ASSERTED_OWNED_OR_AUTHORIZED_COPY",
                "rights_assertion_env": OWNED_ENV,
                "source_locator": source_url or f"telegram://{chat_id}/{candidate['message_id']}",
                "telegram_chat_id": chat_id,
                "telegram_message_id": int(candidate["message_id"]),
                "local_path": path.relative_to(ROOT).as_posix(),
                "sha256": digest,
                "bytes": path.stat().st_size,
                "source_language": "en",
                "acquisition_status": "DOWNLOADED",
                "kb_auto_promotion": False,
                "elapsed_seconds": time.perf_counter() - started,
            }
            (target_dir / "source.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            return meta
        except Exception as exc:
            return {
                "target_id": target_id,
                "acquisition_status": "FAILED",
                "error": f"{type(exc).__name__}: {exc}",
                "elapsed_seconds": time.perf_counter() - started,
            }


async def run(queue: list[dict[str, Any]], workers: int, max_bytes: int) -> list[dict[str, Any]]:
    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for owned-copy Telegram acquisition") from exc
    api_id, api_hash, session = load_credentials()
    client = TelegramClient(str(session), api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized")
        semaphore = asyncio.Semaphore(max(1, min(5, workers)))
        tasks = [download_one(client, row, semaphore, max_bytes) for row in queue]
        return await asyncio.gather(*tasks)
    finally:
        await client.disconnect()


def main() -> int:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    queue, errors = build_queue() if PROBE.exists() else ([], ["latest Telegram bibliography probe not found"] if owned_ids() else [])
    if not owned_ids():
        summary = {
            "record_type": "PROGRAMMING_KB_OWNED_TELEGRAM_ACQUISITION",
            "schema_version": "1.0",
            "status": "PASS_NO_AUTHORIZED_IDS",
            "owned_ids_total": 0,
            "downloaded_total": 0,
            "failed_total": 0,
            "note": f"Set {OWNED_ENV}=BOOK-001,BOOK-... only for copies you own or are authorized to use.",
            "speedup_vs_1_stream_pct": None,
            "eta_seconds": None,
        }
        REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if errors:
        summary = {
            "record_type": "PROGRAMMING_KB_OWNED_TELEGRAM_ACQUISITION",
            "status": "BLOCKED",
            "owned_ids_total": len(owned_ids()),
            "validation_errors": errors,
        }
        REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    started = time.perf_counter()
    try:
        results = asyncio.run(run(queue, workers=5, max_bytes=100 * 1024 * 1024))
    except Exception as exc:
        results = [{"acquisition_status": "FAILED", "error": f"{type(exc).__name__}: {exc}"}]
    downloaded = sum(row.get("acquisition_status") == "DOWNLOADED" for row in results)
    failed = sum(row.get("acquisition_status") == "FAILED" for row in results)
    elapsed = time.perf_counter() - started
    summary = {
        "record_type": "PROGRAMMING_KB_OWNED_TELEGRAM_ACQUISITION",
        "schema_version": "1.0",
        "status": "PASS" if failed == 0 else "PASS_WITH_GAPS" if downloaded else "FAIL",
        "owned_ids_total": len(queue),
        "downloaded_total": downloaded,
        "failed_total": failed,
        "bytes_total": sum(int(row.get("bytes") or 0) for row in results),
        "elapsed_seconds": elapsed,
        "throughput_sources_per_second": downloaded / elapsed if elapsed > 0 else None,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "kb_auto_promotion": False,
        "results": results,
    }
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key != "results"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if summary["status"] in {"PASS", "PASS_WITH_GAPS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
