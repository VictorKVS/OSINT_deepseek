import json
import unittest
from unittest.mock import patch

import scripts.run_programmer_book_main_analyst as base
import scripts.run_programmer_book_main_analyst_resilient as resilient


def candidate(cid):
    return {
        "candidate_id": cid,
        "candidate_type": "CLAIM_CANDIDATE",
        "statement": f"statement {cid}",
        "heading_path": "H",
        "review_score": 10,
    }


class MainAnalystResilientContractTests(unittest.TestCase):
    def test_repair_instruction_separates_relation_type_from_candidate_id(self):
        batch = base.make_batches([candidate("c1"), candidate("c2")], 12)[0]
        text = resilient.repair_instruction(batch, ["invalid relation type: c1"])
        self.assertIn(batch["batch_id"], text)
        self.assertIn("relation.type", text)
        self.assertIn("НИКОГДА не UUID/candidate_id", text)
        self.assertIn("target_candidate_id", text)
        self.assertIn("SUPPORTS", text)

    def test_invalid_first_response_is_repaired_on_second_attempt(self):
        batch = base.make_batches([candidate("c1"), candidate("c2")], 12)[0]
        bad = {
            "batch_id": "WRONG",
            "kb_auto_promotion": False,
            "next_gate": "PROFESSOR_REVIEW_REQUIRED",
            "reviews": [
                {
                    "candidate_id": "c1",
                    "decision": "KEEP_CANDIDATE",
                    "canonical_statement": "s1",
                    "relations": [{
                        "target_candidate_id": "c2",
                        "type": "c2",
                        "confidence": "MEDIUM",
                    }],
                },
                {
                    "candidate_id": "c2",
                    "decision": "KEEP_CANDIDATE",
                    "canonical_statement": "s2",
                    "relations": [],
                },
            ],
        }
        good = {
            "batch_id": batch["batch_id"],
            "kb_auto_promotion": False,
            "next_gate": "PROFESSOR_REVIEW_REQUIRED",
            "reviews": [
                {
                    "candidate_id": "c1",
                    "decision": "KEEP_CANDIDATE",
                    "canonical_statement": "s1",
                    "relations": [{
                        "target_candidate_id": "c2",
                        "type": "SUPPORTS",
                        "confidence": "MEDIUM",
                    }],
                },
                {
                    "candidate_id": "c2",
                    "decision": "KEEP_CANDIDATE",
                    "canonical_statement": "s2",
                    "relations": [],
                },
            ],
        }

        replies = [bad, good]
        captured = []

        def fake_http(url, payload=None, timeout=30):
            captured.append(payload)
            value = replies.pop(0)
            return {
                "choices": [{"message": {"content": json.dumps(value)}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5},
            }

        with patch.object(base, "http_json", side_effect=fake_http):
            result, usage = resilient.call_model_with_contract_repair(
                "http://127.0.0.1:1234/v1", "model", batch, "Book", 30
            )

        self.assertEqual(base.validate(result, batch), [])
        self.assertEqual(len(captured), 2)
        self.assertEqual(usage["prompt_tokens"], 20)
        self.assertEqual(usage["completion_tokens"], 10)
        repair_message = captured[1]["messages"][-1]["content"]
        self.assertIn("batch_id mismatch", repair_message)
        self.assertIn("invalid relation type", repair_message)

    def test_exhausted_repair_fails_closed(self):
        batch = base.make_batches([candidate("c1")], 12)[0]
        bad = {
            "batch_id": "WRONG",
            "kb_auto_promotion": False,
            "next_gate": "PROFESSOR_REVIEW_REQUIRED",
            "reviews": [{
                "candidate_id": "c1",
                "decision": "KEEP_CANDIDATE",
                "canonical_statement": "s1",
                "relations": [],
            }],
        }

        def fake_http(url, payload=None, timeout=30):
            return {"choices": [{"message": {"content": json.dumps(bad)}}]}

        with patch.object(base, "http_json", side_effect=fake_http):
            with self.assertRaisesRegex(ValueError, "contract repair exhausted"):
                resilient.call_model_with_contract_repair(
                    "http://127.0.0.1:1234/v1", "model", batch, "Book", 30
                )


if __name__ == "__main__":
    unittest.main()
