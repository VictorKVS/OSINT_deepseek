from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import (
    CheckDefinition,
    CheckStage,
    CheckStream,
    JurisdictionScope,
    ScreeningDepth,
    SubjectKind,
)

ALL_KINDS = (SubjectKind.PERSON, SubjectKind.LEGAL_ENTITY)
ALL_SCOPES = (JurisdictionScope.RUSSIA, JurisdictionScope.FOREIGN)
PERSON = (SubjectKind.PERSON,)
LEGAL = (SubjectKind.LEGAL_ENTITY,)
RU = (JurisdictionScope.RUSSIA,)
FOREIGN = (JurisdictionScope.FOREIGN,)


@dataclass(frozen=True, slots=True)
class ScreeningProfile:
    profile_id: str
    title_ru: str
    subject_kind: SubjectKind
    jurisdiction_scope: JurisdictionScope
    source_pack_ids: tuple[str, ...]
    check_codes: tuple[str, ...]
    default_depth: ScreeningDepth = ScreeningDepth.STANDARD


CHECKS: tuple[CheckDefinition, ...] = (
    CheckDefinition(
        "ADM-001", "Правовое основание, цель и минимизация данных", CheckStream.RED_TEAM_SOURCE_QUALITY,
        CheckStage.ADMISSION, ScreeningDepth.BASIC, ALL_KINDS, ALL_SCOPES,
        ("CASE_POLICY",), ("POLICY_GATE",), criticality="BLOCKING", freshness_days=1,
        human_review_if_found=True,
        evidence_expectation="Approved purpose, lawful-basis note, source classes and export profile",
        not_implying=("Разрешение на скрытый сбор", "Разрешение на активное воздействие"),
    ),
    CheckDefinition(
        "IDN-001", "Достаточность исходных идентификаторов", CheckStream.IDENTITY_REGISTRY,
        CheckStage.ADMISSION, ScreeningDepth.BASIC, ALL_KINDS, ALL_SCOPES,
        ("SUBJECT_INPUT",), ("IDENTITY_ANCHOR_CHECK",), dependencies=("ADM-001",),
        criticality="BLOCKING", freshness_days=1,
        evidence_expectation="At least one strong identifier or an explicit identity gap",
    ),
    CheckDefinition(
        "IDN-002", "Варианты имени, наименования и транслитерации", CheckStream.IDENTITY_REGISTRY,
        CheckStage.IDENTIFY, ScreeningDepth.BASIC, ALL_KINDS, ALL_SCOPES,
        ("INPUT_NORMALIZATION", "LANGUAGE_VARIANTS"), ("ALIAS_EXPANSION", "TRANSLITERATION"),
        dependencies=("IDN-001",), freshness_days=3650,
        not_implying=("Тождество всех найденных одноимённых объектов",),
    ),
    CheckDefinition(
        "IDN-003", "Проверка тёзок и одноимённых организаций", CheckStream.RED_TEAM_SOURCE_QUALITY,
        CheckStage.REVIEW, ScreeningDepth.BASIC, ALL_KINDS, ALL_SCOPES,
        ("ALL_COLLECTED_SOURCES",), ("ENTITY_RESOLUTION", "COLLISION_REVIEW"),
        dependencies=("IDN-002",), criticality="HIGH", freshness_days=1,
        human_review_if_found=True,
        not_implying=("Автоматическое объединение кандидатов",),
    ),
    CheckDefinition(
        "SRC-001", "Оценка происхождения и независимости источников", CheckStream.RED_TEAM_SOURCE_QUALITY,
        CheckStage.REVIEW, ScreeningDepth.STANDARD, ALL_KINDS, ALL_SCOPES,
        ("ALL_COLLECTED_SOURCES",), ("PROVENANCE_REVIEW", "SOURCE_INDEPENDENCE"),
        dependencies=("IDN-001",), criticality="HIGH", freshness_days=1,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "SAN-001", "Санкции и ограничительные меры", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.BASIC, ALL_KINDS, ALL_SCOPES,
        ("UN_SANCTIONS", "EU_SANCTIONS", "UK_SANCTIONS", "US_OFAC", "NATIONAL_SANCTIONS"),
        ("SANCTIONS_SCREENING",), dependencies=("IDN-002",), criticality="BLOCKING",
        freshness_days=1, human_review_if_found=True,
        evidence_expectation="Official list entry or explicit scoped NO_HIT with list versions",
        not_implying=("Санкционный статус в иных юрисдикциях", "Уголовная виновность"),
    ),
    CheckDefinition(
        "ADV-001", "Негативные публикации и репутационные сигналы", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, ALL_KINDS, ALL_SCOPES,
        ("OFFICIAL_NOTICES", "REPUTABLE_MEDIA", "INVESTIGATIVE_MEDIA", "WEB_ARCHIVES"),
        ("ADVERSE_MEDIA_SEARCH", "NARRATIVE_SEPARATION"), dependencies=("IDN-002",),
        criticality="MEDIUM", freshness_days=30, human_review_if_found=True,
        not_implying=("Истинность обвинений из публикации",),
    ),
    CheckDefinition(
        "RED-001", "Контраргументы, противоречия и альтернативные объяснения", CheckStream.RED_TEAM_SOURCE_QUALITY,
        CheckStage.REVIEW, ScreeningDepth.STANDARD, ALL_KINDS, ALL_SCOPES,
        ("ALL_COLLECTED_SOURCES",), ("COUNTER_EVIDENCE", "CONTRADICTION_REGISTER"),
        dependencies=("SRC-001",), criticality="HIGH", freshness_days=1,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "RED-002", "Финальная проверка недопустимого расширения выводов", CheckStream.RED_TEAM_SOURCE_QUALITY,
        CheckStage.REVIEW, ScreeningDepth.BASIC, ALL_KINDS, ALL_SCOPES,
        ("FINDINGS", "REPORT_DRAFT"), ("OVERCLAIM_REVIEW", "FACT_GATE"),
        dependencies=("IDN-003",), criticality="BLOCKING", freshness_days=1,
        human_review_if_found=True,
    ),

    # Russian legal entity.
    CheckDefinition(
        "RU-LE-001", "ЕГРЮЛ: регистрация, статус и реквизиты", CheckStream.IDENTITY_REGISTRY,
        CheckStage.IDENTIFY, ScreeningDepth.BASIC, LEGAL, RU,
        ("RU_FNS_EGRUL",), ("COMPANY_REGISTRY_LOOKUP",),
        required_identifiers_any=("inn", "ogrn", "name_region"), dependencies=("IDN-002",),
        criticality="BLOCKING", freshness_days=7,
    ),
    CheckDefinition(
        "RU-LE-002", "История наименований, адресов и регистрационных изменений", CheckStream.IDENTITY_REGISTRY,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, LEGAL, RU,
        ("RU_FNS_EGRUL_HISTORY", "RU_FEDRESURS"), ("COMPANY_HISTORY",),
        dependencies=("RU-LE-001",), criticality="HIGH", freshness_days=30,
    ),
    CheckDefinition(
        "RU-LE-003", "Руководители, участники и кандидаты фактического контроля", CheckStream.IDENTITY_REGISTRY,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, LEGAL, RU,
        ("RU_FNS_EGRUL", "RU_OFFICIAL_DISCLOSURES"), ("OFFICER_OWNERSHIP_EXTRACTION",),
        dependencies=("RU-LE-001",), criticality="HIGH", freshness_days=30,
        human_review_if_found=True,
        not_implying=("Фактический контроль только по совпадению адреса или телефона",),
    ),
    CheckDefinition(
        "RU-LE-004", "Связанные организации по идентификаторам и ролям", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.EXPAND, ScreeningDepth.ENHANCED, LEGAL, RU,
        ("RU_FNS_EGRUL", "RU_FEDRESURS", "COLLECTED_DOCUMENTS"),
        ("CORPORATE_LINK_EXPANSION", "COMMON_IDENTIFIER_SEARCH"),
        dependencies=("RU-LE-003",), criticality="MEDIUM", freshness_days=30,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "RU-LE-005", "Бухгалтерская отчётность и финансовые индикаторы", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, LEGAL, RU,
        ("RU_GIR_BO", "RU_OFFICIAL_DISCLOSURES"), ("FINANCIAL_STATEMENT_REVIEW",),
        dependencies=("RU-LE-001",), freshness_days=120,
    ),
    CheckDefinition(
        "RU-LE-006", "Банкротство и существенные сообщения", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.BASIC, LEGAL, RU,
        ("RU_FEDRESURS", "RU_BANKRUPTCY_REGISTER"), ("INSOLVENCY_SCREENING",),
        dependencies=("RU-LE-001",), criticality="HIGH", freshness_days=7,
    ),
    CheckDefinition(
        "RU-LE-007", "Арбитражные и иные судебные споры", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, LEGAL, RU,
        ("RU_ARBITRATION_CASES", "RU_COURT_PORTALS"), ("LITIGATION_SCREENING",),
        dependencies=("RU-LE-001",), criticality="HIGH", freshness_days=14,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "RU-LE-008", "Исполнительные производства и регуляторные ограничения", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.ENHANCED, LEGAL, RU,
        ("RU_FSSP", "RU_REGULATOR_NOTICES"), ("ENFORCEMENT_SCREENING",),
        dependencies=("RU-LE-001",), criticality="HIGH", freshness_days=14,
    ),
    CheckDefinition(
        "RU-LE-009", "Государственные закупки, контракты и исключения", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, LEGAL, RU,
        ("RU_EIS_PROCUREMENT", "RU_SUPPLIER_EXCLUSIONS"), ("PROCUREMENT_SCREENING",),
        dependencies=("RU-LE-001",), freshness_days=30,
    ),
    CheckDefinition(
        "RU-LE-010", "Лицензии, разрешения, товарные знаки и патенты", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.ENHANCED, LEGAL, RU,
        ("RU_LICENSE_REGISTRIES", "RU_ROSPATENT"), ("LICENSE_IP_SCREENING",),
        dependencies=("RU-LE-001",), freshness_days=90,
    ),
    CheckDefinition(
        "RU-LE-011", "Домены, DNS, сертификаты и история сайта", CheckStream.DIGITAL_FOOTPRINT,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, LEGAL, RU,
        ("PUBLIC_DNS", "RDAP_WHOIS", "CERTIFICATE_TRANSPARENCY", "WEB_ARCHIVES"),
        ("PASSIVE_DOMAIN_OSINT", "WEB_ARCHIVE_REVIEW"), dependencies=("RU-LE-001",),
        freshness_days=30,
        not_implying=("Принадлежность домена без дополнительной связи",),
    ),
    CheckDefinition(
        "RU-LE-012", "Фактическое присутствие, адрес и инфраструктура", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.DEEP, LEGAL, RU,
        ("OFFICIAL_ADDRESSES", "PUBLIC_MAPS", "PROCUREMENT_DOCUMENTS", "PROPERTY_PUBLIC_RECORDS"),
        ("OPERATIONAL_PRESENCE_REVIEW", "GEOINT"), dependencies=("RU-LE-002",),
        criticality="MEDIUM", freshness_days=90, human_review_if_found=True,
        not_implying=("Фактическая деятельность только по юридическому адресу",),
    ),

    # Foreign legal entity.
    CheckDefinition(
        "FOR-LE-001", "Национальный реестр: регистрация, статус и номер", CheckStream.IDENTITY_REGISTRY,
        CheckStage.IDENTIFY, ScreeningDepth.BASIC, LEGAL, FOREIGN,
        ("NATIONAL_COMPANY_REGISTER", "BRIS_OR_EQUIVALENT"), ("COMPANY_REGISTRY_LOOKUP",),
        required_identifiers_any=("registration_number", "tax_id", "name_country"),
        dependencies=("IDN-002",), criticality="BLOCKING", freshness_days=7,
    ),
    CheckDefinition(
        "FOR-LE-002", "История наименований, адресов и статусов", CheckStream.IDENTITY_REGISTRY,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, LEGAL, FOREIGN,
        ("NATIONAL_COMPANY_REGISTER_HISTORY", "OFFICIAL_GAZETTE"), ("COMPANY_HISTORY",),
        dependencies=("FOR-LE-001",), criticality="HIGH", freshness_days=30,
    ),
    CheckDefinition(
        "FOR-LE-003", "Директора, участники и UBO-кандидаты", CheckStream.IDENTITY_REGISTRY,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, LEGAL, FOREIGN,
        ("NATIONAL_COMPANY_REGISTER", "UBO_REGISTER_WHERE_LAWFUL", "SECURITIES_FILINGS"),
        ("OFFICER_OWNERSHIP_EXTRACTION",), dependencies=("FOR-LE-001",),
        criticality="HIGH", freshness_days=30, human_review_if_found=True,
        not_implying=("Фактический контроль без прямого подтверждения",),
    ),
    CheckDefinition(
        "FOR-LE-004", "Группа компаний и трансграничные связи", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.EXPAND, ScreeningDepth.ENHANCED, LEGAL, FOREIGN,
        ("NATIONAL_REGISTERS", "SECURITIES_FILINGS", "OFFICIAL_DISCLOSURES"),
        ("CORPORATE_LINK_EXPANSION", "CROSS_BORDER_ENTITY_RESOLUTION"),
        dependencies=("FOR-LE-003",), freshness_days=30, human_review_if_found=True,
    ),
    CheckDefinition(
        "FOR-LE-005", "Финансовая отчётность и платёжеспособность", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, LEGAL, FOREIGN,
        ("OFFICIAL_FINANCIAL_FILINGS", "SECURITIES_REGULATOR"), ("FINANCIAL_STATEMENT_REVIEW",),
        dependencies=("FOR-LE-001",), freshness_days=120,
    ),
    CheckDefinition(
        "FOR-LE-006", "Несостоятельность, ликвидация и реорганизация", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.BASIC, LEGAL, FOREIGN,
        ("NATIONAL_INSOLVENCY_REGISTER", "OFFICIAL_GAZETTE"), ("INSOLVENCY_SCREENING",),
        dependencies=("FOR-LE-001",), criticality="HIGH", freshness_days=7,
    ),
    CheckDefinition(
        "FOR-LE-007", "Суды, регуляторы и принудительные меры", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, LEGAL, FOREIGN,
        ("NATIONAL_COURTS", "REGULATOR_ENFORCEMENT", "SECURITIES_REGULATOR"),
        ("LITIGATION_SCREENING", "ENFORCEMENT_SCREENING"), dependencies=("FOR-LE-001",),
        criticality="HIGH", freshness_days=14, human_review_if_found=True,
    ),
    CheckDefinition(
        "FOR-LE-008", "Закупочные исключения и международная дебарментация", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, LEGAL, FOREIGN,
        ("NATIONAL_DEBARMENT", "WORLD_BANK_DEBARRED", "MDB_DEBARMENT"),
        ("DEBARMENT_SCREENING",), dependencies=("FOR-LE-001",), criticality="HIGH", freshness_days=7,
    ),
    CheckDefinition(
        "FOR-LE-009", "Налоговый/VAT-статус и лицензии", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.ENHANCED, LEGAL, FOREIGN,
        ("NATIONAL_TAX_STATUS", "EU_VIES_WHERE_APPLICABLE", "NATIONAL_LICENSES"),
        ("TAX_LICENSE_SCREENING",), dependencies=("FOR-LE-001",), freshness_days=30,
    ),
    CheckDefinition(
        "FOR-LE-010", "Домены, сертификаты, архивы и публичная инфраструктура", CheckStream.DIGITAL_FOOTPRINT,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, LEGAL, FOREIGN,
        ("PUBLIC_DNS", "RDAP_WHOIS", "CERTIFICATE_TRANSPARENCY", "WEB_ARCHIVES"),
        ("PASSIVE_DOMAIN_OSINT", "WEB_ARCHIVE_REVIEW"), dependencies=("FOR-LE-001",), freshness_days=30,
    ),
    CheckDefinition(
        "FOR-LE-011", "Фактическое присутствие и операционная география", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.ASSESS, ScreeningDepth.DEEP, LEGAL, FOREIGN,
        ("OFFICIAL_ADDRESSES", "PUBLIC_MAPS", "CUSTOMS_LOGISTICS_PUBLIC", "PROPERTY_PUBLIC_RECORDS"),
        ("OPERATIONAL_PRESENCE_REVIEW", "GEOINT"), dependencies=("FOR-LE-002",),
        freshness_days=90, human_review_if_found=True,
    ),

    # Russian person.
    CheckDefinition(
        "RU-PER-001", "Идентификация физического лица и разведение тёзок", CheckStream.IDENTITY_REGISTRY,
        CheckStage.IDENTIFY, ScreeningDepth.BASIC, PERSON, RU,
        ("SUBJECT_INPUT", "OFFICIAL_IDENTITY_ANCHORS_WHERE_LAWFUL"),
        ("PERSON_ENTITY_RESOLUTION",), required_identifiers_any=("dob", "inn", "snils_masked", "name_region"),
        dependencies=("IDN-002",), criticality="BLOCKING", freshness_days=30, human_review_if_found=True,
    ),
    CheckDefinition(
        "RU-PER-002", "ИП, самозанятость и корпоративные роли", CheckStream.IDENTITY_REGISTRY,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, PERSON, RU,
        ("RU_FNS_EGRIP", "RU_FNS_EGRUL", "OFFICIAL_DISCLOSURES"),
        ("PERSON_CORPORATE_ROLES",), dependencies=("RU-PER-001",), freshness_days=30,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "RU-PER-003", "Банкротство и исполнительные производства", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, PERSON, RU,
        ("RU_FEDRESURS", "RU_FSSP"), ("PERSON_INSOLVENCY_ENFORCEMENT",),
        dependencies=("RU-PER-001",), criticality="HIGH", freshness_days=14,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "RU-PER-004", "Суды, профессиональные и регуляторные решения", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.ENHANCED, PERSON, RU,
        ("RU_COURT_PORTALS", "PROFESSIONAL_REGISTERS", "REGULATOR_NOTICES"),
        ("PERSON_LITIGATION_REGULATORY",), dependencies=("RU-PER-001",),
        criticality="HIGH", freshness_days=30, human_review_if_found=True,
        not_implying=("Виновность без вступившего в силу решения и точной идентификации",),
    ),
    CheckDefinition(
        "RU-PER-005", "Публичные аккаунты и цифровой след", CheckStream.DIGITAL_FOOTPRINT,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, PERSON, RU,
        ("PUBLIC_SOCIAL_PROFILES", "PUBLIC_WEB", "WEB_ARCHIVES"),
        ("USERNAME_SEARCH", "PUBLIC_PROFILE_REVIEW"), dependencies=("RU-PER-001",), freshness_days=30,
        human_review_if_found=True,
        not_implying=("Принадлежность найденного аккаунта только по совпадению username",),
    ),
    CheckDefinition(
        "RU-PER-006", "Деловые связи и материально значимые аффилиации", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.EXPAND, ScreeningDepth.ENHANCED, PERSON, RU,
        ("CORPORATE_REGISTERS", "PROCUREMENT_DOCUMENTS", "OFFICIAL_DISCLOSURES"),
        ("PERSON_BUSINESS_NETWORK",), dependencies=("RU-PER-002",), freshness_days=90,
        human_review_if_found=True,
        not_implying=("Родство, контроль или сговор без прямого доказательства",),
    ),

    # Foreign person.
    CheckDefinition(
        "FOR-PER-001", "Идентификация, даты, гражданство и транслитерации", CheckStream.IDENTITY_REGISTRY,
        CheckStage.IDENTIFY, ScreeningDepth.BASIC, PERSON, FOREIGN,
        ("SUBJECT_INPUT", "NATIONAL_PUBLIC_IDENTITY_ANCHORS"),
        ("PERSON_ENTITY_RESOLUTION", "MULTILINGUAL_NAME_EXPANSION"),
        required_identifiers_any=("dob", "national_id_masked", "passport_masked", "name_country"),
        dependencies=("IDN-002",), criticality="BLOCKING", freshness_days=30,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "FOR-PER-002", "Корпоративные роли и предпринимательская деятельность", CheckStream.IDENTITY_REGISTRY,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, PERSON, FOREIGN,
        ("NATIONAL_COMPANY_REGISTERS", "SECURITIES_FILINGS", "OFFICIAL_GAZETTES"),
        ("PERSON_CORPORATE_ROLES",), dependencies=("FOR-PER-001",), freshness_days=30,
        human_review_if_found=True,
    ),
    CheckDefinition(
        "FOR-PER-003", "PEP и публичные должности", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.STANDARD, PERSON, FOREIGN,
        ("OFFICIAL_GOVERNMENT_ROSTERS", "NATIONAL_PEP_SOURCES", "REPUTABLE_AGGREGATORS_AS_LEADS"),
        ("PEP_SCREENING",), dependencies=("FOR-PER-001",), criticality="HIGH", freshness_days=7,
        human_review_if_found=True,
        not_implying=("Нарушение закона только из-за статуса PEP",),
    ),
    CheckDefinition(
        "FOR-PER-004", "Суды, несостоятельность и регуляторные решения", CheckStream.LEGAL_SANCTIONS_ADVERSE,
        CheckStage.ASSESS, ScreeningDepth.ENHANCED, PERSON, FOREIGN,
        ("NATIONAL_COURTS", "NATIONAL_INSOLVENCY", "REGULATOR_ENFORCEMENT"),
        ("PERSON_LITIGATION_REGULATORY",), dependencies=("FOR-PER-001",),
        criticality="HIGH", freshness_days=30, human_review_if_found=True,
        not_implying=("Виновность без точной идентификации и процессуального статуса",),
    ),
    CheckDefinition(
        "FOR-PER-005", "Публичные аккаунты, username и цифровой след", CheckStream.DIGITAL_FOOTPRINT,
        CheckStage.EXPAND, ScreeningDepth.STANDARD, PERSON, FOREIGN,
        ("PUBLIC_SOCIAL_PROFILES", "PUBLIC_WEB", "WEB_ARCHIVES"),
        ("USERNAME_SEARCH", "PUBLIC_PROFILE_REVIEW"), dependencies=("FOR-PER-001",), freshness_days=30,
        human_review_if_found=True,
        not_implying=("Принадлежность аккаунта только по совпадению имени или username",),
    ),
    CheckDefinition(
        "FOR-PER-006", "Трансграничные деловые связи", CheckStream.BUSINESS_FINANCIAL,
        CheckStage.EXPAND, ScreeningDepth.ENHANCED, PERSON, FOREIGN,
        ("NATIONAL_COMPANY_REGISTERS", "PROCUREMENT", "SECURITIES_FILINGS"),
        ("PERSON_BUSINESS_NETWORK", "CROSS_BORDER_ENTITY_RESOLUTION"),
        dependencies=("FOR-PER-002",), freshness_days=90, human_review_if_found=True,
    ),
)

