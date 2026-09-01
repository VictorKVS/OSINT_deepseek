from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import TestCase, mock

from osint_workbench.demo import run_demo
from osint_workbench.http_collect import PublicURLPolicy, URLPolicyError
from osint_workbench.monitoring import CaseMonitor
from osint_workbench.service import make_handler
from osint_workbench.store import WorkbenchStore

from osint_workbench_test_support import WorkbenchTestCase


class TestEndToEndAndService(WorkbenchTestCase):
    def test_synthetic_demo_builds_report_graph_and_valid_journal(self) -> None:
        result = run_demo(self.root, force=True)
        self.assertTrue(Path(result["report"]).is_file())
        self.assertTrue(result["journal"]["valid"])
        self.assertGreaterEqual(result["counts"]["source"], 3)
        self.assertGreaterEqual(result["counts"]["analysis_opinion"], 2)
        report = Path(result["report"]).read_text(encoding="utf-8")
        self.assertIn("СЛУЖЕБНАЯ АНАЛИТИЧЕСКАЯ СПРАВКА", report)
        self.assertIn("NO_HIT", report)
        store = WorkbenchStore(self.root)
        graph = store.get_object(result["case_id"], "graph", result["graph_view_id"])
        self.assertFalse(graph["authoritative"])
        self.assertTrue(graph["evidence_paths"])

    def test_monitor_records_material_changes(self) -> None:
        workbench, boot = self.bootstrap()
        monitor = CaseMonitor(workbench.store)
        first = monitor.snapshot(boot.case["case_id"], label="first")
        workbench.store.create_research_gap(
            boot.case["case_id"],
            subject_refs=[boot.seed_entity["entity_id"]],
            stream="ENTITY_REGISTRY",
            question="Is the seed uniquely identified?",
            why_matters="Namesake risk must be resolved.",
            evidence_needed=["Authoritative registry identifier"],
            owner_role="Analyst",
        )
        second = monitor.snapshot(boot.case["case_id"], label="second")
        self.assertEqual(second["previous_snapshot_id"], first["snapshot_id"])
        self.assertTrue(any(item.startswith("research_gaps:") for item in second["changes"]["added"]))

    def test_read_only_service_exposes_summary_and_rejects_write(self) -> None:
        result = run_demo(self.root, force=True)
        store = WorkbenchStore(self.root)
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(store))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_address[1]}"
            with urllib.request.urlopen(f"{base}/health", timeout=5) as response:
                health = json.loads(response.read().decode("utf-8"))
            self.assertEqual(health["status"], "ok")
            with urllib.request.urlopen(f"{base}/api/v1/cases/{result['case_id']}/summary", timeout=5) as response:
                summary = json.loads(response.read().decode("utf-8"))
            self.assertTrue(summary["journal_integrity"]["valid"])
            request = urllib.request.Request(f"{base}/api/v1/cases", method="POST", data=b"{}")
            with self.assertRaises(urllib.error.HTTPError) as raised:
                urllib.request.urlopen(request, timeout=5)
            self.assertEqual(raised.exception.code, 405)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


class TestPublicURLPolicy(TestCase):
    def test_private_and_credential_urls_are_blocked(self) -> None:
        policy = PublicURLPolicy()
        with self.assertRaises(URLPolicyError):
            policy.validate("http://127.0.0.1/")
        with self.assertRaises(URLPolicyError):
            policy.validate("https://user:pass@example.com/")
        with self.assertRaises(URLPolicyError):
            policy.validate("file:///etc/passwd")

    def test_global_resolution_is_allowed_without_network_request(self) -> None:
        policy = PublicURLPolicy()
        fake = [(2, 1, 6, "", ("93.184.216.34", 443))]
        with mock.patch("socket.getaddrinfo", return_value=fake):
            parsed = policy.validate("https://example.com/path")
        self.assertEqual(parsed.hostname, "example.com")
