from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import run_security_official_master_download as master  # noqa: E402


_ORIGINAL_MERGE_PLAN = master.merge_plan
_ORIGINAL_ACQUIRE = master.acquire


def _append_route(route_map: dict[str, list[str]], document_id: str, value: Any) -> None:
    url = str(value or "").strip()
    if not document_id or not url:
        return
    if url not in route_map[document_id]:
        route_map[document_id].append(url)


def merge_plan_multiroute(plan: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    """Preserve every known official URL for a canonical document.

    The legacy master keeps one preferred URL. This wrapper retains that exact
    ordering semantics while appending other URLs observed in source registries
    and extra documents as fallback candidates. Route collection does not change
    legal/source authority and does not make a non-official host acceptable.
    """
    documents, source_rows = _ORIGINAL_MERGE_PLAN(plan)
    route_map: dict[str, list[str]] = defaultdict(list)

    for source in plan.get("source_registries", []) or []:
        path = ROOT / str(source.get("path") or "")
        if not path.is_file():
            continue
        payload = master.load_json(path)
        field = str(source.get("documents_field") or "documents")
        for row in payload.get(field, []) or []:
            if not isinstance(row, dict):
                continue
            did = str(row.get("document_id") or "").strip()
            _append_route(route_map, did, row.get("official_source_url"))
            for url in row.get("official_routes") or []:
                _append_route(route_map, did, url)

    for row in plan.get("extra_documents", []) or []:
        if not isinstance(row, dict):
            continue
        did = str(row.get("document_id") or "").strip()
        _append_route(route_map, did, row.get("official_source_url"))
        for url in row.get("official_routes") or []:
            _append_route(route_map, did, url)

    overrides = plan.get("official_route_overrides") or {}
    for doc in documents:
        did = str(doc.get("document_id") or "")
        preferred: list[str] = []
        override = overrides.get(did)
        if isinstance(override, list):
            preferred.extend(str(value).strip() for value in override if str(value).strip())
        elif override:
            preferred.append(str(override).strip())

        legacy = str(doc.get("official_source_url") or "").strip()
        if legacy:
            preferred.append(legacy)
        preferred.extend(route_map.get(did, []))

        unique: list[str] = []
        for url in preferred:
            if url and url not in unique:
                unique.append(url)
        doc["official_routes"] = unique
        doc["official_source_url"] = unique[0] if unique else None

    return documents, source_rows


def _metadata_path(document_id: str) -> Path:
    stem = master.base._safe_name(document_id)
    return master.base.META_DIR / f"{stem}.json"


def _enrich_success_metadata(
    document_id: str,
    *,
    routes: list[str],
    attempts: list[dict[str, Any]],
    successful_index: int,
) -> None:
    path = _metadata_path(document_id)
    if not path.is_file():
        return
    try:
        payload = master.load_json(path)
    except Exception:
        return
    payload["official_routes"] = routes
    payload["route_attempts"] = attempts
    payload["successful_route_index"] = successful_index
    payload["fallback_used"] = successful_index > 0
    payload["route_selection_policy"] = "PREFERRED_OFFICIAL_THEN_KNOWN_OFFICIAL_FALLBACK"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def acquire_multiroute(doc: dict[str, Any], progress: Any) -> dict[str, Any]:
    """Try known official routes independently; one route failure never blocks peers."""
    did = str(doc.get("document_id") or "")
    raw_routes = doc.get("official_routes") or [doc.get("official_source_url")]
    routes: list[str] = []
    for value in raw_routes:
        url = str(value or "").strip()
        if url and master.base._is_official(url) and url not in routes:
            routes.append(url)

    if not routes:
        single = dict(doc)
        single["official_source_url"] = None
        result = _ORIGINAL_ACQUIRE(single, progress)
        result["official_routes"] = []
        result["route_attempts"] = []
        return result

    attempts: list[dict[str, Any]] = []
    last_failure: dict[str, Any] | None = None

    for index, url in enumerate(routes):
        route_started = time.perf_counter()
        single = dict(doc)
        single["official_source_url"] = url
        result = _ORIGINAL_ACQUIRE(single, progress)
        status = str(result.get("status") or "")
        attempt = {
            "route_index": index,
            "requested_url": url,
            "status": status,
            "elapsed_seconds": time.perf_counter() - route_started,
            "error_class": result.get("error_class"),
            "error": result.get("error"),
            "final_url": result.get("source_url"),
        }
        attempts.append(attempt)

        if status in {"DOWNLOADED", "REUSED_EXACT", "REUSED_DECLARED_LOCAL_A0"}:
            result["official_routes"] = routes
            result["route_attempts"] = attempts
            result["successful_route_index"] = index
            result["fallback_used"] = index > 0
            if status == "DOWNLOADED":
                _enrich_success_metadata(
                    did,
                    routes=routes,
                    attempts=attempts,
                    successful_index=index,
                )
            return result

        if status == "NEED_OFFICIAL_SOURCE":
            last_failure = result
            continue
        last_failure = result

    errors = [
        f"route[{row['route_index']}] {row['requested_url']}: {row.get('error') or row.get('error_class') or row.get('status')}"
        for row in attempts
    ]
    aggregate_error = " | ".join(errors)
    progress.update(did, status="FAILED", error=aggregate_error, force=True)

    base_result = dict(last_failure or {})
    base_result.update({
        "document_id": did,
        "status": "FAILED",
        "official_source_url": routes[0],
        "official_routes": routes,
        "route_attempts": attempts,
        "error_class": "ALL_OFFICIAL_ROUTES_FAILED",
        "error": aggregate_error,
        "network_used": True,
        "fallback_used": len(routes) > 1,
        "kb_auto_promotion": False,
    })
    return base_result


def main() -> int:
    master.merge_plan = merge_plan_multiroute
    master.acquire = acquire_multiroute
    return master.main()


if __name__ == "__main__":
    raise SystemExit(main())
