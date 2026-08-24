from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from .models import Material, MaterialPackage, utc_now_iso


@dataclass(slots=True)
class ArchitectureCandidate:
    candidate_type: str
    statement: str
    source_locator: str
    translation_unit_id: str | None
    source_text_sha256: str | None
    translated_text_sha256: str
    heading_path: list[str] = field(default_factory=list)
    subject: str | None = None
    value: str | None = None
    confidence: str = "LOW"
    extraction_method: str = "DETERMINISTIC_BOOK_RULE"
    review_status: str = "NEEDS_REVIEW"
    candidate_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ArchitectureBookAnalysis:
    task_id: str
    material_ids: list[str]
    candidates: list[ArchitectureCandidate]
    generated_at: str = field(default_factory=utc_now_iso)
    schema_version: str = "father-osint.architecture-book-analysis.v0.1"

    @property
    def counters(self) -> dict[str, int]:
        counters: dict[str, int] = {
            "materials": len(self.material_ids),
            "candidates": len(self.candidates),
        }
        for candidate in self.candidates:
            counters[candidate.candidate_type] = counters.get(candidate.candidate_type, 0) + 1
        return counters

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "task_id": self.task_id,
            "generated_at": self.generated_at,
            "material_ids": list(self.material_ids),
            "counters": self.counters,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
        }


class ArchitectureBookAnalyst:
    """First deterministic semantic pass for translated architecture literature.

    This class does not decide that an author's recommendation is universally
    correct. It creates typed review candidates and preserves a pointer to the
    original-language unit hash held in the private corpus.
    """

    _sentence_re = re.compile(r"[^.!?\n]+(?:[.!?]+|$)", re.MULTILINE)
    _definition_re = re.compile(
        r"^\s*(?P<term>[A-Za-zА-Яа-яЁё0-9][^:—–]{1,100}?)\s*(?:—|–|:)\s*(?P<value>.+?)\s*$"
    )

    _signals: dict[str, tuple[str, ...]] = {
        "PRINCIPLE_CANDIDATE": (
            " принцип ", " следует ", " стоит ", " рекомендуется ", " предпочтительно ",
            " избегать ", " важно ", " should ", " prefer ", " avoid ", " principle ",
        ),
        "PATTERN_CANDIDATE": (
            " паттерн ", " шаблон ", " архитектурный стиль ", " подход ",
            " pattern ", " architectural style ", " approach ",
        ),
        "TRADEOFF_CANDIDATE": (
            " компромисс ", " компромиссы ", " trade-off ", " tradeoff ",
            " преимущество ", " недостаток ", " цена этого ", " однако ", " но при этом ",
        ),
        "DECISION_CRITERION_CANDIDATE": (
            " выбирать ", " выбрать ", " подходит когда ", " следует использовать ",
            " если ", " зависит от ", " choose ", " when ", " depends on ",
        ),
        "FAILURE_MODE_CANDIDATE": (
            " антипаттерн ", " ошибка ", " риск ", " проблема ", " отказ ", " недостаток ",
            " anti-pattern ", " failure ", " risk ", " problem ", " drawback ",
        ),
        "EXAMPLE_CANDIDATE": (
            " например ", " пример ", " к примеру ", " for example ", " for instance ",
        ),
    }

    def analyze(self, package: MaterialPackage) -> ArchitectureBookAnalysis:
        candidates: list[ArchitectureCandidate] = []
        seen: set[tuple[str, str, str]] = set()

        for material in package.materials:
            if material.source_type != "book" or not (material.raw_text or "").strip():
                continue
            self._analyze_material(material, candidates, seen)

        return ArchitectureBookAnalysis(
            task_id=package.task_id,
            material_ids=[material.material_id for material in package.materials],
            candidates=candidates,
        )

    def _analyze_material(
        self,
        material: Material,
        candidates: list[ArchitectureCandidate],
        seen: set[tuple[str, str, str]],
    ) -> None:
        translated = (material.raw_text or "").strip()
        unit_type = str(material.metadata.get("unit_type") or "")

        if unit_type == "HEADING":
            self._append(
                candidates,
                seen,
                self._candidate(material, "CONCEPT_CANDIDATE", translated, subject=translated, confidence="MEDIUM"),
            )

        for match in self._sentence_re.finditer(translated):
            sentence = match.group(0).strip()
            if not sentence:
                continue

            definition = self._definition_re.match(sentence)
            if definition:
                term = definition.group("term").strip()
                value = definition.group("value").strip()
                self._append(
                    candidates,
                    seen,
                    self._candidate(
                        material,
                        "DEFINITION_CANDIDATE",
                        sentence,
                        subject=term,
                        value=value,
                        confidence="MEDIUM",
                    ),
                )
                self._append(
                    candidates,
                    seen,
                    self._candidate(
                        material,
                        "TERM_CANDIDATE",
                        term,
                        subject=term,
                        confidence="MEDIUM",
                    ),
                )

            # Signal markers are token/phrase oriented. Normalize punctuation to
            # spaces so a phrase such as "Архитектурный компромисс:" matches the
            # same marker as "архитектурный компромисс между ..." without
            # broad substring matching inside words. Keep +/#/- for technical
            # terms and hyphenated English markers such as trade-off.
            signal_text = re.sub(r"[^0-9A-Za-zА-Яа-яЁё_+#-]+", " ", sentence.casefold())
            normalized = " " + " ".join(signal_text.split()) + " "
            matched_any = False
            for candidate_type, markers in self._signals.items():
                if any(marker.casefold() in normalized for marker in markers):
                    self._append(
                        candidates,
                        seen,
                        self._candidate(material, candidate_type, sentence),
                    )
                    matched_any = True

            if matched_any or len(sentence) >= 80:
                self._append(
                    candidates,
                    seen,
                    self._candidate(material, "CLAIM_CANDIDATE", sentence),
                )

    def _candidate(
        self,
        material: Material,
        candidate_type: str,
        statement: str,
        *,
        subject: str | None = None,
        value: str | None = None,
        confidence: str = "LOW",
    ) -> ArchitectureCandidate:
        translated_hash = hashlib.sha256(statement.encode("utf-8")).hexdigest()
        heading_path = material.metadata.get("heading_path") or []
        if not isinstance(heading_path, list):
            heading_path = [str(heading_path)]
        return ArchitectureCandidate(
            candidate_type=candidate_type,
            statement=statement,
            subject=subject,
            value=value,
            source_locator=material.source_locator,
            translation_unit_id=material.metadata.get("translation_unit_id"),
            source_text_sha256=material.metadata.get("source_text_sha256"),
            translated_text_sha256=translated_hash,
            heading_path=[str(value) for value in heading_path],
            confidence=confidence,
        )

    @staticmethod
    def _append(
        candidates: list[ArchitectureCandidate],
        seen: set[tuple[str, str, str]],
        candidate: ArchitectureCandidate,
    ) -> None:
        key = (
            candidate.candidate_type,
            " ".join(candidate.statement.casefold().split()),
            candidate.source_text_sha256 or candidate.source_locator,
        )
        if key in seen:
            return
        seen.add(key)
        candidates.append(candidate)
