from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROLE_REGISTRY = ROOT / "config" / "team_role_material_registry.json"
POLICY_PATH = ROOT / "config" / "library_order_policy.json"
RU_BASELINE_PATH = ROOT / "config" / "role_ru_regulatory_baseline.json"
ORDER_ROOT = ROOT / "reports" / "library_orders"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_role(value: str) -> str:
    return value.strip().upper().replace("-", "_")


def resolve_role(role_id: str) -> dict[str, Any]:
    normalized = normalize_role(role_id)
    registry = load_json(ROLE_REGISTRY)
    for role in registry.get("roles", []):
        if str(role.get("role_id", "")).upper() == normalized:
            return role
    raise RuntimeError(f"unknown role {role_id!r}")


def resolve_ru_baseline(role_id: str) -> dict[str, Any]:
    baseline = load_json(RU_BASELINE_PATH)
    role = (baseline.get("roles") or {}).get(normalize_role(role_id))
    if not isinstance(role, dict):
        return {
            "state": "RESEARCH_REQUIRED",
            "required_clusters": [],
            "documents": [],
            "known_superseded": [],
            "next_research": ["build Russian regulatory and national-standards baseline for this role"],
        }
    active_documents = [row for row in role.get("documents", []) if row.get("status") == "ACTIVE"]
    unverified = [row.get("designation") for row in active_documents if row.get("verification_state") != "OFFICIAL_METADATA_VERIFIED"]
    state = "READY_FOR_APPLICABILITY_REVIEW" if active_documents and not unverified else "RESEARCH_REQUIRED"
    return {
        "state": state,
        "baseline_state": role.get("baseline_state"),
        "required_clusters": role.get("required_clusters", []),
        "documents": active_documents,
        "known_superseded": role.get("known_superseded", []),
        "next_research": role.get("next_research", []),
        "unverified_designations": unverified,
    }


def trace_context() -> dict[str, Any]:
    return {
        "trace_id": os.getenv("FATHER_TRACE_ID") or f"TRACE-{uuid.uuid4().hex[:12]}",
        "correlation_id": os.getenv("FATHER_CORRELATION_ID") or f"CORR-{uuid.uuid4().hex[:12]}",
        "task_id": os.getenv("FATHER_TASK_ID") or f"TASK-{uuid.uuid4().hex[:10]}",
        "command_id": os.getenv("FATHER_COMMAND_ID") or f"CMD-{uuid.uuid4().hex[:10]}",
        "parent_command_id": os.getenv("FATHER_PARENT_COMMAND_ID"),
    }


def parse_sources(raw: str | None, policy: dict[str, Any]) -> list[str]:
    allowed = list(policy.get("default_sources", []))
    if not raw:
        return allowed
    requested = [part.strip().upper() for part in raw.split(",") if part.strip()]
    unknown = [item for item in requested if item not in allowed]
    if unknown:
        raise RuntimeError(f"unsupported source channel(s): {', '.join(unknown)}")
    return requested


