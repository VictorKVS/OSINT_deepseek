from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .resolution import ExplainableEntityResolver
from .workflow import PassiveOSINTWorkbench


def run_demo(root: str | Path, *, force: bool = False) -> dict[str, Any]:
    root_path = Path(root).expanduser().resolve()
    if root_path.exists() and any(root_path.iterdir()):
        if not force:
            raise FileExistsError(f"demo root is not empty: {root_path}")
        shutil.rmtree(root_path)
    workbench = PassiveOSINTWorkbench(root_path)
    boot = workbench.bootstrap_case(
        title="Синтетический пилот основных задач OSINT",
        seed_type="ORGANIZATION",
        seed_value="ООО «Северный Контур»",
        aliases=("Northern Contour LLC",),
        purpose="Проверить полный пассивный OSINT-контур: планирование, фиксацию источников, извлечение, разрешение сущностей, граф, анализ, пробелы и формальную справку.",
        legal_basis_or_usage_note="Полностью синтетическое учебное дело без реальных лиц, организаций и сетевого сбора.",
        owner_role="Главный аналитик",
        case_type="SYNTHETIC_TRAINING",
        access_class="PUBLIC",
        jurisdictions=("SYNTHETIC",),
        objective="Однозначно разрешить учебную организацию и показать доказательственную цепочку без превращения автоматических результатов в факты.",
        approve_plan=True,
        reviewer_id="demo-chief-analyst",
        synthetic=True,
        case_id="CASE-SYNTH-CORE-0001",
    )
    case_id = boot.case["case_id"]

    register_text = """SYNTHETIC PUBLIC REGISTER
Record: SYN-ORG-0001
Organization: ООО «Северный Контур»
Registered address: Учебный проспект, дом 10
Public website: https://north-contour.example
Public contact: office@north-contour.example
Public phone: +7 (900) 555-01-01
Status: training fixture only.
"""
    ingested = workbench.ingest_text(
        case_id,
        text=register_text,
        url="urn:synthetic:register:north-contour:record-0001",
        title="Синтетическая выписка учебного реестра № SYN-ORG-0001",
        publisher="Synthetic Registry Authority",
        source_type="OFFICIAL_REGISTER",
        primary_level="PRIMARY",
        jurisdiction="SYNTHETIC",
        language="ru",
        reliability_grade="A_CONFIRMED",
        access_class="PUBLIC",
        legal_basis_or_usage_note="Synthetic public fixture.",
        republication_status="ALLOWED",
        query_plan_id=boot.plan["query_plan_id"],
        pivot_id="PVT-0001",
    )
    source_id = ingested.source["source_id"]
    verified_org = workbench.store.create_entity(
        case_id,
        entity_type="ORGANIZATION",
        display_name="ООО «Северный Контур»",
        aliases=["Northern Contour LLC"],
        identifiers=[
            {
                "type": "REGISTRY_ID",
                "value": "SYN-ORG-0001",
                "masked": False,
                "source_ids": [source_id],
            }
        ],
        attributes={"registered_address": "Учебный проспект, дом 10", "is_fictional": True},
        source_ids=[source_id],
        access_class="PUBLIC",
        status="CONFIRMED",
        synthetic=True,
    )
    address = workbench.store.create_entity(
        case_id,
        entity_type="ADDRESS",
        display_name="Учебный проспект, дом 10",
        identifiers=[
            {
                "type": "REGISTERED_ADDRESS",
                "value": "Учебный проспект, дом 10",
                "masked": False,
                "source_ids": [source_id],
            }
        ],
        attributes={"is_fictional": True},
        source_ids=[source_id],
        access_class="PUBLIC",
        status="CONFIRMED",
        synthetic=True,
    )
    registration_claim = workbench.store.create_claim(
        case_id,
        source_ids=[source_id],
        statement="Синтетическая запись реестра указывает организацию SYN-ORG-0001 по учебному регистрационному адресу.",
        representation="STRUCTURED_EXTRACTION",
        locator=f"capture:{ingested.capture['capture_id']}; lines:2-4",
        subject_entity_ids=[verified_org["entity_id"]],
        predicate="REGISTERED_AT",
        object_entity_ids=[address["entity_id"]],
        access_class="PUBLIC",
        limitations=[
            "Регистрационный адрес не подтверждает фактическое присутствие или хозяйственную деятельность.",
            "Данные полностью синтетические и не относятся к реальной организации.",
        ],
    )
    registration_relation = workbench.store.create_relation(
        case_id,
        from_entity_id=verified_org["entity_id"],
        relation_type="REGISTERED_AT",
        to_entity_id=address["entity_id"],
        source_ids=[source_id],
        claim_ids=[registration_claim["claim_id"]],
        evidence_grade="A_CONFIRMED",
        status="CONFIRMED",
        not_implying=[
            "Фактическое присутствие по адресу.",
            "Реальную хозяйственную деятельность.",
            "Любой негативный правовой или репутационный статус.",
        ],
    )
    workbench.store.append_journal(
        case_id,
        actor_id="demo-normalizer",
        actor_type="AGENT",
        action_type="LINK",
        stream="ENTITY_REGISTRY",
        query_plan_id=boot.plan["query_plan_id"],
        job_id=ingested.job["job_id"] if ingested.job else None,
        query_or_action="Normalize synthetic registry organization-to-address relation",
        source_or_transform_ids=[source_id],
        result_code="REVIEWED",
        result_summary=f"Created reviewed registration relation {registration_relation['relation_id']}.",
        new_entities=[verified_org["entity_id"], address["entity_id"]],
        new_relations=[registration_relation["relation_id"]],
        new_claims=[registration_claim["claim_id"]],
        access_class="PUBLIC",
        actor_version="demo-normalizer/0.1.0",
    )

    namesake_text = """SYNTHETIC NAMESAKE REGISTER
Record: SYN-ORG-9999
Organization: ООО «Северный Контур»
Registered address: Другой учебный переулок, дом 99
Status: distinct training fixture.
"""
    namesake_source = workbench.store.register_source(
        case_id,
        url="urn:synthetic:register:north-contour:record-9999",
        title="Синтетическая запись одноимённой организации № SYN-ORG-9999",
        publisher="Synthetic Registry Authority B",
        source_type="OFFICIAL_REGISTER",
        primary_level="PRIMARY",
        jurisdiction="SYNTHETIC",
        language="ru",
        affiliation="Independent synthetic fixture publisher.",
        bias_or_interest="None; training fixture.",
        reliability_grade="A_CONFIRMED",
        what_it_supports=["A distinct synthetic registry record with the same display name exists."],
        what_it_does_not_support=["That the two organizations are identical."],
        access_class="PUBLIC",
        legal_basis_or_usage_note="Synthetic public fixture.",
        republication_status="ALLOWED",
    )
    workbench.store.capture_text(
        case_id,
        source_id=namesake_source["source_id"],
        text=namesake_text,
        filename_hint="namesake-register.txt",
        collector_id="demo-fixture",
        collector_version="0.1.0",
        access_class="PUBLIC",
        legal_basis_or_usage_note="Synthetic public fixture.",
    )
    namesake = workbench.store.create_entity(
        case_id,
        entity_type="ORGANIZATION",
        display_name="ООО «Северный Контур»",
        identifiers=[
            {
                "type": "REGISTRY_ID",
                "value": "SYN-ORG-9999",
                "masked": False,
                "source_ids": [namesake_source["source_id"]],
            }
        ],
        attributes={"registered_address": "Другой учебный переулок, дом 99", "is_fictional": True},
        source_ids=[namesake_source["source_id"]],
        access_class="PUBLIC",
        status="CONFIRMED",
        synthetic=True,
    )
    entity_match = ExplainableEntityResolver(workbench.store).compare(
        case_id,
        verified_org["entity_id"],
        namesake["entity_id"],
        query_plan_id=boot.plan["query_plan_id"],
    )

    finding = workbench.store.create_finding(
        case_id,
        classification="FACT",
        statement="В синтетическом учебном реестре организация SYN-ORG-0001 связана с учебным регистрационным адресом.",
        evidence_grade="A_CONFIRMED",
        source_ids=[source_id],
        claim_ids=[registration_claim["claim_id"]],
        entity_ids=[verified_org["entity_id"], address["entity_id"]],
        reasoning_summary="Первичная синтетическая запись и сохранённый capture однозначно содержат регистрационную связь.",
        limitations=[
            "Вывод относится только к синтетической записи.",
            "Не подтверждает фактическое присутствие, деятельность, активы или негативный статус.",
        ],
        alternative_explanations=["Регистрационный адрес может не совпадать с фактическим местом деятельности."],
        approved_by_role="Главный аналитик",
        red_team_status="PASSED",
        access_class="PUBLIC",
    )
    gap = workbench.store.create_research_gap(
        case_id,
        subject_refs=[finding["finding_id"], verified_org["entity_id"]],
        stream="BUSINESS_TRANSACTIONS_LOGISTICS",
        question="Подтверждено ли фактическое присутствие или деятельность по регистрационному адресу?",
        why_matters="Регистрационная запись сама по себе не доказывает операционную деятельность.",
        priority="P1",
        state="NO_HIT",
        evidence_needed=["Независимый источник о площадке", "Документы аренды/владения", "Проверяемые операционные записи"],
        planned_pivot_ids=["PVT-0002"],
        blocking_reasons=["Synthetic fixture intentionally contains no operational evidence."],
        owner_role="Составной аналитик",
        report_effect="LIMITS_REPORT",
    )

    transform = workbench.jobs.register_transform(
        case_id,
        name="Synthetic official-register lookup",
        input_entity_types=["ORGANIZATION"],
        output_object_types=["SOURCE", "SOURCE_CAPTURE", "ORGANIZATION", "CLAIM", "RELATION"],
        source_id=source_id,
        execution_profile="FIXTURE_ONLY",
        safety_class="PASSIVE_PUBLIC",
        network_policy="NO_NETWORK",
        evidence_capture_mode="FULL_CAPTURE",
        parser_version="synthetic-register-parser/0.1.0",
        max_requests=1,
        per_seconds=60,
        concurrency=1,
    )

    workbench.store.append_journal(
        case_id,
        actor_id="demo-chief-analyst",
        actor_type="HUMAN",
        action_type="REVIEW",
        stream="RED_TEAM_SOURCE_QUALITY",
        query_plan_id=boot.plan["query_plan_id"],
        query_or_action=f"Approve finding {finding['finding_id']} and preserve unresolved gap {gap['research_gap_id']}",
        source_or_transform_ids=[source_id, transform["transform_id"]],
        result_code="REVIEWED",
        result_summary="Approved the narrow registration fact; retained operational-presence gap and distinct namesake record.",
        new_findings=[finding["finding_id"]],
        new_research_gaps=[gap["research_gap_id"]],
        next_pivots=["PVT-0002", "PVT-0005"],
        access_class="PUBLIC",
        actor_version="human-review/demo",
    )

    outputs = workbench.build_outputs(
        case_id,
        public_export=True,
        redacted=True,
        include_analysis_zoo=True,
        graph_seed_refs=(verified_org["entity_id"],),
        report_name="main_official_report_redacted.md",
    )
    manifest = {
        "case_id": case_id,
        "root": str(root_path),
        "query_plan_id": boot.plan["query_plan_id"],
        "seed_entity_id": boot.seed_entity["entity_id"],
        "verified_entity_id": verified_org["entity_id"],
        "namesake_entity_id": namesake["entity_id"],
        "entity_match_id": entity_match["entity_match_id"],
        "source_id": source_id,
        "capture_id": ingested.capture["capture_id"],
        "finding_id": finding["finding_id"],
        "research_gap_id": gap["research_gap_id"],
        "transform_id": transform["transform_id"],
        "graph_view_id": outputs.graph["graph_view_id"],
        "analysis_run_id": outputs.analysis.run["run_id"] if outputs.analysis else None,
        "consensus_id": outputs.analysis.consensus["consensus_id"] if outputs.analysis else None,
        "report": outputs.report.path,
        "report_sha256": outputs.report.sha256,
        "monitor_snapshot_id": outputs.monitor_snapshot["snapshot_id"],
        "journal": outputs.summary["journal_integrity"],
        "counts": outputs.summary["counts"],
    }
    manifest_path = root_path / "DEMO_RESULT.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest
