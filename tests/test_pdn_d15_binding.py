from copy import deepcopy

from scripts.promote_pdn_d15 import (
    _request_matches_result,
    _sha256_json,
    _validate_result_integrity,
)


def _valid_result():
    decisions = [
        {
            "decision_id": "RULE-D6",
            "scope_type": "RULE_CLASS",
            "stage": "D6",
            "scope_key": "terms",
            "decision": "ACCEPT",
            "reviewer": "reviewer-1",
            "reason": "checked",
        },
        {
            "decision_id": "D12-1",
            "scope_type": "CONFLICT_CANDIDATE",
            "stage": "D12",
            "scope_key": "candidate-1",
            "decision": "OVERLAP_ONLY",
            "reviewer": "reviewer-1",
            "reason": "checked",
        },
    ]
    return {
        "record_type": "D14_EXPERT_REVIEW_RESULT",
        "corpus_id": "pdn-official-v1",
        "packet_sha256": "a" * 64,
        "decisions_sha256": _sha256_json(decisions),
        "required_decisions": 2,
        "resolved_decisions": 2,
        "accepted_rule_classes": 1,
        "rejected_rule_classes": 0,
        "conflict_overlap_decisions": 1,
        "decisions": decisions,
        "d14_state": "VERIFIED",
        "autonomous_kb_promotion": False,
    }


def _valid_request(result):
    return {
        "record_type": "D15_PROMOTION_REQUEST",
        "corpus_id": result["corpus_id"],
        "packet_sha256": result["packet_sha256"],
        "decisions_sha256": result["decisions_sha256"],
        "accepted_rule_decision_ids": ["RULE-D6"],
        "rejected_rule_decision_ids": [],
        "conflict_overlap_decisions": [deepcopy(result["decisions"][1])],
        "request_state": "AWAITING_EXPLICIT_D15_APPROVAL",
        "autonomous_kb_promotion": False,
    }


def test_d15_result_integrity_rejects_decision_content_tampering():
    result = _valid_result()
    assert _validate_result_integrity(result) == (True, "")

    tampered = deepcopy(result)
    tampered["decisions"][0]["decision"] = "REJECT"
    assert _validate_result_integrity(tampered) == (
        False,
        "D15_D14_DECISIONS_CONTENT_HASH_MISMATCH",
    )


def test_d15_request_must_be_bound_to_the_exact_d14_result():
    result = _valid_result()
    request = _valid_request(result)
    assert _request_matches_result(request, result) == (True, "")

    tampered = deepcopy(request)
    tampered["corpus_id"] = "another-corpus"
    assert _request_matches_result(tampered, result) == (
        False,
        "D15_CORPUS_ID_MISMATCH",
    )


def test_d15_request_rejects_conflict_decision_drift():
    result = _valid_result()
    request = _valid_request(result)
    request["conflict_overlap_decisions"][0]["decision"] = "NOT_CONFLICT"

    assert _request_matches_result(request, result) == (
        False,
        "D15_CONFLICT_DECISION_BINDING_MISMATCH",
    )