def build_order(*, role: dict[str, Any], maturity: str, mode: str, sources: list[str]) -> dict[str, Any]:
    policy = load_json(POLICY_PATH)
    maturity = maturity.upper()
    if maturity not in policy.get("maturity_levels", {}):
        raise RuntimeError(f"unsupported maturity {maturity!r}")
    if mode not in {"AUTO_BOUNDED", "REVIEW_EACH_STAGE"}:
        raise RuntimeError(f"unsupported execution mode {mode!r}")

    role_id = str(role["role_id"]).upper()
    ru_baseline = resolve_ru_baseline(role_id)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    order_id = f"LIB-{role_id}-{stamp}-{uuid.uuid4().hex[:6].upper()}"
    topics = [
        {
            "target_id": f"{role_id}-TOPIC-{idx:02d}",
            "topic": str(topic),
            "destination": f"data/team_role_telegram/{role_id.casefold()}/{role_id.casefold()}-topic-{idx:02d}",
            "state": "PLANNED",
        }
        for idx, topic in enumerate(role.get("topics", []), start=1)
    ]
    source_state = {
        "RU_OFFICIAL_REGULATORY": "READY_FOR_APPLICABILITY_REVIEW" if ru_baseline["state"] == "READY_FOR_APPLICABILITY_REVIEW" else "RESEARCH_REQUIRED",
        "OFFICIAL_WEB": "CONNECTOR_PENDING",
        "GITHUB": "CONNECTOR_PENDING",
        "TELEGRAM": "READY" if "TELEGRAM" in sources else "NOT_REQUESTED",
        "LOCAL_LIBRARY": "MANUAL_OR_USER_AUTHORIZED_IMPORT_PENDING",
    }
    gaps: list[dict[str, Any]] = []
    if ru_baseline["state"] != "READY_FOR_APPLICABILITY_REVIEW":
        gaps.append({
            "type": "RU_REGULATORY_BASELINE_GAP",
            "role_id": role_id,
            "blocking_for_maturity_claim": True,
        })

    return {
        "schema_version": "1.1",
        "record_type": "FATHER_LIBRARY_ORDER",
        "order_id": order_id,
        "created_at_epoch": time.time(),
        "updated_at_epoch": time.time(),
        "role_id": role_id,
        "knowledge_base_id": role.get("knowledge_base_id"),
        "role_priority": role.get("priority"),
        "stream_id": role.get("stream_id"),
        "maturity_target": maturity,
        "maturity_requirements": policy["maturity_levels"][maturity],
        "execution_mode": mode,
        "requested_sources": sources,
        "source_states": {key: value for key, value in source_state.items() if key in sources},
        "regulatory_first_policy": policy.get("regulatory_first_policy", {}),
        "ru_regulatory_baseline": ru_baseline,
        "copyright_policy": policy.get("copyright_policy", {}),
        "topics": topics,
        "topics_total": len(topics),
        "state": "ORDER_CREATED",
        "current_stage": "STAGE_0_RU_REGULATORY_BASELINE",
        "stages": {
            "STAGE_0_RU_REGULATORY_BASELINE": {
                "state": ru_baseline["state"],
                "evidence_refs": [row.get("official_source") for row in ru_baseline.get("documents", []) if row.get("official_source")],
                "documents_total": len(ru_baseline.get("documents", [])),
            },
            "STAGE_1_ACQUISITION": {"state": "READY", "evidence_refs": []},
            "STAGE_1_COVERAGE": {"state": "PENDING", "evidence_refs": []},
            "STAGE_2_DOCUMENT_COMPILER": {"state": "PENDING", "evidence_refs": []},
            "STAGE_3_KNOWLEDGE_EXTRACTION": {"state": "PENDING", "evidence_refs": []},
            "STAGE_4_RELATIONS_AND_CONFLICTS": {"state": "PENDING", "evidence_refs": []},
            "STAGE_5_ANALYST_AND_CRITIC": {"state": "PENDING", "evidence_refs": []},
            "STAGE_6_REVIEW": {"state": "PENDING", "evidence_refs": []},
            "KB_READY": {"state": "BLOCKED_UNTIL_HUMAN_REVIEW", "evidence_refs": []},
        },
        "metrics": {
            "ru_regulatory_documents_total": len(ru_baseline.get("documents", [])),
            "search_hits_total": 0,
            "downloaded_total": 0,
            "reused_total": 0,
            "failed_total": 0,
            "bytes_downloaded": 0,
            "topics_covered": 0,
            "topics_gap": len(topics),
            "speedup_vs_1_stream_pct": None,
            "eta_seconds": None,
        },
        "gaps": gaps,
        "next_actions": ["REVIEW_RU_REGULATORY_APPLICABILITY", "RUN_STAGE_1_ACQUISITION"],
        "kb_auto_promotion": False,
        "trace": trace_context(),
    }


def save_order(order: dict[str, Any]) -> Path:
    ORDER_ROOT.mkdir(parents=True, exist_ok=True)
    path = ORDER_ROOT / f"{order['order_id']}.json"
    path.write_text(json.dumps(order, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    latest = ORDER_ROOT / f"LATEST_{order['role_id']}.json"
    latest.write_text(json.dumps(order, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a traceable FATHER role library order")
    parser.add_argument("--role", required=True)
    parser.add_argument("--maturity", default="MIN", choices=("MIN", "MEDIUM", "MAX"))
    parser.add_argument("--mode", default="AUTO_BOUNDED", choices=("AUTO_BOUNDED", "REVIEW_EACH_STAGE"))
    parser.add_argument("--sources", default=None, help="Comma-separated source channels; default uses policy")
    args = parser.parse_args()

    policy = load_json(POLICY_PATH)
    role = resolve_role(args.role)
    sources = parse_sources(args.sources, policy)
    order = build_order(role=role, maturity=args.maturity, mode=args.mode, sources=sources)
    path = save_order(order)
    print(json.dumps({
        "status": "CREATED",
        "order_id": order["order_id"],
        "role_id": order["role_id"],
        "knowledge_base_id": order["knowledge_base_id"],
        "maturity_target": order["maturity_target"],
        "ru_regulatory_state": order["ru_regulatory_baseline"]["state"],
        "ru_regulatory_documents_total": order["metrics"]["ru_regulatory_documents_total"],
        "topics_total": order["topics_total"],
        "requested_sources": order["requested_sources"],
        "current_stage": order["current_stage"],
        "order_path": str(path.relative_to(ROOT)).replace("\\", "/"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
