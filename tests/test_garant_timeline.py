from father_osint.garant_timeline import official_evidence_requests, parse_garant_timeline_text


def test_garant_timeline_extracts_amendment_dates_and_keeps_evidence_pending():
    text = """
    Федеральный закон от 27 июля 2006 г. N 152-ФЗ
    О персональных данных

    В настоящий документ внесены изменения следующими документами:

    Федеральный закон от 26 июля 2026 г. № 265-ФЗ
    Изменения вступают в силу с 26 июля 2026 г.

    Федеральный закон от 7 июля 2025 г. № 200-ФЗ
    Изменения вступают в силу с 1 марта 2027 г.
    См. будущую редакцию настоящего документа
    """

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )

    assert len(capture.events) == 2
    assert capture.events[0].amending_act_number == "265-ФЗ"
    assert capture.events[0].amending_act_date == "2026-07-26"
    assert capture.events[0].effective_dates == ("2026-07-26",)
    assert capture.events[0].effective_date_basis == "EXPLICIT_CALENDAR_DATE"
    assert capture.events[0].evidence_state == "OFFICIAL_EVIDENCE_PENDING"
    assert capture.events[0].event_id.startswith("GTE-")
    assert capture.events[1].effective_dates == ("2027-03-01",)
    assert capture.future_edition_signalled is True
    assert capture.semantic_text_mirrored is False


def test_garant_timeline_preserves_non_calendar_effective_rule_without_inventing_date():
    text = """
    Приказ Федеральной службы по техническому и экспортному контролю от 23 марта 2017 г. N 49
    Изменения вступают в силу по истечении 10 дней после дня официального опубликования названного приказа
    """

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FSTEC-21-2013",
        source_url="https://base.garant.ru/70380924/",
        observed_on="2026-08-22",
        text=text,
    )

    assert len(capture.events) == 1
    event = capture.events[0]
    assert event.amending_act_number == "49"
    assert event.amending_act_date == "2017-03-23"
    assert event.effective_dates == ()
    assert event.effective_date_basis == "RELATIVE_TO_OFFICIAL_PUBLICATION"
    assert "официального опубликования" in event.effective_rule


def test_garant_timeline_supports_multiple_explicit_effective_dates():
    text = """
    Федеральный закон от 8 августа 2024 г. № 233-ФЗ
    Изменения вступают в силу с 8 августа 2024 г. и с 1 сентября 2025 г.
    """

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )

    assert capture.events[0].effective_dates == ("2024-08-08", "2025-09-01")
    assert capture.events[0].effective_date_basis == "EXPLICIT_CALENDAR_DATE"


def test_official_evidence_requests_are_stable_traceable_and_keep_a2_as_navigation_only():
    text = """
    Приказ Федеральной службы по техническому и экспортному контролю от 14 мая 2020 г. N 68
    Изменения вступают в силу с 1 января 2021 г.
    """
    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FSTEC-21-2013",
        source_url="https://base.garant.ru/70380924/",
        observed_on="2026-08-22",
        text=text,
    )

    source_hash = "a" * 64
    first = official_evidence_requests(capture, source_capture_sha256=source_hash)
    second = official_evidence_requests(capture, source_capture_sha256=source_hash)

    assert first == second
    assert len(first) == 1
    request = first[0]
    assert request["evidence_request_id"].startswith("OER-")
    assert request["timeline_event_id"] == capture.events[0].event_id
    assert request["document_id"] == "DOC-RU-FSTEC-21-2013"
    assert request["amending_act_title"] == "Приказ Федеральной службы по техническому и экспортному контролю"
    assert request["amending_act_number"] == "68"
    assert request["amending_act_date"] == "2020-05-14"
    assert request["effective_dates"] == ["2021-01-01"]
    assert request["effective_rule"] == "Изменения вступают в силу с 1 января 2021 г."
    assert request["effective_date_basis"] == "EXPLICIT_CALENDAR_DATE"
    assert request["required_official_evidence"] == [
        "AMENDING_ACT_IDENTITY",
        "AMENDING_ACT_OFFICIAL_TEXT",
        "EFFECTIVE_RULE",
        "EXPLICIT_EFFECTIVE_DATE",
    ]
    assert request["locator_strategy"] == "SEARCH_A0_A1_BY_ACT_IDENTITY"
    assert request["timeline_source_id"] == "SRC-RU-GARANT-001"
    assert request["timeline_source_url"] == "https://base.garant.ru/70380924/"
    assert request["timeline_observed_on"] == "2026-08-22"
    assert request["timeline_source_capture_sha256"] == source_hash
    assert request["required_evidence_tier"] == "A0_OR_A1"
    assert request["status"] == "EVIDENCE_PENDING"


def test_official_evidence_request_requires_publication_date_for_relative_rule():
    text = """
    Федеральный закон от 1 июля 2017 г. № 148-ФЗ
    Изменения вступают в силу со дня официального опубликования названного Федерального закона
    """
    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )

    request = official_evidence_requests(capture)[0]
    assert request["effective_dates"] == []
    assert request["effective_date_basis"] == "RELATIVE_TO_OFFICIAL_PUBLICATION"
    assert request["required_official_evidence"][-1] == "OFFICIAL_PUBLICATION_DATE"
    assert request["status"] == "EVIDENCE_PENDING"


def test_official_evidence_request_rejects_invalid_capture_hash():
    text = """
    Приказ Федеральной службы по техническому и экспортному контролю от 14 мая 2020 г. N 68
    Изменения вступают в силу с 1 января 2021 г.
    """
    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FSTEC-21-2013",
        source_url="https://base.garant.ru/70380924/",
        observed_on="2026-08-22",
        text=text,
    )

    try:
        official_evidence_requests(capture, source_capture_sha256="not-a-sha256")
    except ValueError as exc:
        assert "64-character hexadecimal" in str(exc)
    else:
        raise AssertionError("invalid source capture hash must be rejected")
