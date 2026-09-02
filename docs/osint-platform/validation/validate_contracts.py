from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

BASE = Path(__file__).resolve().parents[1]
SCHEMAS = BASE / "schemas"
FIXTURES = BASE / "fixtures" / "CASE-SYNTH-0001"

MAPPING = {
    "case.json": "case.schema.json",
    "source.json": "source.schema.json",
    "source-capture.json": "source-capture.schema.json",
    "entity-organization.json": "entity.schema.json",
    "entity-address.json": "entity.schema.json",
    "entity-organization-namesake.json": "entity.schema.json",
    "claim.json": "claim.schema.json",
    "relation.json": "relation.schema.json",
    "analysis-run.json": "analysis-run.schema.json",
    "opn-0001.json": "analysis-opinion.schema.json",
    "opn-0002.json": "analysis-opinion.schema.json",
    "opn-0003.json": "analysis-opinion.schema.json",
    "consensus.json": "consensus.schema.json",
    "finding.json": "finding.schema.json",
    "tool-adapter.json": "tool-adapter.schema.json",
    "audit-event.json": "audit-event.schema.json",
    "export-manifest.json": "export-manifest.schema.json",
    "query-plan.json": "query-plan.schema.json",
    "transform.json": "transform.schema.json",
    "acquisition-job.json": "acquisition-job.schema.json",
    "entity-match.json": "entity-match.schema.json",
    "research-gap.json": "research-gap.schema.json",
    "coverage.json": "coverage.schema.json",
    "graph-view.json": "graph-view.schema.json",
    "journal-0001.json": "search-journal.schema.json",
    "journal-0002.json": "search-journal.schema.json",
    "journal-0003.json": "search-journal.schema.json",
    "journal-0004.json": "search-journal.schema.json",
    "journal-0005.json": "search-journal.schema.json",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash_without(instance: dict[str, Any], field: str) -> str:
    payload = {key: value for key, value in instance.items() if key != field}
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_schema_and_instances() -> list[str]:
    failures: list[str] = []

    schema_files = sorted(SCHEMAS.glob("*.schema.json"))
    for schema_path in schema_files:
        try:
            Draft202012Validator.check_schema(load(schema_path))
            print(f"PASS schema meta-validation: {schema_path.name}")
        except Exception as exc:  # pragma: no cover - CLI diagnostic
            failures.append(f"{schema_path.name}: invalid schema: {exc}")

    for fixture_name, schema_name in MAPPING.items():
        fixture_path = FIXTURES / fixture_name
        schema_path = SCHEMAS / schema_name
        if not fixture_path.exists():
            failures.append(f"{fixture_name}: fixture missing")
            continue
        if not schema_path.exists():
            failures.append(f"{schema_name}: schema missing")
            continue

        instance = load(fixture_path)
        validator = Draft202012Validator(
            load(schema_path),
            format_checker=FormatChecker(),
        )
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        if errors:
            failures.extend(
                f"{fixture_name}: {'/'.join(map(str, error.path))}: {error.message}"
                for error in errors
            )
        else:
            print(f"PASS fixture: {fixture_name} -> {schema_name}")

    return failures


def validate_query_plan_hash() -> list[str]:
    plan = load(FIXTURES / "query-plan.json")
    expected = canonical_hash_without(plan, "plan_hash")
    if plan["plan_hash"] != expected:
        return [f"query-plan.json: plan_hash mismatch; expected {expected}"]
    print("PASS semantic check: query-plan hash")
    return []


def validate_journal_chain() -> list[str]:
    failures: list[str] = []
    entries = [load(path) for path in sorted(FIXTURES.glob("journal-*.json"))]
    expected_sequence = list(range(1, len(entries) + 1))
    actual_sequence = [entry["sequence"] for entry in entries]
    if actual_sequence != expected_sequence:
        failures.append(
            f"search journal sequence mismatch: expected {expected_sequence}, got {actual_sequence}"
        )

    previous: str | None = None
    for entry in entries:
        if entry["previous_entry_hash"] != previous:
            failures.append(
                f"{entry['journal_id']}: previous_entry_hash mismatch; expected {previous}"
            )
        expected_hash = canonical_hash_without(entry, "entry_hash")
        if entry["entry_hash"] != expected_hash:
            failures.append(
                f"{entry['journal_id']}: entry_hash mismatch; expected {expected_hash}"
            )
        previous = entry["entry_hash"]

    if not failures:
        print(f"PASS semantic check: journal hash chain ({len(entries)} entries)")
    return failures


def validate_graph_references() -> list[str]:
    failures: list[str] = []
    graph = load(FIXTURES / "graph-view.json")

    primary_id_fields = (
        "capture_id",
        "entity_id",
        "claim_id",
        "relation_id",
        "analysis_run_id",
        "opinion_id",
        "consensus_id",
        "finding_id",
        "tool_adapter_id",
        "audit_event_id",
        "export_manifest_id",
        "query_plan_id",
        "transform_id",
        "job_id",
        "entity_match_id",
        "research_gap_id",
        "coverage_id",
        "graph_view_id",
        "journal_id",
        "source_id",
        "case_id",
    )
    known_ids: set[str] = set()
    for path in FIXTURES.glob("*.json"):
        document = load(path)
        for field in primary_id_fields:
            value = document.get(field)
            if isinstance(value, str):
                known_ids.add(value)
                break

    node_ids = {node["node_id"] for node in graph["nodes"]}
    for edge in graph["edges"]:
        if edge["from_node_id"] not in node_ids:
            failures.append(f"{edge['edge_id']}: unknown from_node_id")
        if edge["to_node_id"] not in node_ids:
            failures.append(f"{edge['edge_id']}: unknown to_node_id")

    for evidence_path in graph["evidence_paths"]:
        for step in evidence_path["steps"]:
            if step["object_id"] not in known_ids:
                failures.append(
                    f"{evidence_path['evidence_path_id']}: unknown object_id "
                    f"{step['object_id']}"
                )

    if not failures:
        print("PASS semantic check: graph node/edge/evidence-path references")
    return failures


def main() -> int:
    failures: list[str] = []
    failures.extend(validate_schema_and_instances())
    failures.extend(validate_query_plan_hash())
    failures.extend(validate_journal_chain())
    failures.extend(validate_graph_references())

    if failures:
        print("\nFAIL")
        for failure in failures:
            print(f" - {failure}")
        return 1

    schema_count = len(list(SCHEMAS.glob("*.schema.json")))
    print(
        f"\nPASS: {schema_count} schemas meta-validated, "
        f"{len(MAPPING)} fixtures schema-validated, "
        "4 semantic integrity checks passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
