from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import process_programming_kb_sources as source_tools  # noqa: E402
from father_osint.knowledge_analyst import DeterministicKnowledgeAnalyst  # noqa: E402
from father_osint.models import Material, MaterialPackage  # noqa: E402

LOCAL_ROOT = ROOT / "_LOCAL_DOWNLOADS_KB_INTAKE"
ITEM_ROOT = LOCAL_ROOT / "items"
QUEUE_ROOT = LOCAL_ROOT / "model_queue"
REPORT_ROOT = ROOT / "reports" / "downloads_intake"
MODEL_POOL = ROOT / "config" / "local_model_semifabricate_pool.json"
MASTER_PLAN = ROOT / "config" / "security_official_master_download_plan.json"

SUPPORTED_TEXT = {".pdf", ".docx", ".odt", ".rtf", ".txt", ".md", ".html", ".htm", ".epub", ".xml", ".json"}
SUPPORTED_MEDIA = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".mkv", ".webm"}
SKIP_EXT = {".crdownload", ".part", ".tmp", ".download"}

OFFICIAL_HOST_HINTS = (
    "publication.pravo.gov.ru", "pravo.gov.ru", "government.ru", "fstec.ru",
    "fsb.ru", "rkn.gov.ru", "roskomnadzor.gov.ru", "protect.gost.ru", "rst.gov.ru",
    "cdnstatic.rg.ru", "rg.ru",
)
A2_HOST_HINTS = ("consultant.ru", "normativ.kontur.ru", "garant.ru", "docs.cntd.ru")
A3_HOST_HINTS = ("habr.com", "infra-tech.ru")

AUTHORITY_MARKERS: list[tuple[str, tuple[str, ...]]] = [
    ("FSTEC", ("фстэк", "fstek")),
    ("FSB", ("фсб россии", "федеральной службы безопасности")),
    ("ROSKOMNADZOR", ("роскомнадзор", "федеральной службы по надзору в сфере связи")),
    ("ROSSTANDART_GOST", ("росстандарт", "ростехрегулирован", "госстандарт")),
    ("GOVERNMENT", ("постановление правительства", "правительства российской федерации")),
    ("MINZDRAV", ("минздрав", "министерства здравоохранения")),
    ("MINTRANS", ("минтранс", "министерства транспорта")),
    ("MINPROMTORG", ("минпромторг", "министерства промышленности и торговли")),
    ("MINEKONOM", ("минэкономразвит", "министерства экономического развития")),
    ("MINENERGO", ("минэнерго", "министерства энергетики")),
    ("SFR", ("социального фонда россии", "сфр")),
    ("ROSFMON", ("росфинмониторинг", "федеральной службы по финансовому мониторингу")),
]

