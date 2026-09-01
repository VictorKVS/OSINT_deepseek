from father_osint.freshness_discovery import FreshnessWatchTarget
from father_osint.rg_freshness import (
    scan_rg_announcement_feed_xml,
    scan_rg_document_index_html,
)


def test_rg_index_surfaces_265_fz_for_152_without_confusing_unrelated_152_number():
    html = """
    <html><body>
      <a href="/documents/2026/08/03/fz265-dok.html">
        Федеральный закон N 265-ФЗ О внесении изменений в статью 12 Федерального закона "О персональных данных"
      </a>
      <a href="/documents/2026/05/29/dorogi-dok.html">
        Федеральный закон N 152-ФЗ О внесении изменения в закон об автомобильных дорогах
      </a>
    </body></html>
    """.encode("utf-8")

    target = FreshnessWatchTarget(
        "DOC-RU-FZ-152-2006",
        "152-ФЗ",
        "REFERENCE_TO_TARGET_ACT_NUMBER",
        ("Федерального закона \"О персональных данных\"",),
    )
    result = scan_rg_document_index_html(html, targets=(target,))

    assert result.status == "CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION"
    assert result.coverage_complete_for_checkpoint is False
    assert len(result.candidates) == 1
    assert result.candidates[0].url.endswith("/documents/2026/08/03/fz265-dok.html")
    assert result.candidates[0].publish_date == "2026-08-03"
    assert "автомобильных дорогах" not in result.candidates[0].title
    assert result.candidates[0].current_claim_allowed is False
    assert result.candidates[0].exact_bytes_acquired is False
    assert result.candidates[0].legal_truth_promoted is False


def test_rg_documented_xml_feed_surfaces_candidate_metadata_without_mirroring_article_text():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"><channel>
      <item>
        <title>Федеральный закон N 265-ФЗ: изменения в статье 12 закона о персональных данных</title>
        <link>https://rg.ru/documents/2026/08/03/fz265-dok.html</link>
        <description>Внесены изменения в статью 12 Федерального закона "О персональных данных".</description>
        <pubDate>Mon, 03 Aug 2026 03:00:00 +0300</pubDate>
      </item>
      <item>
        <title>Иной материал</title>
        <link>https://rg.ru/news/2026/08/23/other.html</link>
      </item>
    </channel></rss>
    """.encode("utf-8")
    target = FreshnessWatchTarget(
        "DOC-RU-FZ-152-2006",
        "152-ФЗ",
        "REFERENCE_TO_TARGET_ACT_NUMBER",
        ("Федерального закона \"О персональных данных\"",),
    )

    result = scan_rg_announcement_feed_xml(
        xml,
        targets=(target,),
        publish_date_from="2026-05-25",
        publish_date_to="2026-08-23",
    )

    assert result.status == "CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION"
    assert result.metadata_only is True
    assert result.coverage_complete_for_checkpoint is False
    assert result.items_total == 2
    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.source_key == "rg-official-announcement-feed"
    assert candidate.discovery_channel == "ANNOUNCEMENT_XML_FEED"
    assert candidate.publish_date == "2026-08-03"
    assert candidate.url.endswith("/documents/2026/08/03/fz265-dok.html")
    assert candidate.current_claim_allowed is False
    assert candidate.exact_bytes_acquired is False
    assert candidate.d2_d3_promoted is False
    assert candidate.legal_truth_promoted is False


def test_rg_index_never_accepts_off_policy_document_link():
    html = """
    <html><body>
      <a href="https://example.com/documents/2026/08/03/fake.html">Федерального закона "О персональных данных"</a>
    </body></html>
    """.encode("utf-8")
    target = FreshnessWatchTarget(
        "DOC",
        "152-ФЗ",
        "ACT_NUMBER",
        ("О персональных данных",),
    )
    result = scan_rg_document_index_html(html, targets=(target,))
    assert result.candidates == ()
    assert result.document_links_total == 0


def test_rg_feed_never_accepts_off_policy_link_or_advances_checkpoint():
    xml = """<rss><channel><item>
      <title>О персональных данных</title>
      <link>https://example.com/documents/2026/08/03/fake.html</link>
    </item></channel></rss>""".encode("utf-8")
    target = FreshnessWatchTarget(
        "DOC",
        "152-ФЗ",
        "ACT_NUMBER",
        ("О персональных данных",),
    )
    result = scan_rg_announcement_feed_xml(xml, targets=(target,))
    assert result.candidates == ()
    assert result.rg_links_total == 0
    assert result.coverage_complete_for_checkpoint is False


def test_rg_secondary_route_is_candidate_only_and_cannot_advance_checkpoint():
    html = """
    <a href="/documents/2026/08/03/fz265-dok.html">Федерального закона "О персональных данных"</a>
    """.encode("utf-8")
    result = scan_rg_document_index_html(
        html,
        targets=(FreshnessWatchTarget("DOC", "152-ФЗ", "ACT", ("О персональных данных",)),),
    )
    assert result.metadata_only is True
    assert result.coverage_complete_for_checkpoint is False
    assert result.exact_bytes_acquired is False
    assert result.d2_d3_promoted is False
    assert result.current_claim_allowed is False
    assert result.legal_truth_promoted is False
