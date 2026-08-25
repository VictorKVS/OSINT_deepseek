from pathlib import Path


def test_programmer_book_candidate_reduction_is_conservative_and_review_gated():
    text = Path("scripts/reduce_programmer_book_candidates.py").read_text(encoding="utf-8")
    assert "PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES.json" in text
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json" in text
    assert "PROGRAMMER_BOOK_CANDIDATES_HOLD.json" in text
    assert "MAIN_ANALYST_REVIEW_REQUIRED" in text
    assert "HELD_LOW_PRIORITY_NOT_DISCARDED" in text
    assert '"kb_auto_promotion": False' in text
    assert "supporting_source_count" in text
    assert "review_score" in text
    assert "TYPE_CAP" in text
    assert "TYPE_WEIGHT" in text
    assert "No semantic equivalence is asserted" in text


def test_claim_candidates_are_capped_and_high_value_types_have_higher_weight():
    text = Path("scripts/reduce_programmer_book_candidates.py").read_text(encoding="utf-8")
    assert '"CLAIM_CANDIDATE": 160' in text
    assert '"PATTERN_CANDIDATE": 100' in text
    assert '"TRADEOFF_CANDIDATE": 98' in text
    assert '"PRINCIPLE_CANDIDATE": 96' in text
    assert '"CLAIM_CANDIDATE": 40' in text


def test_programmer_book_candidate_reduction_launcher_exists():
    text = Path("RUN_PROGRAMMER_BOOK_KB_REDUCE.cmd").read_text(encoding="utf-8")
    assert "reduce_programmer_book_candidates.py" in text
    assert "LATEST_PROGRAMMER_BOOK_REDUCTION.json" in text
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json" in text
    assert "PROGRAMMER_BOOK_CANDIDATES_HOLD.json" in text
