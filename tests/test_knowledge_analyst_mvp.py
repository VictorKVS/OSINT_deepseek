from __future__ import annotations

from father_osint.knowledge_analyst import DeterministicKnowledgeAnalyst
from father_osint.models import Material, MaterialPackage


def test_extracts_traceable_definition_requirement_and_entity_candidates() -> None:
    material = Material(
        source_type="official",
        source_locator="https://example.test/act",
        title="Test act",
        raw_text=(
            "Оператор — лицо, организующее обработку данных. "
            "Оператор должен определить необходимые меры защиты."
        ),
        metadata={"entities": ["Оператор"]},
        content_hash="abc123",
    )
    package = MaterialPackage(task_id="task-1", materials=[material])

    bundle = DeterministicKnowledgeAnalyst().analyze(package)

    assert bundle.schema_version == "father-osint.knowledge-bundle.v0.1"
    assert bundle.counters["materials"] == 1
    assert bundle.counters["chunks"] == 2
    assert bundle.counters["CLAIM_CANDIDATE"] == 2
    assert bundle.counters["DEFINITION_CANDIDATE"] == 1
    assert bundle.counters["REQUIREMENT_CANDIDATE"] == 1
    assert bundle.counters["ENTITY_CANDIDATE"] == 1

    definition = next(item for item in bundle.items if item.item_type == "DEFINITION_CANDIDATE")
    assert definition.subject == "Оператор"
    assert definition.value == "лицо, организующее обработку данных."
    assert definition.review_status == "NEEDS_REVIEW"

    requirement = next(item for item in bundle.items if item.item_type == "REQUIREMENT_CANDIDATE")
    assert requirement.evidence.material_id == material.material_id
    assert requirement.evidence.source_locator == material.source_locator
    assert requirement.evidence.char_start < requirement.evidence.char_end
    assert len(requirement.evidence.text_sha256) == 64


def test_deduplicates_identical_candidates_but_keeps_chunks() -> None:
    text = "Система должна вести журнал. Система должна вести журнал."
    material = Material(
        source_type="web",
        source_locator="https://example.test/repeated",
        title="Repeated",
        raw_text=text,
    )
    package = MaterialPackage(task_id="task-2", materials=[material])

    bundle = DeterministicKnowledgeAnalyst().analyze(package)

    assert bundle.counters["chunks"] == 2
    assert bundle.counters["CLAIM_CANDIDATE"] == 1
    assert bundle.counters["REQUIREMENT_CANDIDATE"] == 1


def test_empty_local_only_material_does_not_invent_knowledge() -> None:
    material = Material(
        source_type="file",
        source_locator="local://document.pdf",
        title="Binary document",
        local_path="data/document.pdf",
    )
    package = MaterialPackage(task_id="task-3", materials=[material])

    bundle = DeterministicKnowledgeAnalyst().analyze(package)

    assert bundle.counters == {"materials": 1, "chunks": 0}
    assert bundle.items == []
