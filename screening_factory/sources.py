from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SourceDescriptor:
    source_id: str
    title: str
    jurisdiction: str
    source_family: str
    authority_tier: str
    canonical_url: str
    subject_kinds: tuple[str, ...]
    access_mode: str
    freshness_policy: str
    usage_note: str
    discovery_only: bool = False


SOURCES: tuple[SourceDescriptor, ...] = (
    SourceDescriptor(
        "RU-FNS-EGRUL", "ФНС: ЕГРЮЛ/ЕГРИП", "RU", "RU_FNS_EGRUL", "PRIMARY_OFFICIAL",
        "https://egrul.nalog.ru/", ("LEGAL_ENTITY", "PERSON"), "WEB/DOWNLOAD",
        "Capture query time and extract date",
        "Use exact identifiers where available; a registry role does not by itself prove actual control.",
    ),
    SourceDescriptor(
        "RU-FNS-GIRBO", "ФНС: ГИР бухгалтерской отчётности", "RU", "RU_GIR_BO", "PRIMARY_OFFICIAL",
        "https://bo.nalog.ru/", ("LEGAL_ENTITY",), "WEB/DOWNLOAD",
        "Record reporting period and filing revision",
        "Financial statements require contextual analysis; do not convert a ratio into a legal conclusion.",
    ),
    SourceDescriptor(
        "RU-FEDRESURS", "Федресурс", "RU", "RU_FEDRESURS", "PRIMARY_LEGALLY_SIGNIFICANT",
        "https://fedresurs.ru/", ("LEGAL_ENTITY", "PERSON"), "WEB",
        "Capture publication and effective dates separately",
        "Verify the message type, publisher and relation to the screened subject.",
    ),
    SourceDescriptor(
        "RU-KAD", "Картотека арбитражных дел", "RU", "RU_ARBITRATION_CASES", "PRIMARY_COURT_PORTAL",
        "https://kad.arbitr.ru/", ("LEGAL_ENTITY", "PERSON"), "WEB",
        "Record case card, document date and procedural status",
        "Being a party to a case does not imply wrongdoing; distinguish claimant, respondent and third party.",
    ),
    SourceDescriptor(
        "RU-FSSP", "ФССП: банк данных исполнительных производств", "RU", "RU_FSSP", "PRIMARY_OFFICIAL",
        "https://fssp.gov.ru/iss/ip/", ("LEGAL_ENTITY", "PERSON"), "WEB",
        "Short freshness window; capture exact query parameters",
        "Exact identity matching is mandatory, especially for individuals.",
    ),
    SourceDescriptor(
        "RU-EIS", "Единая информационная система в сфере закупок", "RU", "RU_EIS_PROCUREMENT", "PRIMARY_OFFICIAL",
        "https://zakupki.gov.ru/", ("LEGAL_ENTITY", "PERSON"), "WEB/DOWNLOAD",
        "Record contract and notice versions",
        "A contract, bid or exclusion must be tied to the exact registration identifier.",
    ),
    SourceDescriptor(
        "RU-CBR-WARNING", "Банк России: список компаний с выявленными признаками нелегальной деятельности", "RU",
        "RU_REGULATOR_NOTICES", "PRIMARY_REGULATOR", "https://www.cbr.ru/inside/warning-list/",
        ("LEGAL_ENTITY", "PERSON"), "WEB/DOWNLOAD", "Check list version and update date",
        "Use the regulator's exact wording; do not broaden the listed sign or legal status.",
    ),
    SourceDescriptor(
        "UN-CONSOLIDATED", "UN Security Council Consolidated List", "GLOBAL", "UN_SANCTIONS", "PRIMARY_OFFICIAL",
        "https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list",
        ("LEGAL_ENTITY", "PERSON"), "HTML/XML/PDF", "Capture list version and last-updated date",
        "Check aliases, DOB, nationality, identifiers and the specific sanctions regime.",
    ),
    SourceDescriptor(
        "US-OFAC", "OFAC Sanctions List Search", "US", "US_OFAC", "PRIMARY_OFFICIAL",
        "https://sanctionssearch.ofac.treas.gov/", ("LEGAL_ENTITY", "PERSON"), "WEB/DOWNLOAD",
        "Capture list versions and query threshold",
        "Approximate-name matches are candidates only and require identifier-based review.",
    ),
    SourceDescriptor(
        "UK-SANCTIONS", "The UK Sanctions List", "GB", "UK_SANCTIONS", "PRIMARY_OFFICIAL",
        "https://www.gov.uk/government/publications/the-uk-sanctions-list",
        ("LEGAL_ENTITY", "PERSON"), "HTML/XML/CSV/PDF", "Capture update date and designation version",
        "The UK list is jurisdiction-specific; do not describe a UK-only designation as global.",
    ),
    SourceDescriptor(
        "EU-FIN-SANCTIONS", "EU consolidated financial sanctions dataset", "EU", "EU_SANCTIONS", "PRIMARY_OFFICIAL",
        "https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions",
        ("LEGAL_ENTITY", "PERSON"), "DATASET", "Capture dataset revision and legal-act references",
        "Confirm the applicable EU legal act and identifiers for every candidate match.",
    ),
    SourceDescriptor(
        "EU-BRIS", "EU e-Justice Business Registers Interconnection System", "EU", "BRIS_OR_EQUIVALENT",
        "PRIMARY_OFFICIAL_GATEWAY",
        "https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-search-company-eu_en",
        ("LEGAL_ENTITY",), "WEB", "Record national-register source and extraction time",
        "BRIS is a gateway; preserve the national register provenance for each result.",
    ),
    SourceDescriptor(
        "EU-VIES", "European Commission VIES VAT validation", "EU", "EU_VIES_WHERE_APPLICABLE",
        "PRIMARY_OFFICIAL", "https://ec.europa.eu/taxation_customs/vies/", ("LEGAL_ENTITY",), "WEB/SERVICE",
        "Capture member state, VAT number and query timestamp",
        "A valid VAT number does not prove operational substance, ownership or solvency.",
    ),
    SourceDescriptor(
        "UK-COMPANIES-HOUSE", "Companies House register", "GB", "NATIONAL_COMPANY_REGISTER",
        "PRIMARY_OFFICIAL", "https://find-and-update.company-information.service.gov.uk/",
        ("LEGAL_ENTITY", "PERSON"), "WEB/API", "Capture filing date and document image/hash",
        "Companies House notes that it does not verify the accuracy of filed information; retain that limitation.",
    ),
    SourceDescriptor(
        "US-SEC-EDGAR", "SEC EDGAR", "US", "SECURITIES_FILINGS", "PRIMARY_OFFICIAL",
        "https://www.sec.gov/edgar/search/", ("LEGAL_ENTITY", "PERSON"), "WEB/API",
        "Record filing accession number and filing date",
        "A filing is a source document; distinguish issuer statements from regulator findings.",
    ),
    SourceDescriptor(
        "WB-DEBARRED", "World Bank Listing of Ineligible Firms and Individuals", "GLOBAL",
        "WORLD_BANK_DEBARRED", "PRIMARY_INSTITUTIONAL",
        "https://www.worldbank.org/en/projects-operations/procurement/debarred-firms",
        ("LEGAL_ENTITY", "PERSON"), "WEB/DOWNLOAD", "Capture list date and ineligibility period",
        "Debarment scope and cross-debarment status must be reported exactly.",
    ),
)

SOURCE_BY_ID = {source.source_id: source for source in SOURCES}


def sources_for_family(family: str) -> list[SourceDescriptor]:
    return [source for source in SOURCES if source.source_family == family]


def iter_sources() -> Iterable[SourceDescriptor]:
    return SOURCES
