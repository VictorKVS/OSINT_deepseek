from pathlib import Path


def test_main_analyst_case_builder_preserves_provenance_and_no_auto_promotion():
    text = Path("scripts/build_programmer_book_main_analyst_cases.py").read_text(encoding="utf-8")
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json" in text
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_QUEUE.json" in text
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_HOLD.json" in text
    assert '"semantic_equivalence_asserted": False' in text
    assert '"conflict_asserted": False' in text
    assert '"kb_auto_promotion": False' in text
    assert '"supporting_source_ids"' in text
    assert '"source_text_sha256"' in text
    assert '"translated_text_sha256"' in text
    assert '"potential_conflict_signal"' in text
    assert "HEURISTIC_POLARITY_MIX_ONLY" in text


def test_main_analyst_case_builder_has_bounded_type_caps_and_review_questions():
    text = Path("scripts/build_programmer_book_main_analyst_cases.py").read_text(encoding="utf-8")
    assert "TYPE_CAP" in text
    for candidate_type in (
        "PATTERN_CANDIDATE",
        "TRADEOFF_CANDIDATE",
        "PRINCIPLE_CANDIDATE",
        "DECISION_CRITERION_CANDIDATE",
        "FAILURE_MODE_CANDIDATE",
        "DEFINITION_CANDIDATE",
        "CLAIM_CANDIDATE",
    ):
        assert candidate_type in text
    assert "Do sources actually agree, complement each other, or conflict?" in text
    assert "Can a bounded Golden Candidate be formed" in text


def test_main_analyst_case_launcher_exists():
    text = Path("RUN_PROGRAMMER_BOOK_MAIN_ANALYST_CASES.cmd").read_text(encoding="utf-8")
    assert "build_programmer_book_main_analyst_cases.py" in text
    assert "LATEST_PROGRAMMER_BOOK_MAIN_ANALYST_CASES.json" in text
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_QUEUE.json" in text
