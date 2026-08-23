from __future__ import annotations

import json
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.external_assets import authorize_external_asset
from father_osint.freshness_discovery import (
    PravoReferenceDiscovery,
    degraded_observation,
    load_watchlist,
)
from father_osint.proof_resolution import resolve_pack_from_files
from father_osint.source_health import load_source_health, write_source_health


REVIEW = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch" / "review" / "batch_review_manifest.json"
SOURCE_PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
LOCAL_DIR = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack"
WATCHLIST = REPO_ROOT / "config" / "pdn_freshness_watchlist.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_FRESHNESS_DISCOVERY.json"
HEALTH = REPO_ROOT / ".runtime" / "source_health" / "publication-pravo-official-api.json"
SNAPSHOTS = REPO_ROOT / ".runtime" / "freshness" / "pdn_reference_discovery_snapshots.jsonl"
SOURCE_KEY = "publication-pravo-official-api"
COOLDOWN_SECONDS = 30 * 60
FIRST_REQUEST_TIMEOUT_SECONDS = 12.0
FOLLOWUP_REQUEST_TIMEOUT_SECONDS = 8.0


def _write_result(result: dict[str, object]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SNAPSHOTS.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOTS.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    started = time.perf_counter()
    missing = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REVIEW, SOURCE_PACK, WATCHLIST)
        if not path.is_file()
    ]
    if missing:
        result = {
            "record_type": "P0_7_FRESHNESS_DISCOVERY",
            "operational_contract_pass": False,
            "missing_inputs": missing,
            "network_used": False,
            "legal_truth_promoted": False,
        }
        _write_result(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    local_proof = resolve_pack_from_files(
        repo_root=REPO_ROOT,
        review_path=REVIEW,
        source_pack_path=SOURCE_PACK,
        local_dir=LOCAL_DIR,
    )
    serving_proof_available = bool(local_proof.get("all_proofs_available"))
    if not serving_proof_available:
        result = {
            "record_type": "P0_7_FRESHNESS_DISCOVERY",
            "operational_contract_pass": False,
            "local_serving_proof": local_proof,
            "serving_continues_from_verified_local_proof": False,
            "remote_required_for_serving": False,
            "network_used": False,
            "freshness_current_claim_allowed": False,
            "new_d2_d3_promotion": False,
            "legal_truth_promoted": False,
            "error": "verified local A0 serving proof is unavailable",
            "total_seconds": time.perf_counter() - started,
        }
        _write_result(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    asset = authorize_external_asset(SOURCE_KEY, "proof_acquisition")
    watch_payload = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    targets = load_watchlist(watch_payload)
    lookback_days = int(watch_payload.get("default_lookback_days", 7))
    if lookback_days < 1 or lookback_days > 90:
        raise ValueError("default_lookback_days must be between 1 and 90")

    window_to = date.today()
    window_from = window_to - timedelta(days=lookback_days)
    observations = []
    network_used = False
    source_error: str | None = None
    circuit_open_at_start = False
    retry_after_seconds = 0.0

    health = load_source_health(HEALTH, source_key=SOURCE_KEY)
    if health and health.circuit_open():
        circuit_open_at_start = True
        retry_after_seconds = health.remaining_seconds()
        source_error = health.error or "source circuit is open"
        observations = [
            degraded_observation(
                target,
                status="DEGRADED_SOURCE_CIRCUIT_OPEN",
                error=source_error,
            ).to_dict()
            for target in targets
        ]
    else:
        discovery = PravoReferenceDiscovery()
        for index, target in enumerate(targets):
            timeout = FIRST_REQUEST_TIMEOUT_SECONDS if index == 0 else FOLLOWUP_REQUEST_TIMEOUT_SECONDS
            try:
                network_used = True
                observation = discovery.search_recent_reference(
                    target,
                    publish_date_from=window_from.isoformat(),
                    publish_date_to=window_to.isoformat(),
                    timeout_seconds=timeout,
                    page_size=30,
                )
                observations.append(observation.to_dict())
            except Exception as exc:
                source_error = f"{type(exc).__name__}: {exc}"
                state = write_source_health(
                    HEALTH,
                    source_key=SOURCE_KEY,
                    status="FAILED",
                    cooldown_seconds=COOLDOWN_SECONDS,
                    error=source_error,
                )
                retry_after_seconds = state.remaining_seconds()
                observations.append(
                    degraded_observation(
                        target,
                        status="DEGRADED_SOURCE_UNAVAILABLE",
                        error=source_error,
                    ).to_dict()
                )
                for remaining in targets[index + 1:]:
                    observations.append(
                        degraded_observation(
                            remaining,
                            status="SKIPPED_AFTER_SOURCE_FAILURE",
                            error="shared official discovery source failed earlier in this bounded run",
                        ).to_dict()
                    )
                break
        else:
            write_source_health(
                HEALTH,
                source_key=SOURCE_KEY,
                status="OK",
                cooldown_seconds=0,
                error=None,
            )

    complete_statuses = {
        "NO_CANDIDATE_IN_WINDOW",
        "CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION",
    }
    observation_complete = len(observations) == len(targets) and all(
        str(row.get("status")) in complete_statuses for row in observations
    )
    degraded = not observation_complete
    candidate_events_total = sum(len(row.get("candidate_events") or []) for row in observations)
    no_candidate_windows = sum(row.get("status") == "NO_CANDIDATE_IN_WINDOW" for row in observations)
    candidate_targets = sum(row.get("status") == "CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION" for row in observations)
    degraded_targets = len(observations) - no_candidate_windows - candidate_targets

    no_false_current_claim = all(row.get("current_claim_allowed") is False for row in observations)
    no_promotion = all(
        row.get("d2_d3_promoted") is False
        and row.get("legal_truth_promoted") is False
        and row.get("exact_bytes_acquired") is False
        for row in observations
    )
    operational_contract_pass = (
        serving_proof_available
        and len(observations) == len(targets)
        and no_false_current_claim
        and no_promotion
    )

    result = {
        "record_type": "P0_7_FRESHNESS_DISCOVERY",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "watchlist_id": watch_payload.get("watchlist_id"),
        "external_asset_status": asset.status,
        "source_key": SOURCE_KEY,
        "source_role": watch_payload.get("source_role"),
        "window": {
            "publish_date_from": window_from.isoformat(),
            "publish_date_to": window_to.isoformat(),
            "lookback_days": lookback_days,
        },
        "local_serving_proof": {
            "documents_total": local_proof.get("documents_total"),
            "proof_available": local_proof.get("proof_available"),
            "all_proofs_available": local_proof.get("all_proofs_available"),
            "evidence_kind": local_proof.get("evidence_kind"),
        },
        "serving_continues_from_verified_local_proof": serving_proof_available,
        "remote_required_for_serving": False,
        "freshness_observation_complete": observation_complete,
        "freshness_monitoring_degraded": degraded,
        "freshness_current_claim_allowed": False,
        "no_false_unchanged_claim": True,
        "candidate_events_total": candidate_events_total,
        "candidate_targets": candidate_targets,
        "no_candidate_windows": no_candidate_windows,
        "degraded_targets": degraded_targets,
        "circuit_open_at_start": circuit_open_at_start,
        "retry_after_seconds": retry_after_seconds,
        "source_error": source_error,
        "network_used": network_used,
        "metadata_only": True,
        "exact_bytes_acquired": False,
        "new_document_version_created": False,
        "new_d2_d3_promotion": False,
        "legal_truth_promoted": False,
        "observations": observations,
        "operational_contract_pass": operational_contract_pass,
        "total_seconds": time.perf_counter() - started,
    }
    _write_result(result)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"WATCH_TARGETS={len(targets)}")
    print(f"LOCAL_PROOFS_AVAILABLE={local_proof.get('proof_available')}")
    print(f"SERVING_CONTINUES={str(serving_proof_available).lower()}")
    print("REMOTE_REQUIRED_FOR_SERVING=false")
    print(f"FRESHNESS_OBSERVATION_COMPLETE={str(observation_complete).lower()}")
    print(f"FRESHNESS_MONITORING_DEGRADED={str(degraded).lower()}")
    print("FRESHNESS_CURRENT_CLAIM_ALLOWED=false")
    print("NO_FALSE_UNCHANGED_CLAIM=true")
    print(f"CANDIDATE_EVENTS_TOTAL={candidate_events_total}")
    print(f"DEGRADED_TARGETS={degraded_targets}")
    print(f"CIRCUIT_OPEN_AT_START={str(circuit_open_at_start).lower()}")
    print(f"NETWORK_USED={str(network_used).lower()}")
    print("EXACT_BYTES_ACQUIRED=false")
    print("NEW_DOCUMENT_VERSION_CREATED=false")
    print("NEW_D2_D3_PROMOTION=false")
    print(f"OPERATIONAL_CONTRACT_PASS={str(operational_contract_pass).lower()}")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0 if operational_contract_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