CHECK_BY_CODE = {item.code: item for item in CHECKS}

COMMON_CODES = (
    "ADM-001", "IDN-001", "IDN-002", "SAN-001", "ADV-001", "SRC-001", "IDN-003", "RED-001", "RED-002",
)

PROFILES: dict[str, ScreeningProfile] = {
    "RU_LEGAL_ENTITY": ScreeningProfile(
        "RU_LEGAL_ENTITY", "Юридическое лицо — Россия", SubjectKind.LEGAL_ENTITY, JurisdictionScope.RUSSIA,
        ("RU_OFFICIAL_CORE", "GLOBAL_SANCTIONS_OFFICIAL", "PUBLIC_DIGITAL_PASSIVE"),
        COMMON_CODES + tuple(f"RU-LE-{n:03d}" for n in range(1, 13)),
    ),
    "FOREIGN_LEGAL_ENTITY": ScreeningProfile(
        "FOREIGN_LEGAL_ENTITY", "Юридическое лицо — зарубежная юрисдикция", SubjectKind.LEGAL_ENTITY, JurisdictionScope.FOREIGN,
        ("FOREIGN_NATIONAL_CORE", "GLOBAL_SANCTIONS_OFFICIAL", "MDB_DEBARMENT", "PUBLIC_DIGITAL_PASSIVE"),
        COMMON_CODES + tuple(f"FOR-LE-{n:03d}" for n in range(1, 12)),
    ),
    "RU_PERSON": ScreeningProfile(
        "RU_PERSON", "Физическое лицо — Россия", SubjectKind.PERSON, JurisdictionScope.RUSSIA,
        ("RU_PERSON_OFFICIAL", "GLOBAL_SANCTIONS_OFFICIAL", "PUBLIC_IDENTITY_PASSIVE"),
        COMMON_CODES + tuple(f"RU-PER-{n:03d}" for n in range(1, 7)),
    ),
    "FOREIGN_PERSON": ScreeningProfile(
        "FOREIGN_PERSON", "Физическое лицо — зарубежная юрисдикция", SubjectKind.PERSON, JurisdictionScope.FOREIGN,
        ("FOREIGN_PERSON_NATIONAL", "GLOBAL_SANCTIONS_OFFICIAL", "PUBLIC_IDENTITY_PASSIVE"),
        COMMON_CODES + tuple(f"FOR-PER-{n:03d}" for n in range(1, 7)),
    ),
}


