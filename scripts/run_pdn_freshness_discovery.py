from __future__ import annotations

import json
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.external_assets import authorize_external_asset
from father_osint.freshness_checkpoint import (
    load_freshness_checkpoint,
    resolve_freshness_window,
    write_freshness_checkpoint,
)
from father_osint.freshness_discovery import (
    PravoReferenceDiscovery,
    degraded_observation,
    load_watchlist,
)
from father_osint.proof_resolution import resolve_pack_from_files
from father_osint.rg_freshness import RgDocumentIndexDiscovery
from father_osint.source_health import load_source_health, write_source_health


REVIEW = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch" / "review" / "batch_review_manifest.json"
SOURCE_PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
LOCAL_DIR = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack"
WATCHLIST = REPO_ROOT / "config" / "pdn_freshness_watchlist.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_FRESHNESS_DISCOVERY.json"
PRIMARY_HEALTH = REPO_ROOT / ".runtime" / "source_health" / "publication-pravo-official-api.json"
SECONDARY_HEALTH = REPO_ROOT / ".runtime" / "source_health" / "rg-official-doc-index.json"
SNAPSHOTS = REPO_ROOT / ".runtime" / "freshness" / "pdn_reference_discovery_snapshots.jsonl"
CHECKPOINT = REPO_ROOT / ".runtime" / "freshness" / "pdn_freshness_checkpoint.json"
PRIMARY_SOURCE_KEY = "publication-pravo-official-api"
SECONDARY_SOURCE_KEY = "rg-official-doc-index"
COOLDOWN_SECONDS = 30 * 60
FIRST_REQUEST_TIMEOUT_SECONDS = 12.0
FOLLOWUP_REQUEST_TIMEOUT_SECONDS = 8.0
SECONDARY_REQUEST_TIMEOUT_SECONDS = 8.0


