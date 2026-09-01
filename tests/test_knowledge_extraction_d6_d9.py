from father_osint.knowledge_extraction import extract_candidates


def _chunk(text: str) -> dict[str, object]:
    return {
        "document_id": "DOC-RU-FZ-152-2006",
        "version_id": "VER-1",
        "chunk_id": "CHK-1",
        "locator": "article:3/point:1/chunk:1",
        "structure_node_id": "STR-1",
        "artifact_sha256": "a" * 64,
        "text": text,
    }


def test_explicit_definition_creates_term_and_definition_candidates_with_lineage():
    terms, definitions, requirements, entities = extract_candidates(
        _chunk("Пункт 1\nперсональные данные - любая информация, относящаяся к определенному физическому лицу")
    )

    assert definitions
    assert definitions[0].term == "персональные данные"
    assert definitions[0].review_state == "CANDIDATE_NEEDS_REVIEW"
    assert definitions[0].promotion_state == "NOT_PROMOTED"
    assert definitions[0].lineage.chunk_id == "CHK-1"
    assert any(term.term_kind == "EXPLICITLY_DEFINED_TERM" for term in terms)
    assert any(entity.canonical_key == "personal_data" for entity in entities)
    assert requirements == []


def test_normative_trigger_is_candidate_not_promoted_fact():
    _, _, requirements, _ = extract_candidates(
        _chunk("Пункт 10\nОператор обязан принять необходимые правовые, организационные и технические меры.")
    )

    assert len(requirements) == 1
    assert requirements[0].modality == "OBLIGATION"
    assert requirements[0].trigger == "обязан"
    assert requirements[0].review_state == "CANDIDATE_NEEDS_REVIEW"
    assert requirements[0].promotion_state == "NOT_PROMOTED"


def test_controlled_entity_mentions_are_deduped_per_chunk():
    terms, _, _, entities = extract_candidates(
        _chunk("Пункт 2\nОператор обеспечивает безопасность персональных данных. Оператор ведет обработку персональных данных.")
    )

    assert len([e for e in entities if e.canonical_key == "personal_data_operator"]) == 1
    assert any(e.canonical_key == "personal_data_security" for e in entities)
    assert any(t.canonical_key == "personal_data_operator" for t in terms)
