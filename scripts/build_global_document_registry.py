from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCES_CONFIG = ROOT / "config" / "global_document_registry_sources.json"
POLICY_PATH = ROOT / "config" / "global_document_registry_policy.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def designation_key(value: str | None) -> str | None:
    if not value:
        return None
    return re.sub(r"\s+", " ", value.strip().upper().replace("№ ", "№"))


def canonical_document_id(designation: str | None, fallback: str | None) -> str:
    if designation:
        value = designation.upper()
        replacements = {
            "ГОСТ Р ": "GOST-R-",
            "ГОСТ ": "GOST-",
            "ИСО": "ISO",
            "МЭК": "IEC",
            "ФЕДЕРАЛЬНЫЙ ЗАКОН": "FZ",
            "ПОСТАНОВЛЕНИЕ ПРАВИТЕЛЬСТВА РФ": "PP-RF",
            "ПРИКАЗ ФСТЭК РОССИИ": "FSTEC",
            "ПРИКАЗ ФСБ РОССИИ": "FSB",
        }
        for old, new in replacements.items():
            value = value.replace(old, new)
        value = value.replace("/", "-")
        value = re.sub(r"[^A-Z0-9А-ЯЁ.-]+", "-", value).strip("-.")
        return f"DOC-RU-{value}"
    if fallback:
        value = re.sub(r"[^A-Z0-9_.-]+", "-", fallback.upper()).strip("-.")
        return value if value.startswith("DOC-") else f"DOC-RU-{value}"
    raise RuntimeError("document has neither designation nor stable fallback identity")


def normalize_status(value: str | None) -> str:
    raw = str(value or "VERIFY_CURRENTNESS").upper()
    mapping = {
        "ACTIVE": "CURRENT",
        "CURRENT": "CURRENT",
        "FUTURE_EFFECTIVE": "FUTURE_EFFECTIVE",
        "CONDITIONAL": "CONDITIONAL",
        "SUPERSEDED": "SUPERSEDED",
        "REPLACED": "SUPERSEDED",
        "NOT_VALID_IN_RF": "SUPERSEDED",
        "REPEALED": "REPEALED",
        "DRAFT": "DRAFT",
        "VERIFY_CURRENTNESS": "VERIFY_CURRENTNESS",
    }
    return mapping.get(raw, "VERIFY_CURRENTNESS")


def doc_type(designation: str | None, fallback: str = "OFFICIAL_DOCUMENT") -> str:
    d = (designation or "").upper()
    if "ГОСТ" in d:
        return "NATIONAL_STANDARD"
    if "ФЗ" in d or d.startswith("ФЕДЕРАЛЬНЫЙ ЗАКОН"):
        return "FEDERAL_LAW"
    if "ПП" in d or "ПОСТАНОВЛЕНИЕ" in d:
        return "GOVERNMENT_ACT"
    if "ФСТЭК" in d:
        return "REGULATOR_ACT"
    if "ФСБ" in d:
        return "REGULATOR_ACT"
    return fallback


def issuer_for(document_type: str, designation: str | None = None) -> str | None:
    d = (designation or "").upper()
    if document_type == "NATIONAL_STANDARD":
        return "РОССТАНДАРТ"
    if "ФСТЭК" in d:
        return "ФСТЭК РОССИИ"
    if "ФСБ" in d:
        return "ФСБ РОССИИ"
    if document_type == "FEDERAL_LAW":
        return "РОССИЙСКАЯ ФЕДЕРАЦИЯ"
    if document_type == "GOVERNMENT_ACT":
        return "ПРАВИТЕЛЬСТВО РФ"
    return None


def new_document(*, document_id: str, designation: str | None, title: str, status: str,
                 effective_from: str | None, official_url: str | None, revision: str | None,
                 verified_at: str | None, source_id: str, source_path: str, source_payload: dict[str, Any],
                 document_type: str | None = None) -> dict[str, Any]:
    dtype = document_type or doc_type(designation)
    return {
        "document_id": document_id,
        "jurisdiction": "RU",
        "document_type": dtype,
        "designation": designation,
        "title": title,
        "issuer": issuer_for(dtype, designation),
        "legal_status": status,
        "effective_from": effective_from,
        "effective_to": None,
        "current_revision_date": revision,
        "official_source_url": official_url,
        "last_verified_at": verified_at,
        "aliases": [],
        "source_observations": [
            {
                "source_id": source_id,
                "source_path": source_path,
                "observed_status": status,
                "observed_designation": designation,
                "observed_title": title,
                "verification_state": source_payload.get("verification_state") or source_payload.get("detail_metadata_state"),
                "official_source_url": official_url,
            }
        ],
    }


