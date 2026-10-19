"""Offline regression tests for ALINA Research Advisor API."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import alina_research_server as srv

class ResearchAdvisorTests(unittest.TestCase):
    def test_retrieve_returns_source_and_does_not_invent(self):
        docs=[{"id":"a","title":"OSINT Telegram","text":"Проверка источника","source":"docs/a.md"},
              {"id":"b","title":"Other","text":"unrelated","source":"docs/b.md"}]
        results=srv.retrieve("OSINT Telegram",docs)
        self.assertEqual(results[0]["source"],"docs/a.md")
        self.assertEqual(len(results),1)

    def test_build_ranks_verified_with_observations(self):
        channels=[{"channel_id":"1","title":"OSINT Telegram","topics":"OSINT","status":"verified",
                   "verified_at_utc":"2026-10-19T00:00:00Z","evidence_links":"3",
                   "subscribers":"100","posts_30d":"12"},
                  {"channel_id":"2","title":"Unrelated","status":"candidate"}]
        with patch.object(srv,"channels",return_value=channels),patch.object(srv,"knowledge",return_value=[]):
            result=srv.build("OSINT Telegram",threshold=50)
        self.assertEqual([x["channel_id"] for x in result["suggested_channels"]],["1"])
        self.assertEqual(result["execution"],"not_started")
        self.assertEqual(result["approval"],"required_before_collection")

    def test_unknown_metrics_not_awarded_points(self):
        with patch.object(srv,"channels",return_value=[{"channel_id":"a","title":"OSINT","status":"candidate"}]),patch.object(srv,"knowledge",return_value=[]):
            result=srv.build("OSINT",threshold=0)
        self.assertEqual(result["suggested_channels"][0]["reasons"]["dated_metrics"],0)
        self.assertEqual(result["suggested_channels"][0]["reasons"]["verified_identity"],0)

if __name__=="__main__":
    unittest.main()
