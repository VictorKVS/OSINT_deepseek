from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOWNLOADS = Path.home() / "Downloads"
LIBRARY = ROOT / "_LOCAL_DOWNLOADS_KB_INTAKE"
OBJECTS = LIBRARY / "objects"
QUARANTINE = LIBRARY / "quarantine"
MANIFESTS = LIBRARY / "manifests"
REPORT = ROOT / "reports" / "knowledge_intake" / "LATEST_DOWNLOADS_INTAKE.json"
QUEUE = ROOT / "reports" / "knowledge_intake" / "LATEST_MODEL_WORK_QUEUE.json"

SUPPORTED = {
    ".pdf", ".txt", ".md", ".html", ".htm", ".docx", ".odt", ".rtf", ".epub",
    ".json", ".xml", ".csv", ".xlsx", ".pptx", ".doc", ".xls", ".ppt",
}

AUTHORITY_PATTERNS = [
    ("FSTEC", ("фстэк", "fstec")),
    ("FSB", ("фсб", "fsb")),
    ("ROSKOMNADZOR", ("роскомнадзор", "rkn")),
    ("ROSSTANDART_GOST", ("гост", "gost", "росстандарт", "rst.gov")),
    ("GOVERNMENT", ("постановление правительства", "правительство", "government")),
    ("MINZDRAV", ("минздрав", "minzdrav")),
    ("MINTRANS", ("минтранс", "mintrans")),
    ("MINPROMTORG", ("минпромторг", "minpromtorg")),
    ("MINENERGO", ("минэнерго", "minenergo")),
    ("MINEKONOM", ("минэконом", "minekonom")),
    ("ROSMONITORING", ("росфинмонитор", "rosfinmonitor")),
]

DOMAIN_PATTERNS = [
    ("PDN", ("персональн", "пдн", "152-фз", "personal data")),
    ("KII", ("кии", "критическ", "187-фз", "critical information infrastructure")),
    ("GIS", ("государственн информационн систем", "гис", "state information system")),
    ("CRYPTO", ("криптограф", "скзи", "шифров", "cryptograph")),
    ("INCIDENTS", ("инцидент", "госсопка", "computer incident", "incident response")),
    ("SECURE_SDLC", ("безопасн программ", "secure software", "sdlc", "devsecops", "static analysis", "фазз")),
    ("THREAT_MODEL", ("модель угроз", "угроз безопасности", "threat model", "attack surface")),
    ("RISK", ("риск", "risk management", "27005")),
    ("ARCHITECTURE", ("архитектур", "architecture", "system design", "distributed system")),
    ("PROGRAMMING", ("python", "programming", "программирован", "software engineering")),
    ("IAM", ("идентификац", "аутентификац", "управлени доступ", "access control", "identity")),
    ("MONITORING", ("мониторинг информационн безопасност", "siem", "security monitoring")),
]

