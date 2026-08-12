from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import uuid4

from father_osint.models import MaterialPackage


@dataclass(slots=True)
class EvidenceClaim:
    statement: str
    evidence_ids: list[str]
    confidence: float
    claim_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement must not be empty")
        if not self.evidence_ids:
            raise ValueError("claim must cite at least one material_id")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(slots=True)
class AnalysisResult:
    task_id: str
    package_id: str
    claims: list[EvidenceClaim] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CritiqueResult:
    verdict: str
    challenged_claim_ids: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        allowed = {"PASS", "CHALLENGE", "INSUFFICIENT"}
        self.verdict = self.verdict.upper()
        if self.verdict not in allowed:
            raise ValueError(f"verdict must be one of {sorted(allowed)}")


class Analyst(Protocol):
    def analyze(self, package: MaterialPackage) -> AnalysisResult: ...


class Critic(Protocol):
    def critique(self, package: MaterialPackage, analysis: AnalysisResult) -> CritiqueResult: ...


class DeterministicEvidenceAnalyst:
    """Build evidence-backed observation claims without inferring truth.

    This analyst is intentionally conservative. Each claim only states that a
    source material was observed and preserves a short source-text excerpt as
    quoted evidence context. It does not transform a source statement into an
    asserted real-world fact. A future LLM analyst may add semantic claims only
    behind the same EvidenceClaim contract.
    """

    def __init__(self, excerpt_chars: int = 240) -> None:
        if excerpt_chars <= 0:
            raise ValueError("excerpt_chars must be > 0")
        self.excerpt_chars = excerpt_chars

    def analyze(self, package: MaterialPackage) -> AnalysisResult:
        claims: list[EvidenceClaim] = []
        limitations: list[str] = []

        for material in package.materials:
            text = (material.raw_text or "").strip()
            if not text:
                limitations.append(
                    f"material {material.material_id} has no raw_text for deterministic analysis"
                )
                continue

            excerpt = " ".join(text.split())[: self.excerpt_chars]
            statement = (
                f"Observed {material.source_type} source '{material.title}' "
                f"at {material.source_locator}: {excerpt}"
            )
            claims.append(
                EvidenceClaim(
                    statement=statement,
                    evidence_ids=[material.material_id],
                    confidence=1.0,
                )
            )

        if package.collection_errors:
            limitations.extend(package.collection_errors)
        if not package.materials:
            limitations.append("MaterialPackage contains no materials")

        return AnalysisResult(
            task_id=package.task_id,
            package_id=package.package_id,
            claims=claims,
            limitations=limitations,
        )


class DeterministicSocrates:
    """Minimal evidence-integrity critic; no LLM and no source-specific logic."""

    def critique(self, package: MaterialPackage, analysis: AnalysisResult) -> CritiqueResult:
        available_ids = {material.material_id for material in package.materials}
        challenged: list[str] = []
        reasons: list[str] = []

        if analysis.task_id != package.task_id or analysis.package_id != package.package_id:
            return CritiqueResult(
                verdict="INSUFFICIENT",
                reasons=["analysis does not belong to the supplied MaterialPackage"],
            )

        if not analysis.claims:
            return CritiqueResult(
                verdict="INSUFFICIENT",
                missing_evidence=["no evidence-backed claims were produced"],
            )

        for claim in analysis.claims:
            missing = [item for item in claim.evidence_ids if item not in available_ids]
            if missing:
                challenged.append(claim.claim_id)
                reasons.append(
                    f"claim {claim.claim_id} cites material_ids outside the package: {missing}"
                )

        if challenged:
            return CritiqueResult(
                verdict="CHALLENGE",
                challenged_claim_ids=challenged,
                reasons=reasons,
            )

        return CritiqueResult(verdict="PASS")
