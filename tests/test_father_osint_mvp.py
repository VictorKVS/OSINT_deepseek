import tempfile
import unittest

from father_osint import Material, MaterialStore, OSINTAgent, ResearchTask


class FakeCollector:
    name = "fake"
    source_types = {"web"}

    def collect(self, task):
        yield Material(
            source_type="web",
            source_locator="https://example.test/a",
            title="A",
            raw_text="same payload",
        )
        yield Material(
            source_type="web",
            source_locator="https://example.test/b",
            title="B",
            raw_text="same payload",
        )
        yield Material(
            source_type="web",
            source_locator="https://example.test/c",
            title="C",
            raw_text="different payload",
        )


class OSINTAgentMVPTests(unittest.TestCase):
    def test_collects_distinct_source_observations_even_when_payload_matches(self):
        """AC-02: equal payload may share raw storage, but source observations must survive."""
        with tempfile.TemporaryDirectory() as tmp:
            store = MaterialStore(tmp)
            agent = OSINTAgent(store, [FakeCollector()])
            task = ResearchTask(question="Find test materials", source_types=["web"], max_items=10)

            package = agent.run(task)

            self.assertEqual(package.task_id, task.task_id)
            self.assertEqual(len(package.materials), 3)
            self.assertEqual(
                {material.source_locator for material in package.materials},
                {
                    "https://example.test/a",
                    "https://example.test/b",
                    "https://example.test/c",
                },
            )
            self.assertEqual(package.stop_reason, "collectors_exhausted")
            self.assertTrue((store.root / "tasks.jsonl").exists())
            self.assertTrue((store.root / "materials.jsonl").exists())
            self.assertTrue((store.root / "packages.jsonl").exists())

            # Two distinct payloads exist even though three source observations exist.
            self.assertEqual(len(list(store.raw_dir.glob("*.txt"))), 2)

    def test_missing_collector_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MaterialStore(tmp)
            agent = OSINTAgent(store)
            task = ResearchTask(question="Find Telegram posts", source_types=["telegram"])

            package = agent.run(task)

            self.assertEqual(package.stop_reason, "no_eligible_collectors")
            self.assertEqual(len(package.materials), 0)
            self.assertTrue(package.collection_errors)

    def test_max_items_stops_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MaterialStore(tmp)
            agent = OSINTAgent(store, [FakeCollector()])
            task = ResearchTask(question="Only one", source_types=["web"], max_items=1)

            package = agent.run(task)

            self.assertEqual(len(package.materials), 1)
            self.assertEqual(package.stop_reason, "max_items_reached")


if __name__ == "__main__":
    unittest.main()
