from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.pravo_publication import MAX_JSON_BYTES, PravoPublicationClient, PravoPublicationError, PravoPublicationHit

WATCHLIST = REPO_ROOT / "config" / "security_departmental_orders_watchlist.json"
SECTORAL_KII_QUEUE = REPO_ROOT / "config" / "security_sectoral_kii_current_only_queue.json"
REPORT_DIR = REPO_ROOT / "reports" / "security_current_only"
REPORT = REPORT_DIR / "LATEST_DEPARTMENTAL_DISCOVERY.json"
PAGE_SIZE = 200
MAX_PAGES_PER_QUERY = 20
TIMEOUT_SECONDS = 12.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(value: str) -> str:
    return value.casefold().replace("ё", "е")


def _seed_candidate(raw: dict[str, object], *, state_key: str, source_default: str) -> dict[str, object] | None:
    publication_number = str(raw.get("publication_number") or "").strip() or None
    title = str(raw.get("title") or "").strip()
    if not title:
        return None
    return {
        "document_id": str(raw.get("document_id") or "").strip() or None,
        "publication_number": publication_number,
        "title": title,
        "authority": str(raw.get("authority") or "").strip() or None,
        "domain": str(raw.get("domain") or "").strip() or None,
        "priority": str(raw.get("priority") or "").strip() or None,
        "source": str(raw.get("source") or raw.get("official_source_url") or source_default).strip(),
        "seed_state": str(raw.get(state_key) or raw.get("state") or "VERIFY_CURRENTNESS").strip(),
        "candidate_origin": "VERIFIED_SEED",
        "candidate_only": True,
        "verification": "VERIFY_CURRENTNESS_AND_EXACT_SOURCE",
    }


def _seed_candidates(watch: dict[str, object], sectoral: dict[str, object]) -> list[dict[str, object]]:
    by_key: dict[str, dict[str, object]] = {}
    for raw in watch.get("verified_seed_items", []):
        if not isinstance(raw, dict):
            continue
        row = _seed_candidate(raw, state_key="state", source_default="publication.pravo.gov.ru")
        if row is None:
            continue
        key = str(row.get("publication_number") or row.get("document_id") or row.get("title"))
        by_key[key] = row
    for raw in sectoral.get("items", []):
        if not isinstance(raw, dict):
            continue
        row = _seed_candidate(raw, state_key="currentness_state", source_default="publication.pravo.gov.ru")
        if row is None:
            continue
        key = str(row.get("publication_number") or row.get("document_id") or row.get("title"))
        by_key[key] = row
    return list(by_key.values())


