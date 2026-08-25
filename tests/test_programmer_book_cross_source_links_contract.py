from pathlib import Path


def test_cross_source_link_builder_is_conservative_and_traceable():
    text = Path("scripts/build_programmer_book_cross_source_links.py").read_text(encoding="utf-8")
    assert "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json" in text
    assert "PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.json" in text
    assert "PROGRAMMER_BOOK_CROSS_SOURCE_ANALYST_QUEUE.json" in text
    assert "weighted_jaccard" in text
    assert "candidate_source_ids" in text
    assert "source_text_sha256" in text
    assert "translated_text_sha256" in text
    assert '"semantic_equivalence_asserted": False' in text
    assert '"conflict_asserted": False' in text
    assert '"kb_auto_promotion": False' in text
    assert "MAIN_ANALYST_CROSS_SOURCE_REVIEW_REQUIRED" in text


def test_cross_source_builder_requires_distinct_sources_and_bounded_queue():
    text = Path("scripts/build_programmer_book_cross_source_links.py").read_text(encoding="utf-8")
    assert "left_sources & right_sources" in text
    assert "MIN_SCORE" in text
    assert "MAX_MATCHES_PER_CANDIDATE" in text
    assert "QUEUE_CAP" in text
    assert "pairs_above_threshold_total" in text
    assert "distinct_source_pairs_total" in text
    assert "potential_conflict_links_total" in text


def test_cross_source_launcher_exists():
    text = Path("RUN_PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.cmd").read_text(encoding="utf-8")
    assert "build_programmer_book_cross_source_links.py" in text
    assert "LATEST_PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.json" in text
