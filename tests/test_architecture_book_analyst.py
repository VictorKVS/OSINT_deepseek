from father_osint.architecture_book_analyst import ArchitectureBookAnalyst
from father_osint.models import Material, MaterialPackage


def test_architecture_book_analyst_extracts_typed_candidates() -> None:
    materials = [
        Material(
            source_type="book",
            source_locator="private-library://book#unit=1",
            title="Book :: 1",
            raw_text="Архитектурный компромисс: выбор между связанностью и автономностью.",
            metadata={
                "translation_unit_id": "unit-1",
                "source_text_sha256": "a" * 64,
                "heading_path": ["Глава 1"],
                "unit_type": "PARAGRAPH",
            },
        ),
        Material(
            source_type="book",
            source_locator="private-library://book#unit=2",
            title="Book :: 2",
            raw_text="Например, если командам нужна независимая поставка, следует выбирать более автономные границы.",
            metadata={
                "translation_unit_id": "unit-2",
                "source_text_sha256": "b" * 64,
                "heading_path": ["Глава 1"],
                "unit_type": "PARAGRAPH",
            },
        ),
    ]
    package = MaterialPackage(task_id="book-test", materials=materials)

    result = ArchitectureBookAnalyst().analyze(package)
    types = {candidate.candidate_type for candidate in result.candidates}

    assert "DEFINITION_CANDIDATE" in types
    assert "TERM_CANDIDATE" in types
    assert "TRADEOFF_CANDIDATE" in types
    assert "EXAMPLE_CANDIDATE" in types
    assert "DECISION_CRITERION_CANDIDATE" in types
    assert "PRINCIPLE_CANDIDATE" in types
    assert all(candidate.review_status == "NEEDS_REVIEW" for candidate in result.candidates)
    assert all(candidate.source_text_sha256 in {"a" * 64, "b" * 64} for candidate in result.candidates)
