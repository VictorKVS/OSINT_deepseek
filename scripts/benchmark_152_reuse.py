from __future__ import annotations

import hashlib
import json
import re
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
TARGET_ID = "DOC-RU-FZ-152-2006"
TARGET_NUMBER = "152-ФЗ"
TARGET_DATE = "27.07.2006"
TARGET_TITLE_MARKER = "персональных данных"
DATASET = "irlspbru/RusLawOD"
DATASET_SERVER = "https://datasets-server.huggingface.co"


def _http_json(url: str, timeout: int = 30) -> tuple[dict[str, Any], int]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "FATHER-Knowledge-Factory/152-reuse-benchmark",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw.decode("utf-8")), len(raw)


def _dataset_row(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("row")
    return value if isinstance(value, dict) else item


def _fetch_ruslawod_152() -> tuple[dict[str, Any], dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
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
            payload, byte_count = _http_json(url)
            elapsed = time.perf_counter() - started
            rows = [_dataset_row(item) for item in payload.get("rows", [])]
            attempts.append({
                "method": "filter",
                "url": url,
                "elapsed_seconds": elapsed,
                "response_bytes": byte_count,
                "rows": len(rows),
                "error": None,
            })
            exact = [
                row
                for row in rows
                if str(row.get("docNumberIPS", "")).strip() == TARGET_NUMBER
                and str(row.get("docdateIPS", "")).strip() == TARGET_DATE
            ]
            if exact:
                return exact[0], {"attempts": attempts, "selected_method": "filter"}
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            attempts.append({
                "method": "filter",
                "url": url,
                "elapsed_seconds": time.perf_counter() - started,
                "response_bytes": 0,
                "rows": 0,
                "error": f"{type(exc).__name__}: {exc}",
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
    payload, byte_count = _http_json(url)
    elapsed = time.perf_counter() - started
    rows = [_dataset_row(item) for item in payload.get("rows", [])]
    attempts.append({
        "method": "search",
        "url": url,
        "elapsed_seconds": elapsed,
        "response_bytes": byte_count,
        "rows": len(rows),
        "error": None,
    })
    exact = [
        row
        for row in rows
        if str(row.get("docNumberIPS", "")).strip() == TARGET_NUMBER
        and str(row.get("docdateIPS", "")).strip() == TARGET_DATE
    ]
    if not exact:
        raise RuntimeError("RusLawOD query returned no exact 152-ФЗ / 27.07.2006 row")
    return exact[0], {"attempts": attempts, "selected_method": "search"}


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
    candidate, transport = _fetch_ruslawod_152()
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
            "content_compare": compare_seconds,
            "total": total_seconds,
        },
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
    print(f"TOTAL_SECONDS={total_seconds:.3f}")
    print(f"DOWNLOAD_SECONDS={download_seconds:.3f}")
    print(f"COMPARE_SECONDS={compare_seconds:.3f}")
    print(f"IDENTITY_PASS={str(identity_pass).lower()}")
    return 0 if identity_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
