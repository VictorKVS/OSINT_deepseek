from __future__ import annotations

import hashlib
from typing import Any, Iterable


def _norm_number(value: object) -> str:
    return str(value or "").casefold().replace("ё", "е").replace("–", "-").replace("—", "-").replace(" ", "")


def _norm_date(value: object) -> str:
    return str(value or "").strip().casefold()


def _official_tier(value: object) -> bool:
    tier = str(value or "").strip().upper()
    return tier in {"A0", "A1"} or tier.startswith("A0_") or tier.startswith("A1_")


def _stable_id(*parts: object) -> str:
    canonical = "\x1f".join(" ".join(str(part).split()).casefold() for part in parts)
    return "OERRES-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]


def _matches(request: dict[str, Any], proof: dict[str, Any]) -> bool:
    proof_number = proof.get("amending_act_number") or proof.get("document_number") or proof.get("number")
    proof_date = proof.get("amending_act_date") or proof.get("document_date") or proof.get("date")
    return (
        bool(_norm_number(request.get("amending_act_number")))
        and _norm_number(request.get("amending_act_number")) == _norm_number(proof_number)
        and _norm_date(request.get("amending_act_date")) == _norm_date(proof_date)
    )


def resolve_official_evidence_request(
    request: dict[str, Any],
    *,
    official_proofs: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Resolve one OER only from independently verified A0/A1 proof records.

    GARANT remains navigation metadata. Publication-relative rules expose the
    verified publication date but do not calculate a final effective date here.
    """

    matches = [
        proof for proof in official_proofs
        if proof.get("proof_available") is True
        and _official_tier(proof.get("trust_tier"))
        and str(proof.get("artifact_sha256") or "").strip()
        and _matches(request, proof)
    ]
    verified: set[str] = set()
    for proof in matches:
        values = proof.get("verified_evidence") or []
        if isinstance(values, (list, tuple, set)):
            verified.update(str(value) for value in values)

    required = [str(value) for value in (request.get("required_official_evidence") or [])]
    missing = [value for value in required if value not in verified]
    evidence_ids = sorted({
        str(proof.get("evidence_id") or proof.get("proof_id") or "").strip()
        for proof in matches
        if str(proof.get("evidence_id") or proof.get("proof_id") or "").strip()
    })
    artifact_hashes = sorted({str(proof["artifact_sha256"]).strip().lower() for proof in matches})
    publication_dates = sorted({
        str(proof.get("official_publication_date") or "").strip()
        for proof in matches
        if str(proof.get("official_publication_date") or "").strip()
    })

    basis = str(request.get("effective_date_basis") or "")
    complete = bool(matches) and not missing
    state = "EVIDENCE_INCOMPLETE"
    confirmed_dates: list[str] = []
    official_publication_date: str | None = None

    if complete and basis == "EXPLICIT_CALENDAR_DATE":
        confirmed_dates = [str(value) for value in (request.get("effective_dates") or [])]
        state = "CONFIRMED_EXPLICIT_CALENDAR_DATE"
    elif complete and basis == "RELATIVE_TO_OFFICIAL_PUBLICATION":
        if len(publication_dates) == 1 and "OFFICIAL_PUBLICATION_DATE" in verified:
            official_publication_date = publication_dates[0]
            state = "READY_FOR_LEGAL_RULE_EVALUATION"
        else:
            complete = False
            state = "PUBLICATION_DATE_AMBIGUOUS_OR_MISSING"
            if "OFFICIAL_PUBLICATION_DATE" not in missing:
                missing.append("OFFICIAL_PUBLICATION_DATE")
    elif complete:
        state = "OFFICIAL_EVIDENCE_COMPLETE_RULE_NOT_CALENDAR_RESOLVED"

    request_id = str(request.get("evidence_request_id") or "")
    timeline_event_id = str(request.get("timeline_event_id") or "")
    return {
        "resolution_id": _stable_id(request_id, timeline_event_id, *evidence_ids, *artifact_hashes),
        "evidence_request_id": request_id,
        "timeline_event_id": timeline_event_id,
        "document_id": request.get("document_id"),
        "status": "OFFICIAL_EVIDENCE_CONFIRMED" if complete else "OFFICIAL_EVIDENCE_PENDING",
        "evidence_complete": complete,
        "matched_official_evidence_ids": evidence_ids,
        "matched_official_artifact_sha256": artifact_hashes,
        "verified_official_evidence": sorted(verified),
        "missing_official_evidence": missing,
        "effective_date_basis": basis,
        "confirmed_effective_dates": confirmed_dates,
        "official_publication_date": official_publication_date,
        "effective_date_resolution_state": state,
        "timeline_source_remains_non_evidentiary": True,
        "legal_truth_promoted": False,
    }


def resolve_official_evidence_requests(
    requests: Iterable[dict[str, Any]],
    *,
    official_proofs: Iterable[dict[str, Any]],
) -> tuple[dict[str, Any], ...]:
    proof_list = list(official_proofs)
    return tuple(
        resolve_official_evidence_request(request, official_proofs=proof_list)
        for request in requests
    )
