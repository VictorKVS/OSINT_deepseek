"""Reference solution candidates for the FATHER Programmer MIN TRAIN split.

These functions are deliberately small and dependency-free. They are not promoted to
Golden Cases merely by existing: regression tests and critic review must pass first.
The HOLDOUT split is intentionally absent from this module.
"""

from __future__ import annotations

from typing import Any


def sum_positive(values: list[int | float]) -> int | float:
    total: int | float = 0
    for value in values:
        if value > 0:
            total += value
    return total


def stable_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def parse_ints(items: list[object]) -> list[int]:
    result: list[int] = []
    for item in items:
        if isinstance(item, bool):
            continue
        if isinstance(item, int):
            result.append(item)
            continue
        if isinstance(item, str):
            try:
                result.append(int(item, 10))
            except ValueError:
                continue
    return result


def first_index(sorted_values: list[int], target: int) -> int:
    lo = 0
    hi = len(sorted_values)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if sorted_values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    if lo < len(sorted_values) and sorted_values[lo] == target:
        return lo
    return -1


def chunked(values: list[Any], size: int) -> list[list[Any]]:
    if size <= 0:
        raise ValueError("size must be greater than zero")
    return [values[index:index + size] for index in range(0, len(values), size)]


def safe_ratio(numerator: float, denominator: float, default=None):
    if denominator == 0:
        return default
    return numerator / denominator


def word_frequency(words: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def merge_sorted(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged
