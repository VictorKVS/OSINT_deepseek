from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable
from urllib.parse import urlparse
from uuid import uuid4
import re

from father_osint.models import Material, MaterialPackage, utc_now_iso
from father_osint.protocol import DecisionRecord, SearchPlan

URL_RE = re.compile(r"https?://[^\s)\]>]+")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9_@#.-]{4,}")
STOPWORDS = {"this","that","with","from","have","will","your","about","https","http","telegram","котор","этот","этой","того","для","как","что","это","при","или","они","она","его","также","their","there"}

@dataclass(slots=True)
class ReconnaissanceReport:
    case_id: str
    search_plan_id: str
    package_id: str
    sampled_material_refs: list[str]
    source_landscape: list[dict]
    top_terms: list[dict]
    domains: list[dict]
    forward_candidates: list[dict]
    gaps: list[str]
    refinement_actions: list[str]
    marginal_value: str
    stop_recommended: bool
    report_id: str = field(default_factory=lambda: str(uuid4()))
    algorithm_version: str = "telegram-recon-v1"
    created_at: str = field(default_factory=utc_now_iso)

@dataclass(slots=True)
class ReconnaissanceResult:
    report: ReconnaissanceReport
    refined_plan: SearchPlan
    decision_record: DecisionRecord

class DeterministicTelegramReconnaissance:
    algorithm_version = "telegram-recon-v1"
    knowledge_version = "telegram-sikb-v0.1"

    def run(self, plan: SearchPlan, package: MaterialPackage, *, sample_limit: int = 25, previous_terms: Iterable[str] = ()) -> ReconnaissanceResult:
        if sample_limit <= 0:
            raise ValueError("sample_limit must be > 0")
        materials = package.materials[:sample_limit]
        source_counts = Counter()
        terms = Counter()
        domains = Counter()
        forwards = Counter()
        for m in materials:
            source_key = str(m.metadata.get("chat_id") or m.title or m.source_locator)
            source_counts[source_key] += 1
            text = m.raw_text or ""
            for raw in WORD_RE.findall(text.lower()):
                token = raw.strip(".,:;!?()[]{}\"'")
                if len(token) >= 4 and token not in STOPWORDS and not token.startswith("http"):
                    terms[token] += 1
            for url in URL_RE.findall(text):
                host = (urlparse(url).hostname or "").lower()
                if host:
                    domains[host] += 1
            fwd = m.metadata.get("forward_from") or m.metadata.get("forward_origin") or m.metadata.get("forward_sender_name")
            if fwd:
                forwards[str(fwd)] += 1

        previous = {x.lower() for x in previous_terms}
        top = terms.most_common(12)
        novel = [t for t, _ in top if t not in previous]
        gaps = []
        if not materials:
            gaps.append("Reconnaissance sample is empty")
        if len(source_counts) < 2:
            gaps.append("Reconnaissance covers fewer than two observable Telegram sources")
        if not domains:
            gaps.append("No external domains observed in reconnaissance sample")
        if not forwards:
            gaps.append("No explicit forward-origin metadata observed in reconnaissance sample")

        if not materials:
            marginal = "NONE"
            stop = True
        elif previous and not novel:
            marginal = "LOW"
            stop = True
        elif len(novel) <= 2:
            marginal = "LOW"
            stop = False
        else:
            marginal = "USEFUL"
            stop = False

        actions = [f"Add reconnaissance term '{t}' to targeted follow-up search" for t in novel[:5]]
        if domains:
            actions.append("Prioritize observed external domains as candidate origin/corroboration leads")
        if forwards:
            actions.append("Trace observed forward origins before treating repeated messages as independent corroboration")
        if not actions:
            actions.append("Retain current plan; reconnaissance produced no justified expansion")

        report = ReconnaissanceReport(
            case_id=plan.case_id,
            search_plan_id=plan.search_plan_id,
            package_id=package.package_id,
            sampled_material_refs=[m.material_id for m in materials],
            source_landscape=[{"source": k, "sample_items": v} for k, v in source_counts.most_common()],
            top_terms=[{"term": k, "count": v} for k, v in top],
            domains=[{"domain": k, "count": v} for k, v in domains.most_common()],
            forward_candidates=[{"origin": k, "count": v} for k, v in forwards.most_common()],
            gaps=gaps,
            refinement_actions=actions,
            marginal_value=marginal,
            stop_recommended=stop,
        )

        refined = SearchPlan(
            case_id=plan.case_id, request_id=plan.request_id,
            information_gaps=list(plan.information_gaps), source_classes=list(plan.source_classes),
            methods=list(plan.methods), search_sequence=list(plan.search_sequence) + ["Apply G6 reconnaissance refinements before deep collection"],
            expected_coverage=list(plan.expected_coverage), verification_approach=list(plan.verification_approach),
            alternatives_considered=list(plan.alternatives_considered), limitations=list(plan.limitations), risks=list(plan.risks),
            knowledge_refs=list(plan.knowledge_refs), tool_capabilities=list(plan.tool_capabilities), expected_sufficiency=plan.expected_sufficiency,
            knowledge_gap=plan.knowledge_gap, algorithm_version=f"{plan.algorithm_version}+g6-refinement-v1",
            knowledge_version=plan.knowledge_version, search_plan_id=plan.search_plan_id, version=plan.version + 1,
        )
        refined.information_gaps.extend(report.gaps)
        refined.search_sequence.extend(report.refinement_actions)

        decision = DecisionRecord(
            case_id=plan.case_id, role_id="OSINT_EXPERT", decision="REFINE_SEARCH_PLAN_AFTER_RECONNAISSANCE",
            input_refs=[plan.search_plan_id, package.package_id], knowledge_refs=list(plan.knowledge_refs),
            method_refs=["telegram_bounded_reconnaissance", "marginal_value_check"],
            reason_codes=["RECON_SAMPLE_ANALYZED", "REFINEMENT_BEFORE_DEEP_COLLECTION"],
            uncertainties=list(report.gaps), limitations=["Reconnaissance describes observed sample, not the whole Telegram universe"],
            output_refs=[report.report_id, refined.search_plan_id], algorithm_version=self.algorithm_version,
            knowledge_version=self.knowledge_version,
        )
        return ReconnaissanceResult(report=report, refined_plan=refined, decision_record=decision)