DOMAIN_MARKERS: list[tuple[str, tuple[str, ...]]] = [
    ("PDN", ("персональн", "пдн", "152-фз", "152 фз")),
    ("KII", ("критическ", "кии", "187-фз", "187 фз", "значимых объектов")),
    ("GIS", ("государственн информационн систем", "гис", "защищенном исполнении")),
    ("SECURE_SDLC", ("безопасн программ", "secure software", "статическ анализ", "фаззинг", "сборочн сред")),
    ("INCIDENTS", ("инцидент", "госсопка", "компьютерн атак", "реагирован")),
    ("THREAT_MODEL", ("модель угроз", "угроз безопасност", "поверхност атаки")),
    ("CRYPTO", ("криптограф", "скзи", "шифровальн")),
    ("RISK", ("риск информацион", "оценк риска", "менеджмент риска")),
    ("ARCHITECTURE", ("архитектур", "проектирован")),
    ("PROGRAMMING", ("python", "программирован", "разработчик", "software engineering")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-zА-Яа-яЁё._+-]+", "_", value).strip("._")
    return value[:120] or "item"


def resolve_downloads(explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env = os.getenv("FATHER_DOWNLOADS_DIR")
    if env:
        candidates.append(Path(env).expanduser())
    home = Path.home()
    candidates.extend([home / "Downloads", home / "Загрузки"])
    for path in candidates:
        if path.is_dir():
            return path.resolve()
    raise SystemExit("Downloads folder not found. Pass --downloads or set FATHER_DOWNLOADS_DIR.")


def extract_rtf(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    raw = re.sub(r"\\'[0-9a-fA-F]{2}", " ", raw)
    raw = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", raw)
    raw = raw.replace("{", " ").replace("}", " ")
    return " ".join(raw.split()), "BASIC_RTF_TEXT"


def extract_odt(path: Path) -> tuple[str, str]:
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(path) as zf:
        data = zf.read("content.xml")
    root = ET.fromstring(data)
    parts: list[str] = []
    for node in root.iter():
        if node.text and node.text.strip():
            parts.append(node.text.strip())
    return "\n".join(parts), "STDLIB_ODT_XML"


def extract_xml_json(path: Path) -> tuple[str, str]:
    return path.read_text(encoding="utf-8", errors="ignore"), "STDLIB_STRUCTURED_TEXT"


def extract_text(path: Path) -> tuple[str | None, str]:
    ext = path.suffix.lower()
    try:
        if ext == ".rtf":
            return extract_rtf(path)
        if ext == ".odt":
            return extract_odt(path)
        if ext in {".xml", ".json"}:
            return extract_xml_json(path)
        if ext in SUPPORTED_TEXT:
            text, method = source_tools.extract_text(path)
            return text, method
    except Exception as exc:
        return None, f"EXTRACT_FAILED:{type(exc).__name__}:{exc}"
    return None, "NO_TEXT_ADAPTER"


def classify_document_type(name: str, text: str, ext: str) -> str:
    s = (name + "\n" + text[:100000]).casefold()
    if re.search(r"\bгост\b|национальн(?:ый|ого) стандарт", s):
        return "STANDARD"
    if "федеральный закон" in s or re.search(r"\b\d+-фз\b", s):
        return "FEDERAL_LAW"
    if "постановление правительства" in s:
        return "GOVERNMENT_DECREE"
    if "указ президента" in s:
        return "PRESIDENTIAL_DECREE"
    if "приказ" in s:
        return "ORDER"
    if "методическ" in s or "руководящий документ" in s:
        return "METHODOLOGY"
    if "перечень" in s and (s.count("гост") >= 5 or s.count("приказ") >= 5):
        return "CATALOG"
    if ext == ".epub":
        return "BOOK"
    if ext in {".html", ".htm"}:
        return "WEB_SNAPSHOT"
    if ext in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}:
        return "IMAGE"
    if ext in {".mp3", ".wav", ".ogg", ".m4a"}:
        return "AUDIO"
    if ext in {".mp4", ".mkv", ".webm"}:
        return "VIDEO"
    return "DOCUMENT"


def classify_authority(name: str, text: str, doc_type: str) -> str:
    s = (name + "\n" + text[:120000]).casefold()
    for authority, markers in AUTHORITY_MARKERS:
        if any(marker in s for marker in markers):
            return authority
    if doc_type == "FEDERAL_LAW":
        return "FEDERAL_LAWS"
    if doc_type == "STANDARD":
        return "ROSSTANDART_GOST"
    return "OTHER_AUTHORITY"


def classify_domains(name: str, text: str) -> list[str]:
    s = (name + "\n" + text[:180000]).casefold()
    domains = [domain for domain, markers in DOMAIN_MARKERS if any(marker in s for marker in markers)]
    return domains or ["GENERAL_SECURITY"]


def extract_identifiers(text: str, name: str) -> list[str]:
    s = name + "\n" + text[:250000]
    values: set[str] = set()
    patterns = [
        r"ГОСТ\s+Р(?:\s+ИСО/МЭК|\s+ИСО/МЭК\s+ТО|\s+О)?\s*[0-9A-Za-zА-Яа-я./-]+-\d{2,4}",
        r"ГОСТ\s+[0-9A-Za-zА-Яа-я./-]+-\d{2,4}",
        r"№\s*\d+[А-Яа-я]?(?:/\d+)?(?:-ФЗ)?",
        r"\b\d+-ФЗ\b",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, s, flags=re.IGNORECASE):
            value = " ".join(str(match).split())
            if 2 <= len(value) <= 100:
                values.add(value)
    return sorted(values)


def find_sidecar_url(path: Path) -> str | None:
    for candidate in (
        path.with_suffix(path.suffix + ".source.txt"),
        path.with_name(path.stem + ".source.txt"),
    ):
        if candidate.is_file():
            value = candidate.read_text(encoding="utf-8", errors="ignore").strip()
            if value:
                return value.splitlines()[0].strip()
    return None


def trust_tier(url: str | None) -> str:
    value = (url or "").casefold()
    if any(host in value for host in OFFICIAL_HOST_HINTS):
        return "A0_A1_OFFICIAL"
    if any(host in value for host in A2_HOST_HINTS):
        return "A2_TRUSTED_LEGAL_REFERENCE"
    if any(host in value for host in A3_HOST_HINTS):
        return "A3_EXPERT_CATALOG"
    return "UNKNOWN_SOURCE"


def material_source_type(doc_type: str) -> str:
    return {
        "STANDARD": "standard",
        "FEDERAL_LAW": "legal_document",
        "GOVERNMENT_DECREE": "legal_document",
        "PRESIDENTIAL_DECREE": "legal_document",
        "ORDER": "legal_document",
        "METHODOLOGY": "methodology",
        "BOOK": "book",
        "WEB_SNAPSHOT": "web_snapshot",
    }.get(doc_type, "document")


def deterministic_semifabricate(item_dir: Path, *, title: str, text: str, source_path: Path, sha: str, doc_type: str, meta: dict[str, Any]) -> dict[str, Any]:
    material = Material(
        source_type=material_source_type(doc_type),
        source_locator=str(source_path),
        title=title,
        raw_text=text,
        local_path=str(source_path),
        content_hash=sha,
        metadata={"entities": meta.get("identifiers") or [], "candidate": meta.get("authority")},
    )
    package = MaterialPackage(task_id=f"downloads-intake:{sha[:16]}", materials=[material])
    bundle = DeterministicKnowledgeAnalyst().analyze(package)
    out = item_dir / "deterministic_semifabricate.json"
    bundle.write_json(out)
    return {
        "path": out.relative_to(ROOT).as_posix(),
        "counters": bundle.counters,
    }


def load_model_pool() -> list[dict[str, Any]]:
    if not MODEL_POOL.is_file():
        return []
    payload = load_json(MODEL_POOL)
    return [row for row in payload.get("models", []) if isinstance(row, dict)]


def models_for_item(models: list[dict[str, Any]], *, doc_type: str, domains: list[str], ext: str) -> list[str]:
    wanted: set[str] = {"SUMMARY", "APPLICABILITY", "CONTRADICTION_SCOUT", "CROSS_SOURCE_COMPARE"}
    if doc_type in {"FEDERAL_LAW", "GOVERNMENT_DECREE", "ORDER", "STANDARD", "METHODOLOGY"}:
        wanted |= {"LEGAL_STRUCTURE", "DEFINITION_NORMALIZATION", "REQUIREMENT_REWRITE"}
    if any(domain in {"SECURE_SDLC", "PROGRAMMING", "ARCHITECTURE"} for domain in domains):
        wanted |= {"SECURE_SDLC", "ARCHITECTURE", "IMPLEMENTATION_MAPPING", "TEST_DESIGN"}
    if ext in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".pdf"}:
        wanted |= {"SCAN_VISUAL_REVIEW", "TABLE_REVIEW", "DIAGRAM_REVIEW"}
    if ext in {".mp3", ".wav", ".ogg", ".m4a"}:
        wanted |= {"AUDIO_TRANSCRIPTION"}
    if ext in {".mp4", ".mkv", ".webm"}:
        wanted |= {"VIDEO_AUDIO_TRANSCRIPTION"}
    wanted |= {"SEMANTIC_INDEX", "SIMILAR_REQUIREMENT_SEARCH"}

    selected: list[str] = []
    for row in models:
        roles = {str(value) for value in row.get("roles") or []}
        if roles & wanted:
            selected.append(str(row.get("model_id") or ""))
    return [value for value in selected if value]


def make_queue_rows(item: dict[str, Any], models: list[dict[str, Any]]) -> list[dict[str, Any]]:
    assigned = models_for_item(
        models,
        doc_type=str(item["document_type"]),
        domains=list(item["domains"]),
        ext=str(item["extension"]),
    )
    if not assigned:
        return []
    lanes = [
        "STRUCTURE_AND_REQUIREMENTS",
        "APPLICABILITY_AND_CURRENTNESS_QUESTIONS",
        "CROSS_SOURCE_COMPARE",
        "CONTRADICTIONS_AND_EDGE_CASES",
    ]
    if any(domain in {"SECURE_SDLC", "PROGRAMMING", "ARCHITECTURE"} for domain in item["domains"]):
        lanes.append("IMPLEMENTATION_AND_TEST_MAPPING")
    if item["document_type"] in {"IMAGE", "VIDEO"} or item["extension"] == ".pdf":
        lanes.append("VISUAL_REVIEW")

    rows: list[dict[str, Any]] = []
    for lane in lanes:
        rows.append({
            "record_type": "LOCAL_MODEL_SEMIFABRICATE_TASK",
            "task_id": hashlib.sha256(f"{item['sha256']}:{lane}".encode("utf-8")).hexdigest()[:24],
            "source_sha256": item["sha256"],
            "source_item_id": item["item_id"],
            "task_role": lane,
            "assigned_models": assigned,
            "input_metadata": item["metadata_path"],
            "input_text": item.get("extracted_text_path"),
            "deterministic_semifabricate": item.get("deterministic_semifabricate", {}).get("path"),
            "output_dir": f"_LOCAL_DOWNLOADS_KB_INTAKE/model_outputs/{item['item_id']}/{lane}",
            "review_gate": "MAIN_ANALYST_REVIEW_REQUIRED",
            "legal_truth_auto_promotion": False,
            "status": "QUEUED",
        })
    return rows


def scan_files(downloads: Path, recursive: bool) -> list[Path]:
    iterator = downloads.rglob("*") if recursive else downloads.glob("*")
    files: list[Path] = []
    for path in iterator:
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_EXT:
            continue
        if path.name.endswith(".source.txt"):
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory Windows Downloads and build a local knowledge-intake/model queue without modifying originals.")
    parser.add_argument("--downloads", help="Downloads folder; defaults to %%USERPROFILE%%\\Downloads")
    parser.add_argument("--no-recursive", action="store_true", help="Only scan the top level")
    parser.add_argument("--max-files", type=int, default=0, help="Optional safety limit; 0 = all")
    args = parser.parse_args()

    downloads = resolve_downloads(args.downloads)
    files = scan_files(downloads, recursive=not args.no_recursive)
    if args.max_files > 0:
        files = files[: args.max_files]

    ITEM_ROOT.mkdir(parents=True, exist_ok=True)
    QUEUE_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    models = load_model_pool()

    inventory: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    seen_sha: dict[str, str] = {}
    duplicate_total = 0
    catalog_refs: defaultdict[str, set[str]] = defaultdict(set)

    for path in files:
        sha = sha256_file(path)
        if sha in seen_sha:
            duplicate_total += 1
            inventory.append({
                "source_path": str(path),
                "sha256": sha,
                "status": "DUPLICATE_SHA",
                "duplicate_of": seen_sha[sha],
            })
            continue
        seen_sha[sha] = str(path)

        ext = path.suffix.lower()
        text, extractor = extract_text(path)
        normalized = (text or "").replace("\x00", "").strip()
        doc_type = classify_document_type(path.name, normalized, ext)
        authority = classify_authority(path.name, normalized, doc_type)
        domains = classify_domains(path.name, normalized)
        identifiers = extract_identifiers(normalized, path.name)
        source_url = find_sidecar_url(path)
        tier = trust_tier(source_url)
        item_id = f"DL-{sha[:20]}"
        primary_domain = domains[0]
        item_dir = ITEM_ROOT / doc_type / authority / primary_domain / item_id
        item_dir.mkdir(parents=True, exist_ok=True)

        original = item_dir / ("original" + (ext if ext else ".bin"))
        if not original.exists():
            shutil.copy2(path, original)

        extracted_text_path: str | None = None
        if normalized:
            extracted = item_dir / "extracted.txt"
            extracted.write_text(normalized + "\n", encoding="utf-8")
            extracted_text_path = extracted.relative_to(ROOT).as_posix()

        meta: dict[str, Any] = {
            "schema_version": "1.0",
            "record_type": "DOWNLOADS_KB_INTAKE_ITEM",
            "item_id": item_id,
            "source_path": str(path),
            "source_file_name": path.name,
            "extension": ext,
            "byte_length": path.stat().st_size,
            "sha256": sha,
            "extractor": extractor,
            "text_characters": len(normalized),
            "document_type": doc_type,
            "authority": authority,
            "domains": domains,
            "identifiers": identifiers,
            "source_url": source_url,
            "trust_tier": tier,
            "original_copy": original.relative_to(ROOT).as_posix(),
            "extracted_text_path": extracted_text_path,
            "source_original_modified": False,
            "document_identity_confirmed": False,
            "currentness_verified": False,
            "legal_truth_eligible": False,
            "kb_auto_promotion": False,
            "review_status": "INTAKE_REVIEW_REQUIRED",
            "observed_at": utc_now(),
        }

        meta_path = item_dir / "metadata.json"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        item = {**meta, "metadata_path": meta_path.relative_to(ROOT).as_posix()}

        if normalized:
            semi = deterministic_semifabricate(
                item_dir,
                title=path.name,
                text=normalized,
                source_path=path,
                sha=sha,
                doc_type=doc_type,
                meta=meta,
            )
            item["deterministic_semifabricate"] = semi

        if len(identifiers) >= 8 or doc_type == "CATALOG":
            for value in identifiers:
                catalog_refs[sha].add(value)
            item["catalog_reference_count"] = len(identifiers)

        queue_rows.extend(make_queue_rows(item, models))
        inventory.append(item)

    inventory_path = LOCAL_ROOT / "INVENTORY.json"
    inventory_path.write_text(json.dumps({
        "schema_version": "1.0",
        "record_type": "DOWNLOADS_KB_INVENTORY",
        "downloads_root": str(downloads),
        "files_total": len(files),
        "unique_sha_total": len(seen_sha),
        "duplicate_sha_total": duplicate_total,
        "items": inventory,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    queue_path = QUEUE_ROOT / "TASKS.jsonl"
    queue_path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in queue_rows), encoding="utf-8")

    coverage_path = LOCAL_ROOT / "CATALOG_REFERENCES.json"
    coverage_payload = {
        "schema_version": "1.0",
        "record_type": "DOWNLOADS_DISCOVERED_CATALOG_REFERENCES",
        "catalogs_total": len(catalog_refs),
        "references_unique_total": len({ref for refs in catalog_refs.values() for ref in refs}),
        "catalogs": [
            {"source_sha256": sha, "references": sorted(refs), "references_total": len(refs)}
            for sha, refs in sorted(catalog_refs.items())
        ],
    }
    coverage_path.write_text(json.dumps(coverage_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    type_counts = Counter(str(row.get("document_type") or row.get("status") or "UNKNOWN") for row in inventory)
    authority_counts = Counter(str(row.get("authority") or "UNKNOWN") for row in inventory if row.get("authority"))
    domain_counts = Counter(domain for row in inventory for domain in row.get("domains") or [])
    text_ready = sum(bool(row.get("extracted_text_path")) for row in inventory)
    semi_ready = sum(bool(row.get("deterministic_semifabricate")) for row in inventory)

    summary = {
        "schema_version": "1.0",
        "record_type": "DOWNLOADS_KB_INTAKE_RUN",
        "status": "PASS",
        "downloads_root": str(downloads),
        "files_seen_total": len(files),
        "unique_files_total": len(seen_sha),
        "duplicate_sha_total": duplicate_total,
        "text_ready_total": text_ready,
        "deterministic_semifabricates_total": semi_ready,
        "model_tasks_queued_total": len(queue_rows),
        "model_pool_total": len(models),
        "document_type_counts": dict(sorted(type_counts.items())),
        "authority_counts": dict(sorted(authority_counts.items())),
        "domain_counts": dict(sorted(domain_counts.items())),
        "catalogs_detected_total": len(catalog_refs),
        "catalog_references_unique_total": coverage_payload["references_unique_total"],
        "local_root": LOCAL_ROOT.relative_to(ROOT).as_posix(),
        "inventory": inventory_path.relative_to(ROOT).as_posix(),
        "model_queue": queue_path.relative_to(ROOT).as_posix(),
        "catalog_references": coverage_path.relative_to(ROOT).as_posix(),
        "source_originals_modified": False,
        "kb_auto_promotion": False,
        "observed_at": utc_now(),
    }
    summary_path = REPORT_ROOT / "LATEST_DOWNLOADS_KB_INTAKE.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
