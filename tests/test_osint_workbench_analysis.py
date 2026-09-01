from __future__ import annotations

from osint_workbench.analysis_zoo import AnalysisZoo, AnalyzerDraft, AnalyzerSpec
from osint_workbench.resolution import ExplainableEntityResolver

from osint_workbench_test_support import WorkbenchTestCase


class TestResolutionAnalysisAndGraph(WorkbenchTestCase):
    def _two_entities(self) -> tuple[PassiveOSINTWorkbench, object, dict, dict, dict]:
        workbench, boot = self.bootstrap()
        source = workbench.store.register_source(
            boot.case["case_id"],
            url="urn:synthetic:registry:2",
            title="Synthetic registry",
            publisher="Registry",
            source_type="OFFICIAL_REGISTER",
            primary_level="PRIMARY",
            jurisdiction="SYNTHETIC",
            language="en",
            reliability_grade="A_CONFIRMED",
            legal_basis_or_usage_note="Synthetic fixture.",
            republication_status="ALLOWED",
        )
        workbench.store.capture_text(boot.case["case_id"], source_id=source["source_id"], text="registry fixture")
        a = workbench.store.create_entity(
            boot.case["case_id"],
            entity_type="ORGANIZATION",
            display_name="Same Name LLC",
            source_ids=[source["source_id"]],
            identifiers=[{"type": "REGISTRY_ID", "value": "A-1", "masked": False, "source_ids": [source["source_id"]]}],
            attributes={"registered_address": "Address One"},
            status="CONFIRMED",
        )
        b = workbench.store.create_entity(
            boot.case["case_id"],
            entity_type="ORGANIZATION",
            display_name="Same Name LLC",
            source_ids=[source["source_id"]],
            identifiers=[{"type": "REGISTRY_ID", "value": "B-2", "masked": False, "source_ids": [source["source_id"]]}],
            attributes={"registered_address": "Address Two"},
            status="CONFIRMED",
        )
        return workbench, boot, source, a, b

    def test_entity_resolution_never_merges_namesakes(self) -> None:
        workbench, boot, _, a, b = self._two_entities()
        result = ExplainableEntityResolver(workbench.store).compare(boot.case["case_id"], a["entity_id"], b["entity_id"])
        self.assertFalse(result["automatic_merge_performed"])
        self.assertEqual(result["human_review"]["status"], "PENDING")
        self.assertTrue(any(item["feature"] == "identifier_conflict" for item in result["contradicting_features"]))

    def test_analysis_zoo_uses_independent_families_and_cannot_create_fact(self) -> None:
        workbench, boot, source, a, b = self._two_entities()
        claim = workbench.store.create_claim(
            boot.case["case_id"],
            source_ids=[source["source_id"]],
            statement="Synthetic source mentions both records.",
            locator="fixture:1",
            subject_entity_ids=[a["entity_id"]],
            object_entity_ids=[b["entity_id"]],
        )
        relation = workbench.store.create_relation(
            boot.case["case_id"],
            from_entity_id=a["entity_id"],
            relation_type="MENTIONED_IN",
            to_entity_id=b["entity_id"],
            source_ids=[source["source_id"]],
            claim_ids=[claim["claim_id"]],
            status="CANDIDATE",
        )
        result = AnalysisZoo(workbench.store).run(
            boot.case["case_id"],
            task="Challenge the candidate relation before any attribution",
            input_refs=[claim["claim_id"], relation["relation_id"]],
        )
        self.assertFalse(result.run["fact_promotion_allowed"])
        self.assertEqual(result.consensus["human_decision"], "PENDING")
        self.assertGreaterEqual(result.consensus["independent_family_count"], 2)
        self.assertTrue(all(not item["can_create_fact"] for item in result.opinions))

    def test_analysis_zoo_rejects_same_family_only(self) -> None:
        workbench, boot, _, a, _ = self._two_entities()
        zoo = AnalysisZoo(workbench.store)

        def noop(case_id: str, task: str, inputs: list) -> AnalyzerDraft:
            return AnalyzerDraft(output_class="NO_CONCLUSION", answer="No conclusion", limitations=["test"])

        zoo.register(AnalyzerSpec("rule-two", "DETERMINISTIC_RULE", "1", ("TEXT",)), noop)
        with self.assertRaises(ValueError):
            zoo.run(
                boot.case["case_id"],
                task="Same family independence check",
                input_refs=[a["entity_id"]],
                analyzer_ids=["builtin-evidence-lineage", "rule-two"],
            )