def _write_result(result: dict[str, object]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SNAPSHOTS.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOTS.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def _primary_discovery(targets, window):
    observations: list[dict[str, object]] = []
    network_used = False
    source_error: str | None = None
    circuit_open_at_start = False
    retry_after_seconds = 0.0

    health = load_source_health(PRIMARY_HEALTH, source_key=PRIMARY_SOURCE_KEY)
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
                    publish_date_from=window.publish_date_from,
                    publish_date_to=window.publish_date_to,
                    timeout_seconds=timeout,
                    page_size=30,
                )
                observations.append(observation.to_dict())
            except Exception as exc:
                source_error = f"{type(exc).__name__}: {exc}"
                state = write_source_health(
                    PRIMARY_HEALTH,
                    source_key=PRIMARY_SOURCE_KEY,
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
                PRIMARY_HEALTH,
                source_key=PRIMARY_SOURCE_KEY,
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
    return {
        "source_key": PRIMARY_SOURCE_KEY,
        "role": "PRIMARY_COMPLETE_WINDOW_DISCOVERY",
        "observations": observations,
        "observation_complete": observation_complete,
        "network_used": network_used,
        "source_error": source_error,
        "circuit_open_at_start": circuit_open_at_start,
        "retry_after_seconds": retry_after_seconds,
        "checkpoint_coverage_complete": observation_complete,
    }


def _secondary_rg_discovery(targets):
    attempted = True
    network_used = False
    source_error: str | None = None
    circuit_open_at_start = False
    retry_after_seconds = 0.0
    scan: dict[str, object] | None = None

    health = load_source_health(SECONDARY_HEALTH, source_key=SECONDARY_SOURCE_KEY)
    if health and health.circuit_open():
        circuit_open_at_start = True
        retry_after_seconds = health.remaining_seconds()
        source_error = health.error or "secondary source circuit is open"
    else:
        try:
            network_used = True
            scan_result = RgDocumentIndexDiscovery().scan(
                targets=targets,
                timeout_seconds=SECONDARY_REQUEST_TIMEOUT_SECONDS,
            )
            scan = scan_result.to_dict()
            write_source_health(
                SECONDARY_HEALTH,
                source_key=SECONDARY_SOURCE_KEY,
                status="OK",
                cooldown_seconds=0,
                error=None,
            )
        except Exception as exc:
            source_error = f"{type(exc).__name__}: {exc}"
            state = write_source_health(
                SECONDARY_HEALTH,
                source_key=SECONDARY_SOURCE_KEY,
                status="FAILED",
                cooldown_seconds=COOLDOWN_SECONDS,
                error=source_error,
            )
            retry_after_seconds = state.remaining_seconds()

    return {
        "source_key": SECONDARY_SOURCE_KEY,
        "role": "SECONDARY_CANDIDATE_ONLY_DISCOVERY",
        "attempted": attempted,
        "scan_complete": scan is not None,
        "scan": scan,
        "network_used": network_used,
        "source_error": source_error,
        "circuit_open_at_start": circuit_open_at_start,
        "retry_after_seconds": retry_after_seconds,
        "checkpoint_coverage_complete": False,
    }


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

    primary_asset = authorize_external_asset(PRIMARY_SOURCE_KEY, "proof_acquisition")
    secondary_asset = authorize_external_asset(SECONDARY_SOURCE_KEY, "proof_acquisition")
    watch_payload = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    targets = load_watchlist(watch_payload)
    watchlist_id = str(watch_payload.get("watchlist_id") or "").strip()
    if not watchlist_id:
        raise ValueError("watchlist_id is required")

    bootstrap_lookback_days = int(watch_payload.get("bootstrap_lookback_days", 90))
    checkpoint_overlap_days = int(watch_payload.get("checkpoint_overlap_days", 3))
    checkpoint_before = load_freshness_checkpoint(
        CHECKPOINT,
        watchlist_id=watchlist_id,
        source_key=PRIMARY_SOURCE_KEY,
    )
    window = resolve_freshness_window(
        today=date.today(),
        bootstrap_lookback_days=bootstrap_lookback_days,
        checkpoint_overlap_days=checkpoint_overlap_days,
        checkpoint=checkpoint_before,
    )

    primary = _primary_discovery(targets, window)
    primary_observations = list(primary["observations"])
    primary_complete = bool(primary["observation_complete"])

    # The RG route is intentionally independent and candidate-only. We run it
    # whenever the primary complete-window route is degraded. It can surface an
    # amendment candidate, but it cannot certify a 90-day backfill window and
    # therefore cannot advance the primary freshness checkpoint by itself.
    secondary = _secondary_rg_discovery(targets) if not primary_complete else {
        "source_key": SECONDARY_SOURCE_KEY,
        "role": "SECONDARY_CANDIDATE_ONLY_DISCOVERY",
        "attempted": False,
        "scan_complete": False,
        "scan": None,
        "network_used": False,
        "source_error": None,
        "circuit_open_at_start": False,
        "retry_after_seconds": 0.0,
        "checkpoint_coverage_complete": False,
    }

    no_candidate_windows = sum(row.get("status") == "NO_CANDIDATE_IN_WINDOW" for row in primary_observations)
    primary_candidate_targets = sum(row.get("status") == "CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION" for row in primary_observations)
    degraded_targets = len(primary_observations) - no_candidate_windows - primary_candidate_targets
    primary_candidate_events = [
        event
        for row in primary_observations
        for event in (row.get("candidate_events") or [])
    ]
    secondary_scan = secondary.get("scan") if isinstance(secondary, dict) else None
    secondary_candidates = list(secondary_scan.get("candidates") or []) if isinstance(secondary_scan, dict) else []

    all_candidate_events = [
        {"provider": PRIMARY_SOURCE_KEY, **event}
        for event in primary_candidate_events
        if isinstance(event, dict)
    ] + [
        {"provider": SECONDARY_SOURCE_KEY, **event}
        for event in secondary_candidates
        if isinstance(event, dict)
    ]
    candidate_target_ids = {
        str(event.get("document_id") or "")
        for event in all_candidate_events
        if str(event.get("document_id") or "")
    }

    no_false_current_claim = all(row.get("current_claim_allowed") is False for row in primary_observations)
    no_primary_promotion = all(
        row.get("d2_d3_promoted") is False
        and row.get("legal_truth_promoted") is False
        and row.get("exact_bytes_acquired") is False
        for row in primary_observations
    )
    no_secondary_promotion = all(
        event.get("d2_d3_promoted") is False
        and event.get("legal_truth_promoted") is False
        and event.get("exact_bytes_acquired") is False
        and event.get("current_claim_allowed") is False
        for event in secondary_candidates
        if isinstance(event, dict)
    )

    observed_at = datetime.now(timezone.utc).isoformat()
    checkpoint_advanced = False
    checkpoint_after = checkpoint_before
    if primary_complete:
        checkpoint_after = write_freshness_checkpoint(
            CHECKPOINT,
            watchlist_id=watchlist_id,
            source_key=PRIMARY_SOURCE_KEY,
            publish_date_to=window.publish_date_to,
            observed_at=observed_at,
        )
        checkpoint_advanced = True

    degraded = not primary_complete
    checkpoint_safety_pass = primary_complete or not checkpoint_advanced
    operational_contract_pass = (
        serving_proof_available
        and len(primary_observations) == len(targets)
        and no_false_current_claim
        and no_primary_promotion
        and no_secondary_promotion
        and checkpoint_safety_pass
    )

    network_used = bool(primary["network_used"]) or bool(secondary.get("network_used"))
    result = {
        "record_type": "P0_7_FRESHNESS_DISCOVERY",
        "observed_at": observed_at,
        "watchlist_id": watchlist_id,
        "external_asset_status": {
            PRIMARY_SOURCE_KEY: primary_asset.status,
            SECONDARY_SOURCE_KEY: secondary_asset.status,
        },
        "source_key": PRIMARY_SOURCE_KEY,
        "secondary_source_key": SECONDARY_SOURCE_KEY,
        "source_role": watch_payload.get("source_role"),
        "window": window.to_dict(),
        "checkpoint": {
            "path": CHECKPOINT.relative_to(REPO_ROOT).as_posix(),
            "present_before": checkpoint_before is not None,
            "state_before": checkpoint_before.to_dict() if checkpoint_before else None,
            "advanced": checkpoint_advanced,
            "state_after": checkpoint_after.to_dict() if checkpoint_after else None,
            "degraded_run_did_not_advance": degraded and not checkpoint_advanced,
            "secondary_route_can_advance": False,
        },
        "local_serving_proof": {
            "documents_total": local_proof.get("documents_total"),
            "proof_available": local_proof.get("proof_available"),
            "all_proofs_available": local_proof.get("all_proofs_available"),
            "evidence_kind": local_proof.get("evidence_kind"),
        },
        "serving_continues_from_verified_local_proof": serving_proof_available,
        "remote_required_for_serving": False,
        "freshness_observation_complete": primary_complete,
        "freshness_monitoring_degraded": degraded,
        "freshness_current_claim_allowed": False,
        "no_false_unchanged_claim": True,
        "candidate_events_total": len(all_candidate_events),
        "candidate_targets": len(candidate_target_ids),
        "no_candidate_windows": no_candidate_windows,
        "degraded_targets": degraded_targets,
        "primary": primary,
        "secondary": secondary,
        "candidate_events": all_candidate_events,
        "circuit_open_at_start": bool(primary["circuit_open_at_start"]),
        "retry_after_seconds": primary["retry_after_seconds"],
        "source_error": primary["source_error"],
        "network_used": network_used,
        "metadata_only": True,
        "exact_bytes_acquired": False,
        "new_document_version_created": False,
        "new_d2_d3_promotion": False,
        "legal_truth_promoted": False,
        "observations": primary_observations,
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
    print(f"WINDOW_MODE={window.mode}")
    print(f"WINDOW_PUBLISH_DATE_FROM={window.publish_date_from}")
    print(f"WINDOW_PUBLISH_DATE_TO={window.publish_date_to}")
    print(f"CHECKPOINT_PRESENT_BEFORE={str(checkpoint_before is not None).lower()}")
    print(f"CHECKPOINT_ADVANCED={str(checkpoint_advanced).lower()}")
    print(f"DEGRADED_RUN_DID_NOT_ADVANCE_CHECKPOINT={str(degraded and not checkpoint_advanced).lower()}")
    print(f"FRESHNESS_OBSERVATION_COMPLETE={str(primary_complete).lower()}")
    print(f"FRESHNESS_MONITORING_DEGRADED={str(degraded).lower()}")
    print("FRESHNESS_CURRENT_CLAIM_ALLOWED=false")
    print("NO_FALSE_UNCHANGED_CLAIM=true")
    print(f"CANDIDATE_EVENTS_TOTAL={len(all_candidate_events)}")
    print(f"CANDIDATE_TARGETS={len(candidate_target_ids)}")
    print(f"DEGRADED_TARGETS={degraded_targets}")
    print(f"PRIMARY_CIRCUIT_OPEN_AT_START={str(bool(primary['circuit_open_at_start'])).lower()}")
    print(f"PRIMARY_NETWORK_USED={str(bool(primary['network_used'])).lower()}")
    print(f"SECONDARY_RG_ATTEMPTED={str(bool(secondary.get('attempted'))).lower()}")
    print(f"SECONDARY_RG_CIRCUIT_OPEN_AT_START={str(bool(secondary.get('circuit_open_at_start'))).lower()}")
    print(f"SECONDARY_RG_SCAN_COMPLETE={str(bool(secondary.get('scan_complete'))).lower()}")
    print(f"SECONDARY_RG_NETWORK_USED={str(bool(secondary.get('network_used'))).lower()}")
    print(f"SECONDARY_RG_CANDIDATES={len(secondary_candidates)}")
    print("SECONDARY_RG_CHECKPOINT_COVERAGE_COMPLETE=false")
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
