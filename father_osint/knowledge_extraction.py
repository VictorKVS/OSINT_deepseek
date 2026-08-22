from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Iterable


EXTRACTOR_VERSION = "legal-d6-d9-deterministic-v1"
REVIEW_STATE = "CANDIDATE_NEEDS_REVIEW"
PROMOTION_STATE = "NOT_PROMOTED"


@dataclass(frozen=True, slots=True)
class SourceLineage:
    document_id: str
    version_id: str
    chunk_id: str
    chunk_locator: str
    structure_node_id: str
    artifact_sha256: str
    source_text_sha256: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TermCandidate:
    term_id: str
    canonical_key: str
    term: str
    term_kind: str
    extraction_basis: str
    lineage: SourceLineage
    review_state: str = REVIEW_STATE
    promotion_state: str = PROMOTION_STATE
    extractor_version: str = EXTRACTOR_VERSION

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["lineage"] = self.lineage.to_dict()
        return payload


@dataclass(frozen=True, slots=True)
class DefinitionCandidate:
    definition_id: str
    canonical_key: str
    term: str
    definition: str
    extraction_basis: str
    lineage: SourceLineage
    review_state: str = REVIEW_STATE
    promotion_state: str = PROMOTION_STATE
    extractor_version: str = EXTRACTOR_VERSION

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["lineage"] = self.lineage.to_dict()
        return payload


@dataclass(frozen=True, slots=True)
class RequirementCandidate:
    requirement_id: str
    modality: str
    trigger: str
    statement: str
    extraction_basis: str
    lineage: SourceLineage
    review_state: str = REVIEW_STATE
    promotion_state: str = PROMOTION_STATE
    extractor_version: str = EXTRACTOR_VERSION

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["lineage"] = self.lineage.to_dict()
        return payload


@dataclass(frozen=True, slots=True)
class EntityMentionCandidate:
    entity_mention_id: str
    canonical_key: str
    entity: str
    entity_kind: str
    extraction_basis: str
    lineage: SourceLineage
    review_state: str = REVIEW_STATE
    promotion_state: str = PROMOTION_STATE
    extractor_version: str = EXTRACTOR_VERSION

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["lineage"] = self.lineage.to_dict()
        return payload


# This lexicon is intentionally small, explicit and deterministic. It identifies
# mentions only; it does not assert that a mention is a verified KB entity.
_CONTROLLED_MENTIONS: tuple[tuple[str, str, str], ...] = (
    ("персональные данные", "personal_data", "LEGAL_OBJECT"),
    ("субъект персональных данных", "personal_data_subject", "ACTOR"),
    ("оператор", "personal_data_operator", "ACTOR"),
    ("обработка персональных данных", "personal_data_processing", "PROCESS"),
    ("информационная система персональных данных", "personal_data_information_system", "SYSTEM"),
    ("безопасность персональных данных", "personal_data_security", "SECURITY_CONCEPT"),
    ("угрозы безопасности персональных данных", "personal_data_security_threats", "THREAT_CONCEPT"),
    ("уровень защищенности", "protection_level", "SECURITY_CONCEPT"),
    ("средства криптографической защиты информации", "cryptographic_protection_means", "CONTROL_TECHNOLOGY"),
    ("СКЗИ", "cryptographic_protection_means", "CONTROL_TECHNOLOGY"),
    ("ФСТЭК России", "fstec_russia", "AUTHORITY"),
    ("ФСБ России", "fsb_russia", "AUTHORITY"),
    ("Роскомнадзор", "roskomnadzor", "AUTHORITY"),
)

_REQUIREMENT_TRIGGERS: tuple[tuple[str, str], ...] = (
    ("не допускается", "PROHIBITION"),
    ("запрещается", "PROHIBITION"),
    ("запрещено", "PROHIBITION"),
    ("обязаны", "OBLIGATION"),
    ("обязан", "OBLIGATION"),
    ("обязана", "OBLIGATION"),
    ("должны", "OBLIGATION"),
    ("должен", "OBLIGATION"),
    ("должна", "OBLIGATION"),
    ("должно", "OBLIGATION"),
    ("необходимо", "REQUIREMENT"),
    ("подлежит", "OBLIGATION"),
    ("требуется", "REQUIREMENT"),
)

_DEFINITION_RE = re.compile(
    r"^(?P<term>[А-Яа-яЁёA-Za-z0-9][^—–\-:;]{1,119}?)\s*(?:—|–|-)\s*(?P<definition>.+)$",
    re.DOTALL,
)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+(?=[А-ЯЁA-Z0-9])")
_PREFIX_RE = re.compile(r"^(?:Пункт\s+[^\n]+|Статья\s+[^\n]+)\n", re.IGNORECASE)


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _canonical_key(value: str) -> str:
    normalized = _norm(value)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return f"term:{digest}"


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "\x1f".join(" ".join(str(part).split()).casefold() for part in parts)
    return f"{prefix}-{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:24]}"


