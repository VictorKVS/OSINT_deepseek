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

from father_osint.official_transport import RobustOfficialArtifactFetcher  # noqa: E402

REPORT = ROOT / "reports" / "security_current_only" / "LATEST_OFFICIAL_TRANSPORT_DIAGNOSTIC.json"
TIMEOUT_SECONDS = 20.0
MAX_BYTES = 5 * 1024 * 1024

PROBES = [
    {
        "probe_id": "PRAVO_FSTEC_235",
        "url": "https://publication.pravo.gov.ru/document/0001201802220016",
        "expected_host": "publication.pravo.gov.ru",
        "route_class": "OFFICIAL_PUBLICATION_PRIMARY",
    },
    {
        "probe_id": "GOVERNMENT_PP_687",
        "url": "https://government.ru/docs/all/65436/",
        "expected_host": "government.ru",
        "route_class": "GOVERNMENT_OFFICIAL",
    },
    {
        "probe_id": "GOST_56939_2024",
        "url": "https://protect.gost.ru/gost/details/f3818925-a96f-4f55-96e9-46b44720ee64",
        "expected_host": "protect.gost.ru",
        "route_class": "ROSSTANDART_OFFICIAL",
    },
    {
        "probe_id": "RG_FSTEC_117",
        "url": "https://rg.ru/documents/2025/06/18/fstek-prikaz117-site-dok.html",
        "expected_host": "rg.ru",
        "route_class": "OFFICIAL_PUBLICATION_ALTERNATIVE",
    },
    {
        "probe_id": "FSTEC_239",
        "url": "https://fstec.ru/normotvorcheskaya/akty/53-prikazy/1592-prikaz-fstek-rossii-ot-25-dekabrya-2017-g-n-239",
        "expected_host": "fstec.ru",
        "route_class": "PRIMARY_REGULATOR",
    },
]


def result_ok(artifact, elapsed: float) -> dict[str, Any]:
    return {
        "transport": "ROBUST",
        "status": "PASS",
        "elapsed_seconds": elapsed,
        "final_url": artifact.final_url,
        "mime_type": artifact.mime_type,
        "bytes": len(artifact.data),
        "sha256": hashlib.sha256(artifact.data).hexdigest(),
    }


def result_fail(exc: Exception, elapsed: float) -> dict[str, Any]:
    text = f"{type(exc).__name__}: {exc}"
    return {
        "transport": "ROBUST",
        "status": "FAIL",
        "elapsed_seconds": elapsed,
        "error_class": type(exc).__name__,
        "error": text[:4000],
    }


def run_probe(url: str) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        artifact = RobustOfficialArtifactFetcher(
            minimum_timeout_seconds=TIMEOUT_SECONDS
        ).fetch(url, timeout_seconds=TIMEOUT_SECONDS, max_bytes=MAX_BYTES)
        return result_ok(artifact, time.perf_counter() - started)
    except Exception as exc:
        return result_fail(exc, time.perf_counter() - started)


def main() -> int:
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    for probe in PROBES:
        rows.append({**probe, "result": run_probe(str(probe["url"]))})

    robust_pass_total = sum(row["result"]["status"] == "PASS" for row in rows)
    reachable_hosts = [row["expected_host"] for row in rows if row["result"]["status"] == "PASS"]
    unreachable_hosts = [row["expected_host"] for row in rows if row["result"]["status"] != "PASS"]
    payload = {
        "schema_version": "1.2",
        "record_type": "SECURITY_OFFICIAL_TRANSPORT_DIAGNOSTIC",
        "mode": "READ_ONLY_OFFICIAL_ROUTE_MATRIX",
        "status": "PASS" if robust_pass_total == len(PROBES) else "FAIL",
        "probes_total": len(PROBES),
        "robust_pass_total": robust_pass_total,
        "reachable_hosts": reachable_hosts,
        "unreachable_hosts": unreachable_hosts,
        "timeout_seconds": TIMEOUT_SECONDS,
        "max_bytes": MAX_BYTES,
        "elapsed_seconds": time.perf_counter() - started,
        "note": "Read-only official-route matrix. No source bytes are persisted and no KB state is changed. FAIL does not mean documents do not exist; it means one or more tested official network routes are unreachable from this runtime.",
        "results": rows,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