DOC_KIND_PATTERNS = [
    ("LAW_OR_REGULATION", ("федеральный закон", "постановление правительства", "приказ ", "указ президента")),
    ("STANDARD", ("гост ", "gost ", "iso/iec", "исо/мэк")),
    ("METHODOLOGY", ("методик", "методическ", "руководящий документ", "recommendation")),
    ("BOOK", ("o'reilly", "packt", "manning", "addison-wesley", "pearson", "springer", "press", "издательство")),
    ("ARTICLE", ("habr", "статья", "article")),
    ("PRESENTATION", ("презентац", "slides", "presentation")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sample_text(path: Path, limit: int = 200_000) -> str:
    ext = path.suffix.lower()
    try:
        if ext in {".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm", ".rtf"}:
            return path.read_text(encoding="utf-8", errors="ignore")[:limit]
        if ext == ".pdf":
            try:
                from pypdf import PdfReader  # type: ignore
                reader = PdfReader(str(path))
                parts: list[str] = []
                chars = 0
                for page in reader.pages[:8]:
                    text = page.extract_text() or ""
                    parts.append(text)
                    chars += len(text)
                    if chars >= limit:
                        break
                return "\n".join(parts)[:limit]
            except Exception:
                return ""
        if ext in {".docx", ".odt", ".epub", ".pptx", ".xlsx"}:
            import zipfile
            with zipfile.ZipFile(path) as zf:
                chunks: list[str] = []
                chars = 0
                for name in zf.namelist():
                    low = name.lower()
                    if not low.endswith((".xml", ".html", ".xhtml")):
                        continue
                    try:
                        text = zf.read(name).decode("utf-8", errors="ignore")
                    except Exception:
                        continue
                    text = re.sub(r"<[^>]+>", " ", text)
                    chunks.append(text)
                    chars += len(text)
                    if chars >= limit:
                        break
                return "\n".join(chunks)[:limit]
    except Exception:
        return ""
    return ""


def classify(text: str, filename: str) -> dict[str, Any]:
    hay = (filename + "\n" + text).casefold().replace("ё", "е")
    authority = "UNKNOWN"
    for value, needles in AUTHORITY_PATTERNS:
        if any(n.casefold().replace("ё", "е") in hay for n in needles):
            authority = value
            break

    domains = [value for value, needles in DOMAIN_PATTERNS if any(n.casefold().replace("ё", "е") in hay for n in needles)]
    if not domains:
        domains = ["OTHER"]

    kind = "UNKNOWN"
    for value, needles in DOC_KIND_PATTERNS:
        if any(n.casefold().replace("ё", "е") in hay for n in needles):
            kind = value
            break

    low_name = filename.lower()
    if kind == "UNKNOWN":
        if low_name.endswith((".ppt", ".pptx")):
            kind = "PRESENTATION"
        elif low_name.endswith(".epub"):
            kind = "BOOK"

    trust = "UNKNOWN"
    if authority in {"FSTEC", "FSB", "ROSKOMNADZOR", "ROSSTANDART_GOST", "GOVERNMENT", "MINZDRAV", "MINTRANS", "MINPROMTORG", "MINENERGO", "MINEKONOM", "ROSMONITORING"} and kind in {"LAW_OR_REGULATION", "STANDARD", "METHODOLOGY"}:
        trust = "A0_CANDIDATE_NEEDS_PROVENANCE"
    elif kind in {"BOOK", "ARTICLE", "PRESENTATION"}:
        trust = "A3_WORKING_SOURCE"

    relevant = kind != "UNKNOWN" or domains != ["OTHER"] or authority != "UNKNOWN"
    return {
        "authority": authority,
        "domains": domains,
        "document_kind": kind,
        "trust_class": trust,
        "relevant_for_models": relevant,
    }


def model_stages(kind: str) -> list[str]:
    base = ["M0_EVIDENCE_IDENTITY", "M4_SEMANTIC_STRUCTURE", "M5_TERMINOLOGY", "M6_KNOWLEDGE_EXTRACTION"]
    if kind in {"LAW_OR_REGULATION", "STANDARD", "METHODOLOGY", "BOOK", "ARTICLE"}:
        base += ["M7_RELATION_DISCOVERY", "M8_CONTRADICTION_VERIFICATION", "M9_PROFESSOR_SYNTHESIS", "M10_INDEPENDENT_JUDGE"]
    return base


def object_path(root: Path, sha: str, suffix: str) -> Path:
    return root / sha[:2] / f"{sha}{suffix.lower()}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory and copy knowledge-bearing files from Downloads into the FATHER local intake library.")
    parser.add_argument("--downloads", default=os.environ.get("FATHER_DOWNLOADS_DIR") or str(DEFAULT_DOWNLOADS))
    args = parser.parse_args()

    source_root = Path(args.downloads).expanduser().resolve()
    if not source_root.is_dir():
        print(json.dumps({"status": "DOWNLOADS_NOT_FOUND", "path": str(source_root)}, ensure_ascii=False, indent=2))
        return 2

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    OBJECTS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)

    paths = sorted(p for p in source_root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
    rows: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []

    for path in paths:
        try:
            sha = sha256_file(path)
            size = path.stat().st_size
        except OSError as exc:
            rows.append({"source_path": str(path), "status": "READ_FAILED", "error": str(exc)})
            continue

        text = sample_text(path)
        cls = classify(text, path.name)
        mime, _ = mimetypes.guess_type(path.name)
        target_root = OBJECTS if cls["relevant_for_models"] else QUARANTINE
        obj = object_path(target_root, sha, path.suffix)
        obj.parent.mkdir(parents=True, exist_ok=True)
        duplicate = obj.exists()
        if not obj.exists():
            shutil.copy2(path, obj)

        source_id = "SRC-" + sha[:24]
        manifest = {
            "schema_version": "father-osint.downloads-intake.v0.2",
            "source_id": source_id,
            "sha256": sha,
            "byte_length": size,
            "mime_type": mime or "application/octet-stream",
            "original_name": path.name,
            "original_path": str(path),
            "intake_object": obj.relative_to(ROOT).as_posix(),
            "document_kind": cls["document_kind"],
            "authority": cls["authority"],
            "domains": cls["domains"],
            "trust_class": cls["trust_class"],
            "source_locator_status": "LOCAL_DOWNLOAD_PATH_ONLY",
            "duplicate_exact": duplicate,
            "sample_text_chars": len(text),
            "relevant_for_models": cls["relevant_for_models"],
            "review_status": "INTAKE_REVIEW_REQUIRED" if cls["relevant_for_models"] else "QUARANTINED_UNCLASSIFIED",
            "kb_auto_promotion": False,
            "observed_at": utc_now(),
        }
        (MANIFESTS / f"{source_id}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        status = "REUSED_EXACT" if duplicate else "INGESTED" if cls["relevant_for_models"] else "QUARANTINED"
        rows.append({**manifest, "status": status})

        if not cls["relevant_for_models"]:
            continue
        queue.append({
            "work_item_id": "WI-" + sha[:24],
            "source_id": source_id,
            "source_sha256": sha,
            "document_kind": cls["document_kind"],
            "authority": cls["authority"],
            "domains": cls["domains"],
            "trust_class": cls["trust_class"],
            "object_path": obj.relative_to(ROOT).as_posix(),
            "stages": model_stages(cls["document_kind"]),
            "output_contract": {
                "allowed_candidate_types": [
                    "TERM_CANDIDATE", "DEFINITION_CANDIDATE", "CLAIM_CANDIDATE",
                    "REQUIREMENT_CANDIDATE", "PRINCIPLE_CANDIDATE", "PATTERN_CANDIDATE",
                    "TRADEOFF_CANDIDATE", "DECISION_CRITERION_CANDIDATE",
                    "FAILURE_MODE_CANDIDATE", "APPLICABILITY_CANDIDATE", "RELATION_CANDIDATE",
                    "CONTRADICTION_CANDIDATE",
                ],
                "exact_evidence_required": True,
                "source_sha256_required": True,
                "review_status": "MAIN_ANALYST_REVIEW_REQUIRED",
                "kb_auto_promotion": False,
            },
        })

    authority_counts = Counter(str(r.get("authority") or "UNKNOWN") for r in rows if r.get("status") in {"INGESTED", "REUSED_EXACT"})
    kind_counts = Counter(str(r.get("document_kind") or "UNKNOWN") for r in rows if r.get("status") in {"INGESTED", "REUSED_EXACT"})
    domain_counts: Counter[str] = Counter()
    for r in rows:
        if not r.get("relevant_for_models"):
            continue
        for d in r.get("domains") or []:
            domain_counts[str(d)] += 1

    summary = {
        "schema_version": "father-osint.downloads-intake-run.v0.2",
        "record_type": "DOWNLOADS_KNOWLEDGE_INTAKE_RUN",
        "status": "PASS",
        "downloads_root": str(source_root),
        "files_supported_total": len(paths),
        "ingested_total": sum(r.get("status") == "INGESTED" for r in rows),
        "reused_exact_total": sum(r.get("status") == "REUSED_EXACT" for r in rows),
        "quarantined_total": sum(r.get("status") == "QUARANTINED" for r in rows),
        "read_failed_total": sum(r.get("status") == "READ_FAILED" for r in rows),
        "authority_counts": dict(sorted(authority_counts.items())),
        "document_kind_counts": dict(sorted(kind_counts.items())),
        "domain_counts": dict(sorted(domain_counts.items())),
        "knowledge_library": LIBRARY.relative_to(ROOT).as_posix(),
        "model_work_queue": QUEUE.relative_to(ROOT).as_posix(),
        "source_files_modified": False,
        "kb_auto_promotion": False,
        "results": rows,
        "observed_at": utc_now(),
    }
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    QUEUE.write_text(json.dumps({
        "schema_version": "father-osint.model-work-queue.v0.2",
        "record_type": "MODEL_WORK_QUEUE",
        "state": "READY_FOR_MODEL_ROUTER",
        "stage_registry": "config/model_stage_registry.yaml",
        "items_total": len(queue),
        "items": queue,
        "kb_auto_promotion": False,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    compact = {k: v for k, v in summary.items() if k != "results"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Queue: {QUEUE.relative_to(ROOT).as_posix()}")
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
