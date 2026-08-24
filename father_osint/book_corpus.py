from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping
from uuid import uuid4

from .models import Material, MaterialPackage, utc_now_iso


class BookStage(str, Enum):
    SOURCE_REGISTERED = "SOURCE_REGISTERED"
    TEXT_EXTRACTED = "TEXT_EXTRACTED"
    TRANSLATION_ALIGNED = "TRANSLATION_ALIGNED"
    STRUCTURED = "STRUCTURED"
    READY_FOR_ANALYST = "READY_FOR_ANALYST"


@dataclass(slots=True)
class BookSource:
    title: str
    authors: list[str]
    source_language: str
    target_language: str = "ru"
    edition: str | None = None
    isbn: str | None = None
    source_locator: str | None = None
    source_sha256: str | None = None
    rights_basis: str = "USER_LIBRARY_COPY"
    source_status: str = "AWAITING_SOURCE_BYTES"
    book_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.title.strip() or not self.authors:
            raise ValueError("book title and at least one author are required")
        if self.source_sha256 is not None:
            digest = self.source_sha256.strip().lower()
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError("source_sha256 must be a 64-character hexadecimal digest")
            self.source_sha256 = digest

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TranslationUnit:
    unit_id: str
    order: int
    source_char_start: int
    source_char_end: int
    source_text: str
    source_text_sha256: str
    translated_text: str | None = None
    translation_method: str | None = None
    translation_status: str = "PENDING"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SemanticUnit:
    semantic_id: str
    translation_unit_id: str
    order: int
    unit_type: str
    source_text: str
    translated_text: str
    heading_path: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BookCorpus:
    source: BookSource
    extracted_text_sha256: str
    translation_units: list[TranslationUnit]
    semantic_units: list[SemanticUnit] = field(default_factory=list)
    stage: BookStage = BookStage.TEXT_EXTRACTED
    created_at: str = field(default_factory=utc_now_iso)

    @property
    def counters(self) -> dict[str, int]:
        return {
            "translation_units": len(self.translation_units),
            "translated_units": sum(1 for unit in self.translation_units if unit.translation_status == "DONE"),
            "semantic_units": len(self.semantic_units),
        }

    @property
    def translation_complete(self) -> bool:
        return bool(self.translation_units) and all(
            unit.translation_status == "DONE" and bool((unit.translated_text or "").strip())
            for unit in self.translation_units
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "father-osint.book-corpus.v0.1",
            "stage": self.stage.value,
            "created_at": self.created_at,
            "source": self.source.to_dict(),
            "extracted_text_sha256": self.extracted_text_sha256,
            "counters": self.counters,
            "translation_units": [unit.to_dict() for unit in self.translation_units],
            "semantic_units": [unit.to_dict() for unit in self.semantic_units],
        }

    def apply_translations(
        self,
        translations: Mapping[str, str],
        *,
        method: str,
        require_complete: bool = True,
    ) -> None:
        if not method.strip():
            raise ValueError("translation method is required")

        missing: list[str] = []
        for unit in self.translation_units:
            value = translations.get(unit.unit_id)
            if value is None or not str(value).strip():
                missing.append(unit.unit_id)
                continue
            unit.translated_text = str(value).strip()
            unit.translation_method = method
            unit.translation_status = "DONE"

        if require_complete and missing:
            raise ValueError(f"translation is incomplete; missing {len(missing)} unit(s)")

        self.stage = (
            BookStage.TRANSLATION_ALIGNED if self.translation_complete else BookStage.TEXT_EXTRACTED
        )

    def build_semantic_structure(self) -> None:
        if not self.translation_complete:
            raise ValueError("semantic structure requires complete aligned translation")

        semantic_units: list[SemanticUnit] = []
        heading_path: list[str] = []

        for unit in self.translation_units:
            source_text = unit.source_text.strip()
            translated_text = (unit.translated_text or "").strip()
            unit_type = _classify_block(source_text)

            if unit_type == "HEADING":
                heading = translated_text
                heading_path = [heading]

            semantic_units.append(
                SemanticUnit(
                    semantic_id=_stable_id(
                        self.source.book_id,
                        unit.unit_id,
                        unit_type,
                        translated_text,
                    ),
                    translation_unit_id=unit.unit_id,
                    order=unit.order,
                    unit_type=unit_type,
                    source_text=source_text,
                    translated_text=translated_text,
                    heading_path=list(heading_path),
                    metadata={
                        "source_char_start": unit.source_char_start,
                        "source_char_end": unit.source_char_end,
                        "source_text_sha256": unit.source_text_sha256,
                    },
                )
            )

        self.semantic_units = semantic_units
        self.stage = BookStage.STRUCTURED

    def to_material_package(self, *, task_id: str | None = None) -> MaterialPackage:
        if self.stage != BookStage.STRUCTURED or not self.semantic_units:
            raise ValueError("book corpus must be STRUCTURED before analyst handoff")

        materials: list[Material] = []
        for unit in self.semantic_units:
            materials.append(
                Material(
                    source_type="book",
                    source_locator=(self.source.source_locator or self.source.title)
                    + f"#unit={unit.translation_unit_id}",
                    title=f"{self.source.title} :: {unit.order}",
                    raw_text=unit.translated_text,
                    author=", ".join(self.source.authors),
                    metadata={
                        "book_id": self.source.book_id,
                        "translation_unit_id": unit.translation_unit_id,
                        "semantic_id": unit.semantic_id,
                        "unit_type": unit.unit_type,
                        "heading_path": unit.heading_path,
                        "source_text": unit.source_text,
                        "source_text_sha256": unit.metadata["source_text_sha256"],
                        "translation_method": next(
                            item.translation_method
                            for item in self.translation_units
                            if item.unit_id == unit.translation_unit_id
                        ),
                    },
                )
            )

        self.stage = BookStage.READY_FOR_ANALYST
        return MaterialPackage(
            task_id=task_id or f"book:{self.source.book_id}",
            materials=materials,
            notes="Aligned translated book corpus; original source text preserved in metadata.",
        )


