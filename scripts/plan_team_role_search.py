from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
ROLE_REGISTRY = REPO_ROOT / "config" / "team_role_material_registry.json"
DOCTRINE = REPO_ROOT / "config" / "team_material_search_doctrine.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "reports" / "team_role_search_plans"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_role(value: str) -> str:
    return value.strip().upper().replace("-", "_")


def _resolve_role(registry: dict[str, Any], role_id: str) -> dict[str, Any]:
    normalized = _normalize_role(role_id)
    for role in registry.get("roles", []):
        if _normalize_role(str(role.get("role_id") or "")) == normalized:
            return role
    allowed = sorted(str(r.get("role_id")) for r in registry.get("roles", []))
    raise RuntimeError(f"unknown role {role_id!r}; allowed: {', '.join(allowed)}")


def _query(topic: str, template: str) -> str:
    return " ".join(template.format(topic=topic).split())


def build_plan(role: dict[str, Any], doctrine: dict[str, Any], *, max_queries: int) -> dict[str, Any]:
    role_id = _normalize_role(str(role["role_id"]))
    role_rules = doctrine.get("role_specific_rules", {}).get(role_id, {})
    required_dimensions = list(doctrine["topic_package"]["required_dimensions"])
    extra_dimensions = list(role_rules.get("extra_dimensions", []))
    query_templates = doctrine.get("query_templates", {})

    # Planning deliberately starts narrow. P1 anchors are always planned first;
    # P2/P3 are represented as follow-up families but are not exploded into every
    # possible query before evidence/gap analysis.
    family_priority = [
        "OFFICIAL_DOC",
        "CURRENT_VERSION",
        "REFERENCE_IMPLEMENTATION",
        "TEST_VALIDATION",
        "ANTIPATTERN",
        "FAILURE_MODE",
        "TRADEOFF",
    ]

    rows: list[dict[str, Any]] = []
    for topic_index, raw_topic in enumerate(role.get("topics", []), start=1):
        topic = " ".join(str(raw_topic).split()).strip()
        if not topic:
            continue
        topic_id = f"{role_id}-TOPIC-{topic_index:02d}"
        for family in family_priority:
            templates = list(query_templates.get(family, []))
            if not templates:
                continue
            # One deterministic representative query per family. Later passes
            # may generate alternates only for explicit gaps.
            query_text = _query(topic, templates[0])
            if family in {"OFFICIAL_DOC", "CURRENT_VERSION"}:
                pass_id = "P1_ANCHOR"
                channel = "AUTHORITATIVE_WEB_OR_PRIMARY_REPO"
                target_dimension = "AUTHORITATIVE_BASIS"
            elif family in {"REFERENCE_IMPLEMENTATION", "TEST_VALIDATION"}:
                pass_id = "P2_METHOD"
                channel = "PRIMARY_DOCS_REPO_BOOK_COURSE"
                target_dimension = "PRACTICAL_METHOD_OR_IMPLEMENTATION" if family == "REFERENCE_IMPLEMENTATION" else "VALIDATION_OR_TEST"
            else:
                pass_id = "P3_CHALLENGE"
                channel = "POSTMORTEM_ISSUES_BOOK_COMMUNITY"
                target_dimension = "FAILURE_MODE_OR_ANTIPATTERN"
            rows.append(
                {
                    "topic_id": topic_id,
                    "topic": topic,
                    "pass_id": pass_id,
                    "query_family": family,
                    "query": query_text,
                    "target_dimension": target_dimension,
                    "channel": channel,
                    "telegram_allowed": pass_id != "P1_ANCHOR",
                    "priority": "P0" if pass_id == "P1_ANCHOR" else "P1",
                }
            )

    # Enforce a hard bounded plan while preserving topic breadth: take anchors
    # before methods/challenges, then stable topic order.
    pass_order = {"P1_ANCHOR": 0, "P2_METHOD": 1, "P3_CHALLENGE": 2, "P4_GAP_ONLY": 3}
    rows.sort(key=lambda row: (pass_order[row["pass_id"]], row["topic_id"], row["query_family"]))
    selected = rows[:max_queries]

    return {
        "record_type": "TEAM_ROLE_SEARCH_PLAN",
        "schema_version": "1.0",
        "doctrine_id": doctrine.get("doctrine_id"),
        "role_id": role_id,
        "knowledge_base_id": role.get("knowledge_base_id"),
        "role_priority": role.get("priority"),
        "topics_total": len([t for t in role.get("topics", []) if str(t).strip()]),
        "required_dimensions": required_dimensions,
        "role_extra_dimensions": extra_dimensions,
        "planned_queries_total": len(selected),
        "candidate_queries_before_bound": len(rows),
        "max_queries": max_queries,
        "policy": {
            "plan_before_collection": True,
            "authoritative_first": True,
            "telegram_for_anchor_pass": False,
            "gap_only_after_first_pass": True,
            "no_unbounded_role_scraping": True,
            "kb_auto_promotion": False,
        },
        "queries": selected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a bounded doctrine-driven FATHER role search plan")
    parser.add_argument("--role", required=True)
    parser.add_argument("--max-queries", type=int, default=80)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    registry = _load(ROLE_REGISTRY)
    doctrine = _load(DOCTRINE)
    role = _resolve_role(registry, args.role)
    max_queries = max(1, min(200, int(args.max_queries)))
    plan = build_plan(role, doctrine, max_queries=max_queries)

    role_id = plan["role_id"]
    output = Path(args.output).resolve() if args.output else DEFAULT_OUTPUT_ROOT / f"LATEST_{role_id}_SEARCH_PLAN.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = {
        "role_id": role_id,
        "knowledge_base_id": plan.get("knowledge_base_id"),
        "topics_total": plan["topics_total"],
        "planned_queries_total": plan["planned_queries_total"],
        "candidate_queries_before_bound": plan["candidate_queries_before_bound"],
        "max_queries": plan["max_queries"],
        "authoritative_first": plan["policy"]["authoritative_first"],
        "telegram_for_anchor_pass": plan["policy"]["telegram_for_anchor_pass"],
        "report_path": str(output.relative_to(REPO_ROOT)).replace("\\", "/") if output.is_relative_to(REPO_ROOT) else str(output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
