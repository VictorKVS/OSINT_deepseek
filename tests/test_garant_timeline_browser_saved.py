from father_osint.garant_timeline import parse_garant_timeline_text


def test_browser_saved_collapsed_timeline_recovers_amendment_events():
    text = (
        "Федеральный закон от 27 июля 2006 г. N 152-ФЗ О персональных данных "
        "В настоящий документ внесены изменения следующими документами: "
        "Федеральный закон от 26 июля 2026 г. № 265-ФЗ "
        "Изменения вступают в силу с 26 июля 2026 г. "
        "Федеральный закон от 7 июля 2025 г. № 200-ФЗ "
        "Изменения вступают в силу с 1 марта 2027 г. См. будущую редакцию настоящего документа"
    )

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )

    assert [event.amending_act_number for event in capture.events] == ["265-ФЗ", "200-ФЗ"]
    assert capture.events[0].effective_dates == ("2026-07-26",)
    assert capture.events[1].effective_dates == ("2027-03-01",)
    assert capture.future_edition_signalled is True


def test_browser_saved_inline_relative_publication_rule_stays_unresolved():
    text = (
        "Федеральный закон от 4 июня 2014 г. N 142-ФЗ "
        "Изменения вступают в силу по истечении шестидесяти дней после дня официального опубликования названного Федерального закона"
    )

    capture = parse_garant_timeline_text(
        document_id="DOC-RU-FZ-152-2006",
        source_url="https://base.garant.ru/12148567/",
        observed_on="2026-08-22",
        text=text,
    )

    assert len(capture.events) == 1
    assert capture.events[0].effective_dates == ()
    assert capture.events[0].effective_date_basis == "RELATIVE_TO_OFFICIAL_PUBLICATION"