class BookCorpusBuilder:
    """Create a translation-aligned corpus from already extracted book text.

    PDF/EPUB parsing is deliberately outside this class. The parser must first
    produce text while preserving the original bytes/hash. This builder performs
    only minimal paragraph segmentation needed for translation alignment; semantic
    decomposition happens only after translation is complete.
    """

    _paragraph_re = re.compile(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", re.DOTALL)

    def build(self, source: BookSource, extracted_text: str) -> BookCorpus:
        normalized = _normalize_text(extracted_text)
        if not normalized.strip():
            raise ValueError("extracted book text must not be empty")

        units: list[TranslationUnit] = []
        for order, match in enumerate(self._paragraph_re.finditer(normalized), start=1):
            raw = match.group(0)
            leading = len(raw) - len(raw.lstrip())
            trailing = len(raw) - len(raw.rstrip())
            start = match.start() + leading
            end = match.end() - trailing
            if start >= end:
                continue
            text = normalized[start:end]
            text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
            units.append(
                TranslationUnit(
                    unit_id=_stable_id(source.book_id, str(start), str(end), text_hash),
                    order=order,
                    source_char_start=start,
                    source_char_end=end,
                    source_text=text,
                    source_text_sha256=text_hash,
                )
            )

        if not units:
            raise ValueError("no translation units could be extracted")

        return BookCorpus(
            source=source,
            extracted_text_sha256=hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
            translation_units=units,
        )


def _normalize_text(text: str) -> str:
    return str(text).replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")


def _stable_id(*parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _classify_block(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "EMPTY"
    lines = stripped.splitlines()
    if len(lines) == 1 and len(stripped) <= 140:
        if stripped.startswith("#") or stripped.isupper() or re.match(r"^(chapter|part|глава|часть)\b", stripped, re.I):
            return "HEADING"
    if all(re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line) for line in lines if line.strip()):
        return "LIST"
    return "PARAGRAPH"
