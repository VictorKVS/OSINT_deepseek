from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from .knowledge_factory import (
    AuditEvent,
    DocumentRecord,
    DocumentVersion,
    Permission,
    PipelineStage,
    Role,
    StageState,
    is_allowed,
)
from .knowledge_factory_store import KnowledgeFactoryStore


PARSER_VERSION = "legal-preliminary-v1"


class DocumentCompilerError(RuntimeError):
    pass


class _VisibleTextHTMLParser(HTMLParser):
    _block_tags = {
        "article", "aside", "blockquote", "br", "div", "footer", "h1", "h2", "h3", "h4", "h5", "h6",
        "header", "li", "main", "p", "section", "table", "td", "th", "tr", "ul", "ol"
    }
    _ignored_tags = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self._ignored_tags:
            self._ignored_depth += 1
            return
        if not self._ignored_depth and tag in self._block_tags:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._ignored_tags:
            self._ignored_depth = max(0, self._ignored_depth - 1)
            return
        if not self._ignored_depth and tag in self._block_tags:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]
    return f"{prefix}-{digest}"


def _decode_bytes(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise DocumentCompilerError("artifact text encoding is unsupported")


def _json_text(value: Any) -> str:
    strings: list[str] = []

    def walk(item: Any) -> None:
        if isinstance(item, str):
            if item.strip():
                strings.append(item)
        elif isinstance(item, list):
            for child in item:
                walk(child)
        elif isinstance(item, dict):
            for child in item.values():
                walk(child)

    walk(value)
    return "\n".join(strings)


def extract_visible_text(data: bytes, mime_type: str | None) -> str:
    mime = (mime_type or "").split(";", 1)[0].strip().lower()
    raw = _decode_bytes(data)

    if mime in {"text/html", "application/xhtml+xml"} or "<html" in raw[:1000].lower():
        parser = _VisibleTextHTMLParser()
        parser.feed(raw)
        raw = parser.text()
    elif mime in {"application/json", "text/json"} or raw.lstrip().startswith(("{", "[")):
        try:
            raw = _json_text(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise DocumentCompilerError(f"invalid JSON artifact: {exc}") from exc
    elif mime and not (mime.startswith("text/") or mime == "application/octet-stream"):
        raise DocumentCompilerError(f"unsupported preliminary parser MIME: {mime}")

    raw = raw.replace("\xa0", " ").replace("\u200b", "")
    lines: list[str] = []
    previous_blank = False
    for line in raw.splitlines():
        normalized = re.sub(r"[\t ]+", " ", line).strip()
        if not normalized:
            if lines and not previous_blank:
                lines.append("")
            previous_blank = True
            continue
        previous_blank = False
        lines.append(normalized)
    text = "\n".join(lines).strip()
    if not text:
        raise DocumentCompilerError("artifact contains no extractable visible text")
    return text


@dataclass(frozen=True, slots=True)
class StructureNode:
    node_id: str
    document_id: str
    version_id: str
    node_type: str
    locator: str
    title: str
    text: str
    parent_node_id: str | None
    ordinal: int
    content_sha256: str
    parser_version: str = PARSER_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    version_id: str
    structure_node_id: str
    locator: str
    text: str
    content_sha256: str
    artifact_sha256: str
    parser_version: str = PARSER_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CompileResult:
    document_id: str
    version_id: str
    artifact_sha256: str
    parser_version: str
    extracted_text_path: str
    structure_path: str
    chunks_path: str
    manifest_path: str
    structure_nodes: tuple[StructureNode, ...]
    chunks: tuple[DocumentChunk, ...]
    warnings: tuple[str, ...]


_CHAPTER_RE = re.compile(r"^Глава\s+([0-9IVXLCDM]+(?:[.][0-9]+)?)\.?\s*(.*)$", re.IGNORECASE)
_SECTION_RE = re.compile(r"^Раздел\s+([0-9IVXLCDM]+(?:[.][0-9]+)?)\.?\s*(.*)$", re.IGNORECASE)
_ARTICLE_RE = re.compile(r"^Статья\s+(\d+(?:[.][0-9]+)?)\.?\s*(.*)$", re.IGNORECASE)


def _split_long_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    if not paragraphs:
        paragraphs = [text.strip()]

    result: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                result.append(current)
                current = ""
            words = paragraph.split()
            piece = ""
            for word in words:
                candidate = f"{piece} {word}".strip()
                if piece and len(candidate) > max_chars:
                    result.append(piece)
                    piece = word
                else:
                    piece = candidate
            if piece:
                result.append(piece)
            continue

        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current and len(candidate) > max_chars:
            result.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def parse_legal_structure(document_id: str, version_id: str, text: str) -> tuple[list[StructureNode], list[str]]:
    lines = text.splitlines()
    root_id = _stable_id("STR", document_id, version_id, "document")
    nodes: list[StructureNode] = [
        StructureNode(
            node_id=root_id,
            document_id=document_id,
            version_id=version_id,
            node_type="DOCUMENT",
            locator="document",
            title="Document",
            text="",
            parent_node_id=None,
            ordinal=0,
            content_sha256=_sha256_text(""),
        )
    ]
    warnings: list[str] = []
    current_parent = root_id
    current_article: dict[str, Any] | None = None
    article_count = 0

    def flush_article() -> None:
        nonlocal current_article, article_count
        if current_article is None:
            return
        body = "\n".join(current_article["body"]).strip()
        title = current_article["title"]
        locator = current_article["locator"]
        content = f"{title}\n{body}".strip()
        node_id = _stable_id("STR", document_id, version_id, locator, content)
        article_count += 1
        nodes.append(
            StructureNode(
                node_id=node_id,
                document_id=document_id,
                version_id=version_id,
                node_type="ARTICLE",
                locator=locator,
                title=title,
                text=body,
                parent_node_id=current_article["parent"],
                ordinal=article_count,
                content_sha256=_sha256_text(content),
            )
        )
        current_article = None

    structural_ordinal = 0
    for line in lines:
        chapter = _CHAPTER_RE.match(line)
        section = _SECTION_RE.match(line)
        article = _ARTICLE_RE.match(line)

        if chapter or section:
            flush_article()
            match = chapter or section
            assert match is not None
            node_type = "CHAPTER" if chapter else "SECTION"
            number = match.group(1)
            trailing = match.group(2).strip()
            title = f"{node_type.title()} {number}" + (f". {trailing}" if trailing else "")
            locator = f"{node_type.lower()}:{number}"
            node_id = _stable_id("STR", document_id, version_id, locator, title)
            structural_ordinal += 1
            nodes.append(
                StructureNode(
                    node_id=node_id,
                    document_id=document_id,
                    version_id=version_id,
                    node_type=node_type,
                    locator=locator,
                    title=title,
                    text="",
                    parent_node_id=root_id,
                    ordinal=structural_ordinal,
                    content_sha256=_sha256_text(title),
                )
            )
            current_parent = node_id
            continue

        if article:
            flush_article()
            number = article.group(1)
            trailing = article.group(2).strip()
            title = f"Статья {number}" + (f". {trailing}" if trailing else "")
            current_article = {
                "locator": f"article:{number}",
                "title": title,
                "body": [],
                "parent": current_parent,
            }
            continue

        if current_article is not None:
            current_article["body"].append(line)

    flush_article()

    if article_count == 0:
        warnings.append("no article headings detected; fallback BODY structure created")
        body_id = _stable_id("STR", document_id, version_id, "body", text)
        nodes.append(
            StructureNode(
                node_id=body_id,
                document_id=document_id,
                version_id=version_id,
                node_type="BODY",
                locator="body",
                title="Body",
                text=text,
                parent_node_id=root_id,
                ordinal=1,
                content_sha256=_sha256_text(text),
            )
        )

    return nodes, warnings


def build_chunks(
    document_id: str,
    version: DocumentVersion,
    nodes: list[StructureNode],
    *,
    max_chunk_chars: int,
) -> list[DocumentChunk]:
    if max_chunk_chars < 300:
        raise ValueError("max_chunk_chars must be >= 300")
    chunks: list[DocumentChunk] = []
    candidates = [node for node in nodes if node.node_type in {"ARTICLE", "BODY"}]
    for node in candidates:
        source_text = f"{node.title}\n{node.text}".strip()
        for index, piece in enumerate(_split_long_text(source_text, max_chunk_chars), start=1):
            locator = f"{node.locator}/chunk:{index}"
            chunk_id = _stable_id("CHK", document_id, version.version_id, locator, piece)
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    version_id=version.version_id,
                    structure_node_id=node.node_id,
                    locator=locator,
                    text=piece,
                    content_sha256=_sha256_text(piece),
                    artifact_sha256=version.sha256,
                )
            )
    return chunks


