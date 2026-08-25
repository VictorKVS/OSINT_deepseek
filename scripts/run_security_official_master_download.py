from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import run_security_current_only_5stream as base
from download_progress_registry import DownloadProgressRegistry
from father_osint.official_transport import RobustOfficialArtifactFetcher

PLAN_PATH = REPO_ROOT / "config" / "security_official_master_download_plan.json"
REPORT_PATH = REPO_ROOT / "reports" / "security_current_only" / "LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json"
BUILD_GLOBAL = REPO_ROOT / "scripts" / "build_global_document_registry.py"
WORKERS = 5
ROBUST_FETCHER = RobustOfficialArtifactFetcher(minimum_timeout_seconds=45.0)

base.OFFICIAL_HOSTS.add("protect.gost.ru")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def classification_for(row: dict[str, Any], source: dict[str, Any]) -> dict[str, str]:
    if row.get("maturity_level") and row.get("importance_class"):
        return {
            "maturity_level": str(row["maturity_level"]),
            "importance_class": str(row["importance_class"]),
        }
    priority = str(row.get("priority") or "P2").upper()
    mapping = source.get("classification_map") or {}
    return dict(mapping.get(priority) or {"maturity_level": "MAX", "importance_class": "INTERESTING_LATER"})


def merge_plan(plan: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    docs: dict[str, dict[str, Any]] = {}
    source_rows = 0

    def add(row: dict[str, Any], source_id: str, classification: dict[str, str]) -> None:
        nonlocal source_rows
        source_rows += 1
        did = str(row.get("document_id") or "").strip()
        if not did:
            return
        candidate = docs.get(did)
        observed = {
            "source_id": source_id,
            "priority": row.get("priority"),
            "maturity_level": classification["maturity_level"],
            "importance_class": classification["importance_class"],
        }
        if candidate is None:
            candidate = {
                "document_id": did,
                "title": row.get("title") or did,
                "domain": row.get("domain") or row.get("applicability") or "SECURITY",
                "legal_status": row.get("legal_status") or "VERIFY_CURRENTNESS",
                "official_source_url": row.get("official_source_url"),
                "download_status": row.get("download_status"),
                "source_records": [observed],
                "classifications": [classification],
            }
            docs[did] = candidate
        else:
            candidate["source_records"].append(observed)
            candidate["classifications"].append(classification)
            if not candidate.get("official_source_url") and row.get("official_source_url"):
                candidate["official_source_url"] = row.get("official_source_url")
            if row.get("download_status") == "LOCAL_A0_AVAILABLE":
                candidate["download_status"] = "LOCAL_A0_AVAILABLE"
            if len(str(row.get("title") or "")) > len(str(candidate.get("title") or "")):
                candidate["title"] = row.get("title")

    for source in plan.get("source_registries", []):
        payload = load_json(REPO_ROOT / source["path"])
        for row in payload.get(source.get("documents_field", "documents"), []) or []:
            if isinstance(row, dict):
                add(row, str(source["source_id"]), classification_for(row, source))

    extra_source = {"classification_map": {}}
    for row in plan.get("extra_documents", []) or []:
        if isinstance(row, dict):
            add(row, "MASTER_PLAN_EXTRA", classification_for(row, extra_source))

    importance_rank = {"NECESSARY": 0, "DESIRABLE": 1, "INTERESTING_LATER": 2}
    maturity_rank = {"MIN": 0, "MEDIUM": 1, "MAX": 2}
    overrides = plan.get("official_route_overrides") or {}
    for doc in docs.values():
        classes = doc.get("classifications") or []
        strongest = sorted(
            classes,
            key=lambda c: (
                importance_rank.get(c["importance_class"], 9),
                maturity_rank.get(c["maturity_level"], 9),
            ),
        )[0]
        doc["maturity_level"] = strongest["maturity_level"]
        doc["importance_class"] = strongest["importance_class"]
        if overrides.get(doc["document_id"]):
            doc["official_source_url"] = overrides[doc["document_id"]]
    return sorted(docs.values(), key=lambda x: x["document_id"]), source_rows


def exact_reuse(doc: dict[str, Any]) -> dict[str, Any] | None:
    stem = base._safe_name(str(doc["document_id"]))
    meta_path = base.META_DIR / f"{stem}.json"
    if not meta_path.is_file():
        return None
    try:
        meta = load_json(meta_path)
    except (OSError, json.JSONDecodeError):
        return None
    if meta.get("status") not in {"NORMALIZED", "ACQUIRED_RAW"}:
        return None
    sha = str(meta.get("sha256") or "")
    raw_ref = str(meta.get("raw_path") or "")
    if len(sha) != 64 or not raw_ref:
        return None
    raw_path = REPO_ROOT / raw_ref
    if not raw_path.is_file() or hashlib.sha256(raw_path.read_bytes()).hexdigest() != sha:
        return None
    source_url = str(meta.get("source_url") or meta.get("final_url") or "")
    if not source_url or not base._is_official(source_url):
        return None
    return {
        "status": "REUSED_EXACT",
        "sha256": sha,
        "raw_path": raw_ref,
        "normalized_path": meta.get("normalized_path"),
        "source_url": source_url,
        "byte_length": raw_path.stat().st_size,
        "network_used": False,
    }


def robust_fetch(url: str) -> tuple[bytes, str | None, str, str]:
    artifact = ROBUST_FETCHER.fetch(
        url,
        timeout_seconds=base.TIMEOUT_SECONDS,
        max_bytes=base.MAX_BYTES,
    )
    final_url = str(artifact.final_url or url)
    if not base._is_official(final_url):
        raise RuntimeError(f"redirected off official allowlist: {final_url}")
    if not artifact.data:
        raise RuntimeError("empty response")
    return artifact.data, artifact.mime_type, final_url, "ROBUST_OFFICIAL_TRANSPORT"


def acquire(doc: dict[str, Any], progress: DownloadProgressRegistry) -> dict[str, Any]:
    did = str(doc["document_id"])
    started = time.perf_counter()
    common = {
        "document_id": did,
        "title": doc.get("title"),
        "domain": doc.get("domain"),
        "legal_status": doc.get("legal_status"),
        "maturity_level": doc.get("maturity_level"),
        "importance_class": doc.get("importance_class"),
        "source_records": doc.get("source_records") or [],
        "kb_auto_promotion": False,
    }

    reused = exact_reuse(doc)
    if reused:
        progress.update(
            did,
            status="REUSED",
            bytes_received=int(reused["byte_length"]),
            total_bytes=int(reused["byte_length"]),
            sha256=reused["sha256"],
            local_path=reused["raw_path"],
            force=True,
        )
        return {**common, **reused, "seconds": time.perf_counter() - started}

    if doc.get("download_status") == "LOCAL_A0_AVAILABLE":
        progress.update(did, status="REUSED", error="DECLARED_LOCAL_A0_NEEDS_HASH_INVENTORY", force=True)
        return {
            **common,
            "status": "REUSED_DECLARED_LOCAL_A0",
            "network_used": False,
            "needs_hash_inventory": True,
            "seconds": time.perf_counter() - started,
        }

    url = str(doc.get("official_source_url") or "").strip()
    if not url or not base._is_official(url):
        progress.update(did, status="FAILED", error="NEED_OFFICIAL_SOURCE", force=True)
        return {
            **common,
            "status": "NEED_OFFICIAL_SOURCE",
            "network_used": False,
            "official_source_url": url or None,
            "error_class": "MISSING_OR_NON_OFFICIAL_ROUTE",
            "seconds": time.perf_counter() - started,
        }

    progress.update(did, status="DOWNLOADING", force=True)
    try:
        data, mime, final_url, transport = robust_fetch(url)
        digest = hashlib.sha256(data).hexdigest()
        progress.update(did, status="HASHING", bytes_received=len(data), total_bytes=len(data), force=True)
        stem = base._safe_name(did)
        raw_path = base.RAW_DIR / f"{stem}__{digest}.bin"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        if not raw_path.exists():
            raw_path.write_bytes(data)
        if hashlib.sha256(raw_path.read_bytes()).hexdigest() != digest:
            raise RuntimeError("post-write SHA-256 mismatch")
        normalized, normalization = base._normalize(data, mime, final_url)
        normalized_path: Path | None = None
        if normalized and normalized.strip():
            normalized_path = base.NORMALIZED_DIR / f"{stem}__{digest}.txt"
            normalized_path.parent.mkdir(parents=True, exist_ok=True)
            normalized_path.write_text(normalized.strip() + "\n", encoding="utf-8")
        semantic_status = "DOWNLOADED"
        meta = {
            **common,
            "status": "NORMALIZED" if normalized_path else "ACQUIRED_RAW",
            "trust_tier": "A0_A1_OFFICIAL_ROUTE",
            "exact_official_evidence_acquired": True,
            "legal_truth_eligible": False,
            "currentness_verified": False,
            "promotion_block_reason": "CURRENTNESS_AND_AMENDMENT_CHAIN_NOT_VERIFIED",
            "source_url": final_url,
            "requested_source_url": url,
            "transport": transport,
            "mime_type": mime,
            "byte_length": len(data),
            "sha256": digest,
            "raw_path": rel(raw_path),
            "normalized_path": rel(normalized_path) if normalized_path else None,
            "normalization": normalization,
            "network_used": True,
            "seconds": time.perf_counter() - started,
        }
        base.META_DIR.mkdir(parents=True, exist_ok=True)
        (base.META_DIR / f"{stem}.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        progress.update(
            did,
            status=semantic_status,
            bytes_received=len(data),
            total_bytes=len(data),
            sha256=digest,
            local_path=rel(raw_path),
            force=True,
        )
        return {**meta, "status": "DOWNLOADED"}
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        progress.update(did, status="FAILED", error=error, force=True)
        return {
            **common,
            "status": "FAILED",
            "official_source_url": url,
            "error": error,
            "error_class": type(exc).__name__,
            "network_used": True,
            "seconds": time.perf_counter() - started,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reuse-first official security document master downloader")
    parser.add_argument(
        "--necessary-only",
        action="store_true",
        help="Only execute NECESSARY items; default executes the full deduplicated plan",
    )
    args = parser.parse_args()
    started = time.perf_counter()
    plan = load_json(PLAN_PATH)

    registry_proc = subprocess.run([sys.executable, str(BUILD_GLOBAL)], cwd=str(REPO_ROOT), check=False)
    registry_build_status = "PASS" if registry_proc.returncode == 0 else "FAILED"

    documents, source_rows = merge_plan(plan)
    if args.necessary_only:
        documents = [d for d in documents if d.get("importance_class") == "NECESSARY"]

    progress = DownloadProgressRegistry(
        "SECURITY_ENGINEER",
        registry_key="security_official_master",
        context={
            "task": "SECURITY_OFFICIAL_MASTER_DOWNLOAD",
            "workers": WORKERS,
            "mode": "NECESSARY_ONLY" if args.necessary_only else "ALL",
        },
    )
    progress.start(
        [
            {
                "item_id": d["document_id"],
                "file_name": d.get("title"),
                "target_id": d.get("domain"),
                "maturity_level": d.get("maturity_level"),
                "importance_class": d.get("importance_class"),
            }
            for d in documents
        ]
    )

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="security-official-master") as executor:
        futures = {executor.submit(acquire, doc, progress): doc for doc in documents}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            suffix = result.get("sha256") or result.get("error_class") or ""
            print(f"[{result.get('status')}] {result.get('document_id')} {suffix}")
    progress.finish()

    results.sort(key=lambda r: str(r.get("document_id") or ""))
    elapsed = time.perf_counter() - started
    failed_classes = Counter(
        str(r.get("error_class") or "UNKNOWN")
        for r in results
        if r.get("status") == "FAILED"
    )
    counters = {
        "documents_unique_total": len(documents),
        "source_rows_total": source_rows,
        "duplicates_collapsed_total": max(0, source_rows - len(documents)),
        "reused_exact_total": sum(r.get("status") == "REUSED_EXACT" for r in results),
        "reused_declared_local_a0_total": sum(r.get("status") == "REUSED_DECLARED_LOCAL_A0" for r in results),
        "downloaded_total": sum(r.get("status") == "DOWNLOADED" for r in results),
        "need_official_source_total": sum(r.get("status") == "NEED_OFFICIAL_SOURCE" for r in results),
        "failed_total": sum(r.get("status") == "FAILED" for r in results),
        "bytes_downloaded": sum(
            int(r.get("byte_length") or 0)
            for r in results
            if r.get("status") == "DOWNLOADED"
        ),
    }
    status = (
        "FAILED"
        if counters["failed_total"]
        else "PASS_WITH_GAPS"
        if counters["need_official_source_total"]
        else "PASS"
    )
    report = {
        "schema_version": "1.1",
        "record_type": "SECURITY_OFFICIAL_MASTER_DOWNLOAD_RUN",
        "status": status,
        "observed_at": utc_now(),
        "plan": rel(PLAN_PATH),
        "workers": WORKERS,
        "execution_mode": "NECESSARY_ONLY" if args.necessary_only else "ALL_UNIQUE_DOCUMENTS",
        "global_registry_build_status": registry_build_status,
        **counters,
        "failed_error_classes": dict(sorted(failed_classes.items())),
        "elapsed_seconds": elapsed,
        "throughput_downloaded_docs_per_second": counters["downloaded_total"] / elapsed if elapsed > 0 else 0.0,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "transport_policy": "RobustOfficialArtifactFetcher: bounded urllib primary plus TLS-verifying curl fallback; no TLS weakening and final host remains official allowlist constrained.",
        "reuse_policy": "Exact official SHA reuse first; declared LOCAL_A0 is not redownloaded; A2 does not satisfy official exact acquisition.",
        "legal_truth_policy": "Official exact bytes establish source evidence only. CURRENT status/amendment-chain verification remains a separate review gate.",
        "kb_auto_promotion": False,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, ensure_ascii=False, indent=2))
    print(f"Report: {rel(REPORT_PATH)}")
    return 1 if counters["failed_total"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