def merge_document(target: dict[str, Any], incoming: dict[str, Any], conflicts: list[dict[str, Any]]) -> None:
    current = target.get("legal_status")
    observed = incoming.get("legal_status")
    terminal = {"SUPERSEDED", "REPEALED"}
    if current != observed and ((current == "CURRENT" and observed in terminal) or (observed == "CURRENT" and current in terminal)):
        conflicts.append({
            "type": "CONFLICTING_CURRENT_STATUS",
            "document_id": target["document_id"],
            "existing_status": current,
            "incoming_status": observed,
            "incoming_source": incoming.get("source_observations", [{}])[0].get("source_id"),
        })
    rank = {"CURRENT": 6, "FUTURE_EFFECTIVE": 5, "CONDITIONAL": 4, "SUPERSEDED": 3, "REPEALED": 2, "DRAFT": 1, "VERIFY_CURRENTNESS": 0}
    if rank.get(observed, 0) > rank.get(current, 0):
        target["legal_status"] = observed
    for key in ("effective_from", "current_revision_date", "official_source_url", "last_verified_at", "issuer"):
        if not target.get(key) and incoming.get(key):
            target[key] = incoming[key]
    if incoming.get("title") and len(str(incoming["title"])) > len(str(target.get("title") or "")):
        target["title"] = incoming["title"]
    alias = incoming.get("document_id")
    if alias and alias != target["document_id"] and alias not in target["aliases"]:
        target["aliases"].append(alias)
    target["source_observations"].extend(incoming.get("source_observations", []))


def add_relation(relations: list[dict[str, Any]], *, from_id: str, relation_type: str, to_designation: str, source_id: str) -> None:
    to_id = canonical_document_id(to_designation, None)
    row = {
        "relation_id": f"REL-{len(relations)+1:05d}",
        "from_document_id": from_id,
        "relation_type": relation_type,
        "to_document_id": to_id,
        "to_designation": to_designation,
        "source_id": source_id,
    }
    identity = (row["from_document_id"], row["relation_type"], row["to_document_id"])
    if not any((r["from_document_id"], r["relation_type"], r["to_document_id"]) == identity for r in relations):
        relations.append(row)


def add_binding(bindings: list[dict[str, Any]], *, document_id: str, subject_type: str, subject_id: str,
                applicability: str, activation: str | None, legal_force: str, review_state: str,
                source_id: str) -> None:
    identity = (document_id, subject_type, subject_id, applicability, activation)
    if any((r["document_id"], r["subject_type"], r["subject_id"], r["applicability"], r.get("activation_condition")) == identity for r in bindings):
        return
    bindings.append({
        "binding_id": f"BIND-{len(bindings)+1:05d}",
        "document_id": document_id,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "applicability": applicability,
        "activation_condition": activation,
        "legal_force_class": legal_force,
        "review_state": review_state,
        "source_id": source_id,
    })


def import_pdn(payload: dict[str, Any], source: dict[str, Any], add_doc, bindings, relations) -> None:
    for row in payload.get("documents", []):
        did = str(row.get("document_id") or "")
        designation = row.get("designation")
        incoming = new_document(
            document_id=canonical_document_id(designation, did), designation=designation,
            title=str(row.get("title") or did), status=normalize_status(row.get("legal_status")),
            effective_from=row.get("effective_from"), official_url=row.get("official_source_url"),
            revision=row.get("current_revision_date"), verified_at=row.get("last_verified_at"),
            source_id=source["source_id"], source_path=source["path"], source_payload=row,
            document_type=doc_type(designation, "LEGAL_OR_REGULATORY_DOCUMENT"),
        )
        canonical = add_doc(incoming, designation_key(designation) or did.upper())
        add_binding(bindings, document_id=canonical, subject_type="DOMAIN", subject_id="PERSONAL_DATA",
                    applicability=str(row.get("applicability") or "PDN_DOMAIN"), activation="software/system processes personal data",
                    legal_force="CHECK_PRIMARY_LEGAL_APPLICABILITY", review_state="REUSE_EXISTING_PDN_KB", source_id=source["source_id"])


def import_espd(payload: dict[str, Any], source: dict[str, Any], add_doc, bindings, relations) -> None:
    for row in payload.get("records", []):
        designation = str(row.get("designation") or "").strip()
        did = canonical_document_id(designation, None)
        incoming = new_document(
            document_id=did, designation=designation, title=str(row.get("title") or designation),
            status=normalize_status(row.get("status")), effective_from=row.get("effective_from"),
            official_url=row.get("detail_url"), revision=None, verified_at=payload.get("snapshot_date"),
            source_id=source["source_id"], source_path=source["path"], source_payload=row,
            document_type="NATIONAL_STANDARD",
        )
        canonical = add_doc(incoming, designation_key(designation))
        add_binding(bindings, document_id=canonical, subject_type="ROLE", subject_id="PROGRAMMER",
                    applicability="ESPD_PROGRAM_DOCUMENTATION", activation="project, contract, customer or regulatory context activates ESPD requirements",
                    legal_force="NATIONAL_STANDARD_CHECK_APPLICABILITY", review_state="APPLICABILITY_REVIEW_REQUIRED", source_id=source["source_id"])
        if row.get("superseded_by"):
            add_relation(relations, from_id=canonical, relation_type="SUPERSEDED_BY", to_designation=str(row["superseded_by"]), source_id=source["source_id"])


