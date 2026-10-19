import json
import tempfile
import unittest
from pathlib import Path
from tools.import_existing_m5_telegram import run

class M5ImportTests(unittest.TestCase):
    def test_existing_observations_preserved_and_metrics_not_invented(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/"materials.jsonl";reg=root/"registry.json";snap=root/"snapshots.jsonl"
            records=[
                {"source_type":"telegram","source_locator":"https://t.me/ExampleOSINT/12","title":"Example","material_id":"m1","published_at":"2026-08-12","metadata":{"message_id":"12","views":100,"forwards":3}},
                {"source_type":"telegram","source_locator":"https://t.me/ExampleOSINT/12","title":"Example","material_id":"m2","metadata":{"message_id":"12","views":100}},
                {"source_type":"telegram","source_locator":"https://t.me/ExampleOSINT/13","title":"Example","material_id":"m3","metadata":{"message_id":"13","views":200}},
                {"source_type":"web","source_locator":"https://t.me/ExampleOSINT/14","metadata":{"message_id":"14"}}
            ]
            src.write_text("\n".join(json.dumps(x) for x in records),encoding="utf-8")
            result=run(src,reg,snap)
            self.assertEqual(result["distinct_messages"],2)
            row=json.loads(reg.read_text(encoding="utf-8"))["channels"][0]
            self.assertEqual(row["status"],"candidate")
            self.assertEqual(row["avg_views"],"")
            self.assertEqual(row["subscribers"],"")
            snapshot=json.loads(snap.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(snapshot["observed_views_mean"],150)
            self.assertEqual(snapshot["observed_messages"],2)
            self.assertEqual(src.read_text(encoding="utf-8").count("\n"),3)
if __name__=="__main__":unittest.main()
