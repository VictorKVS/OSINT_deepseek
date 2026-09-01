from __future__ import annotations

import json
from pathlib import Path

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
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for fixture_name, schema_name in MAPPING.items():
        schema = load(SCHEMAS / schema_name)
        Draft202012Validator.check_schema(schema)
        instance = load(FIXTURES / fixture_name)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            failures.extend(
                f"{fixture_name}: {'/'.join(map(str, e.path))}: {e.message}"
                for e in errors
            )
        else:
            print(f"PASS {fixture_name} -> {schema_name}")
    if failures:
        print("\nFAIL")
        for failure in failures:
            print(f" - {failure}")
        return 1
    print(f"\nPASS: {len(MAPPING)} fixtures validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
