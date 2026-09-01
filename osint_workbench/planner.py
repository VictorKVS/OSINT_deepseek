from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import normalize_name, sha256_json, transliterate_ru, utc_now_iso
from .store import STREAMS, WorkbenchStore


@dataclass(frozen=True, slots=True)
class StreamTemplate:
    stream: str
    priority: str
    question: str
    why_matters: str
    source_family: str
    expected_output_types: tuple[str, ...]
    action_template: str


_TEMPLATES: dict[str, tuple[StreamTemplate, ...]] = {
    "ORGANIZATION": (
        StreamTemplate("ENTITY_REGISTRY", "P0", "Однозначно ли установлена организация, её реквизиты, названия и контролирующие лица?", "Ошибка идентификации загрязнит все дальнейшие связи.", "official_company_registries", ("ORGANIZATION", "PERSON", "ADDRESS", "SOURCE", "SOURCE_CAPTURE", "CLAIM", "RELATION"), "Resolve registration, identifiers, names, directors, owners and historical changes for {seed}"),
        StreamTemplate("BUSINESS_TRANSACTIONS_LOGISTICS", "P1", "Как организация фактически ведёт деятельность, получает деньги, товары и услуги?", "Регистрационная запись не доказывает реальную деятельность и деловые потоки.", "procurement_trade_logistics", ("ORGANIZATION", "CONTRACT", "ASSET", "EVENT", "SOURCE", "CLAIM", "RELATION", "RESEARCH_GAP"), "Trace contracts, procurement, counterparties, facilities, products, payments and logistics for {seed}"),
        StreamTemplate("DIGITAL_FOOTPRINT", "P1", "Какие домены, контакты, аккаунты и технические активы достоверно связаны с организацией?", "Цифровые идентификаторы дают новые проверяемые pivots, но требуют доказанной атрибуции.", "dns_rdap_certificates_archives_public_accounts", ("DOMAIN", "EMAIL", "PHONE", "ASSET", "SOURCE", "CLAIM", "RELATION"), "Collect passive public digital footprint, domains, certificates, archives, emails and accounts for {seed}"),
        StreamTemplate("LEGAL_SANCTIONS_ADVERSE", "P1", "Какие судебные, санкционные, банкротные и регуляторные сведения относятся именно к этой организации?", "Негативный статус допустим только при точной идентификации и первичном источнике.", "courts_sanctions_regulators_bankruptcy", ("CASE", "EVENT", "ORGANIZATION", "SOURCE", "SOURCE_CAPTURE", "CLAIM", "RELATION", "FINDING"), "Check official court, enforcement, sanctions, bankruptcy and regulator records for {seed}"),
        StreamTemplate("RED_TEAM_SOURCE_QUALITY", "P0", "Какие тёзки, зависимые источники, временные конфликты и альтернативные объяснения ограничивают выводы?", "Критический анализ снижает ложную атрибуцию и превращение близости в причинность.", "internal_review_and_counter_evidence", ("FINDING", "RESEARCH_GAP"), "Challenge identity, source independence, temporal order, causal claims and unsupported conclusions for {seed}"),
    ),
    "PERSON": (
        StreamTemplate("ENTITY_REGISTRY", "P0", "Однозначно ли разрешена личность без смешения тёзок?", "Ошибочная идентификация лица создаёт высокий правовой и аналитический риск.", "official_public_identity_and_corporate_records", ("PERSON", "ORGANIZATION", "ADDRESS", "SOURCE", "CLAIM", "RELATION"), "Resolve lawful public identifiers, name variants, roles and corporate affiliations for {seed}"),
        StreamTemplate("BUSINESS_TRANSACTIONS_LOGISTICS", "P1", "Какие документально подтверждённые деловые роли, активы и контрагенты связаны с лицом?", "Связь должна опираться на документы, а не на социальную близость.", "corporate_procurement_property_public_records", ("PERSON", "ORGANIZATION", "ASSET", "CONTRACT", "SOURCE", "CLAIM", "RELATION"), "Trace documented business roles, assets, contracts and counterparties for {seed}"),
        StreamTemplate("DIGITAL_FOOTPRINT", "P2", "Какие публичные аккаунты и контакты принадлежат именно этому лицу?", "Совпадение имени или аватара не является достаточной атрибуцией.", "public_accounts_and_archives", ("PERSON", "DOMAIN", "EMAIL", "SOURCE", "CLAIM", "RELATION"), "Collect only necessary public accounts and identifiers with attribution evidence for {seed}"),
        StreamTemplate("LEGAL_SANCTIONS_ADVERSE", "P1", "Есть ли относящиеся к лицу официальные правовые или санкционные сведения и каков их процессуальный статус?", "Сообщение СМИ не заменяет решение компетентного органа.", "courts_sanctions_regulators", ("CASE", "EVENT", "ORGANIZATION", "SOURCE", "CLAIM", "FINDING"), "Check official legal, sanctions and regulator records for {seed} and preserve procedural status"),
        StreamTemplate("RED_TEAM_SOURCE_QUALITY", "P0", "Можно ли опровергнуть идентификацию, роль или предполагаемую связь лица?", "Red Team должен проверять тёзок, общие адреса и неподтверждённые родственные/этнические выводы.", "internal_review_and_counter_evidence", ("FINDING", "RESEARCH_GAP"), "Challenge namesake risk, shared identifiers, source bias, chronology and prohibited affiliation inferences for {seed}"),
    ),
    "DOMAIN": (
        StreamTemplate("ENTITY_REGISTRY", "P0", "Кто и на каком основании связан с доменом?", "Регистратор, хостер и пользователь домена — разные роли.", "rdap_dns_certificates", ("DOMAIN", "ORGANIZATION", "PERSON", "SOURCE", "CLAIM", "RELATION"), "Resolve RDAP, DNS, certificate and historical ownership signals for {seed}"),
        StreamTemplate("BUSINESS_TRANSACTIONS_LOGISTICS", "P2", "Как домен используется в бизнес-процессе или инфраструктуре?", "Техническая связь не всегда подтверждает хозяйственный контроль.", "website_content_and_public_business_records", ("ORGANIZATION", "CONTRACT", "SOURCE", "CLAIM", "RELATION"), "Relate website claims, products, payment endpoints and public business records to {seed}"),
        StreamTemplate("DIGITAL_FOOTPRINT", "P0", "Какие пассивно наблюдаемые поддомены, сертификаты, DNS/ASN и архивные версии связаны с доменом?", "Это основной технический OSINT-поток без активного воздействия.", "passive_dns_certificates_archives", ("DOMAIN", "ASSET", "EMAIL", "SOURCE", "SOURCE_CAPTURE", "CLAIM", "RELATION"), "Collect passive DNS, certificates, ASN, archives, public metadata and linked domains for {seed}"),
        StreamTemplate("LEGAL_SANCTIONS_ADVERSE", "P2", "Есть ли официальные ограничения или дела, связанные с владельцем либо использованием домена?", "Правовые выводы требуют отдельной идентификации владельца и статуса документа.", "courts_regulators_sanctions", ("CASE", "ORGANIZATION", "SOURCE", "CLAIM", "FINDING"), "Check regulator, court and sanctions records for entities attributed to {seed}"),
        StreamTemplate("RED_TEAM_SOURCE_QUALITY", "P0", "Может ли инфраструктура быть общей, CDN/хостингом или исторически переиспользованной?", "Общий IP или сертификат сам по себе не доказывает единый контроль.", "internal_review_and_counter_evidence", ("FINDING", "RESEARCH_GAP"), "Challenge shared hosting, CDN, certificate reuse, stale DNS and attribution assumptions for {seed}"),
    ),
    "ACCOUNT": (),
    "ASSET": (),
    "ADDRESS": (),
    "DOCUMENT": (),
}

