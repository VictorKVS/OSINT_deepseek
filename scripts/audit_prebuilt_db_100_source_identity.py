from __future__ import annotations

import hashlib
import html
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.benchmark_152_prebuilt_mcp_db import DB_PATH

REPORT = REPO_ROOT / "reports" / "pdn_live" / "AUDIT_PREBUILT_DB_100_SOURCE_IDENTITY.json"
SAMPLE_SIZE = 100
MAX_WORKERS = 5
TIMEOUT_SECONDS = 20
MAX_BYTES = 5 * 1024 * 1024
RETRIES = 2
ALLOWED_HOSTS = {"pravo.gov.ru", "www.pravo.gov.ru"}
LAW_ID_RE = re.compile(r"\b\d{1,4}\s*[-–—]?\s*ФЗ\b", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
WORD_RE = re.compile(r"[а-яёa-z0-9]+", re.IGNORECASE)
STOPWORDS = {
    "федеральный", "федерального", "федеральном", "федеральным", "федеральным",
    "закон", "закона", "законе", "российской", "федерации", "россия", "о", "об",
    "и", "в", "на", "для", "от", "по", "при", "с", "со", "к", "из", "за",
}


def _normalize_identifier(value: str) -> str:
    value = value.casefold().replace("ё", "е").replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", "", value)
    return value


def _title_tokens(value: str) -> set[str]:
    tokens = {
        token.casefold().replace("ё", "е")
        for token in WORD_RE.findall(value)
        if len(token) >= 4
    }
    return {token for token in tokens if token not in STOPWORDS}


def _visible_text(raw: bytes) -> str:
    text: str | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw.decode("utf-8", errors="replace")
    text = html.unescape(TAG_RE.sub(" ", text))
    return SPACE_RE.sub(" ", text).strip()


def _fetch(url: str) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").casefold()
    if host not in ALLOWED_HOSTS:
        return {"status": "POLICY_BLOCKED", "error": f"off-policy host: {host}"}

    attempts: list[dict[str, Any]] = []
    for attempt in range(1, RETRIES + 1):
        started = time.perf_counter()
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "FATHER-Knowledge-Factory/donor-identity-audit"},
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                final_url = response.geturl()
                final_host = (urllib.parse.urlparse(final_url).hostname or "").casefold()
                if final_host not in ALLOWED_HOSTS:
                    return {
                        "status": "POLICY_BLOCKED",
                        "error": f"redirected to off-policy host: {final_host}",
                        "attempts": attempts,
                    }
                declared = response.headers.get("Content-Length")
                if declared and int(declared) > MAX_BYTES:
                    return {"status": "TOO_LARGE", "declared_bytes": int(declared), "attempts": attempts}
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    return {"status": "TOO_LARGE", "bytes": len(raw), "attempts": attempts}
                elapsed = time.perf_counter() - started
                return {
                    "status": "FETCHED",
                    "http_status": getattr(response, "status", 200),
                    "final_url": final_url,
                    "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "text": _visible_text(raw),
                    "elapsed_seconds": elapsed,
                    "attempts": attempts + [{"attempt": attempt, "status": "SUCCESS", "elapsed_seconds": elapsed}],
                }
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            elapsed = time.perf_counter() - started
            attempts.append({
                "attempt": attempt,
                "status": "FAILED",
                "elapsed_seconds": elapsed,
                "error": f"{type(exc).__name__}: {exc}",
            })
            if attempt < RETRIES:
                time.sleep(0.5 * attempt)
    return {"status": "FETCH_FAILED", "attempts": attempts}


def _classify(law: dict[str, Any]) -> dict[str, Any]:
    fetched = _fetch(str(law["source_url"]))
    text = str(fetched.pop("text", ""))
    normalized_text = text.casefold().replace("ё", "е")
    donor_identifier = str(law["identifier"] or "")
    donor_norm = _normalize_identifier(donor_identifier)
    observed_identifiers = sorted({_normalize_identifier(x) for x in LAW_ID_RE.findall(text)})
    identifier_match = bool(donor_norm) and donor_norm in observed_identifiers

    donor_title_tokens = _title_tokens(str(law["title"] or ""))
    if donor_title_tokens:
        source_tokens = _title_tokens(normalized_text)
        title_token_coverage = len(donor_title_tokens & source_tokens) / len(donor_title_tokens)
    else:
        title_token_coverage = None

    status = fetched.get("status")
    if status != "FETCHED":
        decision = "UNVERIFIED_TRANSPORT"
    elif identifier_match and (title_token_coverage is None or title_token_coverage >= 0.50):
        decision = "VERIFIED_MATCH"
    elif observed_identifiers and donor_norm not in observed_identifiers:
        decision = "IDENTITY_COLLISION"
    else:
        decision = "AMBIGUOUS"

    return {
        "law_id": law["id"],
        "identifier": donor_identifier,
        "title": law["title"],
        "source_url": law["source_url"],
        "status": law["status"],
        "last_updated": law["last_updated"],
        "source_fetch": fetched,
        "observed_identifiers": observed_identifiers[:20],
        "identifier_match": identifier_match,
        "title_token_coverage": title_token_coverage,
        "decision": decision,
        "content_reuse_allowed": False,
        "legal_truth_promoted": False,
    }


def _load_sample() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = [
            dict(row)
            for row in conn.execute(
                "SELECT id, identifier, title, source_url, status, last_updated "
                "FROM laws WHERE source_url LIKE '%pravo.gov.ru%' AND identifier IS NOT NULL AND trim(identifier) <> ''"
            )
        ]
    finally:
        conn.close()

    eligible = len(rows)
    rows.sort(key=lambda x: hashlib.sha256(str(x["id"]).encode("utf-8")).hexdigest())
    sample = rows[:SAMPLE_SIZE]

    nd_to_laws: dict[str, list[str]] = {}
    for row in rows:
        parsed = urllib.parse.urlparse(str(row["source_url"]))
        nd = urllib.parse.parse_qs(parsed.query).get("nd", [None])[0]
        if nd:
            nd_to_laws.setdefault(str(nd), []).append(str(row["id"]))
    duplicate_nd = {nd: ids for nd, ids in nd_to_laws.items() if len(ids) > 1}
    return sample, {
        "eligible_laws": eligible,
        "sample_size": len(sample),
        "duplicate_nd_groups_in_full_eligible_set": len(duplicate_nd),
        "duplicate_nd_examples": dict(list(sorted(duplicate_nd.items()))[:20]),
    }


def main() -> int:
    started = time.perf_counter()
    if not DB_PATH.is_file():
        print(f"PREBUILT_DB_MISSING: {DB_PATH}")
        return 2

    sample, census = _load_sample()
    if not sample:
        print("NO_ELIGIBLE_DONOR_LAWS")
        return 2

    print(f"Auditing {len(sample)} deterministic donor laws with {MAX_WORKERS} workers...")
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_classify, law): law for law in sample}
        for future in as_completed(futures):
            law = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({
                    "law_id": law["id"],
                    "identifier": law["identifier"],
                    "title": law["title"],
                    "source_url": law["source_url"],
                    "decision": "AUDIT_ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                    "content_reuse_allowed": False,
                    "legal_truth_promoted": False,
                })

    results.sort(key=lambda x: str(x.get("law_id")))
    counts: dict[str, int] = {}
    for item in results:
        key = str(item.get("decision"))
        counts[key] = counts.get(key, 0) + 1

    verified = counts.get("VERIFIED_MATCH", 0)
    collisions = counts.get("IDENTITY_COLLISION", 0)
    ambiguous = counts.get("AMBIGUOUS", 0)
    transport = counts.get("UNVERIFIED_TRANSPORT", 0)
    errors = counts.get("AUDIT_ERROR", 0)
    observed = len(results)
    collision_rate = collisions / observed if observed else None

    report = {
        "record_type": "PREBUILT_REFERENCE_DB_100_SOURCE_IDENTITY_AUDIT",
        "database_path": DB_PATH.relative_to(REPO_ROOT).as_posix(),
        "sample_policy": {
            "requested": SAMPLE_SIZE,
            "selected": observed,
            "selection": "deterministic_sha256(law_id) over laws with pravo.gov.ru source_url + identifier",
            "max_workers": MAX_WORKERS,
            "timeout_seconds": TIMEOUT_SECONDS,
            "retries": RETRIES,
        },
        "census": census,
        "summary": {
            "verified_match": verified,
            "identity_collision": collisions,
            "ambiguous": ambiguous,
            "unverified_transport": transport,
            "audit_error": errors,
            "collision_rate_observed": collision_rate,
            "content_reuse_allowed": False,
            "legal_truth_promoted": False,
        },
        "results": results,
        "architecture_decision": {
            "prebuilt_content_remains_quarantined": True,
            "infrastructure_reuse_allowed": True,
            "promotion_requires_independent_FATHER_verification": True,
        },
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print()
    print(f"SAMPLED={observed}")
    print(f"VERIFIED_MATCH={verified}")
    print(f"IDENTITY_COLLISION={collisions}")
    print(f"AMBIGUOUS={ambiguous}")
    print(f"UNVERIFIED_TRANSPORT={transport}")
    print(f"AUDIT_ERROR={errors}")
    print(f"DUPLICATE_ND_GROUPS={census['duplicate_nd_groups_in_full_eligible_set']}")
    print(f"COLLISION_RATE_OBSERVED={collision_rate if collision_rate is not None else 'n/a'}")
    print(f"TOTAL_SECONDS={report['total_seconds']:.3f}")
    print("CONTENT_REUSE_ALLOWED=false")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
