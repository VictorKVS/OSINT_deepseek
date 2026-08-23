from father_osint.freshness_discovery import FreshnessWatchTarget
from father_osint.rg_freshness import scan_rg_document_index_html


def test_rg_index_surfaces_265_fz_for_152_without_confusing_unrelated_152_number():
    html = b"""
    <html><body>
      <a href="/documents/2026/08/03/fz265-dok.html">
        Federalnyi zakon N 265-FZ O vnesenii izmenenii v statyu 12 Federalnogo zakona O personalnyh dannyh
      </a>
      <a href="/documents/2026/05/29/dorogi-dok.html">
        Federalnyi zakon N 152-FZ O vnesenii izmeneniia v zakon ob avtomobilnyh dorogah
      </a>
    </body></html>
    """.replace(b"Federalnyi zakon", "Федеральный закон".encode("utf-8")) \
       .replace(b"O vnesenii izmenenii v statyu 12 Federalnogo zakona O personalnyh dannyh", "О внесении изменений в статью 12 Федерального закона \"О персональных данных\"".encode("utf-8")) \
       .replace(b"O vnesenii izmeneniia v zakon ob avtomobilnyh dorogah", "О внесении изменения в закон об автомобильных дорогах".encode("utf-8"))

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
    assert "автомобильных дорогах" not in result.candidates[0].title
    assert result.candidates[0].current_claim_allowed is False
    assert result.candidates[0].exact_bytes_acquired is False
    assert result.candidates[0].legal_truth_promoted is False


def test_rg_index_never_accepts_off_policy_document_link():
    html = """
    <html><body>
      <a href="https://example.com/documents/2026/08/03/fake.html">Федерального закона \"О персональных данных\"</a>
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


def test_rg_secondary_route_is_candidate_only_and_cannot_advance_checkpoint():
    html = """
    <a href="/documents/2026/08/03/fz265-dok.html">Федерального закона \"О персональных данных\"</a>
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
