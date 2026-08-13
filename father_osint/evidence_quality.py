from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import urlparse
from uuid import uuid4
import re

from father_osint.models import Material, MaterialPackage, utc_now_iso
from father_osint.protocol import DecisionRecord

QUALITY_STATES = {"UNKNOWN", "LOW", "MEDIUM", "HIGH"}
URL_RE = re.compile(r"https?://[^\s)\]>]+")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9_@#.-]{3,}")


@dataclass(slots=True)
class QualityDimension:
    name: str
    state: str
    rationale: str
    method_ref: str
    input_refs: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.state = self.state.upper()
        if self.state not in QUALITY_STATES:
            raise ValueError(f"state must be one of {sorted(QUALITY_STATES)}")
        if not self.name.strip() or not self.rationale.strip() or not self.method_ref.strip():
            raise ValueError("quality dimension requires name, rationale and method_ref")


@dataclass(slots=True)
class EvidenceQualityAssessment:
    material_id: str
    package_id: str
    reliability: QualityDimension
    relevance: QualityDimension
    independence: QualityDimension
    recency: QualityDimension
    directness: QualityDimension
    corroboration: QualityDimension
    provenance_quality: QualityDimension
    limitations: list[str] = field(default_factory=list)
    assessment_id: str = field(default_factory=lambda: str(uuid4()))
    algorithm_version: str = "evidence-quality-v1"
    created_at: str = field(default_factory=utc_now_iso)

    @property
    def dimensions(self) -> list[QualityDimension]:
        return [
            self.reliability,
            self.relevance,
            self.independence,
            self.recency,
            self.directness,
            self.corroboration,
            self.provenance_quality,
        ]

    def aggregate_truth_probability(self) -> float:
        raise RuntimeError("G7 forbids uncalibrated aggregate truth probability")


@dataclass(slots=True)
class EvidenceQualityResult:
    assessments: list[EvidenceQualityAssessment]
    decision_record: DecisionRecord


