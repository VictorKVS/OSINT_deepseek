from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import run_security_official_master_download_multiroute as multiroute  # noqa: E402

master = multiroute.master
RECOVERY_PATH = ROOT / "config" / "security_official_route_recovery.json"
REPORT_PATH = ROOT / "reports" / "security_current_only" / "LATEST_FSTEC_OFFICIAL_RECOVERY_RUN.json"


def load_recovery() -> dict[str, Any]:
    return json.loads(RECOVERY_PATH.read_text(encoding="utf-8"))


def merge_plan_recovery(plan: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    documents, source_rows = multiroute.merge_plan_multiroute(plan)
    recovery = load_recovery()
    route_records = recovery.get("routes") or {}
    selected: list[dict[str, Any]] = []

    for doc in documents:
        did = str(doc.get("document_id") or "")
        rows = route_records.get(did)
        if not isinstance(rows, list) or not rows:
            continue

        recovery_urls = [
            str(row.get("url") or "").strip()
            for row in rows
            if isinstance(row, dict) and str(row.get("url") or "").strip()
        ]
        existing = [str(value).strip() for value in (doc.get("official_routes") or []) if str(value).strip()]

        # This is a targeted recovery test: direct artifact routes are attempted
        # first so already-known dead hosts do not consume the full timeout budget.
        routes: list[str] = []
        for url in recovery_urls + existing:
            if url and url not in routes:
                routes.append(url)

        clone = dict(doc)
        clone["official_routes"] = routes
        clone["official_source_url"] = routes[0] if routes else None
        clone["recovery_route_records"] = rows
        clone["route_selection_policy"] = "TARGETED_RECOVERY_DIRECT_ARTIFACT_FIRST"
        selected.append(clone)

    return selected, source_rows


def _patch_recovery_result(result: dict[str, Any]) -> dict[str, Any]:
    did = str(result.get("document_id") or "")
    recovery = load_recovery()
    rows = (recovery.get("routes") or {}).get(did) or []
    expected = rows[0] if rows and isinstance(rows[0], dict) else {}

    result["recovery_registry"] = RECOVERY_PATH.relative_to(ROOT).as_posix()
    result["recovery_expected_document_number"] = expected.get("expected_document_number")
    result["recovery_expected_document_date"] = expected.get("expected_document_date")
    result["recovery_expected_registration_number"] = expected.get("expected_registration_number")
    result["document_identity_confirmed"] = False
    result["identity_status"] = "PROVISIONAL_ROUTE_METADATA_MATCH_NEEDS_CONTENT_REVIEW"
    result["kb_auto_promotion"] = False

    if result.get("status") in {"DOWNLOADED", "REUSED_EXACT"}:
        raw_ref = str(result.get("raw_path") or "")
        if raw_ref:
            raw_path = ROOT / raw_ref
            if raw_path.is_file():
                result["artifact_pdf_magic_check"] = raw_path.read_bytes()[:5] == b"%PDF-"
        final_url = str(result.get("source_url") or "")
        reg = str(expected.get("expected_registration_number") or "")
        result["route_registration_hint_match"] = bool(reg and reg in final_url)

        # Keep the persisted metadata conservative as well.
        meta_path = master.base.META_DIR / f"{master.base._safe_name(did)}.json"
        if meta_path.is_file():
            try:
                meta = master.load_json(meta_path)
                meta["document_identity_confirmed"] = False
                meta["identity_status"] = result["identity_status"]
                meta["recovery_expected_document_number"] = expected.get("expected_document_number")
                meta["recovery_expected_document_date"] = expected.get("expected_document_date")
                meta["recovery_expected_registration_number"] = expected.get("expected_registration_number")
                meta["artifact_pdf_magic_check"] = result.get("artifact_pdf_magic_check")
                meta["route_registration_hint_match"] = result.get("route_registration_hint_match")
                meta["legal_truth_eligible"] = False
                meta["kb_auto_promotion"] = False
                meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            except Exception:
                pass
    return result


def acquire_recovery(doc: dict[str, Any], progress: Any) -> dict[str, Any]:
    return _patch_recovery_result(multiroute.acquire_multiroute(doc, progress))


def main() -> int:
    master.merge_plan = merge_plan_recovery
    master.acquire = acquire_recovery
    master.REPORT_PATH = REPORT_PATH
    return master.main()


if __name__ == "__main__":
    raise SystemExit(main())
