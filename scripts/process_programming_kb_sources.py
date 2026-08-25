from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "programming_kb_sources"
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
GRAPH_OUT = REPORT_ROOT / "PROGRAMMING_KB_CANDIDATE_GRAPH.json"
LATEST = REPORT_ROOT / "LATEST_SOURCE_PROCESSING.json"
POLICY = ROOT / "config" / "programming_kb_source_factory_policy.json"

from father_osint.book_corpus import BookCorpusBuilder, BookSource  # noqa: E402
from father_osint.knowledge_analyst import DeterministicKnowledgeAnalyst  # noqa: E402


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1
        elif tag in {"p", "div", "section", "article", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1
        elif tag in {"p", "div", "section", "article", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
        return raw.strip()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_html(path: Path) -> tuple[str, str]:
    parser = TextHTMLParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.text(), "STDLIB_HTML_PARSER"


def extract_docx(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as zf:
        data = zf.read("word/document.xml")
    root = ET.fromstring(data)
    texts = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
    return "\n".join(texts), "STDLIB_DOCX_XML"


def extract_epub(path: Path) -> tuple[str, str]:
    parts: list[str] = []
    with zipfile.ZipFile(path) as zf:
        names = sorted(
            name for name in zf.namelist()
            if name.lower().endswith((".xhtml", ".html", ".htm"))
        )
        for name in names:
            parser = TextHTMLParser()
            parser.feed(zf.read(name).decode("utf-8", errors="ignore"))
            text = parser.text()
            if text:
                parts.append(text)
    return "\n\n".join(parts), "STDLIB_EPUB_HTML"


def extract_pdf(path: Path) -> tuple[str, str]:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        return "\n\n".join((page.extract_text() or "") for page in reader.pages), "PYPDF"
    except ImportError:
        pass
    except Exception:
        pass

    try:
        import fitz  # type: ignore

        doc = fitz.open(str(path))
        try:
            return "\n\n".join(page.get_text("text") for page in doc), "PYMUPDF"
        finally:
            doc.close()
    except ImportError:
        pass
    except Exception:
        pass

    executable = shutil.which("pdftotext")
    if executable:
        proc = subprocess.run(
            [executable, "-layout", str(path), "-"],
            capture_output=True,
            check=False,
            timeout=120,
        )
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8", errors="ignore"), "PDFTOTEXT"
    raise RuntimeError("no working PDF text extractor available (pypdf, PyMuPDF or pdftotext)")


def extract_text(path: Path) -> tuple[str, str]:
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore"), "STDLIB_TEXT"
    if ext in {".html", ".htm"}:
        return extract_html(path)
    if ext == ".docx":
        return extract_docx(path)
    if ext == ".epub":
        return extract_epub(path)
    if ext == ".pdf":
        return extract_pdf(path)
    raise RuntimeError(f"no extractor adapter for {ext or '<no extension>'}")


def author_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "Unknown").split(";") if item.strip()] or ["Unknown"]


def stable_node_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return prefix + "-" + hashlib.sha256(payload).hexdigest()[:24]


def process_one(source_meta_path: Path) -> dict[str, Any]:
    meta = load_json(source_meta_path)
    target_id = str(meta.get("target_id") or source_meta_path.parent.name)
    local_path = ROOT / str(meta.get("local_path") or "")
    if not local_path.is_file():
        return {"target_id": target_id, "status": "FAILED", "error": f"source file missing: {local_path}"}
    actual_sha = sha256_file(local_path)
    if meta.get("sha256") and meta.get("sha256") != actual_sha:
        return {"target_id": target_id, "status": "FAILED", "error": "source SHA-256 mismatch"}
    try:
        text, extractor = extract_text(local_path)
    except Exception as exc:
        return {
            "target_id": target_id,
            "status": "PARSER_GAP",
            "error": f"{type(exc).__name__}: {exc}",
            "source_sha256": actual_sha,
            "local_path": local_path.relative_to(ROOT).as_posix(),
        }
    normalized = text.replace("\x00", "").strip()
    if len(normalized) < 100:
        return {
            "target_id": target_id,
            "status": "TEXT_TOO_SMALL",
            "extractor": extractor,
            "characters": len(normalized),
            "source_sha256": actual_sha,
        }

    source = BookSource(
        title=str(meta.get("title") or target_id),
        authors=author_list(meta.get("author")),
        source_language=str(meta.get("source_language") or "en"),
        target_language=str(meta.get("source_language") or "en"),
        source_locator=str(meta.get("source_locator") or meta.get("resolved_url") or local_path),
        source_sha256=actual_sha,
        rights_basis=str(meta.get("rights_basis") or "UNKNOWN_REVIEW_REQUIRED"),
        source_status="EXACT_BYTES_ACQUIRED",
        book_id=target_id,
    )
    corpus = BookCorpusBuilder().build(source, normalized)
    identity = {unit.unit_id: unit.source_text for unit in corpus.translation_units}
    corpus.apply_translations(identity, method="IDENTITY_SOURCE_LANGUAGE")
    corpus.build_semantic_structure()
    package = corpus.to_material_package(task_id=f"programming-kb:{target_id}")
    bundle = DeterministicKnowledgeAnalyst().analyze(package)

    out_dir = REPORT_ROOT / "sources" / target_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "corpus.json").write_text(
        json.dumps(corpus.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    bundle.write_json(out_dir / "knowledge_bundle.json")

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    source_node = f"SRC-{target_id}"
    nodes.append({
        "id": source_node,
        "type": "SOURCE_DOCUMENT",
        "title": meta.get("title") or target_id,
        "target_id": target_id,
        "sha256": actual_sha,
        "rights_basis": meta.get("rights_basis"),
        "source_locator": meta.get("source_locator"),
        "review_status": "SOURCE_REGISTERED",
    })

    heading_nodes: dict[str, str] = {}
    for unit in corpus.semantic_units:
        if unit.unit_type != "HEADING":
            continue
        node_id = stable_node_id("SEC", target_id, unit.semantic_id)
        heading_nodes[unit.semantic_id] = node_id
        nodes.append({
            "id": node_id,
            "type": "SECTION",
            "title": unit.translated_text[:240],
            "source_semantic_id": unit.semantic_id,
            "review_status": "STRUCTURAL",
        })
        edges.append({"from": node_id, "type": "DEFINED_IN", "to": source_node})

    for item in bundle.items:
        node_id = stable_node_id("KN", target_id, item.item_id, item.item_type, item.text)
        nodes.append({
            "id": node_id,
            "type": item.item_type,
            "text": item.text,
            "subject": item.subject,
            "value": item.value,
            "review_status": item.review_status,
            "evidence": item.evidence.to_dict(),
        })
        edges.append({"from": node_id, "type": "DERIVED_FROM", "to": source_node})

    return {
        "target_id": target_id,
        "status": "PROCESSED_REVIEW_REQUIRED",
        "extractor": extractor,
        "source_sha256": actual_sha,
        "characters": len(normalized),
        "translation_units": corpus.counters["translation_units"],
        "semantic_units": corpus.counters["semantic_units"],
        "materials": bundle.counters.get("materials", 0),
        "chunks": bundle.counters.get("chunks", 0),
        "definitions": bundle.counters.get("DEFINITION_CANDIDATE", 0),
        "requirements": bundle.counters.get("REQUIREMENT_CANDIDATE", 0),
        "claims": bundle.counters.get("CLAIM_CANDIDATE", 0),
        "entities": bundle.counters.get("ENTITY_CANDIDATE", 0),
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Decompose acquired PROGRAMMING_KB sources into reviewable knowledge candidates.")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    policy = load_json(POLICY)
    errors: list[str] = []
    if policy.get("policy_id") != "FATHER-PROGRAMMING-KB-SOURCE-FACTORY-001":
        errors.append("unexpected source factory policy id")
    if args.validate_only:
        payload = {
            "record_type": "PROGRAMMING_KB_SOURCE_PROCESSOR_VALIDATION",
            "status": "PASS" if not errors else "FAIL",
            "validation_errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 2

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    metas = sorted(DATA_ROOT.glob("*/source.json")) if DATA_ROOT.exists() else []
    results = [process_one(path) for path in metas]
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    for row in results:
        nodes.extend(row.pop("nodes", []))
        edges.extend(row.pop("edges", []))

    processed = sum(row.get("status") == "PROCESSED_REVIEW_REQUIRED" for row in results)
    parser_gaps = sum(row.get("status") == "PARSER_GAP" for row in results)
    failed = sum(row.get("status") in {"FAILED", "TEXT_TOO_SMALL"} for row in results)
    graph = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMING_KB_CANDIDATE_GRAPH",
        "knowledge_base_id": "PROGRAMMING_KB",
        "region_profile": "RU",
        "state": "REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "nodes": nodes,
        "edges": edges,
    }
    GRAPH_OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "record_type": "PROGRAMMING_KB_SOURCE_PROCESSING",
        "schema_version": "1.0",
        "status": "PASS" if processed > 0 and failed == 0 else "PASS_WITH_GAPS" if processed > 0 else "NO_PROCESSABLE_SOURCES",
        "sources_discovered_total": len(metas),
        "processed_total": processed,
        "parser_gap_total": parser_gaps,
        "failed_total": failed,
        "knowledge_nodes_total": len(nodes),
        "relation_edges_total": len(edges),
        "definitions_total": sum(int(row.get("definitions") or 0) for row in results),
        "requirements_total": sum(int(row.get("requirements") or 0) for row in results),
        "claims_total": sum(int(row.get("claims") or 0) for row in results),
        "chunks_total": sum(int(row.get("chunks") or 0) for row in results),
        "kb_auto_promotion": False,
        "training_state": "HOLD",
        "results": results,
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key != "results"}
    print(json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Graph: {GRAPH_OUT.relative_to(ROOT).as_posix()}")
    print(f"Report: {LATEST.relative_to(ROOT).as_posix()}")
    return 0 if summary["status"] in {"PASS", "PASS_WITH_GAPS"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
