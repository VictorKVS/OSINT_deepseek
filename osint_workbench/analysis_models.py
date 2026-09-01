from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

AnalyzerCallable = Callable[[str, str, list[tuple[str, dict[str, Any]]]], "AnalyzerDraft"]

@dataclass(frozen=True, slots=True)
class AnalyzerSpec:
    analyzer_id: str
    family: str
    version: str
    modality: tuple[str, ...]
    data_boundary: str = "LOCAL_ONLY"
    allowed_access_classes: tuple[str, ...] = (
        "PUBLIC",
        "PUBLIC_WITH_PERSONAL_DATA",
        "AUTHORIZED_INTERNAL",
        "RESTRICTED",
    )
    known_limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        families = {
            "DETERMINISTIC_RULE",
            "LLM_LOCAL",
            "LLM_REMOTE",
            "GRAPH_ALGORITHM",
            "MEDIA_PIPELINE",
            "LEGAL_RULESET",
            "HUMAN_REVIEW",
        }
        boundaries = {"LOCAL_ONLY", "REMOTE_PUBLIC_ONLY", "REMOTE_REDACTED", "HUMAN_ONLY"}
        modalities = {"TEXT", "GRAPH", "IMAGE", "AUDIO", "VIDEO", "METADATA", "LEGAL"}
        if self.family not in families:
            raise ValueError(f"unsupported analyzer family: {self.family}")
        if self.data_boundary not in boundaries:
            raise ValueError(f"unsupported data boundary: {self.data_boundary}")
        if not self.modality or not set(self.modality).issubset(modalities):
            raise ValueError("analyzer modality is empty or unsupported")


@dataclass(slots=True)
class AnalyzerDraft:
    output_class: str
    answer: str
    supporting_refs: list[str] = field(default_factory=list)
    contradicting_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    confidence_decomposition: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class AnalysisZooResult:
    run: dict[str, Any]
    opinions: list[dict[str, Any]]
    consensus: dict[str, Any]


