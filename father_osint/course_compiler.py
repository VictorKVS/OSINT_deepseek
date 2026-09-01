from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from typing import Any


COURSE_PARSER_VERSION = "course-preliminary-v1"


class CourseCompilerError(RuntimeError):
    pass


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
    raise CourseCompilerError("artifact text encoding is unsupported")


class _CourseHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._heading_level: int | None = None
        self._ignored_depth = 0
        self._ignored = {"script", "style", "noscript", "svg"}
        self._blocks = {"p", "div", "section", "article", "li", "br", "pre", "code", "table", "tr", "td", "th"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self._ignored:
            self._ignored_depth += 1
            return
        if self._ignored_depth:
            return
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_level = int(tag[1])
            self.parts.append("\n" + "#" * self._heading_level + " ")
        elif tag in self._blocks:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._ignored:
            self._ignored_depth = max(0, self._ignored_depth - 1)
            return
        if self._ignored_depth:
            return
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_level = None
            self.parts.append("\n")
        elif tag in self._blocks:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


@dataclass(frozen=True, slots=True)
class CourseStructureNode:
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
    parser_version: str = COURSE_PARSER_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CourseChunk:
    chunk_id: str
    document_id: str
    version_id: str
    structure_node_id: str
    locator: str
    text: str
    content_sha256: str
    artifact_sha256: str
    parser_version: str = COURSE_PARSER_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CourseCompileResult:
    extracted_text: str
    structure_nodes: tuple[CourseStructureNode, ...]
    chunks: tuple[CourseChunk, ...]
    warnings: tuple[str, ...]
    parser_version: str = COURSE_PARSER_VERSION


def _normalize_text(raw: str) -> str:
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
    value = "\n".join(lines).strip()
    if not value:
        raise CourseCompilerError("artifact contains no extractable text")
    return value


def extract_course_text(data: bytes, *, mime_type: str | None = None, file_name: str = "") -> str:
    mime = (mime_type or "").split(";", 1)[0].strip().lower()
    suffix = file_name.lower().rsplit(".", 1)[-1] if "." in file_name else ""

    if suffix == "ipynb" or mime == "application/x-ipynb+json":
        try:
            notebook = json.loads(_decode_bytes(data))
        except json.JSONDecodeError as exc:
            raise CourseCompilerError(f"invalid notebook JSON: {exc}") from exc
        parts: list[str] = []
        for index, cell in enumerate(notebook.get("cells", []), start=1):
            source = cell.get("source", [])
            text = "".join(source) if isinstance(source, list) else str(source or "")
            if not text.strip():
                continue
            cell_type = str(cell.get("cell_type", "unknown")).upper()
            if cell_type == "MARKDOWN":
                parts.append(text)
            elif cell_type == "CODE":
                parts.append(f"## Code cell {index}\n```python\n{text.rstrip()}\n```")
            else:
                parts.append(f"## {cell_type.title()} cell {index}\n{text}")
        return _normalize_text("\n\n".join(parts))

    raw = _decode_bytes(data)
    if mime in {"text/html", "application/xhtml+xml"} or "<html" in raw[:1500].lower():
        parser = _CourseHTMLParser()
        parser.feed(raw)
        raw = parser.text()
    elif mime in {"application/json", "text/json"} and suffix != "ipynb":
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise CourseCompilerError(f"invalid JSON artifact: {exc}") from exc
        raw = json.dumps(parsed, ensure_ascii=False, indent=2)
    elif mime and not (mime.startswith("text/") or mime == "application/octet-stream"):
        raise CourseCompilerError(f"unsupported course parser MIME: {mime}")

    return _normalize_text(raw)


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def parse_course_structure(document_id: str, version_id: str, text: str) -> tuple[list[CourseStructureNode], list[str]]:
    root_id = _stable_id("CSTR", document_id, version_id, "document")
    nodes: list[CourseStructureNode] = [
        CourseStructureNode(
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
    stack: list[tuple[int, str]] = [(0, root_id)]
    current: dict[str, Any] | None = None
    section_ordinal = 0

    def flush() -> None:
        nonlocal current, section_ordinal
        if current is None:
            return
        body = "\n".join(current["body"]).strip()
        title = current["title"]
        locator = current["locator"]
        content = f"{title}\n{body}".strip()
        section_ordinal += 1
        nodes.append(
            CourseStructureNode(
                node_id=current["node_id"],
                document_id=document_id,
                version_id=version_id,
                node_type="SECTION",
                locator=locator,
                title=title,
                text=body,
                parent_node_id=current["parent"],
                ordinal=section_ordinal,
                content_sha256=_sha256_text(content),
            )
        )
        current = None

    heading_index = 0
    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            flush()
            level = len(match.group(1))
            title = match.group(2).strip()
            heading_index += 1
            while stack and stack[-1][0] >= level:
                stack.pop()
            parent = stack[-1][1] if stack else root_id
            locator = f"heading:{heading_index}:level:{level}"
            node_id = _stable_id("CSTR", document_id, version_id, locator, title)
            current = {
                "node_id": node_id,
                "title": title,
                "locator": locator,
                "parent": parent,
                "body": [],
            }
            stack.append((level, node_id))
            continue
        if current is not None:
            current["body"].append(line)

    flush()

    if len(nodes) == 1:
        warnings.append("no headings detected; fallback BODY structure created")
        body_id = _stable_id("CSTR", document_id, version_id, "body", text)
        nodes.append(
            CourseStructureNode(
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


def _split_long_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    if not paragraphs:
        paragraphs = [text.strip()]
    result: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current and len(candidate) > max_chars:
            result.append(current)
            current = paragraph
        elif len(paragraph) > max_chars:
            if current:
                result.append(current)
                current = ""
            words = paragraph.split()
            piece = ""
            for word in words:
                trial = f"{piece} {word}".strip()
                if piece and len(trial) > max_chars:
                    result.append(piece)
                    piece = word
                else:
                    piece = trial
            if piece:
                current = piece
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def compile_course_material(
    *,
    document_id: str,
    version_id: str,
    artifact_sha256: str,
    data: bytes,
    mime_type: str | None = None,
    file_name: str = "",
    max_chunk_chars: int = 2400,
) -> CourseCompileResult:
    if max_chunk_chars < 300:
        raise ValueError("max_chunk_chars must be >= 300")
    actual = hashlib.sha256(data).hexdigest()
    if actual != artifact_sha256:
        raise CourseCompilerError("artifact SHA-256 does not match supplied identity")

    text = extract_course_text(data, mime_type=mime_type, file_name=file_name)
    nodes, warnings = parse_course_structure(document_id, version_id, text)
    chunks: list[CourseChunk] = []
    candidates = [node for node in nodes if node.node_type in {"SECTION", "BODY"}]
    for node in candidates:
        source_text = f"{node.title}\n{node.text}".strip()
        for index, piece in enumerate(_split_long_text(source_text, max_chunk_chars), start=1):
            locator = f"{node.locator}/chunk:{index}"
            chunks.append(
                CourseChunk(
                    chunk_id=_stable_id("CCHK", document_id, version_id, locator, piece),
                    document_id=document_id,
                    version_id=version_id,
                    structure_node_id=node.node_id,
                    locator=locator,
                    text=piece,
                    content_sha256=_sha256_text(piece),
                    artifact_sha256=artifact_sha256,
                )
            )
    if not chunks:
        raise CourseCompilerError("course compiler produced zero chunks")
    return CourseCompileResult(
        extracted_text=text,
        structure_nodes=tuple(nodes),
        chunks=tuple(chunks),
        warnings=tuple(warnings),
    )