def _lineage(chunk: dict[str, object]) -> SourceLineage:
    text = str(chunk.get("text", ""))
    return SourceLineage(
        document_id=str(chunk["document_id"]),
        version_id=str(chunk["version_id"]),
        chunk_id=str(chunk["chunk_id"]),
        chunk_locator=str(chunk["locator"]),
        structure_node_id=str(chunk["structure_node_id"]),
        artifact_sha256=str(chunk["artifact_sha256"]),
        source_text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
    )


def _body_text(chunk_text: str) -> str:
    return _PREFIX_RE.sub("", chunk_text.strip(), count=1).strip()


def _explicit_definition(chunk_text: str) -> tuple[str, str] | None:
    body = _body_text(chunk_text)
    if not body:
        return None
    # Definitions in Russian legal acts are often one numbered point with a
    # `term - definition` or `term — definition` lexical form.
    match = _DEFINITION_RE.match(body)
    if not match:
        return None
    term = " ".join(match.group("term").split()).strip(" ,;:")
    definition = " ".join(match.group("definition").split()).strip()
    if len(term) < 2 or len(definition) < 8:
        return None
    return term, definition


def _sentences(text: str) -> Iterable[str]:
    body = _body_text(text)
    if not body:
        return ()
    values: list[str] = []
    for paragraph in body.splitlines():
        for value in _SENTENCE_SPLIT_RE.split(paragraph):
            normalized = " ".join(value.split()).strip()
            if normalized:
                values.append(normalized)
    return values


def extract_candidates(chunk: dict[str, object]) -> tuple[
    list[TermCandidate],
    list[DefinitionCandidate],
    list[RequirementCandidate],
    list[EntityMentionCandidate],
]:
    """Extract reviewable candidates from one evidence-preserving chunk.

    This function is deterministic and intentionally conservative. It produces
    candidates with exact lineage; it never promotes them to verified facts.
    """

    text = str(chunk.get("text", ""))
    if not text.strip():
        return [], [], [], []
    lineage = _lineage(chunk)

    terms: list[TermCandidate] = []
    definitions: list[DefinitionCandidate] = []
    requirements: list[RequirementCandidate] = []
    entities: list[EntityMentionCandidate] = []

    explicit = _explicit_definition(text)
    if explicit:
        term, definition = explicit
        canonical_key = _canonical_key(term)
        terms.append(
            TermCandidate(
                term_id=_stable_id("TERM", lineage.chunk_id, canonical_key, "explicit-definition"),
                canonical_key=canonical_key,
                term=term,
                term_kind="EXPLICITLY_DEFINED_TERM",
                extraction_basis="EXPLICIT_LEXICAL_DEFINITION",
                lineage=lineage,
            )
        )
        definitions.append(
            DefinitionCandidate(
                definition_id=_stable_id("DEF", lineage.chunk_id, canonical_key, definition),
                canonical_key=canonical_key,
                term=term,
                definition=definition,
                extraction_basis="EXPLICIT_LEXICAL_DEFINITION",
                lineage=lineage,
            )
        )

    normalized_text = _norm(text)
    seen_mentions: set[str] = set()
    for surface, canonical_key, entity_kind in _CONTROLLED_MENTIONS:
        if _norm(surface) not in normalized_text or canonical_key in seen_mentions:
            continue
        seen_mentions.add(canonical_key)
        term_kind = "CONTROLLED_DOMAIN_TERM"
        if not any(item.canonical_key == canonical_key for item in terms):
            terms.append(
                TermCandidate(
                    term_id=_stable_id("TERM", lineage.chunk_id, canonical_key, "controlled-mention"),
                    canonical_key=canonical_key,
                    term=surface,
                    term_kind=term_kind,
                    extraction_basis="CONTROLLED_LEXICON_MENTION",
                    lineage=lineage,
                )
            )
        entities.append(
            EntityMentionCandidate(
                entity_mention_id=_stable_id("ENT", lineage.chunk_id, canonical_key),
                canonical_key=canonical_key,
                entity=surface,
                entity_kind=entity_kind,
                extraction_basis="CONTROLLED_LEXICON_MENTION",
                lineage=lineage,
            )
        )

    seen_requirements: set[str] = set()
    for sentence in _sentences(text):
        normalized_sentence = _norm(sentence)
        for trigger, modality in _REQUIREMENT_TRIGGERS:
            if _norm(trigger) not in normalized_sentence:
                continue
            key = hashlib.sha256(normalized_sentence.encode("utf-8")).hexdigest()
            if key in seen_requirements:
                break
            seen_requirements.add(key)
            requirements.append(
                RequirementCandidate(
                    requirement_id=_stable_id("REQ", lineage.chunk_id, key),
                    modality=modality,
                    trigger=trigger,
                    statement=sentence,
                    extraction_basis="EXPLICIT_NORMATIVE_TRIGGER",
                    lineage=lineage,
                )
            )
            break

    return terms, definitions, requirements, entities
