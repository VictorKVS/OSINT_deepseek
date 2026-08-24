from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from .models import Material, MaterialPackage, utc_now_iso


SCHEMA_VERSION = "father-osint.knowledge-bundle.v0.1"


@dataclass(slots=True)
class EvidenceSpan:
    material_id: str
    source_type: str
    source_locator: str
    title: str
    char_start: int
    char_end: int
    text_sha256: str
    content_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class KnowledgeChunk:
    chunk_id: str
    text: str
    evidence: EvidenceSpan

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence"] = self.evidence.to_dict()
        return payload


@dataclass(slots=True)
class KnowledgeItem:
    item_type: str
    text: str
    evidence: EvidenceSpan
    subject: str | None = None
    value: str | None = None
    extraction_method: str = "DETERMINISTIC_RULE"
    review_status: str = "NEEDS_REVIEW"
    item_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence"] = self.evidence.to_dict()
        return payload


@dataclass(slots=True)
class KnowledgeBundle:
    task_id: str
    package_id: str
    material_ids: list[str]
    chunks: list[KnowledgeChunk] = field(default_factory=list)
    items: list[KnowledgeItem] = field(default_factory=list)
    schema_version: str = SCHEMA_VERSION
    bundle_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    @property
    def counters(self) -> dict[str, int]:
        result: dict[str, int] = {"materials": len(self.material_ids), "chunks": len(self.chunks)}
        for item in self.items:
            result[item.item_type] = result.get(item.item_type, 0) + 1
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "bundle_id": self.bundle_id,
            "task_id": self.task_id,
            "package_id": self.package_id,
            "material_ids": list(self.material_ids),
            "created_at": self.created_at,
            "counters": self.counters,
            "chunks": [chunk.to_dict() for chunk in self.chunks],
            "items": [item.to_dict() for item in self.items],
        }

    def write_json(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        tmp = destination.with_suffix(destination.suffix + ".tmp")
        tmp.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        tmp.replace(destination)
        return destination


class DeterministicKnowledgeAnalyst:
    """Extract traceable knowledge candidates from material already in the corpus.

    This layer deliberately does not decide whether a statement is legally true,
    current, or universally applicable. It produces reviewable candidates with
    exact source spans so later expert/LLM stages can reason without losing
    provenance.
    """

    _sentence_re = re.compile(r"[^.!?\n]+(?:[.!?]+|$)", re.MULTILINE)
    _definition_re = re.compile(
        r"^\s*(?P<term>[A-Za-zА-Яа-яЁё0-9][^:—–\-]{1,100}?)\s*(?:—|–|:)\s*(?P<definition>.+?)\s*$"
    )
    _requirement_markers = (
        " должен ",
        " должна ",
        " должны ",
        " обязан ",
        " обязана ",
        " обязаны ",
        " требуется ",
        " необходимо ",
        " не допускается ",
        " запрещается ",
        " shall ",
        " must ",
        " required ",
    )

    def analyze(self, package: MaterialPackage) -> KnowledgeBundle:
        chunks: list[KnowledgeChunk] = []
        items: list[KnowledgeItem] = []
        seen_items: set[tuple[str, str]] = set()

        for material in package.materials:
            material_chunks = list(self._chunk_material(material))
            chunks.extend(material_chunks)
            self._extract_metadata_entities(material, material_chunks, items, seen_items)

            for chunk in material_chunks:
                text = chunk.text.strip()
                if not text:
                    continue

                self._append_item(
                    items,
                    seen_items,
                    KnowledgeItem(
                        item_type="CLAIM_CANDIDATE",
                        text=text,
                        evidence=chunk.evidence,
                    ),
                )

                definition = self._definition_re.match(text)
                if definition:
                    term = definition.group("term").strip()
                    value = definition.group("definition").strip()
                    self._append_item(
                        items,
                        seen_items,
                        KnowledgeItem(
                            item_type="DEFINITION_CANDIDATE",
                            subject=term,
                            value=value,
                            text=text,
                            evidence=chunk.evidence,
                        ),
                    )

                if self._looks_like_requirement(text):
                    self._append_item(
                        items,
                        seen_items,
                        KnowledgeItem(
                            item_type="REQUIREMENT_CANDIDATE",
                            text=text,
                            evidence=chunk.evidence,
                        ),
                    )

        return KnowledgeBundle(
            task_id=package.task_id,
            package_id=package.package_id,
            material_ids=[material.material_id for material in package.materials],
            chunks=chunks,
            items=items,
        )

    def _chunk_material(self, material: Material) -> Iterable[KnowledgeChunk]:
        text = material.raw_text or ""
        if not text:
            return []

        chunks: list[KnowledgeChunk] = []
        for match in self._sentence_re.finditer(text):
            raw = match.group(0)
            leading = len(raw) - len(raw.lstrip())
            trailing = len(raw) - len(raw.rstrip())
            start = match.start() + leading
            end = match.end() - trailing
            if start >= end:
                continue
            chunk_text = text[start:end]
            digest = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
            chunk_key = f"{material.material_id}:{start}:{end}:{digest}".encode("utf-8")
            chunk_id = hashlib.sha256(chunk_key).hexdigest()
            evidence = EvidenceSpan(
                material_id=material.material_id,
                source_type=material.source_type,
                source_locator=material.source_locator,
                title=material.title,
                char_start=start,
                char_end=end,
                text_sha256=digest,
                content_hash=material.content_hash,
            )
            chunks.append(KnowledgeChunk(chunk_id=chunk_id, text=chunk_text, evidence=evidence))
        return chunks

    def _extract_metadata_entities(
        self,
        material: Material,
        chunks: list[KnowledgeChunk],
        items: list[KnowledgeItem],
        seen_items: set[tuple[str, str]],
    ) -> None:
        if not chunks:
            return
        values: list[str] = []
        candidate = material.metadata.get("candidate")
        if candidate:
            values.append(str(candidate))
        entities = material.metadata.get("entities", [])
        if isinstance(entities, (list, tuple, set)):
            values.extend(str(value) for value in entities if str(value).strip())

        for value in values:
            normalized = value.strip()
            if not normalized:
                continue
            self._append_item(
                items,
                seen_items,
                KnowledgeItem(
                    item_type="ENTITY_CANDIDATE",
                    text=normalized,
                    subject=normalized,
                    evidence=chunks[0].evidence,
                    extraction_method="SOURCE_METADATA",
                ),
            )

    def _looks_like_requirement(self, text: str) -> bool:
        normalized = " " + " ".join(text.casefold().split()) + " "
        return any(marker in normalized for marker in self._requirement_markers)

    @staticmethod
    def _append_item(
        items: list[KnowledgeItem],
        seen_items: set[tuple[str, str]],
        item: KnowledgeItem,
    ) -> None:
        key = (item.item_type, " ".join(item.text.casefold().split()))
        if key in seen_items:
            return
        seen_items.add(key)
        items.append(item)
