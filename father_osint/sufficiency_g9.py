from __future__ import annotations

from copy import deepcopy

from father_osint.counter_evidence import CounterEvidenceAssessmentResult
from father_osint.evidence_quality import EvidenceQualityResult
from father_osint.protocol import EvidencePackage
from father_osint.sufficiency import (
    DeterministicResearchSufficiencyAssessor,
    ResearchSufficiencyResult,
)


class LineageBoundResearchSufficiencyAssessor:
    """G9 compatibility wrapper around the accepted G8 sufficiency policy.

    The G8 assessor accepts a coverage signal named `counter_evidence_searched`.
    G9 makes that signal trustworthy: caller-supplied values are ignored and the
    value is derived only from an auditable CounterEvidenceAssessmentResult.
    """

    algorithm_version = "research-sufficiency-g9-lineage-v1"

    def __init__(self) -> None:
        self._base = DeterministicResearchSufficiencyAssessor()

    def assess(
        self,
        package: EvidencePackage,
        *,
        quality: EvidenceQualityResult | None = None,
        counter_evidence: CounterEvidenceAssessmentResult | None = None,
    ) -> ResearchSufficiencyResult:
        trusted_package = deepcopy(package)
        trusted_package.coverage = dict(trusted_package.coverage or {})

        # Never trust a naked boolean supplied by collection/reconnaissance code.
        trusted_package.coverage["counter_evidence_searched"] = False
        counter_decision_id: str | None = None

        if counter_evidence is not None:
            assessment = counter_evidence.assessment
            if assessment.case_id != package.case_id or assessment.request_id != package.request_id:
                raise ValueError("counter-evidence assessment does not belong to this case/request")
            trusted_package.coverage["counter_evidence_searched"] = assessment.status in {
                "SEARCHED",
                "NOT_APPLICABLE",
            }
            counter_decision_id = counter_evidence.decision_record.decision_id

        result = self._base.assess(trusted_package, quality=quality)
        result.decision_record.algorithm_version = self.algorithm_version
        result.decision_record.method_refs.append("g9.counter-evidence-lineage-required-v1")
        result.decision_record.limitations.append(
            "counter_evidence_searched is derived only from a G9 assessment; bare coverage flags are ignored"
        )
        if counter_decision_id:
            result.decision_record.input_refs.append(counter_decision_id)
        return result