def profile_for(kind: SubjectKind, scope: JurisdictionScope) -> ScreeningProfile:
    key = {
        (SubjectKind.LEGAL_ENTITY, JurisdictionScope.RUSSIA): "RU_LEGAL_ENTITY",
        (SubjectKind.LEGAL_ENTITY, JurisdictionScope.FOREIGN): "FOREIGN_LEGAL_ENTITY",
        (SubjectKind.PERSON, JurisdictionScope.RUSSIA): "RU_PERSON",
        (SubjectKind.PERSON, JurisdictionScope.FOREIGN): "FOREIGN_PERSON",
    }[(kind, scope)]
    return PROFILES[key]


def checks_for_profile(profile: ScreeningProfile) -> list[CheckDefinition]:
    return [CHECK_BY_CODE[code] for code in profile.check_codes]


def validate_profiles() -> None:
    required_streams = set(CheckStream)
    for profile in PROFILES.values():
        definitions = checks_for_profile(profile)
        missing_codes = [code for code in profile.check_codes if code not in CHECK_BY_CODE]
        if missing_codes:
            raise ValueError(f"{profile.profile_id}: missing check definitions {missing_codes}")
        actual_streams = {item.stream for item in definitions}
        if not required_streams.issubset(actual_streams):
            raise ValueError(f"{profile.profile_id}: does not cover all five streams")


def iter_profiles() -> Iterable[ScreeningProfile]:
    return PROFILES.values()
