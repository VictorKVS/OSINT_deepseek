from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGETS_PATH = REPO_ROOT / "config" / "programmer_bibliography_targets.json"
ACQUISITION_PATH = REPO_ROOT / "config" / "programmer_bibliography_acquisition_registry.json"
PROBE_PATH = REPO_ROOT / "reports" / "team_role_telegram" / "LATEST_PROGRAMMER_BIBLIOGRAPHY_PROBE.json"
REPORT_PATH = REPO_ROOT / "reports" / "team_role_telegram" / "LATEST_PROGRAMMER_BIBLIOGRAPHY_ACQUISITION_PLAN.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    targets = load_json(TARGETS_PATH)
    acquisition = load_json(ACQUISITION_PATH)
    probe = load_json(PROBE_PATH)

    target_by_id = {row["id"]: row for row in targets["targets"]}
    route_by_id = {row["id"]: row for row in acquisition["targets"]}
    probe_by_id = {row["id"]: row for row in probe["targets"]}

    rows = []
    for target_id, target in target_by_id.items():
        route = route_by_id[target_id]
        observed = probe_by_id.get(target_id, {})
        telegram_status = observed.get("status", "NOT_PROBED")
        best_score = observed.get("best_score")
        candidate = (observed.get("candidates") or [None])[0]

        if route["route"] in {"OFFICIAL_OPEN_WEB", "OFFICIAL_OPEN_PDF", "OFFICIAL_REPOSITORY_DOWNLOAD"}:
            next_action = "ACQUIRE_FROM_OFFICIAL_SOURCE"
        elif telegram_status == "FOUND_CANDIDATE":
            next_action = "VERIFY_RIGHTS_AND_EXACT_EDITION_BEFORE_INGEST"
        else:
            next_action = "OFFICIAL_PURCHASE_OR_USER_OWNED_COPY_REQUIRED"

        rows.append({
            "id": target_id,
            "kind": target.get("kind"),
            "priority": target.get("priority"),
            "author": target.get("author"),
            "title": target.get("title"),
            "telegram_status": telegram_status,
            "telegram_best_score": best_score,
            "telegram_best_candidate": candidate,
            "route": route["route"],
            "rights_class": route["rights_class"],
            "official_url": route["official_url"],
            "next_action": next_action,
            "exact_edition_verified": False,
            "ingest_ready": next_action == "ACQUIRE_FROM_OFFICIAL_SOURCE",
        })

    summary = {
        "record_type": "PROGRAMMER_BIBLIOGRAPHY_ACQUISITION_PLAN",
        "schema_version": "1.0",
        "targets_total": len(rows),
        "telegram_found_total": sum(r["telegram_status"] == "FOUND_CANDIDATE" for r in rows),
        "official_source_actionable_total": sum(r["next_action"] == "ACQUIRE_FROM_OFFICIAL_SOURCE" for r in rows),
        "telegram_candidates_requiring_rights_and_edition_verification_total": sum(
            r["next_action"] == "VERIFY_RIGHTS_AND_EXACT_EDITION_BEFORE_INGEST" for r in rows
        ),
        "commercial_or_owned_copy_required_total": sum(
            r["next_action"] == "OFFICIAL_PURCHASE_OR_USER_OWNED_COPY_REQUIRED" for r in rows
        ),
        "kb_auto_promotion": False,
        "targets": rows,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    compact = {key: value for key, value in summary.items() if key != "targets"}
    compact["report"] = str(REPORT_PATH.relative_to(REPO_ROOT)).replace("\\", "/")
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
