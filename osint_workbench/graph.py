from __future__ import annotations

from typing import Any

from .canonical import utc_now_iso
from .store import WorkbenchStore


class GraphProjector:
    """Build a derived, non-authoritative graph payload with evidence paths."""

    version = "graph-projector/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def build(
        self,
        case_id: str,
        *,
        seed_refs: list[str] | None = None,
        mode: str = "GRAPH",
        purpose: str = "OSINT case relationship and evidence-path view",
        bounded_hops: int = 2,
    ) -> dict[str, Any]:
        mode = mode.upper()
        if mode not in {"SEARCH_TABLE", "GRAPH", "MAP_TIMELINE", "DOSSIER", "REPORT_PATH"}:
            raise ValueError("unsupported graph mode")
        sources = self.store.list_objects(case_id, "source")
        captures = self.store.list_objects(case_id, "capture")
        entities = self.store.list_objects(case_id, "entity")
        claims = self.store.list_objects(case_id, "claim")
        relations = self.store.list_objects(case_id, "relation")
        findings = self.store.list_objects(case_id, "finding")
        gaps = self.store.list_objects(case_id, "research_gap")

        nodes: list[dict[str, Any]] = []
        positions: dict[str, dict[str, float]] = {}

        def add_node(node_id: str, object_type: str, subtype: str, label: str, status: str, access_class: str, source_ids: list[str]) -> None:
            if node_id in positions:
                return
            index = len(nodes)
            position = {"x": float((index % 4) * 320), "y": float((index // 4) * 180)}
            positions[node_id] = position
            nodes.append(
                {
                    "node_id": node_id,
                    "object_type": object_type,
                    "subtype": subtype,
                    "label": label,
                    "status": status,
                    "access_class": access_class,
                    "source_ids": list(dict.fromkeys(source_ids)),
                    "position": position,
                }
            )

        for item in entities:
            add_node(item["entity_id"], "ENTITY", item["entity_type"], item["display_name"], item["status"], item["access_class"], item["source_ids"])
        for item in sources:
            add_node(item["source_id"], "SOURCE", item["source_type"], item["title"], item.get("status", "ACTIVE"), item["access_class"], [item["source_id"]])
        for item in claims:
            add_node(item["claim_id"], "CLAIM", item.get("predicate") or item["representation"], item["statement"], item["status"], item["access_class"], item["source_ids"])
        for item in findings:
            add_node(item["finding_id"], "FINDING", item["classification"], item["statement"], "APPROVED" if item["human_approved"] else "PENDING", item["access_class"], item["source_ids"])
        for item in gaps:
            add_node(item["research_gap_id"], "RESEARCH_GAP", item["stream"], item["question"], item["state"], self.store.get_case(case_id)["access_class"], [])
        if not nodes:
            case = self.store.get_case(case_id)
            add_node(case_id, "CASE", case["case_type"], case["title"], case["status"], case["access_class"], [])

        edges: list[dict[str, Any]] = []
        evidence_paths: list[dict[str, Any]] = []
        evidence_path_by_relation: dict[str, str] = {}
        capture_by_source: dict[str, list[dict[str, Any]]] = {}
        for capture in captures:
            capture_by_source.setdefault(capture["source_id"], []).append(capture)
        findings_by_claim: dict[str, list[dict[str, Any]]] = {}
        for finding in findings:
            for claim_id in finding["claim_ids"]:
                findings_by_claim.setdefault(claim_id, []).append(finding)

        for relation in relations:
            evidence_path_id = f"EPATH-{relation['relation_id'].split('-', 1)[-1]}"
            evidence_path_by_relation[relation["relation_id"]] = evidence_path_id
            primary_source_id = relation["source_ids"][0]
            primary_claim_id = relation["claim_ids"][0]
            steps: list[dict[str, Any]] = [
                {"order": 1, "object_type": "SOURCE", "object_id": primary_source_id, "role": "origin"}
            ]
            source_captures = capture_by_source.get(primary_source_id, [])
            if source_captures:
                steps.append({"order": len(steps) + 1, "object_type": "SOURCE_CAPTURE", "object_id": source_captures[0]["capture_id"], "role": "immutable_capture"})
            steps.append({"order": len(steps) + 1, "object_type": "CLAIM", "object_id": primary_claim_id, "role": "source_statement"})
            steps.append({"order": len(steps) + 1, "object_type": "RELATION", "object_id": relation["relation_id"], "role": "normalized_relation"})
            linked_findings = findings_by_claim.get(primary_claim_id, [])
            if linked_findings:
                steps.append({"order": len(steps) + 1, "object_type": "FINDING", "object_id": linked_findings[0]["finding_id"], "role": "human_reviewed_finding"})
            evidence_paths.append(
                {
                    "evidence_path_id": evidence_path_id,
                    "target_ref": relation["relation_id"],
                    "steps": steps,
                    "limitations": relation["not_implying"],
                }
            )
            semantic_status = "FACT" if relation["status"] == "CONFIRMED" else "INFERENCE" if relation["status"] == "REVIEWED" else "HYPOTHESIS"
            edges.append(
                {
                    "edge_id": f"EDGE-{relation['relation_id']}",
                    "from_node_id": relation["from_entity_id"],
                    "to_node_id": relation["to_entity_id"],
                    "relation_type": relation["relation_type"],
                    "semantic_status": semantic_status,
                    "relation_id": relation["relation_id"],
                    "source_ids": relation["source_ids"],
                    "confidence_grade": relation["evidence_grade"],
                    "evidence_path_id": evidence_path_id,
                }
            )

        for claim in claims:
            for source_id in claim["source_ids"]:
                edges.append(
                    {
                        "edge_id": f"EDGE-{source_id}-{claim['claim_id']}",
                        "from_node_id": source_id,
                        "to_node_id": claim["claim_id"],
                        "relation_type": "ASSERTS",
                        "semantic_status": "SOURCE_CLAIM",
                        "relation_id": None,
                        "source_ids": [source_id],
                        "confidence_grade": "NOT_APPLICABLE",
                        "evidence_path_id": None,
                    }
                )
            for entity_id in claim["subject_entity_ids"]:
                edges.append(
                    {
                        "edge_id": f"EDGE-{claim['claim_id']}-{entity_id}",
                        "from_node_id": claim["claim_id"],
                        "to_node_id": entity_id,
                        "relation_type": "ABOUT",
                        "semantic_status": "DERIVED_NAVIGATION",
                        "relation_id": None,
                        "source_ids": claim["source_ids"],
                        "confidence_grade": "NOT_APPLICABLE",
                        "evidence_path_id": None,
                    }
                )

        for finding in findings:
            for entity_id in finding["entity_ids"]:
                edges.append(
                    {
                        "edge_id": f"EDGE-{entity_id}-{finding['finding_id']}",
                        "from_node_id": entity_id,
                        "to_node_id": finding["finding_id"],
                        "relation_type": "SUPPORTS_FINDING",
                        "semantic_status": "DERIVED_NAVIGATION",
                        "relation_id": None,
                        "source_ids": finding["source_ids"],
                        "confidence_grade": finding["evidence_grade"],
                        "evidence_path_id": None,
                    }
                )
        for gap in gaps:
            targets = [ref for ref in gap["subject_refs"] if ref in positions]
            if targets:
                edges.append(
                    {
                        "edge_id": f"EDGE-{targets[0]}-{gap['research_gap_id']}",
                        "from_node_id": targets[0],
                        "to_node_id": gap["research_gap_id"],
                        "relation_type": "LIMITED_BY",
                        "semantic_status": "DERIVED_NAVIGATION",
                        "relation_id": None,
                        "source_ids": [],
                        "confidence_grade": "NOT_APPLICABLE",
                        "evidence_path_id": None,
                    }
                )

        graph_view_id = self.store._allocate_id(case_id, "GVIEW")
        payload = {
            "schema_version": "father-osint.graph-view.v0.1",
            "graph_view_id": graph_view_id,
            "case_id": case_id,
            "purpose": purpose,
            "generated_at_utc": utc_now_iso(),
            "authoritative": False,
            "mode": mode,
            "query_context": {
                "seed_refs": seed_refs or ([entities[0]["entity_id"]] if entities else [case_id]),
                "filters": ["evidence-linked", "policy-visible"],
                "bounded_hops": max(1, min(int(bounded_hops), 6)),
            },
            "nodes": nodes,
            "edges": edges,
            "evidence_paths": evidence_paths,
            "unresolved_research_gap_ids": [
                item["research_gap_id"] for item in gaps if item["state"] not in {"RESOLVED", "WAIVED"}
            ],
            "synthetic": self.store.get_case(case_id)["synthetic"],
        }
        self.store.save_object(case_id, "graph", payload)
        self.store.append_journal(
            case_id,
            actor_id="graph-projector",
            actor_type="AGENT",
            action_type="ANALYZE",
            stream="RED_TEAM_SOURCE_QUALITY",
            query_or_action=f"Build derived graph view {graph_view_id}",
            result_code="FOUND",
            result_summary=f"Projected {len(nodes)} nodes, {len(edges)} edges and {len(evidence_paths)} evidence paths.",
            next_pivots=payload["unresolved_research_gap_ids"],
            access_class=self.store.get_case(case_id)["access_class"],
            actor_version=self.version,
        )
        return payload
