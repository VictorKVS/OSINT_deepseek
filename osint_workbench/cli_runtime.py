from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable

from .analysis_zoo import AnalysisZoo
from .coverage import EvidenceCoverageAssessor
from .demo import run_demo
from .extractor import DeterministicIdentifierExtractor
from .graph import GraphProjector
from .http_collect import PassiveHTTPCollector
from .monitoring import CaseMonitor
from .planner import CoreQueryPlanner
from .reporting import OfficialReportComposer
from .resolution import ExplainableEntityResolver
from .service import serve
from .store import WorkbenchStore
from .workflow import PassiveOSINTWorkbench
from .cli_parser import build_parser


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    return value


def _print(value: Any) -> None:
    print(json.dumps(_jsonable(value), ensure_ascii=False, sort_keys=True, indent=2))


def _csv(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def _identifier_values(items: Iterable[str], source_ids: list[str]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for raw in items:
        if "=" not in raw:
            raise ValueError(f"identifier must be TYPE=VALUE: {raw}")
        kind, value = raw.split("=", 1)
        result.append({"type": kind.upper(), "value": value, "masked": False, "source_ids": source_ids})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            _print(run_demo(args.root, force=args.force))
            return 0
        store = WorkbenchStore(args.root)

        if args.command == "init-case":
            workbench = PassiveOSINTWorkbench(args.root)
            result = workbench.bootstrap_case(
                title=args.title,
                seed_type=args.seed_type,
                seed_value=args.seed,
                aliases=tuple(_csv(args.aliases)),
                purpose=args.purpose,
                legal_basis_or_usage_note=args.legal_basis,
                owner_role=args.owner_role,
                case_type=args.case_type,
                access_class=args.access_class,
                jurisdictions=tuple(_csv(args.jurisdictions)),
                objective=args.objective,
                approve_plan=args.approve_plan,
                reviewer_id=args.reviewer_id,
                synthetic=args.synthetic,
                case_id=args.case_id,
            )
            _print(result)
        elif args.command == "plan":
            _print(CoreQueryPlanner(store).plan(
                args.case_id,
                seed_entity_id=args.seed_entity_id,
                objective=args.objective,
                mode=args.mode,
                approve=args.approve,
                reviewer_id=args.reviewer_id,
            ))
        elif args.command == "add-source":
            _print(store.register_source(
                args.case_id,
                url=args.url,
                title=args.title,
                publisher=args.publisher,
                source_type=args.source_type,
                primary_level=args.primary_level,
                jurisdiction=args.jurisdiction,
                language=args.language,
                reliability_grade=args.reliability_grade,
                what_it_supports=_csv(args.supports),
                what_it_does_not_support=_csv(args.does_not_support),
                access_class=args.access_class,
                legal_basis_or_usage_note=args.legal_basis,
                republication_status=args.republication_status,
            ))
        elif args.command == "capture-file":
            path = Path(args.path)
            _print(store.capture_bytes(
                args.case_id,
                source_id=args.source_id,
                data=path.read_bytes(),
                filename_hint=path.name,
                capture_method="MANUAL_UPLOAD",
                access_class=args.access_class,
                legal_basis_or_usage_note=args.legal_basis,
            ))
        elif args.command == "capture-text":
            text = args.text if args.text is not None else sys.stdin.read()
            _print(store.capture_text(
                args.case_id,
                source_id=args.source_id,
                text=text,
                filename_hint=args.filename,
                access_class=args.access_class,
                legal_basis_or_usage_note=args.legal_basis,
            ))
        elif args.command == "extract":
            _print(DeterministicIdentifierExtractor(store).extract_capture(
                args.case_id,
                source_id=args.source_id,
                capture_id=args.capture_id,
                query_plan_id=args.query_plan_id,
                job_id=args.job_id,
            ))
        elif args.command == "add-entity":
            source_ids = _csv(args.sources)
            _print(store.create_entity(
                args.case_id,
                entity_type=args.entity_type,
                display_name=args.name,
                source_ids=source_ids,
                aliases=_csv(args.aliases),
                identifiers=_identifier_values(args.identifier, source_ids),
                access_class=args.access_class,
                status=args.status,
            ))
        elif args.command == "add-claim":
            _print(store.create_claim(
                args.case_id,
                source_ids=_csv(args.sources),
                statement=args.statement,
                locator=args.locator,
                subject_entity_ids=_csv(args.subjects),
                representation=args.representation,
                predicate=args.predicate,
                object_entity_ids=_csv(args.objects),
                object_text=args.object_text,
                access_class=args.access_class,
            ))
        elif args.command == "add-relation":
            _print(store.create_relation(
                args.case_id,
                from_entity_id=args.from_entity_id,
                relation_type=args.relation_type,
                to_entity_id=args.to_entity_id,
                source_ids=_csv(args.sources),
                claim_ids=_csv(args.claims),
                evidence_grade=args.evidence_grade,
                status=args.status,
            ))
        elif args.command == "approve-finding":
            _print(store.create_finding(
                args.case_id,
                classification=args.classification,
                statement=args.statement,
                evidence_grade=args.evidence_grade,
                source_ids=_csv(args.sources),
                claim_ids=_csv(args.claims),
                entity_ids=_csv(args.entities),
                reasoning_summary=args.reasoning,
                limitations=_csv(args.limitations),
                alternative_explanations=_csv(args.alternatives),
                approved_by_role=args.approved_by_role,
                red_team_status=args.red_team_status,
                access_class=args.access_class,
            ))
        elif args.command == "add-gap":
            _print(store.create_research_gap(
                args.case_id,
                subject_refs=_csv(args.subjects),
                stream=args.stream,
                question=args.question,
                why_matters=args.why,
                evidence_needed=_csv(args.evidence_needed),
                owner_role=args.owner_role,
                priority=args.priority,
                state=args.state,
                report_effect=args.report_effect,
            ))
        elif args.command == "resolve":
            _print(ExplainableEntityResolver(store).compare(
                args.case_id,
                args.entity_a_id,
                args.entity_b_id,
                query_plan_id=args.query_plan_id,
            ))
        elif args.command == "fetch-url":
            collector = PassiveHTTPCollector(store, timeout_seconds=args.timeout, max_bytes=args.max_bytes)
            _print(collector.fetch(
                args.case_id,
                query_plan_id=args.query_plan_id,
                pivot_id=args.pivot_id,
                url=args.url,
                title=args.title,
                publisher=args.publisher,
                source_type=args.source_type,
                primary_level=args.primary_level,
                jurisdiction=args.jurisdiction,
                language=args.language,
                reliability_grade=args.reliability_grade,
                legal_basis_or_usage_note=args.legal_basis,
                republication_status=args.republication_status,
                extract_identifiers=not args.no_extract,
            ))
        elif args.command == "coverage":
            _print(EvidenceCoverageAssessor(store).assess(args.case_id, args.finding_id))
        elif args.command == "graph":
            _print(GraphProjector(store).build(
                args.case_id,
                seed_refs=_csv(args.seed_refs),
                mode=args.mode,
                purpose=args.purpose,
                bounded_hops=args.bounded_hops,
            ))
        elif args.command == "analyze":
            _print(AnalysisZoo(store).run(
                args.case_id,
                task=args.task,
                input_refs=_csv(args.input_refs),
                analyzer_ids=_csv(args.analyzers),
            ))
        elif args.command == "analyzers":
            _print([asdict(item) for item in AnalysisZoo(store).list_analyzers()])
        elif args.command == "report":
            _print(OfficialReportComposer(store).build(
                args.case_id,
                public_export=args.public,
                redacted=not args.unredacted,
                report_name=args.name,
            ))
        elif args.command == "monitor":
            _print(CaseMonitor(store).snapshot(args.case_id, label=args.label))
        elif args.command == "summary":
            _print(store.summary(args.case_id))
        elif args.command == "verify-journal":
            result = store.verify_journal(args.case_id)
            _print(result)
            return 0 if result["valid"] else 1
        elif args.command == "serve":
            serve(store, host=args.host, port=args.port, expose_local_paths=args.expose_local_paths)
        else:  # pragma: no cover
            parser.error(f"unknown command: {args.command}")
        return 0
    except (ValueError, RuntimeError, PermissionError, FileNotFoundError) as exc:
        print(json.dumps({"error": type(exc).__name__, "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
