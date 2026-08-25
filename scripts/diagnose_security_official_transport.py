from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from father_osint.acquisition import UrllibArtifactFetcher  # noqa: E402
from father_osint.official_transport import CurlArtifactFetcher, RobustOfficialArtifactFetcher  # noqa: E402

REPORT = ROOT / "reports" / "security_current_only" / "LATEST_OFFICIAL_TRANSPORT_DIAGNOSTIC.json"
TIMEOUT_SECONDS = 45.0
MAX_BYTES = 5 * 1024 * 1024

PROBES = [
    {
        "probe_id": "PRAVO_FSTEC_235",
        "url": "https://publication.pravo.gov.ru/document/0001201802220016",
        "expected_host": "publication.pravo.gov.ru",
    },
    {
        "probe_id": "GOVERNMENT_PP_687",
        "url": "https://government.ru/docs/all/65436/",
        "expected_host": "government.ru",
    },
    {
        "probe_id": "GOST_56939_2024",
        "url": "https://protect.gost.ru/gost/details/f3818925-a96f-4f55-96e9-46b44720ee64",
        "expected_host": "protect.gost.ru",
    },
]


def result_ok(name: str, artifact, elapsed: float) -> dict[str, Any]:
    return {
        "transport": name,
        "status": "PASS",
        "elapsed_seconds": elapsed,
        "final_url": artifact.final_url,
        "mime_type": artifact.mime_type,
        "bytes": len(artifact.data),
        "sha256": hashlib.sha256(artifact.data).hexdigest(),
    }


def result_fail(name: str, exc: Exception, elapsed: float) -> dict[str, Any]:
    text = f"{type(exc).__name__}: {exc}"
    return {
        "transport": name,
        "status": "FAIL",
        "elapsed_seconds": elapsed,
        "error_class": type(exc).__name__,
        "error": text[:4000],
    }


def run_transport(name: str, fetcher, url: str) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        artifact = fetcher.fetch(url, timeout_seconds=TIMEOUT_SECONDS, max_bytes=MAX_BYTES)
        return result_ok(name, artifact, time.perf_counter() - started)
    except Exception as exc:
        return result_fail(name, exc, time.perf_counter() - started)


def main() -> int:
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    for probe in PROBES:
        url = probe["url"]
        transports = [
            run_transport("URLLIB", UrllibArtifactFetcher(), url),
            run_transport("CURL", CurlArtifactFetcher(), url),
            run_transport(
                "ROBUST",
                RobustOfficialArtifactFetcher(minimum_timeout_seconds=TIMEOUT_SECONDS),
                url,
            ),
        ]
        rows.append({**probe, "transports": transports})

    robust_pass_total = sum(
        any(t["transport"] == "ROBUST" and t["status"] == "PASS" for t in row["transports"])
        for row in rows
    )
    payload = {
        "schema_version": "1.1",
        "record_type": "SECURITY_OFFICIAL_TRANSPORT_DIAGNOSTIC",
        "mode": "READ_ONLY_NETWORK_PROBE",
        "status": "PASS" if robust_pass_total == len(PROBES) else "FAIL",
        "probes_total": len(PROBES),
        "robust_pass_total": robust_pass_total,
        "timeout_seconds": TIMEOUT_SECONDS,
        "max_bytes": MAX_BYTES,
        "elapsed_seconds": time.perf_counter() - started,
        "note": "Read-only transport diagnosis. No source bytes are persisted and no KB state is changed.",
        "results": rows,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
