from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training.programmer import min_reference_solutions as ref


def expect_value_error(func, *args) -> None:
    try:
        func(*args)
    except ValueError:
        return
    raise AssertionError(f"expected ValueError from {getattr(func, '__name__', func)!r}")


def main() -> int:
    checks: list[tuple[str, callable]] = [
        (
            "PT-MIN-001",
            lambda: (
                (lambda values: (
                    (_ for _ in ()).throw(AssertionError("sum_positive result mismatch"))
                    if ref.sum_positive(values) != 5.5 else None,
                    (_ for _ in ()).throw(AssertionError("sum_positive mutated input"))
                    if values != [1, -2, 3, 0, 1.5] else None,
                    (_ for _ in ()).throw(AssertionError("sum_positive empty mismatch"))
                    if ref.sum_positive([]) != 0 else None,
                ))([1, -2, 3, 0, 1.5])
            ),
        ),
        (
            "PT-MIN-002",
            lambda: (
                (lambda values: (
                    (_ for _ in ()).throw(AssertionError("stable_unique result mismatch"))
                    if ref.stable_unique(values) != ["a", "b", "c"] else None,
                    (_ for _ in ()).throw(AssertionError("stable_unique mutated input"))
                    if values != ["a", "b", "a", "c", "b"] else None,
                    (_ for _ in ()).throw(AssertionError("stable_unique empty mismatch"))
                    if ref.stable_unique([]) != [] else None,
                ))(["a", "b", "a", "c", "b"])
            ),
        ),
        (
            "PT-MIN-003",
            lambda: (
                (_ for _ in ()).throw(AssertionError("parse_ints mismatch"))
                if ref.parse_ints(["1", " -2 ", 3, True, False, 4.0, "x", None]) != [1, -2, 3]
                else None
            ),
        ),
        (
            "PT-MIN-004",
            lambda: (
                (_ for _ in ()).throw(AssertionError("first_index leftmost mismatch"))
                if ref.first_index([1, 2, 2, 2, 3], 2) != 1
                else None,
                (_ for _ in ()).throw(AssertionError("first_index missing mismatch"))
                if ref.first_index([1, 3, 5], 4) != -1
                else None,
                (_ for _ in ()).throw(AssertionError("first_index empty mismatch"))
                if ref.first_index([], 1) != -1
                else None,
                (_ for _ in ()).throw(AssertionError("first_index singleton mismatch"))
                if ref.first_index([7], 7) != 0
                else None,
            ),
        ),
        (
            "PT-MIN-005",
            lambda: (
                (lambda values: (
                    (_ for _ in ()).throw(AssertionError("chunked result mismatch"))
                    if ref.chunked(values, 2) != [[1, 2], [3, 4], [5]] else None,
                    (_ for _ in ()).throw(AssertionError("chunked mutated input"))
                    if values != [1, 2, 3, 4, 5] else None,
                    expect_value_error(ref.chunked, values, 0),
                    expect_value_error(ref.chunked, values, -1),
                ))([1, 2, 3, 4, 5])
            ),
        ),
        (
            "PT-MIN-006",
            lambda: (
                (_ for _ in ()).throw(AssertionError("safe_ratio normal mismatch"))
                if ref.safe_ratio(10, 2) != 5
                else None,
                (_ for _ in ()).throw(AssertionError("safe_ratio zero mismatch"))
                if ref.safe_ratio(1, 0) is not None
                else None,
                (_ for _ in ()).throw(AssertionError("safe_ratio default mismatch"))
                if ref.safe_ratio(1, 0, default="NA") != "NA"
                else None,
            ),
        ),
        (
            "PT-MIN-007",
            lambda: (
                (_ for _ in ()).throw(AssertionError("word_frequency mismatch"))
                if ref.word_frequency(["a", "b", "a", "A"]) != {"a": 2, "b": 1, "A": 1}
                else None
            ),
        ),
        (
            "PT-MIN-008",
            lambda: (
                (lambda left, right: (
                    (_ for _ in ()).throw(AssertionError("merge_sorted mismatch"))
                    if ref.merge_sorted(left, right) != [1, 2, 3, 4, 5, 6] else None,
                    (_ for _ in ()).throw(AssertionError("merge_sorted mutated left"))
                    if left != [1, 3, 5] else None,
                    (_ for _ in ()).throw(AssertionError("merge_sorted mutated right"))
                    if right != [2, 4, 6] else None,
                    (_ for _ in ()).throw(AssertionError("merge_sorted duplicate mismatch"))
                    if ref.merge_sorted([1, 1], [1, 2]) != [1, 1, 1, 2] else None,
                ))([1, 3, 5], [2, 4, 6])
            ),
        ),
    ]

    failures: list[dict[str, str]] = []
    passed = 0
    for task_id, check in checks:
        try:
            check()
            passed += 1
        except Exception as exc:  # verification report must preserve the actual defect
            failures.append({"task_id": task_id, "error": f"{type(exc).__name__}: {exc}"})

    holdout_names = ("validate_port", "top_k_frequent", "redact_secret", "backoff_schedule")
    leaked = [name for name in holdout_names if hasattr(ref, name)]
    if leaked:
        failures.append({"task_id": "HOLDOUT_ISOLATION", "error": "unexpected holdout implementations: " + ", ".join(leaked)})

    payload = {
        "record_type": "PROGRAMMER_MIN_STDLIB_REGRESSION",
        "status": "PASS" if not failures else "FAIL",
        "checks_total": len(checks),
        "checks_passed": passed,
        "checks_failed": len(failures),
        "holdout_implementation_leak_total": len(leaked),
        "failures": failures,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
