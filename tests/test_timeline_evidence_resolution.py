from __future__ import annotations

from father_osint.timeline_evidence_resolution import resolve_official_evidence_request


def _request(basis: str, required: list[str], dates: list[str] | None = None) -> dict[str, object]:
    return {
        "evidence_request_id": "OER-test",
        "timeline_event_id": "GTE-test",
        "document_id": "DOC-RU-FZ-152-2006",
        "amending_act_number": "420-ФЗ",
        "amending_act_date": "2024-11-30",
        "effective_date_basis": basis,
        "effective_dates": dates or [],
        "required_official_evidence": required,
    }


def _proof(*, tier: str = "A0_OFFICIAL_PUBLICATION", publication_date: str | None = None) -> dict[str, object]:
    proof: dict[str, object] = {
        "evidence_id": "A0-EVID-420",
        "proof_available": True,
        "trust_tier": tier,
        "artifact_sha256": "a" * 64,
        "document_number": "420-ФЗ",
        "document_date": "2024-11-30",
        "verified_evidence": [
            "AMENDING_ACT_IDENTITY",
            "AMENDING_ACT_OFFICIAL_TEXT",
            "EFFECTIVE_RULE",
        ],
    }
    if publication_date is not None:
        proof["official_publication_date"] = publication_date
        proof["verified_evidence"] = [*proof["verified_evidence"], "OFFICIAL_PUBLICATION_DATE"]
    return proof


def test_explicit_effective_date_confirms_only_with_complete_a0_a1_evidence():
    request = _request(
        "EXPLICIT_CALENDAR_DATE",
        ["AMENDING_ACT_IDENTITY", "AMENDING_ACT_OFFICIAL_TEXT", "EFFECTIVE_RULE", "EXPLICIT_EFFECTIVE_DATE"],
        ["2024-12-01"],
    )
    proof = _proof()
    proof["verified_evidence"] = [*proof["verified_evidence"], "EXPLICIT_EFFECTIVE_DATE"]

    result = resolve_official_evidence_request(request, official_proofs=[proof])

    assert result["status"] == "OFFICIAL_EVIDENCE_CONFIRMED"
    assert result["confirmed_effective_dates"] == ["2024-12-01"]
    assert result["timeline_source_remains_non_evidentiary"] is True
    assert result["legal_truth_promoted"] is False


def test_publication_relative_rule_exposes_verified_publication_date_without_inventing_effective_date():
    request = _request(
        "RELATIVE_TO_OFFICIAL_PUBLICATION",
        ["AMENDING_ACT_IDENTITY", "AMENDING_ACT_OFFICIAL_TEXT", "EFFECTIVE_RULE", "OFFICIAL_PUBLICATION_DATE"],
    )
    result = resolve_official_evidence_request(
        request,
        official_proofs=[_proof(publication_date="2024-11-30")],
    )

    assert result["status"] == "OFFICIAL_EVIDENCE_CONFIRMED"
    assert result["official_publication_date"] == "2024-11-30"
    assert result["confirmed_effective_dates"] == []
    assert result["effective_date_resolution_state"] == "READY_FOR_LEGAL_RULE_EVALUATION"


def test_non_official_or_identity_mismatched_proof_cannot_satisfy_oer():
    request = _request(
        "RELATIVE_TO_OFFICIAL_PUBLICATION",
        ["AMENDING_ACT_IDENTITY", "AMENDING_ACT_OFFICIAL_TEXT", "EFFECTIVE_RULE", "OFFICIAL_PUBLICATION_DATE"],
    )
    a2 = _proof(tier="A2_CONSOLIDATED_REFERENCE", publication_date="2024-11-30")
    wrong = _proof(publication_date="2024-11-30")
    wrong["document_number"] = "999-ФЗ"

    result = resolve_official_evidence_request(request, official_proofs=[a2, wrong])

    assert result["status"] == "OFFICIAL_EVIDENCE_PENDING"
    assert result["evidence_complete"] is False
    assert result["matched_official_evidence_ids"] == []
    assert "OFFICIAL_PUBLICATION_DATE" in result["missing_official_evidence"]
