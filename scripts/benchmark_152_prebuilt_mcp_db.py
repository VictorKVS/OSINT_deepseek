from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.benchmark_152_reuse import TARGET_ID, TARGET_NUMBER, TARGET_TITLE_MARKER, _compare, _father_reference

RUNTIME = REPO_ROOT / ".runtime" / "external_kb" / "russian-law-mcp"
PACK_DIR = RUNTIME / "pack"
DB_PATH = RUNTIME / "database.db"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "BENCHMARK_152_PREBUILT_MCP_DB.json"
PACKAGE_SPEC = "@ansvar/russian-law-mcp@0.1.0"
PACKAGE_DB_MEMBER = "package/data/database.db"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _acquire_db() -> dict[str, object]:
    if DB_PATH.is_file():
        return {
            "mode": "REUSED_LOCAL_PREBUILT_DB",
            "download_seconds": 0.0,
            "extract_seconds": 0.0,
            "package_spec": PACKAGE_SPEC,
        }

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        raise RuntimeError("NPM_NOT_FOUND")

    RUNTIME.mkdir(parents=True, exist_ok=True)
    PACK_DIR.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    completed = subprocess.run(
        [npm, "pack", PACKAGE_SPEC, "--json", "--pack-destination", str(PACK_DIR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=1200,
    )
    download_seconds = time.perf_counter() - started
    if completed.returncode != 0:
        raise RuntimeError("NPM_PACK_FAILED: " + (completed.stderr[-2000:] or completed.stdout[-2000:]))

    try:
        payload = json.loads(completed.stdout)
        filename = str(payload[0]["filename"])
    except Exception as exc:
        raise RuntimeError("NPM_PACK_OUTPUT_INVALID") from exc

    archive = PACK_DIR / filename
    if not archive.is_file():
        raise RuntimeError(f"NPM_ARCHIVE_MISSING: {archive}")

    extract_started = time.perf_counter()
    with tarfile.open(archive, "r:gz") as tf:
        try:
            member = tf.getmember(PACKAGE_DB_MEMBER)
        except KeyError as exc:
            raise RuntimeError("PREBUILT_DATABASE_NOT_BUNDLED_IN_NPM_PACKAGE") from exc
        if not member.isfile():
            raise RuntimeError("PREBUILT_DATABASE_MEMBER_NOT_FILE")
        source = tf.extractfile(member)
        if source is None:
            raise RuntimeError("PREBUILT_DATABASE_EXTRACTION_FAILED")
        tmp = DB_PATH.with_suffix(".db.tmp")
        with tmp.open("wb") as target:
            shutil.copyfileobj(source, target, length=1024 * 1024)
        tmp.replace(DB_PATH)
    extract_seconds = time.perf_counter() - extract_started

    return {
        "mode": "DOWNLOADED_PREBUILT_NPM_DB",
        "download_seconds": download_seconds,
        "extract_seconds": extract_seconds,
        "package_spec": PACKAGE_SPEC,
        "package_archive_bytes": archive.stat().st_size,
    }


def _query_db() -> tuple[dict[str, object], str, dict[str, object]]:
    started = time.perf_counter()
    conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        quick_check = conn.execute("PRAGMA quick_check").fetchone()[0]
        metadata = {
            row["key"]: row["value"]
            for row in conn.execute("SELECT key, value FROM db_metadata")
        }
        counts = {
            "laws": conn.execute("SELECT COUNT(*) FROM laws").fetchone()[0],
            "provisions": conn.execute("SELECT COUNT(*) FROM provisions").fetchone()[0],
        }

        law = conn.execute(
            "SELECT id, title, identifier, law_type, status, effective_date, publication_date, "
            "source_url, last_amended, last_updated, provision_count "
            "FROM laws WHERE identifier = ? OR title LIKE ? ORDER BY provision_count DESC LIMIT 1",
            (TARGET_NUMBER, f"%{TARGET_TITLE_MARKER}%"),
        ).fetchone()
        if law is None:
            raise RuntimeError("152_FZ_NOT_FOUND_IN_PREBUILT_DB")

        provisions = conn.execute(
            "SELECT article, title, content, provision_ref, order_index "
            "FROM provisions WHERE law_id = ? ORDER BY order_index, id",
            (law["id"],),
        ).fetchall()
        if not provisions:
            raise RuntimeError("152_FZ_HAS_NO_PROVISIONS_IN_PREBUILT_DB")

        text = "\n".join(str(row["content"] or "") for row in provisions if str(row["content"] or "").strip())
        law_payload = dict(law)
        law_payload["retrieved_provisions"] = len(provisions)
        return law_payload, text, {
            "quick_check": quick_check,
            "metadata": metadata,
            "counts": counts,
            "query_seconds": time.perf_counter() - started,
        }
    finally:
        conn.close()


def main() -> int:
    total_started = time.perf_counter()

    father_started = time.perf_counter()
    father_text, father_meta = _father_reference()
    father_seconds = time.perf_counter() - father_started

    acquire_started = time.perf_counter()
    try:
        acquisition = _acquire_db()
    except Exception as exc:
        failure = {
            "record_type": "REUSE_FIRST_BENCHMARK_152_PREBUILT_MCP_DB_FAILURE",
            "error": f"{type(exc).__name__}: {exc}",
            "package_spec": PACKAGE_SPEC,
            "timing_seconds": {
                "father_reference_load": father_seconds,
                "acquisition": time.perf_counter() - acquire_started,
                "total": time.perf_counter() - total_started,
            },
            "legal_truth_promoted": False,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2))
        return 2

    db_sha = _sha256(DB_PATH)
    db_bytes = DB_PATH.stat().st_size

    query_started = time.perf_counter()
    try:
        law, external_text, db_info = _query_db()
    except Exception as exc:
        print(f"DATABASE_QUERY_FAILED: {type(exc).__name__}: {exc}")
        return 2
    query_seconds = time.perf_counter() - query_started

    compare_started = time.perf_counter()
    comparison = _compare(father_text, external_text)
    compare_seconds = time.perf_counter() - compare_started

    identifier_match = TARGET_NUMBER.casefold() in str(law.get("identifier") or "").casefold()
    title_match = TARGET_TITLE_MARKER in str(law.get("title") or "").casefold()
    identity_pass = identifier_match and title_match
    total_seconds = time.perf_counter() - total_started

    result = {
        "record_type": "REUSE_FIRST_BENCHMARK_152_PREBUILT_MCP_DB",
        "target_document_id": TARGET_ID,
        "provider": "ansvar_russian_law_mcp_prebuilt_sqlite",
        "package_spec": PACKAGE_SPEC,
        "database": {
            "path": DB_PATH.relative_to(REPO_ROOT).as_posix(),
            "bytes": db_bytes,
            "sha256": db_sha,
            "quick_check": db_info["quick_check"],
            "metadata": db_info["metadata"],
            "counts": db_info["counts"],
        },
        "acquisition": acquisition,
        "law": law,
        "identity": {
            "identifier_match": identifier_match,
            "title_marker_match": title_match,
            "identity_pass": identity_pass,
        },
        "father_reference": father_meta,
        "comparison": comparison,
        "timing_seconds": {
            "father_reference_load": father_seconds,
            "database_query": query_seconds,
            "content_compare": compare_seconds,
            "total": total_seconds,
        },
        "interpretation": {
            "role": "REFERENCE_KB_NOT_A0_PROOF",
            "database_is_local_after_first_acquisition": True,
            "network_required_on_warm_path": False,
            "legal_truth_promoted": False,
        },
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"ACQUISITION_MODE={acquisition['mode']}")
    print(f"DB_BYTES={db_bytes}")
    print(f"DB_QUERY_SECONDS={query_seconds:.6f}")
    print(f"COMPARE_SECONDS={compare_seconds:.6f}")
    print(f"TOTAL_SECONDS={total_seconds:.6f}")
    print(f"IDENTITY_PASS={str(identity_pass).lower()}")
    return 0 if identity_pass and db_info["quick_check"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
