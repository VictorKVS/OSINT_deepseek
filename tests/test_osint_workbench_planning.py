from __future__ import annotations

import json

from osint_workbench.extractor import DeterministicIdentifierExtractor
from osint_workbench.policy import authorize_public_export

from osint_workbench_test_support import WorkbenchTestCase


class TestPlanningAndPolicy(WorkbenchTestCase):
    def test_bootstrap_generates_five_streams_and_passive_scope(self) -> None:
        workbench, boot = self.bootstrap()
        streams = {pivot["stream"] for pivot in boot.plan["pivots"]}
        self.assertEqual(streams, {
            "ENTITY_REGISTRY",
            "BUSINESS_TRANSACTIONS_LOGISTICS",
            "DIGITAL_FOOTPRINT",
            "LEGAL_SANCTIONS_ADVERSE",
            "RED_TEAM_SOURCE_QUALITY",
        })
        self.assertFalse(boot.case["scope"]["active_actions_allowed"])
        self.assertEqual(boot.plan["status"], "APPROVED")
        self.assertTrue(workbench.store.verify_journal(boot.case["case_id"])["valid"])

    def test_active_transform_is_registered_disabled_in_passive_case(self) -> None:
        workbench, boot = self.bootstrap()
        transform = workbench.jobs.register_transform(
            boot.case["case_id"],
            name="Active scanner inventory record",
            input_entity_types=["DOMAIN"],
            output_object_types=["ASSET"],
            safety_class="ACTIVE_AUTHORIZED",
            network_policy="AUTHORIZED_TARGET_SCOPE",
        )
        self.assertFalse(transform["enabled"])
        self.assertEqual(transform["health"], "DISABLED")
        self.assertTrue(transform["requires_human_approval"])

    def test_public_export_policy_requires_redaction_and_review(self) -> None:
        denied = authorize_public_export(
            access_class="PUBLIC_WITH_PERSONAL_DATA",
            republication_status="ALLOWED",
            contains_personal_data=True,
            redacted=False,
            evidence_trace_complete=True,
            human_reviewed=True,
        )
        self.assertEqual(denied.decision, "DENY")
        self.assertIn("UNREDACTED_PERSONAL_DATA", denied.reason_codes)


class TestEvidenceAndExtraction(WorkbenchTestCase):
    def test_capture_is_content_addressed_and_integrity_checked(self) -> None:
        workbench, boot = self.bootstrap()
        first = workbench.store.capture_text(
            boot.case["case_id"],
            source_id=boot.seed_source["source_id"],
            text="same bytes",
            filename_hint="a.txt",
        )
        second = workbench.store.capture_text(
            boot.case["case_id"],
            source_id=boot.seed_source["source_id"],
            text="same bytes",
            filename_hint="a.txt",
        )
        self.assertNotEqual(first["capture_id"], second["capture_id"])
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(first["storage_uri"], second["storage_uri"])
        self.assertEqual(workbench.store.read_capture_bytes(boot.case["case_id"], first["capture_id"]), b"same bytes")

    def test_extractor_links_indicators_to_document_not_seed(self) -> None:
        workbench, boot = self.bootstrap()
        source = workbench.store.register_source(
            boot.case["case_id"],
            url="urn:synthetic:web:1",
            title="Synthetic page",
            publisher="Synthetic",
            jurisdiction="SYNTHETIC",
            language="en",
            legal_basis_or_usage_note="Synthetic fixture.",
        )
        capture = workbench.store.capture_text(
            boot.case["case_id"],
            source_id=source["source_id"],
            text="Contact analyst@example.test and visit https://example.test. Wallet 0x1111111111111111111111111111111111111111.",
        )
        result = DeterministicIdentifierExtractor(workbench.store).extract_capture(
            boot.case["case_id"], source_id=source["source_id"], capture_id=capture["capture_id"]
        )
        self.assertGreaterEqual(len(result.indicators), 3)
        relations = workbench.store.list_objects(boot.case["case_id"], "relation")
        self.assertTrue(relations)
        self.assertTrue(all(item["relation_type"] == "MENTIONED_IN" for item in relations))
        self.assertTrue(all(item["to_entity_id"] == result.document_entity_id for item in relations))
        self.assertTrue(all(item["from_entity_id"] != boot.seed_entity["entity_id"] for item in relations))

    def test_journal_tampering_is_detected(self) -> None:
        workbench, boot = self.bootstrap()
        journal_dir = workbench.store.case_dir(boot.case["case_id"]) / "journal"
        path = sorted(journal_dir.glob("*.json"))[0]
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["result_summary"] = "tampered"
        path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        check = workbench.store.verify_journal(boot.case["case_id"])
        self.assertFalse(check["valid"])
        self.assertTrue(any("entry hash mismatch" in item for item in check["failures"]))