class DeterministicEvidenceQualityAssessor:
    """Conservative policy assessment for G7.

    States are categorical policy outputs, not probabilities of truth. Missing
    evidence stays UNKNOWN. Repeated payloads and forwards are not promoted to
    independent corroboration merely because they appear multiple times.
    """

    algorithm_version = "evidence-quality-v1"
    knowledge_version = "information-evidence-standard-v1"

    def assess_package(
        self,
        package: MaterialPackage,
        *,
        relevant_terms: Iterable[str] = (),
        reference_time: datetime | None = None,
        case_id: str | None = None,
    ) -> EvidenceQualityResult:
        ref_time = reference_time or datetime.now(timezone.utc)
        terms = {t.lower().strip() for t in relevant_terms if t.strip()}
        hash_counts: dict[str, int] = {}
        for material in package.materials:
            if material.content_hash:
                hash_counts[material.content_hash] = hash_counts.get(material.content_hash, 0) + 1

        assessments = [
            self._assess_material(material, package, terms, ref_time, hash_counts)
            for material in package.materials
        ]
        decision = DecisionRecord(
            case_id=case_id or package.task_id,
            role_id="OSINT_EXPERT",
            decision="ASSESS_EVIDENCE_QUALITY_DIMENSIONS",
            input_refs=[package.package_id] + [m.material_id for m in package.materials],
            knowledge_refs=["information-evidence-standard.v1", "EC-005.information-evidence-standard"],
            method_refs=[
                "g7.separate-dimensions-v1",
                "g7.no-uncalibrated-truth-score",
                "g7.derivative-copy-independence-check",
            ],
            reason_codes=["EVIDENCE_PACKAGE_QUALITY_REVIEW"],
            limitations=[
                "Source reliability is UNKNOWN unless supported by explicit source-history metadata",
                "Directness is UNKNOWN unless source class is explicit",
                "Categorical states are policy labels, not calibrated truth probabilities",
            ],
            output_refs=[a.assessment_id for a in assessments],
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )
        return EvidenceQualityResult(assessments=assessments, decision_record=decision)

    def _assess_material(
        self,
        material: Material,
        package: MaterialPackage,
        terms: set[str],
        ref_time: datetime,
        hash_counts: dict[str, int],
    ) -> EvidenceQualityAssessment:
        derivative = bool(
            material.metadata.get("forward_from")
            or material.metadata.get("forward_origin")
            or material.metadata.get("forward_sender_name")
        )
        duplicate_payload = bool(material.content_hash and hash_counts.get(material.content_hash, 0) > 1)

        reliability = QualityDimension(
            "reliability",
            "UNKNOWN",
            "No explicit validated source-history reliability record is attached to this material",
            "source-history-required-v1",
            [material.material_id],
        )

        relevance = self._relevance(material, terms)
        independence = QualityDimension(
            "independence",
            "LOW" if derivative or duplicate_payload else "MEDIUM",
            (
                "Forward/derivative or repeated payload signal prevents treating this observation as independent"
                if derivative or duplicate_payload
                else "No derivative/repeated-payload signal observed, but independence is not proven by absence of such metadata"
            ),
            "derivative-copy-independence-v1",
            [material.material_id],
        )
        recency = self._recency(material, ref_time)
        directness = self._directness(material, derivative)
        corroboration = self._corroboration(material, package, duplicate_payload)
        provenance = self._provenance(material)

        limitations: list[str] = []
        if reliability.state == "UNKNOWN":
            limitations.append("Reliability requires source-history evidence")
        if directness.state == "UNKNOWN":
            limitations.append("Directness to the investigated real-world fact is not established")

        return EvidenceQualityAssessment(
            material_id=material.material_id,
            package_id=package.package_id,
            reliability=reliability,
            relevance=relevance,
            independence=independence,
            recency=recency,
            directness=directness,
            corroboration=corroboration,
            provenance_quality=provenance,
            limitations=limitations,
        )

    def _relevance(self, material: Material, terms: set[str]) -> QualityDimension:
        if not terms:
            return QualityDimension(
                "relevance", "UNKNOWN",
                "No explicit research terms were supplied to the quality assessor",
                "research-term-overlap-v1", [material.material_id],
            )
        text_terms = {x.lower() for x in WORD_RE.findall(material.raw_text or "")}
        hits = sorted(terms & text_terms)
        state = "HIGH" if len(hits) >= 2 else "MEDIUM" if hits else "LOW"
        return QualityDimension(
            "relevance", state,
            f"Research-term overlap hits={hits}" if hits else "No supplied research terms were observed in material text",
            "research-term-overlap-v1", [material.material_id],
        )

    def _recency(self, material: Material, ref_time: datetime) -> QualityDimension:
        if not material.published_at:
            return QualityDimension("recency", "UNKNOWN", "Publication time is missing", "publication-age-policy-v1", [material.material_id])
        try:
            published = datetime.fromisoformat(material.published_at.replace("Z", "+00:00"))
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
            age_days = max(0.0, (ref_time - published.astimezone(timezone.utc)).total_seconds() / 86400)
        except ValueError:
            return QualityDimension("recency", "UNKNOWN", "Publication time could not be parsed", "publication-age-policy-v1", [material.material_id])
        state = "HIGH" if age_days <= 7 else "MEDIUM" if age_days <= 30 else "LOW"
        return QualityDimension("recency", state, f"Publication age is {age_days:.1f} day(s) under policy thresholds", "publication-age-policy-v1", [material.material_id])

    def _directness(self, material: Material, derivative: bool) -> QualityDimension:
        source_class = str(material.metadata.get("source_class") or "").lower()
        if derivative:
            return QualityDimension("directness", "LOW", "Material carries forward/derivative metadata", "source-class-directness-v1", [material.material_id])
        if source_class in {"primary", "first_party", "first-party"}:
            return QualityDimension("directness", "HIGH", f"Explicit source_class={source_class}", "source-class-directness-v1", [material.material_id])
        if source_class in {"secondary", "tertiary"}:
            return QualityDimension("directness", "LOW", f"Explicit source_class={source_class}", "source-class-directness-v1", [material.material_id])
        return QualityDimension("directness", "UNKNOWN", "No explicit source_class establishes directness to the investigated fact", "source-class-directness-v1", [material.material_id])

    def _corroboration(self, material: Material, package: MaterialPackage, duplicate_payload: bool) -> QualityDimension:
        if duplicate_payload:
            return QualityDimension("corroboration", "LOW", "Repeated identical payload is derivative repetition, not independent corroboration", "independent-corroboration-v1", [material.material_id])
        material_domains = {urlparse(u).hostname for u in URL_RE.findall(material.raw_text or "") if urlparse(u).hostname}
        distinct_sources = set()
        for other in package.materials:
            if other.material_id == material.material_id:
                continue
            other_domains = {urlparse(u).hostname for u in URL_RE.findall(other.raw_text or "") if urlparse(u).hostname}
            if material_domains and material_domains & other_domains and other.content_hash != material.content_hash:
                distinct_sources.add(str(other.metadata.get("chat_id") or other.source_locator))
        if distinct_sources:
            return QualityDimension("corroboration", "MEDIUM", f"Distinct observations reference shared external domain(s); independent factual support still requires verification: {sorted(distinct_sources)}", "independent-corroboration-v1", [material.material_id])
        return QualityDimension("corroboration", "UNKNOWN", "No deterministic independent corroboration signal was established", "independent-corroboration-v1", [material.material_id])

    def _provenance(self, material: Material) -> QualityDimension:
        signals = [
            bool(material.source_locator),
            bool(material.content_hash),
            bool(material.collected_at),
            bool(material.metadata.get("transport")),
            bool(material.metadata.get("message_id") or material.metadata.get("chat_id")),
        ]
        count = sum(signals)
        state = "HIGH" if count >= 5 else "MEDIUM" if count >= 3 else "LOW"
        return QualityDimension("provenance_quality", state, f"{count}/5 canonical provenance signals are present", "canonical-provenance-completeness-v1", [material.material_id])
