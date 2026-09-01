from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .analysis_zoo import AnalysisZoo, AnalysisZooResult
from .coverage import EvidenceCoverageAssessor
from .extractor import DeterministicIdentifierExtractor, ExtractionResult
from .graph import GraphProjector
from .jobs import PassiveAcquisitionOrchestrator
from .monitoring import CaseMonitor
from .planner import CoreQueryPlanner
from .reporting import OfficialReportComposer, ReportBuildResult
from .store import WorkbenchStore


@dataclass(slots=True)
class BootstrapResult:
    case: dict[str, Any]
    seed_source: dict[str, Any]
    seed_capture: dict[str, Any]
    seed_entity: dict[str, Any]
    plan: dict[str, Any]


@dataclass(slots=True)
class IngestResult:
    source: dict[str, Any]
    capture: dict[str, Any]
    extraction: ExtractionResult
    job: dict[str, Any] | None


@dataclass(slots=True)
class OutputBundle:
    coverage: list[dict[str, Any]]
    graph: dict[str, Any]
    analysis: AnalysisZooResult | None
    report: ReportBuildResult
    monitor_snapshot: dict[str, Any]
    summary: dict[str, Any]


class PassiveOSINTWorkbench:
    """Facade for the core passive OSINT workflow.

    The facade coordinates existing contract objects but intentionally exposes no
    method that converts an automated output into FACT. Reviewed findings must be
    created explicitly through ``WorkbenchStore.create_finding`` with an approving
    human role.
    """

    version = "passive-osint-workbench/0.1.0"

    def __init__(self, root: str | Path = "data/osint-workbench") -> None:
        self.store = WorkbenchStore(root)
        self.planner = CoreQueryPlanner(self.store)
        self.extractor = DeterministicIdentifierExtractor(self.store)
        self.jobs = PassiveAcquisitionOrchestrator(self.store)
        self.coverage = EvidenceCoverageAssessor(self.store)
        self.graph = GraphProjector(self.store)
        self.reporting = OfficialReportComposer(self.store)
        self.monitor = CaseMonitor(self.store)
        self.analysis_zoo = AnalysisZoo(self.store)

    def bootstrap_case(
        self,
        *,
        title: str,
        seed_type: str,
        seed_value: str,
        purpose: str,
        legal_basis_or_usage_note: str,
        owner_role: str = "Главный аналитик",
        case_type: str = "CORPORATE_DUE_DILIGENCE",
        access_class: str = "PUBLIC",
        jurisdictions: tuple[str, ...] = ("UNSPECIFIED",),
        aliases: tuple[str, ...] = (),
        objective: str | None = None,
        approve_plan: bool = False,
        reviewer_id: str | None = None,
        synthetic: bool = False,
        case_id: str | None = None,
    ) -> BootstrapResult:
        case = self.store.create_case(
            title=title,
            case_type=case_type,
            purpose=purpose,
            owner_role=owner_role,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
            access_class=access_class,
            jurisdictions=jurisdictions,
            active_actions_allowed=False,
            synthetic=synthetic,
            case_id=case_id,
        )
        seed_source = self.store.register_source(
            case["case_id"],
            url=f"urn:father-osint:analyst-seed:{case['case_id'].lower()}",
            title="Исходные данные постановщика задачи",
            publisher="Постановщик задачи",
            source_type="OTHER",
            primary_level="PRIMARY",
            jurisdiction=jurisdictions[0] if jurisdictions else "UNSPECIFIED",
            language="ru",
            affiliation="Internal case initiation record.",
            bias_or_interest="Seed supplied by requester; identity and assertions require independent verification.",
            reliability_grade="D_LEAD",
            what_it_supports=["The analyst received the stated seed for research."],
            what_it_does_not_support=["The truth, identity, ownership or risk status of the seed."],
            access_class=access_class,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
            republication_status="METADATA_ONLY",
        )
        seed_text = (
            f"CASE SEED\nType: {seed_type.upper()}\nValue: {seed_value}\n"
            f"Aliases: {', '.join(aliases) if aliases else 'none supplied'}\n"
            "Status: unverified analyst input; requires independent source resolution.\n"
        )
        seed_capture = self.store.capture_text(
            case["case_id"],
            source_id=seed_source["source_id"],
            text=seed_text,
            filename_hint="analyst-seed.txt",
            collector_id="passive-osint-workbench",
            collector_version=self.version,
            access_class=access_class,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
        )
        seed_entity = self.store.create_entity(
            case["case_id"],
            entity_type=seed_type,
            display_name=seed_value,
            aliases=aliases,
            identifiers=[
                {
                    "type": "ANALYST_SEED",
                    "value": seed_value,
                    "masked": False,
                    "source_ids": [seed_source["source_id"]],
                }
            ],
            attributes={
                "seed_capture_id": seed_capture["capture_id"],
                "identity_status": "UNRESOLVED",
            },
            source_ids=[seed_source["source_id"]],
            access_class=access_class,
            status="CANDIDATE",
            synthetic=synthetic,
        )
        self.store.append_journal(
            case["case_id"],
            actor_id="passive-osint-workbench",
            actor_type="SYSTEM",
            action_type="NORMALIZE",
            stream="ENTITY_REGISTRY",
            query_or_action=f"Create case and normalize {seed_type.upper()} seed",
            source_or_transform_ids=[seed_source["source_id"]],
            result_code="FOUND",
            result_summary=(
                f"Created case {case['case_id']}, preserved seed as {seed_capture['capture_id']} and created "
                f"unresolved entity {seed_entity['entity_id']}."
            ),
            new_entities=[seed_entity["entity_id"]],
            next_pivots=["Resolve seed against independent primary sources"],
            access_class=access_class,
            actor_version=self.version,
        )
        plan = self.planner.plan(
            case["case_id"],
            seed_entity_id=seed_entity["entity_id"],
            objective=objective or purpose,
            mode="IDENTIFY",
            approve=approve_plan,
            reviewer_id=reviewer_id,
        )
        return BootstrapResult(case, seed_source, seed_capture, seed_entity, plan)

    def ingest_text(
        self,
        case_id: str,
        *,
        text: str,
        url: str,
        title: str,
        publisher: str,
        source_type: str = "WEB_PAGE",
        primary_level: str = "UNKNOWN",
        jurisdiction: str = "UNSPECIFIED",
        language: str = "und",
        reliability_grade: str = "D_LEAD",
        access_class: str = "PUBLIC",
        legal_basis_or_usage_note: str = "Lawfully accessible material supplied for the documented case purpose.",
        republication_status: str = "METADATA_ONLY",
        query_plan_id: str | None = None,
        pivot_id: str | None = None,
    ) -> IngestResult:
        source = self.store.register_source(
            case_id,
            url=url,
            title=title,
            publisher=publisher,
            source_type=source_type,
            primary_level=primary_level,
            jurisdiction=jurisdiction,
            language=language,
            affiliation="Declared publisher; analyst review required.",
            bias_or_interest="Not automatically assessed.",
            reliability_grade=reliability_grade,
            what_it_supports=["The preserved source contains the captured text."],
            what_it_does_not_support=["Any assertion beyond the captured text and reviewed evidence."],
            access_class=access_class,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
            republication_status=republication_status,
        )
        capture = self.store.capture_text(
            case_id,
            source_id=source["source_id"],
            text=text,
            filename_hint="source.txt",
            collector_id="passive-osint-workbench",
            collector_version=self.version,
            access_class=access_class,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
        )
        extraction = self.extractor.extract_capture(
            case_id,
            source_id=source["source_id"],
            capture_id=capture["capture_id"],
            query_plan_id=query_plan_id,
        )
        job: dict[str, Any] | None = None
        if query_plan_id and pivot_id:
            plan = self.store.get_object(case_id, "query_plan", query_plan_id)
            pivot = next((item for item in plan["pivots"] if item["pivot_id"] == pivot_id), None)
            if pivot is None:
                raise ValueError(f"pivot not found: {pivot_id}")
            normalized_output = {
                "source_id": source["source_id"],
                "capture_id": capture["capture_id"],
                "indicator_count": len(extraction.indicators),
                "entity_ids": extraction.entity_ids,
                "claim_ids": extraction.claim_ids,
                "relation_ids": extraction.relation_ids,
            }
            job = self.jobs.record_completed_job(
                case_id,
                query_plan_id=query_plan_id,
                pivot_id=pivot_id,
                stream=pivot["stream"],
                input_type="DOCUMENT",
                input_reference=capture["capture_id"],
                raw_output=text.encode("utf-8"),
                normalized_output=normalized_output,
                result_code="FOUND",
                summary=f"Ingested supplied text and extracted {len(extraction.indicators)} identifier candidate(s).",
                source_id=source["source_id"],
                source_ids=[source["source_id"]],
                capture_ids=[capture["capture_id"]],
                entity_ids=extraction.entity_ids,
                relation_ids=extraction.relation_ids,
                claim_ids=extraction.claim_ids,
                execution_profile="MANUAL_EXTERNAL",
                safety_class="PASSIVE_PUBLIC",
                network_policy="NO_NETWORK",
                parser_name="deterministic-identifier-extractor",
                parser_version=self.extractor.version,
            )
        return IngestResult(source, capture, extraction, job)

    def build_outputs(
        self,
        case_id: str,
        *,
        public_export: bool = False,
        redacted: bool = True,
        include_analysis_zoo: bool = True,
        graph_seed_refs: tuple[str, ...] = (),
        report_name: str = "main_official_report.md",
    ) -> OutputBundle:
        coverage_items = [
            self.coverage.assess(case_id, item["finding_id"])
            for item in self.store.list_objects(case_id, "finding")
        ]
        graph = self.graph.build(
            case_id,
            seed_refs=graph_seed_refs,
            mode="GRAPH",
            purpose="Evidence-linked case relationship view",
        )
        analysis: AnalysisZooResult | None = None
        refs = [
            *[item["finding_id"] for item in self.store.list_objects(case_id, "finding")],
            *[item["relation_id"] for item in self.store.list_objects(case_id, "relation")],
            *[item["claim_id"] for item in self.store.list_objects(case_id, "claim")],
        ]
        if include_analysis_zoo and refs:
            analysis = self.analysis_zoo.run(
                case_id,
                task="Challenge evidence lineage, identity and graph overclaiming before report generation",
                input_refs=refs,
            )
        report = self.reporting.build(
            case_id,
            public_export=public_export,
            redacted=redacted,
            report_name=report_name,
        )
        snapshot = self.monitor.snapshot(case_id, label="post-report")
        return OutputBundle(
            coverage=coverage_items,
            graph=graph,
            analysis=analysis,
            report=report,
            monitor_snapshot=snapshot,
            summary=self.store.summary(case_id),
        )