def import_automated_systems(payload: dict[str, Any], source: dict[str, Any], add_doc, bindings, relations) -> None:
    role_id = str(payload.get("role_id") or "PROGRAMMER")
    activation = "software is part of an automated system or project/contract/regulation activates this layer"
    for row in payload.get("current_documents", []):
        designation = str(row.get("designation") or "").strip()
        incoming = new_document(
            document_id=canonical_document_id(designation, None), designation=designation,
            title=str(row.get("title") or designation), status=normalize_status(row.get("status")),
            effective_from=row.get("effective_from"), official_url=row.get("official_source"), revision=None,
            verified_at=None, source_id=source["source_id"], source_path=source["path"], source_payload=row,
            document_type="NATIONAL_STANDARD",
        )
        canonical = add_doc(incoming, designation_key(designation))
        add_binding(bindings, document_id=canonical, subject_type="ROLE", subject_id=role_id,
                    applicability="AUTOMATED_SYSTEMS_CONDITIONAL", activation=activation,
                    legal_force="NATIONAL_STANDARD_CHECK_PROJECT_REFERENCE", review_state="CONDITIONAL", source_id=source["source_id"])
        replaced = row.get("replaces") or row.get("replaces_for_rf_use")
        if replaced:
            add_relation(relations, from_id=canonical, relation_type="SUPERSEDES", to_designation=str(replaced), source_id=source["source_id"])
    for row in payload.get("historical_do_not_use_as_current", []):
        designation = str(row.get("designation") or "").strip()
        incoming = new_document(
            document_id=canonical_document_id(designation, None), designation=designation,
            title=designation, status="SUPERSEDED", effective_from=None, official_url=None, revision=None,
            verified_at=None, source_id=source["source_id"], source_path=source["path"], source_payload=row,
            document_type="NATIONAL_STANDARD",
        )
        canonical = add_doc(incoming, designation_key(designation))
        successor = row.get("superseded_by") or row.get("use_in_rf")
        if successor:
            add_relation(relations, from_id=canonical, relation_type="SUPERSEDED_BY", to_designation=str(successor), source_id=source["source_id"])


def import_role_baseline(payload: dict[str, Any], source: dict[str, Any], add_doc, bindings, relations) -> None:
    for role_id, role in (payload.get("roles") or {}).items():
        kb_id = str(role.get("knowledge_base_id") or "")
        for row in role.get("documents", []):
            designation = str(row.get("designation") or "").strip()
            incoming = new_document(
                document_id=canonical_document_id(designation, row.get("document_id")), designation=designation or None,
                title=str(row.get("title") or designation), status=normalize_status(row.get("status")),
                effective_from=row.get("effective_from"), official_url=row.get("official_source"), revision=None,
                verified_at=None, source_id=source["source_id"], source_path=source["path"], source_payload=row,
                document_type=doc_type(designation),
            )
            canonical = add_doc(incoming, designation_key(designation) or str(row.get("document_id") or "").upper())
            add_binding(bindings, document_id=canonical, subject_type="ROLE", subject_id=str(role_id),
                        applicability=str(row.get("applicability") or row.get("cluster") or "ROLE_BASELINE"),
                        activation=None, legal_force=str(row.get("legal_force_class") or "CHECK_APPLICABILITY"),
                        review_state="HUMAN_APPLICABILITY_REVIEW_REQUIRED", source_id=source["source_id"])
            if kb_id:
                add_binding(bindings, document_id=canonical, subject_type="KNOWLEDGE_BASE", subject_id=kb_id,
                            applicability=str(row.get("cluster") or "ROLE_BASELINE"), activation=None,
                            legal_force=str(row.get("legal_force_class") or "CHECK_APPLICABILITY"),
                            review_state="LINKED_FROM_ROLE_BASELINE", source_id=source["source_id"])
            for replaced in row.get("replaces", []) or []:
                add_relation(relations, from_id=canonical, relation_type="SUPERSEDES", to_designation=str(replaced), source_id=source["source_id"])


