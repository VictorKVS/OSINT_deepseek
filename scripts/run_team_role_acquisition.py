from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TEAM_REGISTRY = REPO_ROOT / "config" / "team_role_material_registry.json"
ARCHITECT_PROFILE = REPO_ROOT / "config" / "architect_telegram_acquisition_profile.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "data" / "team_role_telegram"
DEFAULT_REPORT_ROOT = REPO_ROOT / "reports" / "team_role_telegram"

from scripts.run_architect_telegram_acquisition import (  # noqa: E402
    Candidate,
    SearchTarget,
    _candidate_from_hit,
    _load_credentials,
    _local_display_path,
    _message_file_info,
    _safe_name,
    _search_target,
    _sha256_file,
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_role(registry: dict[str, Any], role_id: str) -> dict[str, Any]:
    normalized = role_id.strip().upper().replace("-", "_")
    for role in registry.get("roles", []):
        if str(role.get("role_id", "")).upper() == normalized:
            if normalized == "ARCHITECT":
                raise RuntimeError("ARCHITECT remains the proven reference; use RUN_ARCHITECT_TELEGRAM_ACQUISITION.cmd")
            return role
    allowed = sorted(str(role.get("role_id")) for role in registry.get("roles", []) if role.get("role_id") != "ARCHITECT")
    raise RuntimeError(f"unknown role {role_id!r}; allowed: {', '.join(allowed)}")


def _build_targets(role: dict[str, Any], *, max_queries: int) -> list[SearchTarget]:
    targets: list[SearchTarget] = []
    for index, raw_topic in enumerate(role.get("topics", []), start=1):
        topic = " ".join(str(raw_topic).split()).strip()
        if not topic:
            continue
        targets.append(
            SearchTarget(
                target_id=f"{role['role_id']}-TOPIC-{index:02d}",
                query=topic,
                kind="ROLE_TOPIC",
                lesson_number=None,
                lesson_title=None,
                local_path=None,
            )
        )
    return targets[:max_queries]


def _scan_existing_hashes(roots: list[Path], *, max_bytes: int) -> tuple[set[str], dict[str, str]]:
    hashes: set[str] = set()
    locations: dict[str, str] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.name.endswith(".json"):
                continue
            try:
                if path.stat().st_size > max_bytes:
                    continue
                digest = _sha256_file(path)
            except OSError:
                continue
            hashes.add(digest)
            locations.setdefault(digest, _local_display_path(path))
    return hashes, locations


def _role_output_dir(output_root: Path, role_id: str) -> Path:
    return output_root / role_id.casefold()


def _topic_dir(output_dir: Path, candidate: Candidate) -> Path:
    target = candidate.matched_target_ids[0] if candidate.matched_target_ids else "UNMATCHED"
    return output_dir / _safe_name(target.casefold())


async def _run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter()
    registry = _load_json(TEAM_REGISTRY)
    architect_profile = _load_json(ARCHITECT_PROFILE)
    role = _resolve_role(registry, args.role)
    role_id = str(role["role_id"])
    global_policy = registry.get("global_policy", {})

    max_parallel = min(5, max(1, int(global_policy.get("max_parallel_streams", 5))))
    search_streams = min(max_parallel, max(1, int(args.search_streams or max_parallel)))
    download_streams = min(max_parallel, max(1, int(args.download_streams or max_parallel)))
    search_limit = max(1, int(args.search_limit or architect_profile["telegram"].get("search_limit_per_query", 30)))
    max_file_size_mb = max(1, int(args.max_file_size_mb or architect_profile["telegram"].get("max_file_size_mb", 100)))
    max_bytes = max_file_size_mb * 1024 * 1024
    max_queries = max(1, int(args.max_queries or 40))

    targets = _build_targets(role, max_queries=max_queries)
    if not targets:
        raise RuntimeError(f"role {role_id} has no topic queries")

    output_root = Path(args.output_root).resolve() if args.output_root else DEFAULT_OUTPUT_ROOT
    output_dir = _role_output_dir(output_root, role_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_root = Path(args.report_root).resolve() if args.report_root else DEFAULT_REPORT_ROOT
    report_root.mkdir(parents=True, exist_ok=True)
    report_path = report_root / f"LATEST_{role_id}_TELEGRAM_RUN.json"

    dedup_roots = [
        REPO_ROOT / "data" / "architect_telegram_downloads",
        DEFAULT_OUTPUT_ROOT,
    ]
    if output_root != DEFAULT_OUTPUT_ROOT:
        dedup_roots.append(output_root)
    existing_hashes, existing_locations = _scan_existing_hashes(dedup_roots, max_bytes=max_bytes)

    api_id, api_hash, session = _load_credentials(architect_profile)
    try:
        from telethon import TelegramClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Telethon is required for the team-role acquisition runner") from exc

    client = TelegramClient(str(session), api_id, api_hash)
    errors: list[str] = []
    downloaded_rows: list[dict[str, Any]] = []
    reused_rows: list[dict[str, Any]] = []
    skipped_type_total = 0
    skipped_size_total = 0
    bytes_downloaded = 0
    search_hits_total = 0
    candidate_map: dict[str, Candidate] = {}

    allowed_exts = {str(value).casefold() for value in architect_profile["inventory"]["downloadable_extensions"]}
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized; run the standard local authorization gate")

        search_sem = asyncio.Semaphore(search_streams)
        search_tasks = [
            asyncio.create_task(_search_target(client, target, limit=search_limit, semaphore=search_sem, errors=errors))
            for target in targets
        ]
        raw_hits: list[tuple[Any, SearchTarget]] = []
        for task in asyncio.as_completed(search_tasks):
            raw_hits.extend(await task)
        search_hits_total = len(raw_hits)

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
        download_sem = asyncio.Semaphore(download_streams)

        async def download_one(candidate: Candidate) -> tuple[str, dict[str, Any]]:
            nonlocal bytes_downloaded
            async with download_sem:
                target_dir = _topic_dir(output_dir, candidate)
                target_dir.mkdir(parents=True, exist_ok=True)
                original = _safe_name(candidate.file_name, fallback=f"telegram_{candidate.message_id}{candidate.extension}")
                destination = target_dir / f"{_safe_name(candidate.chat_id)}_{candidate.message_id}_{original}"

                if destination.exists():
                    try:
                        digest = _sha256_file(destination)
                        if digest in existing_hashes:
                            return "REUSED", {
                                "role_id": role_id,
                                "knowledge_base_id": role.get("knowledge_base_id"),
                                "chat_id": candidate.chat_id,
                                "message_id": candidate.message_id,
                                "chat_title": candidate.chat_title,
                                "source_url": candidate.source_url,
                                "file_name": candidate.file_name,
                                "local_path": _local_display_path(destination),
                                "sha256": digest,
                                "matched_target_ids": list(candidate.matched_target_ids),
                                "matched_queries": list(candidate.matched_queries),
                                "reason": "existing local role payload",
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
                        "role_id": role_id,
                        "knowledge_base_id": role.get("knowledge_base_id"),
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
                        "matched_target_ids": list(candidate.matched_target_ids),
                        "matched_queries": list(candidate.matched_queries),
                    }
                    if digest in existing_hashes:
                        try:
                            path.unlink()
                        except OSError:
                            pass
                        return "REUSED", {
                            **common,
                            "local_path": existing_locations.get(digest),
                            "reason": "SHA-256 already exists in Architect/team-role corpus",
                        }
                    existing_hashes.add(digest)
                    existing_locations[digest] = _local_display_path(path)
                    bytes_downloaded += size
                    return "DOWNLOADED", {**common, "local_path": _local_display_path(path)}
                except Exception as exc:
                    return "ERROR", {
                        "role_id": role_id,
                        "chat_id": candidate.chat_id,
                        "message_id": candidate.message_id,
                        "file_name": candidate.file_name,
                        "matched_target_ids": list(candidate.matched_target_ids),
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
    hit_to_candidate_ratio = (len(candidate_map) / search_hits_total) if search_hits_total else None
    report = {
        "record_type": "TEAM_ROLE_TELEGRAM_ACQUISITION_RUN",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "PASS_WITH_ERRORS",
        "role_id": role_id,
        "knowledge_base_id": role.get("knowledge_base_id"),
        "role_priority": role.get("priority"),
        "role_state": role.get("state"),
        "stream_id": role.get("stream_id"),
        "material_types": list(role.get("material_types", [])),
        "policy": global_policy,
        "search_streams": search_streams,
        "download_streams": download_streams,
        "queries_total": len(targets),
        "topics_total": len(role.get("topics", [])),
        "search_hits_total": search_hits_total,
        "media_candidates_total": len(candidate_map),
        "downloaded_total": len(downloaded_rows),
        "payload_reused_total": len(reused_rows),
        "skipped_type_total": skipped_type_total,
        "skipped_size_total": skipped_size_total,
        "errors_total": len(errors),
        "bytes_downloaded": bytes_downloaded,
        "elapsed_seconds": elapsed,
        "throughput_files_per_second": len(downloaded_rows) / elapsed if elapsed > 0 else 0.0,
        "throughput_megabytes_per_second": (bytes_downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0.0,
        "useful_candidate_ratio": hit_to_candidate_ratio,
        "speedup_vs_1_stream_pct": None,
        "speedup_note": "No same-queue 1-stream baseline has been measured for this role.",
        "kb_auto_promotion": False,
        "targets": [target.to_dict() for target in targets],
        "downloads": downloaded_rows,
        "reused": reused_rows,
        "errors": errors,
        "report_path": _local_display_path(report_path),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Universal FATHER Telegram acquisition runner for one team role")
    parser.add_argument("--role", required=True, help="Role ID from config/team_role_material_registry.json")
    parser.add_argument("--search-limit", type=int, default=None)
    parser.add_argument("--search-streams", type=int, default=None)
    parser.add_argument("--download-streams", type=int, default=None)
    parser.add_argument("--max-file-size-mb", type=int, default=None)
    parser.add_argument("--max-queries", type=int, default=None)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--report-root", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = asyncio.run(_run(args))
    except Exception as exc:
        report = {
            "record_type": "TEAM_ROLE_TELEGRAM_ACQUISITION_RUN",
            "schema_version": "1.0",
            "status": "FATAL",
            "role_id": str(args.role).upper(),
            "error": f"{type(exc).__name__}: {exc}",
            "kb_auto_promotion": False,
        }
    compact_keys = (
        "status", "role_id", "knowledge_base_id", "role_priority", "stream_id", "search_streams",
        "download_streams", "queries_total", "topics_total", "search_hits_total", "media_candidates_total",
        "downloaded_total", "payload_reused_total", "skipped_type_total", "skipped_size_total", "errors_total",
        "bytes_downloaded", "elapsed_seconds", "throughput_files_per_second", "throughput_megabytes_per_second",
        "useful_candidate_ratio", "speedup_vs_1_stream_pct", "report_path", "error",
    )
    print(json.dumps({key: report.get(key) for key in compact_keys if key in report}, ensure_ascii=False, indent=2))
    return 0 if report.get("status") in {"PASS", "PASS_WITH_ERRORS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
