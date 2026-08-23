from urllib.parse import parse_qs, urlparse

from father_osint.freshness_discovery import (
    FreshnessWatchTarget,
    PravoReferenceDiscovery,
    degraded_observation,
    load_watchlist,
)
from father_osint.pravo_publication import PravoPublicationClient


class FakeTransport:
    def __init__(self, payload):
        self.payload = payload
        self.urls = []
        self.last_transport = "fake_https"
        self.last_failures = []

    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int):
        self.urls.append(url)
        return self.payload


def test_watchlist_requires_unique_bounded_targets():
    targets = load_watchlist({
        "targets": [
            {"document_id": "A", "query_text": "152-ФЗ", "query_basis": "ACT_NUMBER"},
            {"document_id": "B", "query_text": "1119", "query_basis": "ACT_NUMBER"},
        ]
    })
    assert [item.document_id for item in targets] == ["A", "B"]


def test_recent_reference_search_is_metadata_only_and_never_claims_currentness():
    transport = FakeTransport({
        "items": [
            {
                "eoNumber": "EO-1",
                "number": "999-ФЗ",
                "title": "О внесении изменений",
                "documentDate": "2026-08-20",
                "publishDateShort": "2026-08-21",
                "pdfFileLength": 123,
            }
        ]
    })
    client = PravoPublicationClient(transport=transport)
    discovery = PravoReferenceDiscovery(client)
    target = FreshnessWatchTarget("DOC", "152-ФЗ", "REFERENCE_TO_TARGET_ACT_NUMBER")

    observation = discovery.search_recent_reference(
        target,
        publish_date_from="2026-08-16",
        publish_date_to="2026-08-23",
        timeout_seconds=5.0,
    )

    assert observation.status == "CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION"
    assert observation.current_claim_allowed is False
    assert observation.exact_bytes_acquired is False
    assert observation.d2_d3_promoted is False
    assert observation.legal_truth_promoted is False
    assert len(observation.candidate_events) == 1
    parsed = urlparse(transport.urls[0])
    query = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.hostname == "publication.pravo.gov.ru"
    assert query["DocumentText"] == ["152-ФЗ"]
    assert query["PublishDateFrom"] == ["2026-08-16"]
    assert query["PublishDateTo"] == ["2026-08-23"]


def test_empty_remote_window_is_not_an_unchanged_or_current_claim():
    client = PravoPublicationClient(transport=FakeTransport({"items": []}))
    observation = PravoReferenceDiscovery(client).search_recent_reference(
        FreshnessWatchTarget("DOC", "152-ФЗ", "ACT_NUMBER"),
        publish_date_from="2026-08-16",
        publish_date_to="2026-08-23",
    )
    assert observation.status == "NO_CANDIDATE_IN_WINDOW"
    assert observation.current_claim_allowed is False
    assert observation.exact_bytes_acquired is False


def test_degraded_remote_source_never_breaks_serving_semantics_or_promotes_truth():
    observation = degraded_observation(
        FreshnessWatchTarget("DOC", "152-ФЗ", "ACT_NUMBER"),
        status="DEGRADED_SOURCE_CIRCUIT_OPEN",
        error="timeout",
    )
    assert observation.candidate_events == ()
    assert observation.current_claim_allowed is False
    assert observation.exact_bytes_acquired is False
    assert observation.d2_d3_promoted is False
    assert observation.legal_truth_promoted is False


def test_freshness_runner_contract_is_fail_safe_and_logged():
    script = open("scripts/run_pdn_freshness_discovery.py", encoding="utf-8").read()
    cmd = open("RUN_PDN_FRESHNESS_DISCOVERY.cmd", encoding="utf-8").read()

    assert "serving_continues_from_verified_local_proof" in script
    assert "freshness_monitoring_degraded" in script
    assert "freshness_current_claim_allowed" in script
    assert "no_false_unchanged_claim" in script
    assert "new_document_version_created" in script
    assert "new_d2_d3_promotion" in script
    assert "legal_truth_promoted" in script
    assert "load_source_health" in script
    assert "write_source_health" in script
    assert "PDN_FRESHNESS_DISCOVERY" in cmd
    assert "run_logged_python_sequence.ps1" in cmd