def main() -> int:
    watch = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    sectoral = json.loads(SECTORAL_KII_QUEUE.read_text(encoding="utf-8")) if SECTORAL_KII_QUEUE.exists() else {"items": []}
    queries = [str(v).strip() for v in watch.get("discovery_queries", []) if str(v).strip()]
    authorities = [str(v).strip() for v in watch.get("coverage", {}).get("sectoral_foiv", []) if str(v).strip()]
    seed_rows = _seed_candidates(watch, sectoral)
    known = {
        str(row.get("publication_number") or "").strip()
        for row in seed_rows
        if str(row.get("publication_number") or "").strip()
    }

    client = PravoPublicationClient()
    candidates: dict[str, dict[str, object]] = {}
    query_results: list[dict[str, object]] = []
    source_failed = False

    for query in queries:
        if source_failed:
            query_results.append({"query": query, "status": "SKIPPED_AFTER_SOURCE_FAILURE", "hits": 0})
            continue

        query_hits = 0
        scanned = 0
        try:
            for page in range(1, MAX_PAGES_PER_QUERY + 1):
                url = client._url(
                    "api/Documents",
                    {"DocumentText": query, "PageSize": PAGE_SIZE, "Index": page},
                )
                payload = client.transport.get_json(
                    url,
                    timeout_seconds=TIMEOUT_SECONDS,
                    max_bytes=MAX_JSON_BYTES,
                )
                items = payload.get("items") or []
                if not isinstance(items, list):
                    raise PravoPublicationError("api/Documents items must be a list")
                scanned += len(items)
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    hit = PravoPublicationHit.from_api(item)
                    title_n = norm(hit.title)
                    authority_match = next((a for a in authorities if norm(a.replace(" России", "")) in title_n), None)
                    if not authority_match:
                        if not any(
                            token in title_n
                            for token in (
                                "министерств",
                                "федеральн",
                                "служб",
                                "агентств",
                                "фонд пенсионного",
                                "социального страхования",
                            )
                        ):
                            continue
                    key = hit.eo_number or f"{hit.number}|{hit.document_date}|{hit.title}"
                    if not key:
                        continue
                    candidates[key] = {
                        "eo_number": hit.eo_number or None,
                        "number": hit.number or None,
                        "title": hit.title,
                        "document_date": hit.document_date or None,
                        "publish_date": hit.publish_date or None,
                        "matched_query": query,
                        "matched_authority": authority_match,
                        "known_seed": bool(hit.eo_number and hit.eo_number in known),
                        "candidate_origin": "LIVE_API",
                        "candidate_only": True,
                        "verification": "VERIFY_CURRENTNESS_AND_EXACT_SOURCE",
                    }
                    query_hits += 1
                if len(items) < PAGE_SIZE:
                    break
            query_results.append(
                {
                    "query": query,
                    "status": "COMPLETE",
                    "items_scanned": scanned,
                    "hits": query_hits,
                    "transport": getattr(client.transport, "last_transport", None),
                }
            )
        except Exception as exc:
            source_failed = True
            query_results.append(
                {
                    "query": query,
                    "status": "DEGRADED_SOURCE_UNAVAILABLE",
                    "items_scanned": scanned,
                    "hits": query_hits,
                    "error": f"{type(exc).__name__}: {exc}",
                    "transport_failures": list(getattr(client.transport, "last_failures", []) or []),
                }
            )

    live_rows = sorted(
        candidates.values(),
        key=lambda r: (str(r.get("document_date") or ""), str(r.get("title") or "")),
        reverse=True,
    )
    live_known_publications = {
        str(row.get("eo_number") or "").strip()
        for row in live_rows
        if bool(row.get("known_seed")) and str(row.get("eo_number") or "").strip()
    }
    fallback_seeds = [
        row
        for row in seed_rows
        if not row.get("publication_number") or str(row.get("publication_number")) not in live_known_publications
    ]
    operational_rows = live_rows + fallback_seeds

    summary = {
        "record_type": "SECURITY_DEPARTMENTAL_DISCOVERY",
        "schema_version": "1.2",
        "observed_at": utc_now(),
        "watchlist": WATCHLIST.relative_to(REPO_ROOT).as_posix(),
        "sectoral_kii_queue": SECTORAL_KII_QUEUE.relative_to(REPO_ROOT).as_posix(),
        "queries_total": len(queries),
        "queries_complete": sum(r.get("status") == "COMPLETE" for r in query_results),
        "source_degraded": source_failed,
        "discovery_mode": "DEGRADED_WITH_VERIFIED_SEED_FALLBACK" if source_failed else "LIVE_API_PLUS_VERIFIED_SEEDS",
        "live_api_candidate_total": len(live_rows),
        "seed_candidate_total": len(seed_rows),
        "candidate_total": len(operational_rows),
        "new_candidate_total": sum(not bool(r.get("known_seed")) for r in live_rows),
        "known_seed_matches": sum(bool(r.get("known_seed")) for r in live_rows),
        "legal_truth_promoted": False,
        "promotion_policy": "Discovery metadata and verified seed identity never promote CURRENT. Exact bytes, SHA-256, legal status and replacement/amendment chain verification are required.",
        "query_results": query_results,
        "candidates": operational_rows,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
