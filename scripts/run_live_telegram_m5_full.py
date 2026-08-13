from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.acquisition_report import DeterministicAcquisitionReportBuilder
from father_osint.collectors.telegram import TelegramCollector
from father_osint.counter_evidence import (
    DeterministicCounterEvidenceAssessor,
    DeterministicCounterEvidencePlanner,
)
from father_osint.evidence_quality import DeterministicEvidenceQualityAssessor
from father_osint.models import MaterialPackage, ResearchTask
from father_osint.protocol import EvidencePackage, PlanDecision, ResearchRequest, ResearchWorkflow
from father_osint.reconnaissance import DeterministicTelegramReconnaissance
from father_osint.reasoning import DeterministicEvidenceAnalyst, DeterministicSocrates
from father_osint.reliability import DurableObservationWriter, JsonCheckpointStore
from father_osint.search_planning import DeterministicTelegramSearchPlanner
from father_osint.storage import MaterialStore
from father_osint.sufficiency import DeterministicResearchSufficiencyAssessor
from father_osint.transports.telethon import TelethonTransport

DEFAULT_CONFIG = REPO_ROOT / "legacy/telegram/config.yaml"
DEFAULT_SESSION = REPO_ROOT / "legacy/telegram/reader_session"
DEFAULT_OUTPUT = REPO_ROOT / "data/m5_live_telegram_full"


