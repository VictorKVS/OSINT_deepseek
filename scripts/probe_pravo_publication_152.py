from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.external_assets import authorize_external_asset
from father_osint.pravo_publication import PravoPublicationClient


REPORT = REPO_ROOT / "reports" / "pdn_live" / "PROBE_PRAVO_PUBLICATION_152.json"
TARGET_NUMBER = "152-ФЗ"
TARGET_DATE = "2006-07-27"
TARGET_TITLE_MARKER = "персональных данных"


def _transport_state(client: PravoPublicationClient) -> dict[str, object]:
    transport = client.transport
    return {
        "transport": getattr(transport, "last_transport", None),
        "transport_failures": list(getattr(transport, "last_failures", []) or []),
    }


def main() -> int:
    started = time.perf_counter()
    asset = authorize_external_asset("publication-pravo-official-api", "proof_acquisition")
    client = PravoPublicationClient()

    search_started = time.perf_counter()
    try:
        hits, search_meta = client.search_documents(
            number=TARGET_NUMBER,
            page_size=30,
            page=1,
            timeout_seconds=30.0,
        )
    except Exception as exc:
        transport_state = _transport_state(client)
        result = {
            "record_type": "PRAVO_PUBLICATION_152_RUNTIME_PROBE",
            "api_reachable": False,
            "target_number": TARGET_NUMBER,
            "target_date": TARGET_DATE,
            "external_asset_status": asset.status,
            "error": f"{type(exc).__name__}: {exc}",
            **transport_state,
            "metadata_only": True,
            "d2_d3_promoted": False,
            "legal_truth_promoted": False,
            "total_seconds": time.perf_counter() - started,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("API_REACHABLE=false")
        print(f"TRANSPORT={transport_state['transport'] or 'none'}")
        print(f"TRANSPORT_FAILURES={len(transport_state['transport_failures'])}")
        print("D2_D3_PROMOTED=false")
        print("LEGAL_TRUTH_PROMOTED=false")
        return 2

    search_seconds = time.perf_counter() - search_started
    exact = client.exact_identity_hits(hits, number=TARGET_NUMBER, document_date=TARGET_DATE)
    exact_with_title = [
        hit for hit in exact if TARGET_TITLE_MARKER in hit.title.casefold().replace("ё", "е")
    ]

    details = []
    detail_errors = []
    detail_seconds = 0.0
    for hit in exact_with_title[:3]:
        detail_started = time.perf_counter()
        try:
            detail = client.get_document(hit.eo_number, timeout_seconds=30.0)
            details.append({
                "eo_number": hit.eo_number,
                "detail": detail,
                "pdf_url": client.pdf_url(hit.eo_number),
                "zip_url": client.zip_url(hit.eo_number),
                "pdf_file_length": hit.pdf_file_length,
                "zip_file_length": hit.zip_file_length,
            })
        except Exception as exc:
            detail_errors.append({
                "eo_number": hit.eo_number,
                "error": f"{type(exc).__name__}: {exc}",
                **_transport_state(client),
            })
        detail_seconds += time.perf_counter() - detail_started

    exact_identity_found = bool(exact_with_title)
    file_candidate_found = any(
        (item.get("pdf_file_length") or 0) > 0 or (item.get("zip_file_length") or 0) > 0
        for item in details
    )

    if exact_identity_found and file_candidate_found:
        next_action = "READY_FOR_EXACT_FILE_ACQUISITION_PROBE"
    elif exact_identity_found:
        next_action = "EXACT_METADATA_FOUND_BUT_NO_FILE_LENGTH__DO_NOT_PROMOTE"
    else:
        next_action = "NO_EXACT_2006_PUBLICATION_EVENT_FOUND__KEEP_EXISTING_A0_CAPTURE_AND_USE_API_FOR_NEWER_EVENTS"

    result = {
        "record_type": "PRAVO_PUBLICATION_152_RUNTIME_PROBE",
        "api_reachable": True,
        "external_asset_status": asset.status,
        "target_number": TARGET_NUMBER,
        "target_date": TARGET_DATE,
        "search": search_meta,
        "hits": [
            {
                "eo_number": hit.eo_number,
                "number": hit.number,
                "title": hit.title,
                "document_date": hit.document_date,
                "publish_date": hit.publish_date,
                "pdf_file_length": hit.pdf_file_length,
                "zip_file_length": hit.zip_file_length,
            }
            for hit in hits
        ],
        "exact_identity_hits": len(exact_with_title),
        "details": details,
        "detail_errors": detail_errors,
        "metadata_only": True,
        "d2_d3_promoted": False,
        "legal_truth_promoted": False,
        "timing_seconds": {
            "search": search_seconds,
            "details": detail_seconds,
            "total": time.perf_counter() - started,
        },
        "next_action": next_action,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print("API_REACHABLE=true")
    print(f"TRANSPORT={search_meta.get('transport') or 'unknown'}")
    print(f"TRANSPORT_FAILURES={len(search_meta.get('transport_failures_before_success') or [])}")
    print(f"HITS_TOTAL={len(hits)}")
    print(f"EXACT_IDENTITY_HITS={len(exact_with_title)}")
    print(f"FILE_CANDIDATE_FOUND={str(file_candidate_found).lower()}")
    print(f"SEARCH_SECONDS={search_seconds:.6f}")
    print(f"TOTAL_SECONDS={result['timing_seconds']['total']:.6f}")
    print(f"NEXT_ACTION={next_action}")
    print("D2_D3_PROMOTED=false")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