class DocumentCompiler:
    """Preliminary D4-D5 compiler for evidence-preserving KB analysis.

    It does not infer facts or requirements. It only extracts readable text,
    creates deterministic legal structure/chunks and preserves lineage to the
    exact acquired artifact/version.
    """

    def __init__(self, store: KnowledgeFactoryStore) -> None:
        self.store = store

    @staticmethod
    def _current_version(document: DocumentRecord) -> DocumentVersion:
        if not document.current_version_id:
            raise DocumentCompilerError("document has no current version")
        for version in document.versions:
            if version.version_id == document.current_version_id:
                return version
        raise DocumentCompilerError("current_version_id does not resolve to a version")

    def compile(
        self,
        document: DocumentRecord,
        *,
        actor_id: str,
        actor_role: Role | str = Role.KNOWLEDGE_CURATOR,
        max_chunk_chars: int = 2400,
    ) -> CompileResult:
        role = actor_role if isinstance(actor_role, Role) else Role(str(actor_role))
        if not is_allowed(role, Permission.ADVANCE_PIPELINE):
            raise DocumentCompilerError(f"role {role.value} cannot advance document pipeline")
        if document.stage_states.get(PipelineStage.D3_INTEGRITY_METADATA_VERIFIED.value) not in {
            StageState.DONE.value,
            StageState.VERIFIED.value,
        }:
            raise DocumentCompilerError("D3 must be complete before D4-D5 compilation")

        version = self._current_version(document)
        artifact_path = (self.store.root / version.local_path).resolve()
        root_resolved = self.store.root.resolve()
        if root_resolved not in artifact_path.parents:
            raise DocumentCompilerError("artifact path escapes KnowledgeFactoryStore root")
        if not artifact_path.exists():
            raise DocumentCompilerError("original artifact is missing")
        artifact = artifact_path.read_bytes()
        actual_sha = hashlib.sha256(artifact).hexdigest()
        if actual_sha != version.sha256:
            raise DocumentCompilerError("original artifact SHA-256 no longer matches DocumentVersion")

        text = extract_visible_text(artifact, version.mime_type)
        nodes, warnings = parse_legal_structure(document.document_id, version.version_id, text)
        chunks = build_chunks(
            document.document_id,
            version,
            nodes,
            max_chunk_chars=max_chunk_chars,
        )
        if not chunks:
            raise DocumentCompilerError("preliminary compiler produced zero chunks")

        output_dir = self.store.root / "compiled" / document.document_id / version.version_id
        output_dir.mkdir(parents=True, exist_ok=True)
        text_path = output_dir / "extracted_text.txt"
        structure_path = output_dir / "structure.jsonl"
        chunks_path = output_dir / "chunks.jsonl"
        manifest_path = output_dir / "manifest.json"

        text_path.write_text(text, encoding="utf-8", newline="\n")
        with structure_path.open("w", encoding="utf-8", newline="\n") as handle:
            for node in nodes:
                handle.write(json.dumps(node.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        with chunks_path.open("w", encoding="utf-8", newline="\n") as handle:
            for chunk in chunks:
                handle.write(json.dumps(chunk.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

        manifest = {
            "schema_version": "1.0",
            "document_id": document.document_id,
            "version_id": version.version_id,
            "artifact_sha256": version.sha256,
            "source_url": version.source_url,
            "mime_type": version.mime_type,
            "parser_version": PARSER_VERSION,
            "structure_nodes": len(nodes),
            "chunks": len(chunks),
            "warnings": warnings,
            "semantic_extraction_performed": False,
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        document.set_stage_state(PipelineStage.D4_STRUCTURE_PARSED, StageState.DONE)
        document.set_stage_state(PipelineStage.D5_CHUNKED, StageState.DONE)
        self.store.save_document(document)
        self.store.append_audit(
            AuditEvent(
                actor_id=actor_id,
                actor_role=role.value,
                action="COMPILE_DOCUMENT_D4_D5",
                object_type="DOCUMENT",
                object_id=document.document_id,
                result="SUCCESS",
                metadata={
                    "version_id": version.version_id,
                    "artifact_sha256": version.sha256,
                    "parser_version": PARSER_VERSION,
                    "structure_nodes": len(nodes),
                    "chunks": len(chunks),
                    "manifest_path": manifest_path.relative_to(self.store.root).as_posix(),
                },
            )
        )

        return CompileResult(
            document_id=document.document_id,
            version_id=version.version_id,
            artifact_sha256=version.sha256,
            parser_version=PARSER_VERSION,
            extracted_text_path=text_path.relative_to(self.store.root).as_posix(),
            structure_path=structure_path.relative_to(self.store.root).as_posix(),
            chunks_path=chunks_path.relative_to(self.store.root).as_posix(),
            manifest_path=manifest_path.relative_to(self.store.root).as_posix(),
            structure_nodes=tuple(nodes),
            chunks=tuple(chunks),
            warnings=tuple(warnings),
        )
