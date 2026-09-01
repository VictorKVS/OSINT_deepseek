import unittest

from scripts.run_programmer_book_main_analyst import make_batches, validate


def candidate(cid, heading="H", score=10):
    return {
        "candidate_id": cid,
        "candidate_type": "CLAIM_CANDIDATE",
        "statement": f"statement {cid}",
        "heading_path": heading,
        "review_score": score,
    }


class MainAnalystContractTests(unittest.TestCase):
    def test_batches_are_heading_scoped_and_deterministic(self):
        rows = [candidate("c2", "B"), candidate("c1", "A"), candidate("c3", "A")]
        first = make_batches(rows, 2)
        second = make_batches(rows, 2)
        self.assertEqual(first, second)
        self.assertEqual([b["heading"] for b in first], ["A", "B"])
        self.assertEqual([len(b["candidates"]) for b in first], [2, 1])

    def test_valid_review_covers_every_candidate_once(self):
        batch = make_batches([candidate("c1"), candidate("c2")], 12)[0]
        result = {
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
                    "decision": "HOLD_AMBIGUOUS",
                    "canonical_statement": "s2",
                    "relations": [],
                },
            ],
        }
        self.assertEqual(validate(result, batch), [])

    def test_review_fails_on_out_of_batch_relation_and_missing_candidate(self):
        batch = make_batches([candidate("c1"), candidate("c2")], 12)[0]
        result = {
            "batch_id": batch["batch_id"],
            "kb_auto_promotion": False,
            "next_gate": "PROFESSOR_REVIEW_REQUIRED",
            "reviews": [{
                "candidate_id": "c1",
                "decision": "KEEP_CANDIDATE",
                "canonical_statement": "s1",
                "relations": [{
                    "target_candidate_id": "outside",
                    "type": "SUPPORTS",
                    "confidence": "HIGH",
                }],
            }],
        }
        errors = validate(result, batch)
        self.assertTrue(any("outside batch" in error for error in errors))
        self.assertTrue(any("exactly once" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