def load_local_config(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required for the live operator runner") from exc
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def count_jsonl_records(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def count_raw_payload_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.iterdir() if item.is_file())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Integrated M5 live Telegram G6-G10 proof")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--session", type=Path, default=DEFAULT_SESSION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-items", type=int, default=25)
    parser.add_argument("--recon-sample", type=int, default=10)
    parser.add_argument("--expect-reuse-min", type=int, default=0)
    parser.add_argument("--sufficiency", choices=["MINIMUM", "GOOD", "DESIRABLE"], default="GOOD")
    parser.add_argument("--term", action="append", default=[], help="Explicit research term for G7 relevance assessment")
    parser.add_argument("--hypothesis", action="append", default=[], help="Leading hypothesis; without an executed challenge search G9 remains INCOMPLETE")
    parser.add_argument("--checkpoint", type=Path, default=None)
    parser.add_argument("--resume", action="store_true")
    return parser


def _source_attempts(channels: list[str], errors: list[str]) -> list[dict]:
    attempts = [{"source": str(channel), "source_class": "telegram", "status": "ATTEMPTED"} for channel in channels]
    for error in errors:
        source = str(error).split(":", 1)[0].strip() or "telegram:unknown"
        attempts.append({"source": source, "source_class": "telegram", "status": "FAILED", "reason": str(error)})
    return attempts


def _explicit_primary_count(materials) -> int:
    return sum(
        1 for material in materials
        if str(material.metadata.get("source_class") or "").lower() in {"primary", "first_party", "first-party"}
    )


def main() -> int:
    args = build_parser().parse_args()
    if args.max_items <= 0 or args.recon_sample <= 0:
        raise SystemExit("--max-items and --recon-sample must be > 0")
    if args.expect_reuse_min < 0:
        raise SystemExit("--expect-reuse-min must be >= 0")

    config = load_local_config(args.config)
    telegram = config["telegram"]
    channels = list(telegram.get("channels", []))
    per_channel_limit = int(telegram.get("collection", {}).get("limit_per_channel", 100))

    request = ResearchRequest(
        objective="Run the integrated M5 Telegram evidence-acquisition proof",
        research_questions=[
            "What source landscape is observable in the configured Telegram scope?",
            "What evidence quality, gaps and sufficiency can be justified from the bounded collection?",
            "What must Analyst know about failures, limitations and follow-up before using the material?",
        ],
        required_sufficiency=args.sufficiency,
        hypotheses=list(args.hypothesis),
        acceptance_criteria=[
            "G6 reconnaissance/refinement is explicit",
            "G7 quality dimensions remain separate",
            "G8 sufficiency is coverage-based rather than item-count based",
            "G9 counter-evidence state is explicit",
            "G10 AcquisitionReport preserves failures, gaps and lineage",
        ],
        constraints=[f"max_items={args.max_items}", f"recon_sample={args.recon_sample}", "source_class=telegram"],
    )
    workflow = ResearchWorkflow(request.case_id)
    workflow.transition("ISSUED", actor_role="ANALYST", reason="ResearchRequest issued")
    workflow.transition("PLANNING", actor_role="OSINT_EXPERT", reason="OSINT planning started")

    planned = DeterministicTelegramSearchPlanner().plan(request)
    workflow.transition("PLAN_REVIEW", actor_role="OSINT_EXPERT", reason="SearchPlanProposal ready")
    plan_decision = PlanDecision(
        case_id=request.case_id,
        search_plan_id=planned.plan.search_plan_id,
        status="ACCEPT",
        reason_codes=["M5_INTEGRATED_G6_G10_LIVE_PROOF"],
        decided_by="ANALYST",
    )
    workflow.apply_plan_decision(plan_decision)
    workflow.transition("COLLECTING", actor_role="OSINT_EXPERT", reason="Approved SearchPlan execution")

    task = ResearchTask(
        question=request.objective,
        topics=request.research_questions,
        source_types=planned.plan.source_classes,
        max_items=args.max_items,
        requested_by="OSINT_EXPERT",
    )
    transport = TelethonTransport(
        api_id=int(telegram["api_id"]),
        api_hash=str(telegram["api_hash"]),
        session_path=args.session,
        channels=channels,
        per_channel_limit=per_channel_limit,
    )
    collector = TelegramCollector(transport)
    store = MaterialStore(args.output)

    checkpoint_path = args.checkpoint or (args.output / "checkpoints.json")
    checkpoint_store = JsonCheckpointStore(checkpoint_path) if args.resume else None
    durable_writer = DurableObservationWriter(store, checkpoint_store) if checkpoint_store else None

    material_records_before = count_jsonl_records(store.materials_file)
    raw_payload_files_before = count_raw_payload_files(store.raw_dir)
    store.save_task(task)

    materials = []
    payloads_reused = 0
    resumed_sources = 0
    checkpoint_commits = 0
    seen_source_keys: set[str] = set()

    for material in collector.collect(task):
        source_key = str(material.metadata.get("chat_id") or material.source_locator)
        cursor = str(material.metadata.get("message_id") or material.content_hash)
        if checkpoint_store and source_key not in seen_source_keys:
            if checkpoint_store.load(material.source_type, source_key) is not None:
                resumed_sources += 1
            seen_source_keys.add(source_key)
        if durable_writer:
            payloads_reused += int(durable_writer.save_then_checkpoint(material=material, source_key=source_key, cursor=cursor))
            checkpoint_commits += 1
        else:
            payloads_reused += int(store.save_material(material))
        materials.append(material)

    package = MaterialPackage(
        task_id=task.task_id,
        materials=materials,
        payloads_reused=payloads_reused,
        collection_errors=list(getattr(transport, "last_errors", []) or []),
        stop_reason="completed",
        notes="Integrated M5 G6-G10 live proof",
    )
    store.save_package(package)

    recon = DeterministicTelegramReconnaissance().run(
        planned.plan,
        package,
        sample_limit=min(args.recon_sample, max(1, args.max_items)),
    )
    explicit_terms = [str(item).strip() for item in args.term if str(item).strip()]
    quality = DeterministicEvidenceQualityAssessor().assess_package(
        package,
        relevant_terms=explicit_terms,
        case_id=request.case_id,
    )

    counter_plan = DeterministicCounterEvidencePlanner().plan(request)
    counter = DeterministicCounterEvidenceAssessor().assess(counter_plan.directive)

    distinct_source_ids = len({
        str(material.metadata.get("chat_id") or material.source_locator)
        for material in materials
    })
    independent_evidence_refs = sum(
        1 for item in quality.assessments
        if item.independence.state == "HIGH"
    )
    evidence_package = EvidencePackage(
        case_id=request.case_id,
        request_id=request.request_id,
        search_plan_id=planned.plan.search_plan_id,
        requested_sufficiency=request.required_sufficiency,
        achieved_sufficiency="MINIMUM" if materials else "INSUFFICIENT",
        material_refs=[material.material_id for material in materials],
        evidence_refs=[material.material_id for material in materials],
        source_attempts=_source_attempts(channels, list(package.collection_errors)),
        provenance_refs=[material.source_locator for material in materials],
        contradictions=list(counter.assessment.contradictory_evidence_refs),
        coverage={
            "configured_sources": len(channels),
            "successful_source_classes": 1 if materials else 0,
            "distinct_source_ids": distinct_source_ids,
            "independent_evidence_refs": independent_evidence_refs,
            "primary_evidence_refs": _explicit_primary_count(materials),
            "counter_evidence_searched": counter.assessment.counter_evidence_searched,
            "counter_evidence_status": counter.assessment.status,
            "temporal_coverage_complete": False,
            "target_coverage_complete": False,
            "materials_collected": len(materials),
            "collection_errors": len(package.collection_errors),
        },
        limitations=list(dict.fromkeys(list(planned.plan.limitations) + list(recon.report.gaps) + list(counter.assessment.limitations))),
        critical_gaps=(
            ["Non-Telegram corroboration is not covered by this Telegram-only live proof"]
            if request.required_sufficiency in {"GOOD", "DESIRABLE"}
            else []
        ),
        decision_record_refs=[
            planned.decision_record.decision_id,
            recon.decision_record.decision_id,
            quality.decision_record.decision_id,
            counter_plan.decision_record.decision_id,
            counter.decision_record.decision_id,
        ],
    )

    sufficiency = DeterministicResearchSufficiencyAssessor().assess(evidence_package, quality=quality)
    evidence_package.achieved_sufficiency = sufficiency.assessment.achieved_sufficiency
    evidence_package.recommended_follow_up = list(sufficiency.assessment.recommended_next_search)
    evidence_package.decision_record_refs.append(sufficiency.decision_record.decision_id)

    acquisition = DeterministicAcquisitionReportBuilder().build(
        request,
        recon.refined_plan,
        evidence_package,
        reconnaissance=recon,
        quality=quality,
        sufficiency=sufficiency,
        counter_evidence=counter,
        collection_bounds={
            "max_items": args.max_items,
            "recon_sample": args.recon_sample,
            "per_channel_limit": per_channel_limit,
            "resume": args.resume,
        },
    )

    workflow.transition("EVIDENCE_DELIVERED", actor_role="OSINT_EXPERT", reason="EvidencePackage and AcquisitionReport delivered")
    workflow.transition("ANALYSIS", actor_role="ANALYST", reason="Analyst accepted audited OSINT handoff")
    analysis = DeterministicEvidenceAnalyst().analyze(package)
    critique = DeterministicSocrates().critique(package, analysis)

    material_records_after = count_jsonl_records(store.materials_file)
    raw_payload_files_after = count_raw_payload_files(store.raw_dir)
    observations_appended = material_records_after - material_records_before
    new_raw_payload_files = raw_payload_files_after - raw_payload_files_before
    observations_preserved = observations_appended == len(materials)
    reuse_expectation_met = payloads_reused >= args.expect_reuse_min
    restart_reconciliation_passed = (
        not args.resume
        or (
            checkpoint_commits == len(materials)
            and observations_preserved
            and all(
                checkpoint_store.load(
                    material.source_type,
                    str(material.metadata.get("chat_id") or material.source_locator),
                ) is not None
                for material in materials
            )
        )
    )
    reasoning_passed = critique.verdict == "PASS"

    if not materials:
        status, exit_code = "NO_MATERIAL", 2
    elif not reuse_expectation_met:
        status, exit_code = "REUSE_EXPECTATION_FAILED", 3
    elif not observations_preserved:
        status, exit_code = "OBSERVATION_APPEND_FAILED", 4
    elif not restart_reconciliation_passed:
        status, exit_code = "RESTART_RECONCILIATION_FAILED", 5
    elif not reasoning_passed:
        status, exit_code = "REASONING_REVIEW_FAILED", 6
    else:
        workflow.transition("CLOSED", actor_role="ANALYST", reason="Integrated M5 G6-G10 live proof completed")
        status, exit_code = "PASS", 0

    summary = {
        "status": status,
        "case_id": request.case_id,
        "research_request_id": request.request_id,
        "search_plan_id": planned.plan.search_plan_id,
        "refined_search_plan_version": recon.refined_plan.version,
        "workflow_state": workflow.state,
        "materials": len(materials),
        "payloads_reused": payloads_reused,
        "observations_preserved": observations_preserved,
        "new_raw_payload_files": new_raw_payload_files,
        "resumed_sources": resumed_sources,
        "restart_reconciliation_passed": restart_reconciliation_passed,
        "g6_recon_report_id": recon.report.report_id,
        "g6_marginal_value": recon.report.marginal_value,
        "g6_stop_recommended": recon.report.stop_recommended,
        "g6_gaps": recon.report.gaps,
        "g7_quality_assessments": len(quality.assessments),
        "g7_truth_probability": "NOT_CALCULATED",
        "g8_requested_sufficiency": request.required_sufficiency,
        "g8_achieved_sufficiency": sufficiency.assessment.achieved_sufficiency,
        "g8_reasons": sufficiency.assessment.reasons,
        "g8_recommended_next_search": sufficiency.assessment.recommended_next_search,
        "g9_counter_evidence_directive": counter_plan.directive.status,
        "g9_counter_evidence_status": counter.assessment.status,
        "g9_limitations": counter.assessment.limitations,
        "g10_acquisition_report_id": acquisition.report.report_id,
        "g10_source_attempts": len(acquisition.report.source_attempts),
        "g10_source_failures": acquisition.report.source_failures,
        "g10_unresolved_gaps": acquisition.report.unresolved_gaps,
        "g10_lineage_refs": len(acquisition.report.lineage_refs),
        "analysis_claims": len(analysis.claims),
        "socrates_verdict": critique.verdict,
        "output": str(args.output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
