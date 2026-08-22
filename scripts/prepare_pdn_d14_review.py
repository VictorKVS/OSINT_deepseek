from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REPORT_ROOT = REPO_ROOT / "reports" / "pdn_live"
D13_QUALITY = REPORT_ROOT / "D13_QUALITY.json"
D6_SUMMARY = REPORT_ROOT / "D6_D9_EXTRACTION_SUMMARY.json"
REL_ROOT = STORE_ROOT / "relations"
PACKET_JSON = REPORT_ROOT / "D14_REVIEW_PACKET.json"
PACKET_MD = REPORT_ROOT / "D14_REVIEW_PACKET.md"
DECISIONS = REPORT_ROOT / "D14_DECISIONS.jsonl"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)

RULE_SPECS: tuple[tuple[str, str, str], ...] = (
    ("RULE-D6-CONTROLLED-TERM", "D6", "CONTROLLED_LEXICON_MENTION"),
    ("RULE-D7-EXPLICIT-DEFINITION", "D7", "EXPLICIT_LEXICAL_DEFINITION"),
    ("RULE-D8-NORMATIVE-TRIGGER", "D8", "EXPLICIT_NORMATIVE_TRIGGER"),
    ("RULE-D9-CONTROLLED-ENTITY", "D9", "CONTROLLED_LEXICON_MENTION"),
    ("RULE-D10-TERM-DEFINED-BY", "D10", "TERM_DEFINED_BY"),
    ("RULE-D10-REQUIREMENT-MENTIONS-ENTITY", "D10", "REQUIREMENT_MENTIONS_ENTITY"),
    ("RULE-D11-SHARED-TERM", "D11", "SHARED_TERM_ACROSS_DOCUMENTS"),
    ("RULE-D11-SHARED-ENTITY", "D11", "SHARED_ENTITY_ACROSS_DOCUMENTS"),
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _stable_packet_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_bytes(raw)


def _short(value: object, limit: int = 320) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _lineage_ok(row: dict[str, Any]) -> bool:
    lineage = row.get("lineage")
    if not isinstance(lineage, dict):
        return False
    required = {
        "document_id",
        "version_id",
        "chunk_id",
        "chunk_locator",
        "structure_node_id",
        "artifact_sha256",
        "source_text_sha256",
    }
    return required.issubset(lineage) and all(str(lineage.get(key, "")).strip() for key in required)


def _candidate_id(row: dict[str, Any]) -> str:
    for key in ("term_id", "definition_id", "requirement_id", "entity_mention_id", "relation_id", "candidate_id"):
        if row.get(key):
            return str(row[key])
    return "UNKNOWN"


def _sample(row: dict[str, Any]) -> dict[str, Any]:
    lineage = row.get("lineage") if isinstance(row.get("lineage"), dict) else {}
    return {
        "id": _candidate_id(row),
        "document_id": lineage.get("document_id") or row.get("document_id") or row.get("document_ids"),
        "chunk_locator": lineage.get("chunk_locator"),
        "term": _short(row.get("term"), 120) if row.get("term") else None,
        "definition": _short(row.get("definition")) if row.get("definition") else None,
        "statement": _short(row.get("statement")) if row.get("statement") else None,
        "relation_type": row.get("relation_type"),
        "canonical_key": row.get("canonical_key"),
    }


def main() -> int:
    if not D13_QUALITY.is_file():
        print("D13_QUALITY_MISSING")
        return 2
    d13_quality = _read_json(D13_QUALITY)
    if d13_quality.get("summary", {}).get("quality_pass") is not True:
        print("D14_PREP_BLOCKED_BY_D13_QUALITY")
        return 2
    if not D6_SUMMARY.is_file():
        print("D6_D9_SUMMARY_MISSING")
        return 2

    d6_summary = _read_json(D6_SUMMARY)
    by_doc = {str(item.get("document_id")): item for item in d6_summary.get("documents", [])}
    if any(document_id not in by_doc for document_id in TARGETS):
        print("D14_PREP_INPUT_INCOMPLETE")
        return 2

    terms: list[dict[str, Any]] = []
    definitions: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    entities: list[dict[str, Any]] = []
    for document_id in TARGETS:
        version_id = str(by_doc[document_id]["version_id"])
        base = STORE_ROOT / "knowledge" / document_id / version_id
        terms.extend(_read_jsonl(base / "terms.jsonl"))
        definitions.extend(_read_jsonl(base / "definitions.jsonl"))
        requirements.extend(_read_jsonl(base / "requirements.jsonl"))
        entities.extend(_read_jsonl(base / "entities.jsonl"))

    internal = _read_jsonl(REL_ROOT / "internal.jsonl")
    cross = _read_jsonl(REL_ROOT / "cross_document.jsonl")
    conflicts = _read_jsonl(REL_ROOT / "conflicts_overlaps.jsonl")

    all_extracted = terms + definitions + requirements + entities
    precheck_failures: list[str] = []
    for row in all_extracted:
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW":
            precheck_failures.append(f"BAD_REVIEW_STATE:{_candidate_id(row)}")
        if row.get("promotion_state") != "NOT_PROMOTED":
            precheck_failures.append(f"BAD_PROMOTION_STATE:{_candidate_id(row)}")
        if not _lineage_ok(row):
            precheck_failures.append(f"BAD_LINEAGE:{_candidate_id(row)}")
    for row in internal + cross:
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED":
            precheck_failures.append(f"BAD_RELATION_STATE:{_candidate_id(row)}")
    for row in conflicts:
        if row.get("confirmed_conflict") is not False:
            precheck_failures.append(f"PREMATURE_CONFLICT:{_candidate_id(row)}")
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED":
            precheck_failures.append(f"BAD_CONFLICT_STATE:{_candidate_id(row)}")
    if precheck_failures:
        print("D14_PREP_PRECHECK_FAILED: " + ", ".join(precheck_failures[:20]))
        return 2

    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    groups[("D6", "CONTROLLED_LEXICON_MENTION")].extend(
        row for row in terms if row.get("extraction_basis") == "CONTROLLED_LEXICON_MENTION"
    )
    groups[("D7", "EXPLICIT_LEXICAL_DEFINITION")].extend(definitions)
    groups[("D8", "EXPLICIT_NORMATIVE_TRIGGER")].extend(requirements)
    groups[("D9", "CONTROLLED_LEXICON_MENTION")].extend(entities)
    groups[("D10", "TERM_DEFINED_BY")].extend(row for row in internal if row.get("relation_type") == "TERM_DEFINED_BY")
    groups[("D10", "REQUIREMENT_MENTIONS_ENTITY")].extend(
        row for row in internal if row.get("relation_type") == "REQUIREMENT_MENTIONS_ENTITY"
    )
    groups[("D11", "SHARED_TERM_ACROSS_DOCUMENTS")].extend(
        row for row in cross if row.get("relation_type") == "SHARED_TERM_ACROSS_DOCUMENTS"
    )
    groups[("D11", "SHARED_ENTITY_ACROSS_DOCUMENTS")].extend(
        row for row in cross if row.get("relation_type") == "SHARED_ENTITY_ACROSS_DOCUMENTS"
    )

    decision_items: list[dict[str, Any]] = []
    for decision_id, stage, rule_key in RULE_SPECS:
        rows = groups[(stage, rule_key)]
        decision_items.append({
            "decision_id": decision_id,
            "scope_type": "RULE_CLASS",
            "stage": stage,
            "scope_key": rule_key,
            "objects_covered": len(rows),
            "machine_precheck": "PASS",
            "samples": [_sample(row) for row in rows[:5]],
            "allowed_decisions": ["ACCEPT", "REJECT", "ESCALATE"],
            "decision": "PENDING",
        })

    definitions_by_id = {str(row["definition_id"]): row for row in definitions}
    requirements_by_id = {str(row["requirement_id"]): row for row in requirements}
    for conflict in conflicts:
        evidence: list[dict[str, Any]] = []
        if conflict.get("candidate_type") == "DEFINITION_VARIANCE_CANDIDATE":
            for definition_id in conflict.get("definition_ids", []):
                row = definitions_by_id.get(str(definition_id))
                if row:
                    evidence.append({
                        "definition_id": definition_id,
                        "document_id": row["lineage"]["document_id"],
                        "term": _short(row.get("term"), 120),
                        "definition": _short(row.get("definition"), 500),
                        "chunk_locator": row["lineage"]["chunk_locator"],
                    })
        elif conflict.get("candidate_type") == "REQUIREMENT_OVERLAP_CANDIDATE":
            for requirement_id in conflict.get("requirement_ids", []):
                row = requirements_by_id.get(str(requirement_id))
                if row:
                    evidence.append({
                        "requirement_id": requirement_id,
                        "document_id": row["lineage"]["document_id"],
                        "statement": _short(row.get("statement"), 500),
                        "chunk_locator": row["lineage"]["chunk_locator"],
                    })
        decision_items.append({
            "decision_id": f"D12-{conflict['candidate_id']}",
            "scope_type": "CONFLICT_OR_OVERLAP_CANDIDATE",
            "stage": "D12",
            "scope_key": conflict["candidate_id"],
            "candidate_type": conflict.get("candidate_type"),
            "document_ids": conflict.get("document_ids", []),
            "machine_precheck": "PASS",
            "evidence": evidence,
            "allowed_decisions": ["CONFIRMED_CONFLICT", "NOT_CONFLICT", "OVERLAP_ONLY", "ESCALATE"],
            "decision": "PENDING",
        })

    source_hashes = {
        "d13_quality_sha256": _sha256_file(D13_QUALITY),
        "d6_summary_sha256": _sha256_file(D6_SUMMARY),
        "internal_relations_sha256": _sha256_file(REL_ROOT / "internal.jsonl"),
        "cross_relations_sha256": _sha256_file(REL_ROOT / "cross_document.jsonl"),
        "conflicts_sha256": _sha256_file(REL_ROOT / "conflicts_overlaps.jsonl"),
    }
    payload_without_hash = {
        "schema_version": "1.0",
        "record_type": "D14_EXPERT_REVIEW_PACKET",
        "corpus_id": "PDN-OFFICIAL-SOURCE-PACK-001",
        "targets": list(TARGETS),
        "review_strategy": "RULE_CLASS_PLUS_EACH_D12_CANDIDATE",
        "candidate_counts": {
            "terms": len(terms),
            "definitions": len(definitions),
            "requirements": len(requirements),
            "entities": len(entities),
            "internal_relations": len(internal),
            "cross_document_relations": len(cross),
            "conflict_overlap_candidates": len(conflicts),
        },
        "decision_items": decision_items,
        "required_decisions": len(decision_items),
        "pending_decisions": len(decision_items),
        "d14_state": "NEEDS_REVIEW",
        "d15_state": "BLOCKED",
        "autonomous_kb_promotion": False,
        "source_hashes": source_hashes,
    }
    packet_hash = _stable_packet_hash(payload_without_hash)
    payload = {**payload_without_hash, "packet_sha256": packet_hash}

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    PACKET_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not DECISIONS.exists():
        with DECISIONS.open("w", encoding="utf-8", newline="\n") as handle:
            for item in decision_items:
                row = {
                    "decision_id": item["decision_id"],
                    "packet_sha256": packet_hash,
                    "decision": "PENDING",
                    "reviewer": "",
                    "reason": "",
                }
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    counts = payload["candidate_counts"]
    lines = [
        "# PDn D14 expert review packet",
        "",
        "The machine pipeline passed D0-D13. This packet compresses D14 into rule-class review plus each D12 conflict/overlap candidate. No decision is auto-approved.",
        "",
        f"- packet SHA-256: `{packet_hash}`",
        f"- required review decisions: **{len(decision_items)}**",
        f"- terms: {counts['terms']}; definitions: {counts['definitions']}; requirements: {counts['requirements']}; entities: {counts['entities']}",
        f"- internal relations: {counts['internal_relations']}; cross-document relations: {counts['cross_document_relations']}",
        f"- conflict/overlap candidates: {counts['conflict_overlap_candidates']}",
        "- D14: **NEEDS_REVIEW**",
        "- D15: **BLOCKED**",
        "",
        "## Rule-class decisions",
        "",
        "| Decision ID | Stage | Rule | Objects | Machine precheck | Human decision |",
        "|---|---|---|---:|---|---|",
    ]
    for item in decision_items:
        if item["scope_type"] != "RULE_CLASS":
            continue
        lines.append(
            f"| `{item['decision_id']}` | {item['stage']} | `{item['scope_key']}` | {item['objects_covered']} | PASS | PENDING |"
        )
        samples = item.get("samples", [])
        if samples:
            lines.append("")
            lines.append(f"Samples for `{item['decision_id']}`:")
            for sample in samples:
                detail = sample.get("definition") or sample.get("statement") or sample.get("term") or sample.get("relation_type") or sample.get("canonical_key")
                lines.append(f"- `{sample.get('id')}` — {_short(detail, 220)}")
            lines.append("")

    lines += ["", "## D12 candidate decisions", ""]
    for item in decision_items:
        if item["scope_type"] == "RULE_CLASS":
            continue
        lines.append(f"### `{item['decision_id']}` — {item.get('candidate_type')}")
        lines.append("")
        lines.append(f"Documents: {', '.join(item.get('document_ids', [])) or '—'}")
        lines.append("")
        for evidence in item.get("evidence", []):
            detail = evidence.get("definition") or evidence.get("statement")
            lines.append(f"- `{evidence.get('document_id')}` / `{evidence.get('chunk_locator')}` — {_short(detail, 500)}")
        lines.append("")
        lines.append("Decision: **PENDING**")
        lines.append("")

    lines += [
        "## How to complete D14",
        "",
        "Edit `reports/pdn_live/D14_DECISIONS.jsonl`: replace each `PENDING` with an allowed decision, set `reviewer`, and add a short `reason`. Then run `RUN_PDN_D14_APPLY_DECISIONS.cmd`.",
        "",
        "Rejecting a rule is allowed and excludes that rule class from the future D15 package. `ESCALATE` keeps D14 open. D15 cannot be reached autonomously.",
    ]
    PACKET_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({
        "record_type": "D14_REVIEW_PREP_SUMMARY",
        "packet_sha256": packet_hash,
        "required_decisions": len(decision_items),
        "rule_class_decisions": sum(item["scope_type"] == "RULE_CLASS" for item in decision_items),
        "d12_candidate_decisions": sum(item["scope_type"] != "RULE_CLASS" for item in decision_items),
        "decisions_file": DECISIONS.relative_to(REPO_ROOT).as_posix(),
        "review_packet": PACKET_MD.relative_to(REPO_ROOT).as_posix(),
        "d14_state": "NEEDS_REVIEW",
        "d15_state": "BLOCKED",
        "autonomous_kb_promotion": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
