from pathlib import Path


def test_programmer_book_deep_analysis_uses_existing_corpus_and_architecture_analyst():
    text = Path("scripts/process_programmer_books_deep.py").read_text(encoding="utf-8")
    assert "BookCorpusBuilder" in text
    assert "ArchitectureBookAnalyst" in text
    assert "process_programming_kb_sources as source_processor" in text
    assert "IDENTITY_SOURCE_LANGUAGE" in text
    assert '"MAIN_ANALYST_REVIEW_REQUIRED"' in text
    assert '"kb_auto_promotion": False' in text
    for candidate_type in (
        "PRINCIPLE_CANDIDATE",
        "PATTERN_CANDIDATE",
        "TRADEOFF_CANDIDATE",
        "DECISION_CRITERION_CANDIDATE",
        "FAILURE_MODE_CANDIDATE",
        "EXAMPLE_CANDIDATE",
        "CLAIM_CANDIDATE",
    ):
        # Candidate types are produced by ArchitectureBookAnalyst and preserved
        # in the aggregate counter/report contract.
        assert "candidate_type_counts" in text


def test_programmer_book_deep_launcher_exists():
    text = Path("RUN_PROGRAMMER_BOOK_KB_DEEP.cmd").read_text(encoding="utf-8")
    assert "process_programmer_books_deep.py" in text
    assert "LATEST_PROGRAMMER_BOOK_DEEP_ANALYSIS.json" in text
    assert "PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES.json" in text
