from __future__ import annotations

from dataclasses import dataclass

from father_osint.protocol import DecisionRecord, ResearchRequest, SearchPlan


TELEGRAM_KB_REFS = [
    "SIKB.telegram.source-playbook.v0.1",
    "EC-004.search-intelligence-kb",
    "information-evidence-standard.v1",
]


@dataclass(slots=True)
class PlannedSearch:
    plan: SearchPlan
    decision_record: DecisionRecord


class DeterministicTelegramSearchPlanner:
    """First deterministic OSINT_EXPERT planner for the Telegram source class.

    It does not infer which real-world sources are sufficient for the truth of a
    hypothesis. It produces an auditable acquisition plan for the information
    need supplied by ANALYST and explicitly records Telegram-only limitations.
    """

    algorithm_version = "telegram-search-plan-v1"
    knowledge_version = "telegram-sikb-v0.1"

    def plan(self, request: ResearchRequest) -> PlannedSearch:
        questions = [item.strip() for item in request.research_questions if item.strip()]
        if not questions:
            raise ValueError("ResearchRequest has no usable research questions")

        gaps = [f"Evidence required for research question: {question}" for question in questions]

        methods = [
            "telegram_source_reconnaissance",
            "bounded_historical_collection",
            "provenance_preserving_capture",
            "duplicate_and_repost_detection",
            "timeline_reconstruction",
            "counter_evidence_keyword_search",
        ]

        sequence = [
            "Inventory configured Telegram sources and record accessibility/failures",
            "Run bounded reconnaissance sample across accessible sources",
            "Extract recurring entities, terms, links, forwards and candidate origin sources",
            "Refine Telegram search terms from reconnaissance findings",
            "Collect relevant messages within the requested time window when supplied",
            "Preserve raw payload, message identity, publication/observation time and provenance",
            "Separate duplicate/repost propagation from independent corroboration",
            "Search for contradictory statements and alternative explanations",
            "Assess source/time coverage and report unresolved gaps",
            "Return EvidencePackage to ANALYST without asserting the research hypothesis as fact",
        ]

        expected_coverage = [
            "configured Telegram sources attempted",
            "accessible versus failed sources reported",
            "message/time coverage reported",
            "origin/repost relationships recorded when observable",
            "contradictions and unverified leads retained",
        ]

        verification = [
            "preserve stable chat_id/message_id or source locator",
            "preserve content hash and collection timestamp",
            "treat repeated/reposted content as propagation until independence is established",
            "retain contradictory material",
            "label external factual claims as unverified until corroborated beyond source assertion",
        ]

        limitations = [
            "Telegram-only acquisition cannot by itself establish facts that require non-Telegram primary or independent sources",
            "Configured channels are a bounded source universe and do not imply complete Telegram coverage",
            "Deleted, private, inaccessible or historically unavailable messages may create unobservable gaps",
        ]

        if request.required_sufficiency in {"GOOD", "DESIRABLE"}:
            limitations.append(
                "Requested sufficiency may require additional source classes; this planner currently covers Telegram acquisition only"
            )

        plan = SearchPlan(
            case_id=request.case_id,
            request_id=request.request_id,
            information_gaps=gaps,
            source_classes=["telegram"],
            methods=methods,
            search_sequence=sequence,
            expected_coverage=expected_coverage,
            verification_approach=verification,
            alternatives_considered=[
                "unbounded Telegram collection rejected because acquisition must remain bounded and auditable",
                "treating post count as sufficiency rejected because repetition does not equal independent corroboration",
            ],
            limitations=limitations,
            risks=[
                "source selection bias",
                "repost amplification mistaken for corroboration",
                "historical gaps caused by inaccessible/deleted content",
            ],
            knowledge_refs=list(TELEGRAM_KB_REFS),
            tool_capabilities=[
                "telegram_history_collection",
                "telegram_message_identity",
                "telegram_provenance_capture",
                "telegram_checkpoint_resume",
            ],
            expected_sufficiency=request.required_sufficiency,
            knowledge_gap=False,
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )

        decision = DecisionRecord(
            case_id=request.case_id,
            role_id="OSINT_EXPERT",
            decision="PROPOSE_TELEGRAM_SEARCH_PLAN",
            input_refs=[request.request_id],
            knowledge_refs=list(TELEGRAM_KB_REFS),
            method_refs=methods,
            reason_codes=[
                "TELEGRAM_AVAILABLE_SOURCE_CLASS",
                "PROVENANCE_REQUIRED",
                "BOUNDED_COLLECTION_REQUIRED",
                "COUNTER_EVIDENCE_REQUIRED",
            ],
            alternatives_considered=list(plan.alternatives_considered),
            uncertainties=[
                "actual configured source coverage is unknown until reconnaissance executes",
                "non-Telegram corroboration needs cannot be resolved by this source-specific planner",
            ],
            limitations=list(plan.limitations),
            output_refs=[plan.search_plan_id],
            algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )

        return PlannedSearch(plan=plan, decision_record=decision)
