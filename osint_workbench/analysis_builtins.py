from __future__ import annotations

from typing import Any

from .analysis_models import AnalyzerDraft
from .store import WorkbenchStore

def evidence_lineage_analyzer(
    store: WorkbenchStore,
    case_id: str,
    task: str,
    inputs: list[tuple[str, dict[str, Any]]],
) -> AnalyzerDraft:
    issues: list[str] = []
    supporting: list[str] = []
    contradicting: list[str] = []
    capture_sources = {item["source_id"] for item in store.list_objects(case_id, "capture")}
    for kind, payload in inputs:
        object_id = str(payload.get(store.ID_FIELDS.get(kind, ""), ""))
        if object_id:
            supporting.append(object_id)
        if kind in {"claim", "relation", "finding"}:
            for source_id in payload.get("source_ids", []):
                if source_id not in capture_sources:
                    issues.append(f"{object_id} references {source_id} without a preserved capture")
                    contradicting.append(object_id)
        if kind == "finding" and not payload.get("human_approved"):
            issues.append(f"{object_id} is not human-approved")
            contradicting.append(object_id)
    if issues:
        return AnalyzerDraft(
            output_class="CONTRADICTION_CANDIDATE",
            answer="Evidence-lineage issues detected: " + "; ".join(issues),
            supporting_refs=supporting,
            contradicting_refs=contradicting,
            assumptions=["Input object files accurately represent the current case state."],
            limitations=["Lineage completeness does not prove the underlying real-world assertion."],
            confidence_decomposition={
                "authority": 0.6,
                "directness": 0.9,
                "independence": 0.8,
                "corroboration": 0.2,
                "recency": 0.8,
                "ambiguity": 0.2,
                "bias_risk": 0.1,
                "contradiction_severity": 0.8,
            },
        )
    return AnalyzerDraft(
        output_class="NO_CONCLUSION",
        answer="No deterministic break in source/capture/object lineage was detected for the supplied references.",
        supporting_refs=supporting,
        assumptions=["All relevant case objects were supplied as input references."],
        limitations=["This check validates lineage structure, not factual truth, source authenticity or completeness."],
        confidence_decomposition={
            "authority": 0.6,
            "directness": 0.9,
            "independence": 0.8,
            "corroboration": 0.2,
            "recency": 0.8,
            "ambiguity": 0.2,
            "bias_risk": 0.1,
            "contradiction_severity": 0.0,
        },
    )

def graph_contrarian_analyzer(
    store: WorkbenchStore,
    case_id: str,
    task: str,
    inputs: list[tuple[str, dict[str, Any]]],
) -> AnalyzerDraft:
    candidate_relations = [
        payload
        for kind, payload in inputs
        if kind == "relation" and payload.get("status") in {"CANDIDATE", "DISPUTED"}
    ]
    shared_source_relations = [
        payload for payload in candidate_relations if len(payload.get("source_ids", [])) <= 1
    ]
    refs = [item["relation_id"] for item in candidate_relations]
    if candidate_relations:
        return AnalyzerDraft(
            output_class="HYPOTHESIS_CANDIDATE",
            answer=(
                f"Graph challenge: {len(candidate_relations)} candidate/disputed relation(s) require human review; "
                f"{len(shared_source_relations)} rely on no more than one recorded source."
            ),
            supporting_refs=refs,
            contradicting_refs=[item["relation_id"] for item in shared_source_relations],
            assumptions=["Only relations supplied in input_refs were evaluated."],
            limitations=[
                "Graph proximity, shared source, address, IP, certificate, contact or wallet does not establish common control.",
                "No causal, legal or attribution conclusion is produced.",
            ],
            confidence_decomposition={
                "authority": 0.5,
                "directness": 0.7,
                "independence": 0.6,
                "corroboration": 0.2,
                "recency": 0.5,
                "ambiguity": 0.6,
                "bias_risk": 0.2,
                "contradiction_severity": 0.5 if shared_source_relations else 0.2,
            },
        )
    return AnalyzerDraft(
        output_class="NO_CONCLUSION",
        answer="No candidate or disputed relation was present in the supplied graph references; no attribution conclusion is justified.",
        supporting_refs=[
            str(payload.get(store.ID_FIELDS.get(kind, ""), ""))
            for kind, payload in inputs
            if str(payload.get(store.ID_FIELDS.get(kind, ""), ""))
        ],
        assumptions=["The supplied input set is the intended bounded graph scope."],
        limitations=["Absence of candidate relations in the input set is not proof that no relationship exists."],
        confidence_decomposition={
            "authority": 0.5,
            "directness": 0.6,
            "independence": 0.6,
            "corroboration": 0.0,
            "recency": 0.5,
            "ambiguity": 0.5,
            "bias_risk": 0.2,
            "contradiction_severity": 0.0,
        },
    )
