from __future__ import annotations

import hashlib
import importlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REVIEW = STORE_ROOT / "review" / "batch_review_manifest.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "BENCHMARK_152_REUSE.json"
CANDIDATE = REPO_ROOT / ".runtime" / "benchmarks" / "152_fz" / "ruslawod_candidate.json"
VENDOR_DIR = REPO_ROOT / ".runtime" / "benchmarks" / "vendor"
TARGET_ID = "DOC-RU-FZ-152-2006"
TARGET_NUMBER = "152-ФЗ"
TARGET_DATE = "27.07.2006"
TARGET_TITLE_MARKER = "персональных данных"
DATASET = "irlspbru/RusLawOD"
DATASET_SERVER = "https://datasets-server.huggingface.co"
DUCKDB_VERSION = "1.5.5"
PARQUET_URLS = tuple(
    f"https://huggingface.co/datasets/{DATASET}/resolve/main/ruslawod_{index:02d}.parquet"
    for index in range(1, 12)
)


class ProviderUnavailable(RuntimeError):
    def __init__(self, message: str, attempts: list[dict[str, Any]] | None = None) -> None:
        super().__init__(message)
        self.attempts = attempts or []


def _http_json_with_retries(
    url: str,
    *,
    timeout: int = 30,
    retries: int = 3,
    backoff_seconds: float = 0.6,
) -> tuple[dict[str, Any], int, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    last_error: BaseException | None = None
    for attempt in range(1, retries + 1):
        started = time.perf_counter()
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "FATHER-Knowledge-Factory/152-reuse-benchmark",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
            elapsed = time.perf_counter() - started
            attempts.append({
                "attempt": attempt,
                "elapsed_seconds": elapsed,
                "response_bytes": len(raw),
                "status": "SUCCESS",
                "error": None,
            })
            return json.loads(raw.decode("utf-8")), len(raw), attempts
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            elapsed = time.perf_counter() - started
            status_code = exc.code if isinstance(exc, urllib.error.HTTPError) else None
            attempts.append({
                "attempt": attempt,
                "elapsed_seconds": elapsed,
                "response_bytes": 0,
                "status": "FAILED",
                "http_status": status_code,
                "error": f"{type(exc).__name__}: {exc}",
            })
            if attempt < retries:
                time.sleep(backoff_seconds * (2 ** (attempt - 1)))
    raise ProviderUnavailable(f"HTTP provider failed after {retries} attempts: {last_error}", attempts)


def _dataset_row(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("row")
    return value if isinstance(value, dict) else item


def _fetch_ruslawod_dataset_server() -> tuple[dict[str, Any], dict[str, Any]]:
    transport_attempts: list[dict[str, Any]] = []
    where_variants = (
        '"docNumberIPS" = \'152-ФЗ\' AND "docdateIPS" = \'27.07.2006\'',
        "docNumberIPS = '152-ФЗ' AND docdateIPS = '27.07.2006'",
    )
    for where in where_variants:
        params = urllib.parse.urlencode(
            {
                "dataset": DATASET,
                "config": "default",
                "split": "train",
                "where": where,
                "offset": 0,
                "length": 20,
            }
        )
        url = f"{DATASET_SERVER}/filter?{params}"
        started = time.perf_counter()
        try:
            payload, byte_count, retry_attempts = _http_json_with_retries(url)
            rows = [_dataset_row(item) for item in payload.get("rows", [])]
            transport_attempts.append({
                "method": "filter",
                "url": url,
                "elapsed_seconds": time.perf_counter() - started,
                "response_bytes": byte_count,
                "rows": len(rows),
                "retry_attempts": retry_attempts,
                "error": None,
            })
            exact = [
                row
                for row in rows
                if str(row.get("docNumberIPS", "")).strip() == TARGET_NUMBER
                and str(row.get("docdateIPS", "")).strip() == TARGET_DATE
            ]
            if exact:
                return exact[0], {
                    "provider": "huggingface_dataset_server",
                    "selected_method": "filter",
                    "attempts": transport_attempts,
                }
        except ProviderUnavailable as exc:
            transport_attempts.append({
                "method": "filter",
                "url": url,
                "elapsed_seconds": time.perf_counter() - started,
                "response_bytes": 0,
                "rows": 0,
                "retry_attempts": exc.attempts,
                "error": str(exc),
            })

    params = urllib.parse.urlencode(
        {
            "dataset": DATASET,
            "config": "default",
            "split": "train",
            "query": TARGET_NUMBER,
            "offset": 0,
            "length": 100,
        }
    )
    url = f"{DATASET_SERVER}/search?{params}"
    started = time.perf_counter()
    try:
        payload, byte_count, retry_attempts = _http_json_with_retries(url)
        rows = [_dataset_row(item) for item in payload.get("rows", [])]
        transport_attempts.append({
            "method": "search",
            "url": url,
            "elapsed_seconds": time.perf_counter() - started,
            "response_bytes": byte_count,
            "rows": len(rows),
            "retry_attempts": retry_attempts,
            "error": None,
        })
        exact = [
            row
            for row in rows
            if str(row.get("docNumberIPS", "")).strip() == TARGET_NUMBER
            and str(row.get("docdateIPS", "")).strip() == TARGET_DATE
        ]
        if exact:
            return exact[0], {
                "provider": "huggingface_dataset_server",
                "selected_method": "search",
                "attempts": transport_attempts,
            }
    except ProviderUnavailable as exc:
        transport_attempts.append({
            "method": "search",
            "url": url,
            "elapsed_seconds": time.perf_counter() - started,
            "response_bytes": 0,
            "rows": 0,
            "retry_attempts": exc.attempts,
            "error": str(exc),
        })

    raise ProviderUnavailable("Hugging Face Dataset Server did not return the exact 152-ФЗ row", transport_attempts)


def _ensure_duckdb() -> tuple[Any, dict[str, Any]]:
    started = time.perf_counter()
    try:
        module = importlib.import_module("duckdb")
        return module, {
            "installed_now": False,
            "version": getattr(module, "__version__", None),
            "elapsed_seconds": time.perf_counter() - started,
            "location": "existing_environment",
        }
    except ImportError:
        pass

    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Dataset Server unavailable. Installing isolated fallback duckdb=={DUCKDB_VERSION} ...")
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        f"duckdb=={DUCKDB_VERSION}",
        "--target",
        str(VENDOR_DIR),
        "--disable-pip-version-check",
        "--no-input",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if completed.returncode != 0:
        raise ProviderUnavailable(
            "DuckDB fallback dependency installation failed: "
            + (completed.stderr[-1200:] or completed.stdout[-1200:])
        )
    sys.path.insert(0, str(VENDOR_DIR))
    importlib.invalidate_caches()
    module = importlib.import_module("duckdb")
    return module, {
        "installed_now": True,
        "version": getattr(module, "__version__", None),
        "elapsed_seconds": time.perf_counter() - started,
        "location": VENDOR_DIR.relative_to(REPO_ROOT).as_posix(),
    }


def _fetch_ruslawod_duckdb() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    duckdb, dependency = _ensure_duckdb()
    connection = duckdb.connect(database=":memory:")
    attempts: list[dict[str, Any]] = []
    try:
        extension_started = time.perf_counter()
        try:
            connection.execute("INSTALL httpfs")
            connection.execute("LOAD httpfs")
            extension_error = None
        except Exception as exc:  # DuckDB extension errors are version-specific.
            extension_error = f"{type(exc).__name__}: {exc}"
        extension_seconds = time.perf_counter() - extension_started

        for url in PARQUET_URLS:
            started = time.perf_counter()
            escaped = url.replace("'", "''")
            query = f'''
                SELECT
                    "pravogovruNd", "issuedByIPS", "docdateIPS", "docNumberIPS",
                    "doc_typeIPS", "headingIPS", "statusIPS", "textIPS"
                FROM read_parquet('{escaped}')
                WHERE "docNumberIPS" = ? AND "docdateIPS" = ?
                LIMIT 1
            '''
            try:
                row = connection.execute(query, [TARGET_NUMBER, TARGET_DATE]).fetchone()
                attempts.append({
                    "method": "duckdb_remote_parquet",
                    "url": url,
                    "elapsed_seconds": time.perf_counter() - started,
                    "found": row is not None,
                    "error": None,
                })
                if row is not None:
                    columns = [
                        "pravogovruNd",
                        "issuedByIPS",
                        "docdateIPS",
                        "docNumberIPS",
                        "doc_typeIPS",
                        "headingIPS",
                        "statusIPS",
                        "textIPS",
                    ]
                    return dict(zip(columns, row)), {
                        "provider": "duckdb_remote_parquet",
                        "selected_method": "remote_parquet_filter_pushdown",
                        "files_scanned": len(attempts),
                        "httpfs_setup_seconds": extension_seconds,
                        "httpfs_setup_error": extension_error,
                        "attempts": attempts,
                    }, dependency
            except Exception as exc:
                attempts.append({
                    "method": "duckdb_remote_parquet",
                    "url": url,
                    "elapsed_seconds": time.perf_counter() - started,
                    "found": False,
                    "error": f"{type(exc).__name__}: {exc}",
                })
    finally:
        connection.close()

    raise ProviderUnavailable("DuckDB remote Parquet fallback did not find 152-ФЗ", attempts)


def _fetch_ruslawod_152() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    provider_failures: list[dict[str, Any]] = []
    try:
        candidate, transport = _fetch_ruslawod_dataset_server()
        return candidate, transport, {
            "installed_now": False,
            "version": None,
            "elapsed_seconds": 0.0,
            "location": None,
        }
    except ProviderUnavailable as exc:
        provider_failures.append({
            "provider": "huggingface_dataset_server",
            "error": str(exc),
            "attempts": exc.attempts,
        })

    try:
        candidate, transport, dependency = _fetch_ruslawod_duckdb()
        transport["provider_failures_before_success"] = provider_failures
        return candidate, transport, dependency
    except ProviderUnavailable as exc:
        provider_failures.append({
            "provider": "duckdb_remote_parquet",
            "error": str(exc),
            "attempts": exc.attempts,
        })
        raise ProviderUnavailable("All RusLawOD retrieval providers failed", provider_failures) from exc


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _father_reference() -> tuple[str, dict[str, Any]]:
    if not REVIEW.is_file():
        raise RuntimeError("FATHER review manifest is missing; run the normal PDN conveyor first")
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    target = next(
        (item for item in review.get("documents", []) if item.get("document_id") == TARGET_ID),
        None,
    )
    if not target:
        raise RuntimeError("152-ФЗ is missing from FATHER review manifest")
    chunks_rel = target.get("chunks_path")
    if not chunks_rel:
        raise RuntimeError("152-ФЗ chunks_path is missing")
    chunks_path = STORE_ROOT / str(chunks_rel)
    if not chunks_path.is_file():
        raise RuntimeError(f"152-ФЗ chunks are missing: {chunks_path}")
    chunks = _read_jsonl(chunks_path)
    text = "\n".join(str(row.get("text", "")) for row in chunks if str(row.get("text", "")).strip())
    return text, {
        "artifact_sha256": target.get("artifact_sha256"),
        "version_id": target.get("version_id"),
        "chunks_path": str(chunks_rel),
        "chunks": len(chunks),
    }


def _tokens(text: str) -> list[str]:
    normalized = text.casefold().replace("ё", "е")
    return re.findall(r"[а-яa-z0-9]+", normalized, flags=re.IGNORECASE)


def _shingles(tokens: list[str], width: int = 5) -> set[tuple[str, ...]]:
    if len(tokens) < width:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[index : index + width]) for index in range(len(tokens) - width + 1)}


