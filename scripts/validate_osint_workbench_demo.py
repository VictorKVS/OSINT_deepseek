from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from osint_workbench.canonical import sha256_json
from osint_workbench.store import WorkbenchStore

SCHEMA_MAPPING = {
    "case.json": "case.schema.json",
    "query_plans": "query-plan.schema.json",
    "sources": "source.schema.json",
    "captures": "source-capture.schema.json",
    "entities": "entity.schema.json",
    "claims": "claim.schema.json",
    "relations": "relation.schema.json",
    "findings": "finding.schema.json",
    "research_gaps": "research-gap.schema.json",
    "entity_matches": "entity-match.schema.json",
    "coverage": "coverage.schema.json",
    "graphs": "graph-view.schema.json",
    "transforms": "transform.schema.json",
    "jobs": "acquisition-job.schema.json",
    "journal": "search-journal.schema.json",
    "analysis_runs": "analysis-run.schema.json",
    "analysis_opinions": "analysis-opinion.schema.json",
    "consensus": "consensus.schema.json",
}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate(root: Path, case_id: str, schemas: Path) -> dict[str, Any]:
    store = WorkbenchStore(root)
    case_dir = store.case_dir(case_id)
    failures: list[str] = []
    validated = 0
    for target, schema_name in SCHEMA_MAPPING.items():
        schema = load(schemas / schema_name)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        paths = [case_dir / target] if target.endswith(".json") else sorted((case_dir / target).glob("*.json"))
        for path in paths:
            instance = load(path)
            validated += 1
            for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
                locator = "/".join(map(str, error.path))
                failures.append(f"{path.relative_to(case_dir)}:{locator}: {error.message}")

    plans = store.list_objects(case_id, "query_plan")
    for plan in plans:
        expected = sha256_json(plan, exclude_fields={"plan_hash"})
        if plan.get("plan_hash") != expected:
            failures.append(f"{plan.get('query_plan_id')}: canonical plan hash mismatch")

    journal = store.verify_journal(case_id)
    failures.extend(f"journal: {item}" for item in journal["failures"])

    known_refs: set[str] = set()
    for kind in store.OBJECT_DIRS:
        for item in store.list_objects(case_id, kind):
            id_field = store.ID_FIELDS[kind]
            if item.get(id_field):
                known_refs.add(str(item[id_field]))
    for graph in store.list_objects(case_id, "graph"):
        for edge in graph.get("edges", []):
            for key in ("from_node_id", "to_node_id"):
                if edge.get(key) not in known_refs:
                    failures.append(f"{graph['graph_view_id']}: missing graph {key}={edge.get(key)}")
        for path in graph.get("evidence_paths", []):
            for step in path.get("steps", []):
                if step.get("object_id") not in known_refs:
                    failures.append(f"{graph['graph_view_id']}: unresolved evidence path ref {step.get('object_id')}")

    result = {
        "case_id": case_id,
        "schema_objects_validated": validated,
        "schema_count": len(SCHEMA_MAPPING),
        "journal_entries": journal["entries"],
        "journal_valid": journal["valid"],
        "semantic_checks": ["query_plan_hash", "journal_hash_chain", "graph_reference_integrity"],
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated OSINT Workbench objects against Architecture Baseline schemas")
    parser.add_argument("--root", default="data/osint-workbench-demo")
    parser.add_argument("--case-id", default="CASE-SYNTH-CORE-0001")
    parser.add_argument("--schemas", default="docs/osint-platform/schemas")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = validate(Path(args.root), args.case_id, Path(args.schemas))
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    print(text, end="")
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
