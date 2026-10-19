"""Tests for official TGStat adapter: no network or API key required."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import tgstat_channel_discovery as adapter

class TGStatTests(unittest.TestCase):
    def test_channel_mapping(self):
        row=adapter.row_from_item({"peer_type":"channel","username":"@ExampleOSINT","title":"OSINT",
            "participants_count":1234},"osint","2026-10-19T00:00:00Z")
        self.assertEqual(row["url"],"https://t.me/ExampleOSINT")
        self.assertEqual(row["subscribers"],"1234")
        self.assertEqual(row["status"],"candidate")
        self.assertEqual(row["verified_at_utc"],"")
    def test_reject_chat_and_bad_handle(self):
        self.assertIsNone(adapter.row_from_item({"peer_type":"chat","username":"@ValidName"},"q","now"))
        self.assertIsNone(adapter.row_from_item({"peer_type":"channel","username":"bad!"},"q","now"))
    def test_search_and_stat_snapshots(self):
        class Args:pass
        with tempfile.TemporaryDirectory() as temp:
            args=Args();root=Path(temp)
            args.query=["OSINT"];args.limit=20;args.country="ru";args.stats=True
            args.max_stats=1;args.pause=0
            args.registry=root/"registry.json";args.snapshots=root/"snapshots.jsonl";args.report=root/"report.json"
            def fake_get(path,params,token):
                if path.endswith("/search"):
                    return {"items":[{"id":77,"tg_id":88,"peer_type":"channel","username":"@ExampleOSINT","title":"Example","participants_count":100}]}
                return {"peer_type":"channel","participants_count":120,"avg_post_reach":35,"err_percent":29}
            with patch.object(adapter,"get",side_effect=fake_get):
                adapter.run(args,"fake-token")
            registry=json.loads(args.registry.read_text(encoding="utf-8"))["channels"]
            self.assertEqual(registry[0]["subscribers"],"120")
            self.assertEqual(registry[0]["avg_views"],"35")
            self.assertEqual(registry[0]["status"],"candidate")
            snaps=[json.loads(line) for line in args.snapshots.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(snaps),2)
            self.assertEqual(snaps[1]["provider"],"tgstat")
    def test_api_errors_do_not_echo_token(self):
        def opener(request,timeout):
            raise __import__("urllib").error.HTTPError(request.full_url,403,"Forbidden",None,None)
        with self.assertRaisesRegex(RuntimeError,"HTTP 403") as ctx:
            adapter.get("/channels/search",{"q":"osint"},"secret-token",opener=opener)
        self.assertNotIn("secret-token",str(ctx.exception))

if __name__=="__main__":unittest.main()
