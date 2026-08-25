import pytest

from training.programmer import min_reference_solutions as ref


def test_pt_min_001_sum_positive():
    values = [1, -2, 3, 0, 1.5]
    before = list(values)
    assert ref.sum_positive(values) == 5.5
    assert values == before
    assert ref.sum_positive([]) == 0


def test_pt_min_002_stable_unique():
    values = ["a", "b", "a", "c", "b"]
    before = list(values)
    assert ref.stable_unique(values) == ["a", "b", "c"]
    assert values == before
    assert ref.stable_unique([]) == []


def test_pt_min_003_parse_ints_rejects_bool_and_bad_values():
    assert ref.parse_ints(["1", " -2 ", 3, True, False, 4.0, "x", None]) == [1, -2, 3]
    assert ref.parse_ints([]) == []


def test_pt_min_004_first_index_is_leftmost():
    assert ref.first_index([1, 2, 2, 2, 3], 2) == 1
    assert ref.first_index([1, 3, 5], 4) == -1
    assert ref.first_index([], 1) == -1
    assert ref.first_index([7], 7) == 0


def test_pt_min_005_chunked_validates_size_and_preserves_input():
    values = [1, 2, 3, 4, 5]
    before = list(values)
    assert ref.chunked(values, 2) == [[1, 2], [3, 4], [5]]
    assert ref.chunked([], 3) == []
    assert values == before
    with pytest.raises(ValueError):
        ref.chunked(values, 0)
    with pytest.raises(ValueError):
        ref.chunked(values, -1)


def test_pt_min_006_safe_ratio():
    assert ref.safe_ratio(10, 2) == 5
    assert ref.safe_ratio(1, 0) is None
    assert ref.safe_ratio(1, 0, default="NA") == "NA"


def test_pt_min_007_word_frequency_preserves_case():
    assert ref.word_frequency(["a", "b", "a", "A"]) == {"a": 2, "b": 1, "A": 1}
    assert ref.word_frequency([]) == {}


def test_pt_min_008_merge_sorted_linear_merge_contract():
    left = [1, 3, 5]
    right = [2, 4, 6]
    left_before = list(left)
    right_before = list(right)
    assert ref.merge_sorted(left, right) == [1, 2, 3, 4, 5, 6]
    assert ref.merge_sorted([], [1]) == [1]
    assert ref.merge_sorted([1], []) == [1]
    assert ref.merge_sorted([1, 1], [1, 2]) == [1, 1, 1, 2]
    assert left == left_before
    assert right == right_before


def test_holdout_reference_solutions_are_not_present():
    for name in ("validate_port", "top_k_frequent", "redact_secret", "backoff_schedule"):
        assert not hasattr(ref, name)
