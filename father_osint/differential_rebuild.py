from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, Mapping


def _canonical_payload(row: Mapping[str, object]) -> str:
    return json.dumps(dict(row), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class DifferentialProjectionResult:
    id_key: str
    reusable_ids_requested: tuple[str, ...]
    reusable_ids_present_in_oracle: tuple[str, ...]
    missing_reusable_ids: tuple[str, ...]
    reusable_payload_mismatch_ids: tuple[str, ...]
    projection_rows: tuple[dict[str, object], ...]
    oracle_rows: tuple[dict[str, object], ...]
    parity: bool

    @property
    def reusable_payload_exact(self) -> bool:
        return not self.missing_reusable_ids and not self.reusable_payload_mismatch_ids

    def summary(self) -> dict[str, object]:
        return {
            "id_key": self.id_key,
            "reusable_requested": len(self.reusable_ids_requested),
            "reusable_present_in_oracle": len(self.reusable_ids_present_in_oracle),
            "missing_reusable_ids": list(self.missing_reusable_ids),
            "reusable_payload_mismatch_ids": list(self.reusable_payload_mismatch_ids),
            "reusable_payload_exact": self.reusable_payload_exact,
            "projection_rows": len(self.projection_rows),
            "oracle_rows": len(self.oracle_rows),
            "parity": self.parity,
        }


def assemble_selective_projection(
    canonical_rows: Iterable[Mapping[str, object]],
    oracle_rows: Iterable[Mapping[str, object]],
    *,
    reusable_ids: Iterable[str],
    id_key: str,
) -> DifferentialProjectionResult:
    """Assemble a selective projection and compare it with a full oracle result.

    Objects declared reusable are copied byte-for-byte at the logical JSON-object
    level from the canonical graph. Every non-reusable object comes from the full
    rebuilt oracle, including newly created IDs. The proof fails if a supposedly
    reusable object disappears or changes payload in the oracle.

    This verifier intentionally does not promote the projection. It is a bounded
    differential-regression primitive for validating an invalidation partition.
    """

    canonical_by_id: dict[str, dict[str, object]] = {}
    oracle_by_id: dict[str, dict[str, object]] = {}

    for source, target, label in (
        (canonical_rows, canonical_by_id, "canonical"),
        (oracle_rows, oracle_by_id, "oracle"),
    ):
        for row in source:
            object_id = str(row.get(id_key, ""))
            if not object_id:
                raise ValueError(f"{label} row is missing {id_key}")
            if object_id in target:
                raise ValueError(f"duplicate {label} {id_key}: {object_id}")
            target[object_id] = dict(row)

    reusable = tuple(sorted({str(value) for value in reusable_ids if str(value)}))
    missing_canonical = [value for value in reusable if value not in canonical_by_id]
    if missing_canonical:
        raise ValueError(
            "reusable IDs are absent from canonical input: " + ", ".join(missing_canonical[:10])
        )

    missing_oracle = tuple(sorted(value for value in reusable if value not in oracle_by_id))
    mismatches = tuple(
        sorted(
            value
            for value in reusable
            if value in oracle_by_id
            and _canonical_payload(canonical_by_id[value]) != _canonical_payload(oracle_by_id[value])
        )
    )

    projection_by_id: dict[str, dict[str, object]] = {
        value: canonical_by_id[value]
        for value in reusable
        if value in oracle_by_id
    }
    for object_id, row in oracle_by_id.items():
        if object_id not in projection_by_id:
            projection_by_id[object_id] = row

    projection_rows = tuple(projection_by_id[key] for key in sorted(projection_by_id))
    sorted_oracle_rows = tuple(oracle_by_id[key] for key in sorted(oracle_by_id))
    parity = (
        not missing_oracle
        and not mismatches
        and [_canonical_payload(row) for row in projection_rows]
        == [_canonical_payload(row) for row in sorted_oracle_rows]
    )

    return DifferentialProjectionResult(
        id_key=id_key,
        reusable_ids_requested=reusable,
        reusable_ids_present_in_oracle=tuple(sorted(set(reusable) & set(oracle_by_id))),
        missing_reusable_ids=missing_oracle,
        reusable_payload_mismatch_ids=mismatches,
        projection_rows=projection_rows,
        oracle_rows=sorted_oracle_rows,
        parity=parity,
    )
