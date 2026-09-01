from __future__ import annotations

from typing import Any, Iterable

from .analysis_builtins import evidence_lineage_analyzer, graph_contrarian_analyzer
from .analysis_models import AnalysisZooResult, AnalyzerCallable, AnalyzerDraft, AnalyzerSpec
from .canonical import sha256_json, utc_now_iso
from .policy import strictest_access_class
from .store import WorkbenchStore

class AnalysisZoo:
    """Governed multi-analyzer gateway.

    Analyzers return independent opinions. This class never promotes an opinion
    to FACT and never hides dissent. Remote analyzers are blocked for data classes
    outside their declared boundary.
    """

    version = "analysis-zoo/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store
        self._registry: dict[str, tuple[AnalyzerSpec, AnalyzerCallable]] = {}
        self.register(
            AnalyzerSpec(
                analyzer_id="builtin-evidence-lineage",
                family="DETERMINISTIC_RULE",
                version="0.1.0",
                modality=("METADATA", "TEXT"),
                known_limitations=("Checks object lineage and capture availability, not real-world truth.",),
            ),
            lambda case_id, task, inputs: evidence_lineage_analyzer(self.store, case_id, task, inputs),
        )
        self.register(
            AnalyzerSpec(
                analyzer_id="builtin-graph-contrarian",
                family="GRAPH_ALGORITHM",
                version="0.1.0",
                modality=("GRAPH", "METADATA"),
                known_limitations=("Graph structure cannot establish causation, control or wrongdoing.",),
            ),
            lambda case_id, task, inputs: graph_contrarian_analyzer(self.store, case_id, task, inputs),
        )

    def register(self, spec: AnalyzerSpec, runner: AnalyzerCallable) -> None:
        if not spec.analyzer_id.strip():
            raise ValueError("analyzer_id must not be empty")
        if spec.analyzer_id in self._registry:
            raise ValueError(f"analyzer already registered: {spec.analyzer_id}")
        self._registry[spec.analyzer_id] = (spec, runner)

    def list_analyzers(self) -> list[AnalyzerSpec]:
        return [item[0] for item in self._registry.values()]

    def run(
        self,
        case_id: str,
        *,
        task: str,
        input_refs: Iterable[str],
        analyzer_ids: Iterable[str] = ("builtin-evidence-lineage", "builtin-graph-contrarian"),
        prompt_template_sha256: str | None = None,
    ) -> AnalysisZooResult:
        refs = list(dict.fromkeys(str(item) for item in input_refs if str(item).strip()))
        selected = list(dict.fromkeys(str(item) for item in analyzer_ids if str(item).strip()))
        if not refs:
            raise ValueError("analysis requires input_refs")
        if len(selected) < 2:
            raise ValueError("analysis zoo requires at least two analyzers")
        if len(task.strip()) < 5:
            raise ValueError("analysis task is too short")

        inputs = [self.store.find_by_ref(case_id, ref) for ref in refs]
        access_class = strictest_access_class(
            self.store.get_case(case_id)["access_class"],
            *(str(payload.get("access_class", "PUBLIC")) for _, payload in inputs),
        )
        specs: list[AnalyzerSpec] = []
        for analyzer_id in selected:
            if analyzer_id not in self._registry:
                raise ValueError(f"unknown analyzer: {analyzer_id}")
            spec = self._registry[analyzer_id][0]
            if access_class not in spec.allowed_access_classes:
                raise PermissionError(f"{analyzer_id} cannot process access class {access_class}")
            if spec.data_boundary in {"REMOTE_PUBLIC_ONLY", "REMOTE_REDACTED"} and access_class != "PUBLIC":
                raise PermissionError(f"{analyzer_id} remote boundary blocks {access_class} input")
            specs.append(spec)
        family_count = len({spec.family for spec in specs})
        if family_count < 2:
            raise ValueError("at least two independent analyzer families are required")

        task_id = self.store._allocate_id(case_id, "TASK")
        run_id = self.store._allocate_id(case_id, "ARUN")
        started_at = utc_now_iso()
        input_bundle = [{"kind": kind, "object": payload} for kind, payload in inputs]
        bundle_hash = sha256_json(input_bundle)
        opinions: list[dict[str, Any]] = []

        for spec in specs:
            runner = self._registry[spec.analyzer_id][1]
            draft = runner(case_id, task, inputs)
            limitations = list(dict.fromkeys([*draft.limitations, *spec.known_limitations]))
            if not limitations:
                limitations = ["Automated opinion is not an established fact and requires human review."]
            confidence = self._normalize_confidence(draft.confidence_decomposition)
            opinion_id = self.store._allocate_id(case_id, "OPN")
            opinion: dict[str, Any] = {
                "schema_version": "father-osint.analysis-opinion.v0.1",
                "opinion_id": opinion_id,
                "run_id": run_id,
                "case_id": case_id,
                "task_id": task_id,
                "analyzer_id": spec.analyzer_id,
                "analyzer_family": spec.family,
                "analyzer_version": spec.version,
                "modality": list(spec.modality),
                "output_class": draft.output_class,
                "answer": draft.answer,
                "supporting_refs": list(dict.fromkeys(draft.supporting_refs)),
                "contradicting_refs": list(dict.fromkeys(draft.contradicting_refs)),
                "assumptions": list(dict.fromkeys(draft.assumptions)),
                "limitations": limitations,
                "confidence_decomposition": confidence,
                "data_boundary": spec.data_boundary,
                "access_class": access_class,
                "generated_at_utc": utc_now_iso(),
                "output_sha256": "",
                "can_create_fact": False,
            }
            opinion["output_sha256"] = sha256_json(opinion, exclude_fields={"output_sha256"})
            self.store.save_object(case_id, "analysis_opinion", opinion)
            opinions.append(opinion)

        completed_at = utc_now_iso()
        run = {
            "schema_version": "father-osint.analysis-run.v0.1",
            "run_id": run_id,
            "case_id": case_id,
            "task_id": task_id,
            "task": task.strip(),
            "input_refs": refs,
            "input_bundle_sha256": bundle_hash,
            "analyzer_ids": selected,
            "independent_first_pass": True,
            "started_at_utc": started_at,
            "completed_at_utc": completed_at,
            "policy_decision": "ALLOW",
            "fact_promotion_allowed": False,
            "prompt_template_sha256": prompt_template_sha256,
            "notes": [
                "Each analyzer executed independently over the same immutable object bundle.",
                "Opinions remain candidates and cannot create FACT.",
            ],
        }
        self.store.save_object(case_id, "analysis_run", run)

        consensus_id = self.store._allocate_id(case_id, "CNS")
        answer_positions = list(dict.fromkeys(item["answer"] for item in opinions))
        disagreements: list[dict[str, Any]] = []
        if len(answer_positions) > 1:
            disagreements.append(
                {
                    "question": task.strip(),
                    "positions": answer_positions,
                    "likely_cause": "Analyzers have different roles, methods and failure modes.",
                    "required_next_action": "Human analyst must compare each position with the cited evidence and unresolved gaps.",
                }
            )
        output_classes = {item["output_class"] for item in opinions}
        recommended_status = (
            "RESEARCH_MORE"
            if "CONTRADICTION_CANDIDATE" in output_classes or output_classes == {"NO_CONCLUSION"}
            else "HYPOTHESIS_CANDIDATE"
        )
        consensus = {
            "schema_version": "father-osint.consensus.v0.1",
            "consensus_id": consensus_id,
            "case_id": case_id,
            "task_id": task_id,
            "opinion_ids": [item["opinion_id"] for item in opinions],
            "method": "EVIDENCE_WEIGHTED",
            "independent_family_count": family_count,
            "common_ground": [
                "Automated analysis cannot create FACT.",
                "Every conclusion must remain linked to preserved input references.",
            ],
            "disagreements": disagreements,
            "minority_views": answer_positions[1:] if len(answer_positions) > 1 else [],
            "unresolved_questions": [
                "Has a human reviewer checked the cited evidence and alternative explanations?",
                "Are source independence and object identity sufficiently established?",
            ],
            "recommended_status": recommended_status,
            "human_review_required": True,
            "human_decision": "PENDING",
        }
        self.store.save_object(case_id, "consensus", consensus)
        self.store.append_journal(
            case_id,
            actor_id="analysis-zoo",
            actor_type="AGENT",
            action_type="ANALYZE",
            stream="RED_TEAM_SOURCE_QUALITY",
            query_or_action=task.strip(),
            result_code="REVIEWED",
            result_summary=(
                f"Produced {len(opinions)} independent opinions from {family_count} analyzer families; "
                f"recommended_status={recommended_status}; human decision=PENDING."
            ),
            new_findings=[],
            next_pivots=list(consensus["unresolved_questions"]),
            access_class=access_class,
            actor_version=self.version,
        )
        return AnalysisZooResult(run=run, opinions=opinions, consensus=consensus)

    @staticmethod
    def _normalize_confidence(values: dict[str, float]) -> dict[str, float]:
        defaults = {
            "authority": 0.5,
            "directness": 0.5,
            "independence": 0.5,
            "corroboration": 0.0,
            "recency": 0.5,
            "ambiguity": 0.5,
            "bias_risk": 0.5,
            "contradiction_severity": 0.0,
        }
        for key, value in values.items():
            if key in defaults:
                defaults[key] = max(0.0, min(1.0, float(value)))
        return defaults


__all__ = ["AnalysisZoo", "AnalysisZooResult", "AnalyzerCallable", "AnalyzerDraft", "AnalyzerSpec"]
