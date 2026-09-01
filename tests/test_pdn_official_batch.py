import json

from father_osint.acquisition import FetchedArtifact
from father_osint.knowledge_factory_store import KnowledgeFactoryStore
from father_osint.pdn_batch import PdnOfficialBatchRunner


HTML_A = b"""
<html><body>
<h1>Document A</h1>
<h2>\xd0\x93\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xb0 1. General</h2>
<p>\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x8c\xd1\x8f 1. Scope</p>
<p>1. Personal data processing is regulated by this document.</p>
</body></html>
"""

HTML_B = b"""
<html><body>
<h1>Document B</h1>
<p>Requirements for protection of personal data in information systems.</p>
</body></html>
"""


class MappingFetcher:
    def __init__(self):
        self.calls = []

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        self.calls.append(url)
        data = HTML_A if url.endswith("/a") else HTML_B
        return FetchedArtifact(data=data, mime_type="text/html", final_url=url)


def registry_fixture():
    return {
        "schema_version": "1.0",
        "registry_id": "PDN-TEST",
        "purpose": "test",
        "sources": {
            "SRC-A": {
                "name": "Official A",
                "domain": "official.example",
                "organization": "Authority A",
                "source_class": "OFFICIAL",
                "status": "VERIFIED",
                "trust_basis": "official source",
                "verified_by": "reviewer",
                "verified_at": "2026-08-22T00:00:00+00:00",
                "trust_tier": "A0_OFFICIAL_PUBLICATION",
                "domains": ["official.example"],
                "verification_evidence": ["official"]
            }
        },
        "documents": [
            {
                "document_id": "DOC-A",
                "priority": "P0",
                "enabled": True,
                "title": "A",
                "document_type": "federal_law",
                "jurisdiction": "RU",
                "language": "ru",
                "source_id": "SRC-A",
                "source_state": "VERIFIED_ARTIFACT_LOCATOR",
                "source_url": "https://official.example/a",
                "file_name": "a.html",
                "tags": ["pdn"],
                "kb_targets": ["PDN_KB"]
            },
            {
                "document_id": "DOC-B",
                "priority": "P0",
                "enabled": True,
                "title": "B",
                "document_type": "government_decree",
                "jurisdiction": "RU",
                "language": "ru",
                "source_id": "SRC-A",
                "source_state": "VERIFIED_ARTIFACT_LOCATOR",
                "source_url": "https://official.example/b",
                "file_name": "b.html",
                "tags": ["pdn", "security"],
                "kb_targets": ["PDN_KB", "SECURITY_KB"]
            },
            {
                "document_id": "DOC-PENDING",
                "priority": "P0-CRYPTO",
                "enabled": False,
                "title": "Pending",
                "document_type": "fsb_order",
                "jurisdiction": "RU",
                "language": "ru",
                "source_id": "SRC-A",
                "source_state": "SOURCE_PENDING",
                "source_url": None,
                "file_name": "pending.bin",
                "tags": ["crypto"],
                "kb_targets": ["PDN_KB"]
            }
        ]
    }


def test_batch_processes_all_enabled_documents_and_keeps_pending_explicit(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    fetcher = MappingFetcher()

    result = PdnOfficialBatchRunner(store, fetcher=fetcher).run(registry_fixture())

    assert result.counters["listed"] == 3
    assert result.counters["ready_d5"] == 2
    assert result.counters["source_pending"] == 1
    assert result.counters["acquisition_failed"] == 0
    assert len(fetcher.calls) == 2
    assert [item.status for item in result.results] == ["READY_D5", "READY_D5", "SOURCE_PENDING"]

    review = json.loads((store.root / result.review_json_path).read_text(encoding="utf-8"))
    assert review["counters"]["ready_d5"] == 2
    assert review["review_required_before_d6"] is True
    assert review["semantic_extraction_performed"] is False
    assert review["documents"][0]["artifact_sha256"]
    assert review["documents"][0]["chunks"] >= 1
    assert review["documents"][2]["artifact_sha256"] is None


def test_batch_review_markdown_is_human_readable_and_lists_sha(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    result = PdnOfficialBatchRunner(store, fetcher=MappingFetcher()).run(registry_fixture())

    text = (store.root / result.review_md_path).read_text(encoding="utf-8")
    assert "PDn official corpus review" in text
    assert "READY_D5" in text
    assert "SOURCE_PENDING" in text
    assert result.results[0].artifact_sha256 in text


def test_batch_repeated_run_reuses_artifacts_but_keeps_review_current(tmp_path):
    store = KnowledgeFactoryStore(tmp_path)
    fetcher = MappingFetcher()
    runner = PdnOfficialBatchRunner(store, fetcher=fetcher)

    first = runner.run(registry_fixture())
    second = runner.run(registry_fixture())

    assert first.counters["ready_d5"] == second.counters["ready_d5"] == 2
    assert all(item.status == "READY_D5" for item in second.results[:2])
    assert all(item.acquisition_disposition == "REUSED" for item in second.results[:2])
    assert len(store.list_acquisitions()) == 4