# Fallback to the organization-style five-stream workflow while preserving the seed type.
_FALLBACK = _TEMPLATES["ORGANIZATION"]


class CoreQueryPlanner:
    """Deterministic five-stream planner for the passive core OSINT workflow."""

    version = "core-query-planner/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    @staticmethod
    def expand_seed_variants(display_name: str, aliases: list[str] | None = None) -> list[str]:
        aliases = aliases or []
        variants: list[str] = []
        for value in [display_name, *aliases]:
            cleaned = " ".join(value.split()).strip()
            if not cleaned:
                continue
            variants.extend([cleaned, cleaned.upper(), normalize_name(cleaned), transliterate_ru(cleaned)])
            if cleaned.lower().startswith("ооо "):
                variants.extend([cleaned[4:].strip(), f'LLC {cleaned[4:].strip()}'])
            if cleaned.lower().endswith(" llc"):
                variants.append(cleaned[:-4].strip())
        return list(dict.fromkeys(item for item in variants if item))

    def plan(
        self,
        case_id: str,
        *,
        seed_entity_id: str,
        objective: str,
        mode: str = "IDENTIFY",
        approve: bool = False,
        reviewer_id: str | None = None,
        created_by: str = "core-query-planner",
        max_network_requests_per_pivot: int = 10,
    ) -> dict[str, Any]:
        case = self.store.get_case(case_id)
        seed = self.store.get_object(case_id, "entity", seed_entity_id)
        mode = mode.upper()
        if mode not in {"IDENTIFY", "INVESTIGATE", "MONITOR"}:
            raise ValueError("mode must be IDENTIFY, INVESTIGATE or MONITOR")
        templates = _TEMPLATES.get(seed["entity_type"]) or _FALLBACK
        query_plan_id = self.store._allocate_id(case_id, "QPLAN")
        variants = self.expand_seed_variants(seed["display_name"], seed.get("aliases", []))
        unknowns: list[dict[str, Any]] = []
        pivots: list[dict[str, Any]] = []
        registry_pivot_id = "PVT-0001"
        for index, template in enumerate(templates, start=1):
            question_id = f"Q-{index:04d}"
            pivot_id = f"PVT-{index:04d}"
            unknowns.append(
                {
                    "question_id": question_id,
                    "question": template.question,
                    "why_matters": template.why_matters,
                    "priority": template.priority,
                    "stream": template.stream,
                    "status": "PLANNED",
                }
            )
            dependencies: list[str] = [] if index == 1 else [registry_pivot_id]
            if template.stream == "RED_TEAM_SOURCE_QUALITY":
                dependencies = [f"PVT-{i:04d}" for i in range(1, index)]
            query = template.action_template.format(seed=seed["display_name"])
            query += f" | variants: {'; '.join(variants[:8])}"
            pivots.append(
                {
                    "pivot_id": pivot_id,
                    "stream": template.stream,
                    "query_or_action": query,
                    "input_entity_ids": [seed_entity_id],
                    "source_family": template.source_family,
                    "execution_mode": "MANUAL_EXTERNAL",
                    "expected_output_types": list(template.expected_output_types),
                    "priority": template.priority,
                    "status": "READY" if approve else "PLANNED",
                    "access_class": case["access_class"],
                    "dependencies": dependencies,
                    "timeout_seconds": 600,
                    "max_requests": max(0, int(max_network_requests_per_pivot)),
                    "notes": "Passive collection only. Every terminal result must be journaled as FOUND/NO_HIT/BLOCKED/CONFLICT/ERROR.",
                }
            )

        payload: dict[str, Any] = {
            "schema_version": "father-osint.query-plan.v0.1",
            "query_plan_id": query_plan_id,
            "case_id": case_id,
            "objective": objective.strip(),
            "mode": mode,
            "status": "APPROVED" if approve else "AWAITING_APPROVAL",
            "created_at_utc": utc_now_iso(),
            "created_by": {"actor_id": created_by, "actor_type": "RULE_ENGINE", "version": self.version},
            "seed_entity_ids": [seed_entity_id],
            "known_fact_ids": [],
            "unknowns": unknowns,
            "pivots": pivots,
            "legal_constraints": [
                "Use only lawfully accessible information within the documented case purpose.",
                "Do not bypass authentication, access controls, paywalls, CAPTCHA or platform restrictions.",
                "Do not convert a source claim, model opinion, shared address or technical proximity into a fact without review.",
                "Collect only necessary personal data and keep restricted evidence outside public exports.",
                "Active scanning, exploitation, credential attacks, phishing and interception are outside this passive plan.",
            ],
            "stop_conditions": [
                "Stop when every planned pivot has a terminal result or an explicit blocking reason.",
                "Stop and escalate when a source or datum is classified PROHIBITED.",
                "Stop broadening when new collection no longer changes entities, relations, contradictions or decisive gaps.",
                "Do not promote any automated output directly to FACT.",
            ],
            "expected_cost_time": {
                "estimated_jobs": len(pivots),
                "estimated_minutes": float(len(pivots) * 10),
                "max_network_requests": len(pivots) * max(0, int(max_network_requests_per_pivot)),
                "estimate_basis": "Planning estimate only; production duration requires measured source telemetry.",
            },
            "human_approval": {
                "required": True,
                "status": "APPROVED" if approve else "PENDING",
                "reviewer_id": reviewer_id if approve else None,
                "reviewed_at_utc": utc_now_iso() if approve else None,
                "note": "Approved for passive public-source collection only." if approve else "Awaiting analyst review.",
            },
            "plan_hash": "",
            "synthetic": case["synthetic"],
        }
        payload["plan_hash"] = sha256_json(payload, exclude_fields={"plan_hash"})
        self.store.save_object(case_id, "query_plan", payload)
        self.store.append_journal(
            case_id,
            actor_id=created_by,
            actor_type="AGENT",
            action_type="PLAN",
            stream="ENTITY_REGISTRY",
            query_plan_id=query_plan_id,
            query_or_action=f"Create five-stream {mode} plan for {seed_entity_id}",
            result_code="REVIEWED" if approve else "FOUND",
            result_summary=f"Generated {len(pivots)} passive pivots; human approval status={payload['human_approval']['status']}.",
            next_pivots=[item["pivot_id"] for item in pivots],
            access_class=case["access_class"],
            actor_version=self.version,
        )
        return payload