def _compare(father_text: str, external_text: str) -> dict[str, Any]:
    father_tokens = _tokens(father_text)
    external_tokens = _tokens(external_text)
    father_shingles = _shingles(father_tokens)
    external_shingles = _shingles(external_tokens)
    union = father_shingles | external_shingles
    intersection = father_shingles & external_shingles
    return {
        "father_chars": len(father_text),
        "external_chars": len(external_text),
        "father_tokens": len(father_tokens),
        "external_tokens": len(external_tokens),
        "sequence_ratio": SequenceMatcher(a=father_tokens, b=external_tokens, autojunk=False).ratio(),
        "five_token_shingle_jaccard": (len(intersection) / len(union)) if union else None,
        "shared_five_token_shingles": len(intersection),
        "father_five_token_shingles": len(father_shingles),
        "external_five_token_shingles": len(external_shingles),
    }


def main() -> int:
    total_started = time.perf_counter()

    reference_started = time.perf_counter()
    father_text, father_meta = _father_reference()
    father_reference_seconds = time.perf_counter() - reference_started

    download_started = time.perf_counter()
    try:
        candidate, transport, dependency = _fetch_ruslawod_152()
    except ProviderUnavailable as exc:
        failure = {
            "record_type": "REUSE_FIRST_BENCHMARK_152_FZ_FAILURE",
            "target_document_id": TARGET_ID,
            "error": str(exc),
            "provider_attempts": exc.attempts,
            "timing_seconds": {
                "father_reference_load": father_reference_seconds,
                "external_lookup_and_download": time.perf_counter() - download_started,
                "total": time.perf_counter() - total_started,
            },
            "legal_truth_promoted": False,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2))
        return 2
    download_seconds = time.perf_counter() - download_started

    CANDIDATE.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE.write_text(json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    external_text = str(candidate.get("textIPS") or "")
    if not external_text.strip():
        raise RuntimeError("RusLawOD candidate has no textIPS")

    compare_started = time.perf_counter()
    comparison = _compare(father_text, external_text)
    compare_seconds = time.perf_counter() - compare_started

    number_match = str(candidate.get("docNumberIPS", "")).strip() == TARGET_NUMBER
    date_match = str(candidate.get("docdateIPS", "")).strip() == TARGET_DATE
    title = str(candidate.get("headingIPS") or "")
    title_match = TARGET_TITLE_MARKER in title.casefold()
    identity_pass = number_match and date_match and title_match

    total_seconds = time.perf_counter() - total_started
    result = {
        "record_type": "REUSE_FIRST_BENCHMARK_152_FZ",
        "target_document_id": TARGET_ID,
        "successful_provider": transport.get("provider"),
        "external_source": {
            "dataset": DATASET,
            "source_class": "BOOTSTRAP_CORPUS_NOT_A0_PROOF",
            "candidate_saved_to": CANDIDATE.relative_to(REPO_ROOT).as_posix(),
            "pravogovruNd": candidate.get("pravogovruNd"),
            "docNumberIPS": candidate.get("docNumberIPS"),
            "docdateIPS": candidate.get("docdateIPS"),
            "headingIPS": candidate.get("headingIPS"),
            "issuedByIPS": candidate.get("issuedByIPS"),
            "statusIPS": candidate.get("statusIPS"),
        },
        "father_reference": father_meta,
        "identity": {
            "number_match": number_match,
            "date_match": date_match,
            "title_marker_match": title_match,
            "identity_pass": identity_pass,
        },
        "comparison": comparison,
        "timing_seconds": {
            "father_reference_load": father_reference_seconds,
            "external_lookup_and_download": download_seconds,
            "dependency_setup": float(dependency.get("elapsed_seconds") or 0.0),
            "content_compare": compare_seconds,
            "total": total_seconds,
        },
        "dependency": dependency,
        "transport": transport,
        "interpretation": {
            "exact_byte_equality_expected": False,
            "reason": "RusLawOD is a normalized bootstrap corpus, while FATHER evidence is the preserved official-publication capture; compare identity/content, not raw bytes.",
            "legal_truth_promoted": False,
        },
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"PROVIDER={transport.get('provider')}")
    print(f"TOTAL_SECONDS={total_seconds:.3f}")
    print(f"DOWNLOAD_SECONDS={download_seconds:.3f}")
    print(f"DEPENDENCY_SETUP_SECONDS={float(dependency.get('elapsed_seconds') or 0.0):.3f}")
    print(f"COMPARE_SECONDS={compare_seconds:.3f}")
    print(f"IDENTITY_PASS={str(identity_pass).lower()}")
    return 0 if identity_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