ADAPTERS = {
    "PDN_DOCUMENTS": import_pdn,
    "ESPD_RECORDS": import_espd,
    "AUTOMATED_SYSTEMS_RECORDS": import_automated_systems,
    "ROLE_BASELINE_DOCUMENTS": import_role_baseline,
}


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    config = load_json(SOURCES_CONFIG)
    policy = load_json(POLICY_PATH)
    documents_by_identity: dict[str, dict[str, Any]] = {}
    id_to_identity: dict[str, str] = {}
    conflicts: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []

    def add_doc(incoming: dict[str, Any], identity: str) -> str:
        if not identity:
            identity = incoming["document_id"]
        if identity in documents_by_identity:
            target = documents_by_identity[identity]
            merge_document(target, incoming, conflicts)
            id_to_identity[incoming["document_id"]] = identity
            return target["document_id"]
        documents_by_identity[identity] = incoming
        id_to_identity[incoming["document_id"]] = identity
        return incoming["document_id"]

    imported_sources = []
    for source in config.get("sources", []):
        if not source.get("enabled", True):
            continue
        path = ROOT / source["path"]
        if not path.is_file():
            conflicts.append({"type": "MISSING_SOURCE_REGISTRY", "source_id": source["source_id"], "path": source["path"]})
            continue
        payload = load_json(path)
        adapter = ADAPTERS.get(str(source.get("adapter")))
        if adapter is None:
            conflicts.append({"type": "UNKNOWN_ADAPTER", "source_id": source["source_id"], "adapter": source.get("adapter")})
            continue
        adapter(payload, source, add_doc, bindings, relations)
        imported_sources.append(source["source_id"])

    documents = sorted(documents_by_identity.values(), key=lambda row: (str(row.get("jurisdiction")), str(row.get("designation") or row["document_id"])))
    known_ids = {row["document_id"] for row in documents}
    relation_missing = [row for row in relations if row["from_document_id"] not in known_ids or row["to_document_id"] not in known_ids]
    for row in relation_missing:
        conflicts.append({"type": "RELATION_ENDPOINT_NOT_REGISTERED", **row})

    status_counts: dict[str, int] = {}
    for row in documents:
        status = str(row.get("legal_status"))
        status_counts[status] = status_counts.get(status, 0) + 1

    registry = {
        "schema_version": "1.0",
        "record_type": "FATHER_GLOBAL_DOCUMENT_REGISTRY",
        "registry_id": policy["registry_id"],
        "generated_at_epoch": time.time(),
        "source_config": str(SOURCES_CONFIG.relative_to(ROOT)).replace("\\", "/"),
        "imported_sources": imported_sources,
        "documents_total": len(documents),
        "relations_total": len(relations),
        "bindings_total": len(bindings),
        "conflicts_total": len(conflicts),
        "status_counts": status_counts,
        "documents": documents,
        "relations": relations,
        "acceptance": {
            "duplicate_canonical_document_ids": len(documents) != len(known_ids),
            "conflicting_current_status_total": sum(1 for row in conflicts if row.get("type") == "CONFLICTING_CURRENT_STATUS"),
            "relation_missing_endpoint_total": len(relation_missing),
            "ready_for_shared_use": not any(row.get("type") == "CONFLICTING_CURRENT_STATUS" for row in conflicts),
        },
    }
    bindings_payload = {
        "schema_version": "1.0",
        "record_type": "FATHER_GLOBAL_APPLICABILITY_BINDINGS",
        "registry_id": policy["registry_id"],
        "bindings_total": len(bindings),
        "bindings": bindings,
    }
    conflicts_payload = {
        "schema_version": "1.0",
        "record_type": "FATHER_GLOBAL_DOCUMENT_REGISTRY_CONFLICTS",
        "registry_id": policy["registry_id"],
        "conflicts_total": len(conflicts),
        "conflicts": conflicts,
    }
    return registry, bindings_payload, conflicts_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the shared FATHER global document registry")
    parser.add_argument("--strict", action="store_true", help="Fail if canonical status conflicts or missing relation endpoints exist")
    args = parser.parse_args()
    config = load_json(SOURCES_CONFIG)
    registry, bindings, conflicts = build()
    out = config["output"]
    write_json(ROOT / out["registry_path"], registry)
    write_json(ROOT / out["bindings_path"], bindings)
    write_json(ROOT / out["conflicts_path"], conflicts)
    print(json.dumps({
        "status": "PASS" if registry["acceptance"]["ready_for_shared_use"] else "NEEDS_REVIEW",
        "documents_total": registry["documents_total"],
        "relations_total": registry["relations_total"],
        "bindings_total": registry["bindings_total"],
        "conflicts_total": registry["conflicts_total"],
        "status_counts": registry["status_counts"],
        "registry_path": out["registry_path"],
        "bindings_path": out["bindings_path"],
        "conflicts_path": out["conflicts_path"],
    }, ensure_ascii=False, indent=2))
    blockers = registry["acceptance"]["conflicting_current_status_total"] + registry["acceptance"]["relation_missing_endpoint_total"]
    return 1 if args.strict and blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
