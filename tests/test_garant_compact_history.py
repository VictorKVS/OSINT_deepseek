from father_osint.garant_timeline import official_evidence_requests, parse_garant_timeline_text


def test_compact_garant_history_becomes_navigation_hints_without_fake_events():
    text = """
    Федеральный закон от 27 июля 2006 г. N 152-ФЗ
    "О персональных данных"

    С изменениями и дополнениями от:
    25 ноября, 27 декабря 2009 г., 28 июня, 27 июля, 29 ноября, 23 декабря 2010 г.,
    4 июня, 25 июля 2011 г., 8 августа, 28 декабря 2024 г., 26 июля 2026 г.

    Принят Государственной Думой 8 июля 2006 года
    """

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )

    assert capture.events == ()
    assert [item.amendment_date for item in capture.amendment_date_hints] == [
        "2009-11-25",
        "2009-12-27",
        "2010-06-28",
        "2010-07-27",
        "2010-11-29",
        "2010-12-23",
        "2011-06-04",
        "2011-07-25",
        "2024-08-08",
        "2024-12-28",
        "2026-07-26",
    ]
    assert all(item.evidence_state == "A2_NAVIGATION_HINT_ONLY" for item in capture.amendment_date_hints)
    assert official_evidence_requests(capture) == ()


def test_compact_history_is_exported_as_metadata_only():
    text = """
    Федеральный закон от 27 июля 2006 г. N 152-ФЗ
    О персональных данных
    С изменениями и дополнениями от:
    28 февраля, 23 мая, 24 июня, 7 июля 2025 г., 26 июля 2026 г.
    Принят Государственной Думой 8 июля 2006 года
    """

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )
    payload = capture.to_dict()

    assert payload["semantic_text_mirrored"] is False
    assert [item["amendment_date"] for item in payload["amendment_date_hints"]] == [
        "2025-02-28",
        "2025-05-23",
        "2025-06-24",
        "2025-07-07",
        "2026-07-26",
    ]
    assert all(item["evidence_state"] == "A2_NAVIGATION_HINT_ONLY" for item in payload["amendment_date_hints"])
