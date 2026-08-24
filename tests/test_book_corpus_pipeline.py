from father_osint.book_corpus import BookCorpusBuilder, BookSource, BookStage
from father_osint.knowledge_analyst import DeterministicKnowledgeAnalyst


def _source() -> BookSource:
    return BookSource(
        title="Pilot Architecture Book",
        authors=["Author A"],
        source_language="en",
        target_language="ru",
        source_locator="private-library://pilot-book.pdf",
    )


def test_book_translation_alignment_preserves_original_spans() -> None:
    source = _source()
    corpus = BookCorpusBuilder().build(
        source,
        "CHAPTER 1\n\nArchitecture is a set of decisions.\n\nTrade-offs are explicit.",
    )

    assert corpus.stage == BookStage.TEXT_EXTRACTED
    assert len(corpus.translation_units) == 3
    first = corpus.translation_units[0]
    assert first.source_text == "CHAPTER 1"
    assert len(first.source_text_sha256) == 64

    translations = {
        corpus.translation_units[0].unit_id: "ГЛАВА 1",
        corpus.translation_units[1].unit_id: "Архитектура — это набор решений.",
        corpus.translation_units[2].unit_id: "Компромиссы формулируются явно.",
    }
    corpus.apply_translations(translations, method="TEST_TRANSLATOR")
    assert corpus.translation_complete is True
    assert corpus.stage == BookStage.TRANSLATION_ALIGNED

    corpus.build_semantic_structure()
    assert corpus.stage == BookStage.STRUCTURED
    assert corpus.semantic_units[0].unit_type == "HEADING"
    assert corpus.semantic_units[1].source_text == "Architecture is a set of decisions."
    assert corpus.semantic_units[1].translated_text == "Архитектура — это набор решений."


def test_incomplete_translation_fails_closed_before_semantic_structure() -> None:
    corpus = BookCorpusBuilder().build(_source(), "One paragraph.\n\nSecond paragraph.")
    corpus.apply_translations(
        {corpus.translation_units[0].unit_id: "Первый абзац."},
        method="TEST_TRANSLATOR",
        require_complete=False,
    )

    assert corpus.translation_complete is False
    assert corpus.stage == BookStage.TEXT_EXTRACTED

    try:
        corpus.build_semantic_structure()
    except ValueError as exc:
        assert "complete aligned translation" in str(exc)
    else:
        raise AssertionError("semantic structure must fail closed on incomplete translation")


def test_structured_book_can_enter_existing_knowledge_analyst() -> None:
    corpus = BookCorpusBuilder().build(
        _source(),
        "CHAPTER 1\n\nArchitecture: a set of consequential design decisions.\n\nArchitects must make trade-offs explicit.",
    )
    corpus.apply_translations(
        {
            corpus.translation_units[0].unit_id: "ГЛАВА 1",
            corpus.translation_units[1].unit_id: "Архитектура: набор значимых проектных решений.",
            corpus.translation_units[2].unit_id: "Архитекторы должны явно фиксировать компромиссы.",
        },
        method="TEST_TRANSLATOR",
    )
    corpus.build_semantic_structure()

    package = corpus.to_material_package(task_id="book-pilot")
    bundle = DeterministicKnowledgeAnalyst().analyze(package)

    assert corpus.stage == BookStage.READY_FOR_ANALYST
    assert bundle.counters["materials"] == 3
    assert bundle.counters["DEFINITION_CANDIDATE"] >= 1
    assert bundle.counters["REQUIREMENT_CANDIDATE"] >= 1
    assert all(item.review_status == "NEEDS_REVIEW" for item in bundle.items)
    assert any(item.evidence.source_type == "book" for item in bundle.items)
