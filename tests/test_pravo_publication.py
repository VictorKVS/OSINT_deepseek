from urllib.parse import parse_qs, urlparse

import pytest

from father_osint.pravo_publication import (
    PravoPublicationClient,
    PravoPublicationError,
    ResilientJsonTransport,
)


class FakeTransport:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.urls = []

    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int):
        self.urls.append(url)
        if not self.payloads:
            raise AssertionError("unexpected request")
        payload = self.payloads.pop(0)
        if isinstance(payload, Exception):
            raise payload
        return payload


class NamedTransport(FakeTransport):
    def __init__(self, name, payloads):
        super().__init__(payloads)
        self.last_transport = name
        self.last_failures = []
        self.timeouts = []

    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int):
        self.timeouts.append(timeout_seconds)
        return super().get_json(url, timeout_seconds=timeout_seconds, max_bytes=max_bytes)


def test_search_uses_exact_number_and_metadata_only_contract():
    transport = FakeTransport([
        {
            "items": [
                {
                    "eoNumber": "0001202601010001",
                    "number": "152-ФЗ",
                    "title": "О персональных данных",
                    "documentDate": "27.07.2006",
                    "publishDateShort": "29.07.2006",
                    "pdfFileLength": 12345,
                    "zipFileLength": None,
                }
            ]
        }
    ])
    client = PravoPublicationClient(transport=transport)
    hits, meta = client.search_documents(number="152-ФЗ", page_size=30, page=1)

    assert len(hits) == 1
    assert hits[0].eo_number == "0001202601010001"
    assert meta["metadata_only"] is True
    parsed = urlparse(transport.urls[0])
    query = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.hostname == "publication.pravo.gov.ru"
    assert query["NumberSearchType"] == ["0"]
    assert query["Number"] == ["152-ФЗ"]
    assert query["PageSize"] == ["30"]
    assert query["Index"] == ["1"]


def test_exact_identity_normalizes_common_date_forms_without_promoting_bytes():
    transport = FakeTransport([
        {
            "items": [
                {
                    "eoNumber": "EO1",
                    "number": "152-ФЗ",
                    "title": "О персональных данных",
                    "documentDate": "27.07.2006",
                    "pdfFileLength": 100,
                },
                {
                    "eoNumber": "EO2",
                    "number": "152-ФЗ",
                    "title": "Иной документ",
                    "documentDate": "2007-07-27",
                    "pdfFileLength": 200,
                },
            ]
        }
    ])
    client = PravoPublicationClient(transport=transport)
    hits, _ = client.search_documents(number="152-ФЗ")
    exact = client.exact_identity_hits(hits, number="152-ФЗ", document_date="2006-07-27")
    assert [item.eo_number for item in exact] == ["EO1"]


def test_detail_and_file_urls_keep_official_host_and_metadata_boundary():
    transport = FakeTransport([{"eoNumber": "EO1", "number": "152-ФЗ"}])
    client = PravoPublicationClient(transport=transport)
    detail = client.get_document("EO1")
    assert detail["_father_metadata_only"] is True
    assert client.pdf_url("EO1") == "https://publication.pravo.gov.ru/File/Pdf?eoNumber=EO1"
    assert client.zip_url("EO1") == "https://publication.pravo.gov.ru/File/Zip?eoNumber=EO1"


def test_client_rejects_non_https_or_non_official_base_url():
    with pytest.raises(ValueError):
        PravoPublicationClient(base_url="http://publication.pravo.gov.ru")
    with pytest.raises(ValueError):
        PravoPublicationClient(base_url="https://example.com")


def test_bad_api_shape_fails_closed():
    client = PravoPublicationClient(transport=FakeTransport([{"items": "not-a-list"}]))
    with pytest.raises(PravoPublicationError):
        client.search_documents(number="152-ФЗ")


def test_resilient_transport_caps_urllib_then_uses_https_fallback():
    primary = NamedTransport("urllib_https", [PravoPublicationError("WinError 10060")])
    fallback = NamedTransport("curl_https", [{"items": []}])
    transport = ResilientJsonTransport(
        primary=primary,
        fallback=fallback,
        primary_timeout_cap_seconds=8.0,
    )
    client = PravoPublicationClient(transport=transport)

    hits, meta = client.search_documents(number="152-ФЗ", timeout_seconds=30.0)

    assert hits == []
    assert primary.timeouts == [8.0]
    assert fallback.timeouts == [22.0]
    assert meta["transport"] == "curl_https"
    assert len(meta["transport_failures_before_success"]) == 1
    assert "WinError 10060" in meta["transport_failures_before_success"][0]


def test_resilient_transport_fails_closed_when_both_https_transports_fail():
    primary = NamedTransport("urllib_https", [PravoPublicationError("primary down")])
    fallback = NamedTransport("curl_https", [PravoPublicationError("fallback down")])
    transport = ResilientJsonTransport(primary=primary, fallback=fallback)
    client = PravoPublicationClient(transport=transport)

    with pytest.raises(PravoPublicationError, match="transports failed"):
        client.search_documents(number="152-ФЗ", timeout_seconds=10.0)
