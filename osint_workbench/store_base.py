from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from typing import Any, Iterable

from .canonical import safe_token, utc_now_iso
from .policy import validate_access_class

CASE_TYPES = {
    "CORPORATE_DUE_DILIGENCE",
    "THREAT_INTELLIGENCE",
    "BRAND_PROTECTION",
    "SUPPLIER_RISK",
    "REGULATORY_INTELLIGENCE",
    "MEDIA_NARRATIVE_ANALYSIS",
    "AUTHORIZED_SECURITY_ASSESSMENT",
    "SYNTHETIC_TRAINING",
}
ENTITY_TYPES = {
    "PERSON", "ORGANIZATION", "ADDRESS", "DOMAIN", "ACCOUNT",
    "ASSET", "DOCUMENT", "EVENT", "AUTHORITY", "LOCATION",
}
RELATION_TYPES = {
    "OWNS", "CONTROLS", "DIRECTS", "REPRESENTS", "EMPLOYED_BY",
    "LOCATED_AT", "SUPPLIED_TO", "MENTIONED_IN", "SANCTIONED_BY",
    "ALLEGED_BY", "CONFIRMED_BY", "REGISTERED_AT", "PUBLISHED_BY", "OTHER",
}
EVIDENCE_GRADES = {"A_CONFIRMED", "B_HIGHLY_PROBABLE", "C_ANALYTICAL_HYPOTHESIS", "D_LEAD"}
STREAMS = {
    "ENTITY_REGISTRY",
    "BUSINESS_TRANSACTIONS_LOGISTICS",
    "DIGITAL_FOOTPRINT",
    "LEGAL_SANCTIONS_ADVERSE",
    "RED_TEAM_SOURCE_QUALITY",
}
SOURCE_TYPES = {"OFFICIAL_REGISTER", "OFFICIAL_DOCUMENT", "COURT", "REGULATOR", "COMPANY_PUBLICATION", "NEWS", "INVESTIGATIVE_REPORT", "SOCIAL_PUBLIC", "WEB_PAGE", "ARCHIVE", "DATASET", "OTHER"}
PRIMARY_LEVELS = {"PRIMARY", "SECONDARY", "TERTIARY", "UNKNOWN"}
REPUBLICATION_STATUSES = {"ALLOWED", "METADATA_ONLY", "REDACTED_ONLY", "PROHIBITED", "UNKNOWN"}
ENTITY_STATUSES = {"CANDIDATE", "REVIEWED", "CONFIRMED", "DISPUTED", "SUPERSEDED"}
CLAIM_REPRESENTATIONS = {"EXACT_QUOTE", "FAITHFUL_PARAPHRASE", "STRUCTURED_EXTRACTION"}
JOURNAL_ACTIONS = {"PLAN", "QUERY", "COLLECT", "PARSE", "NORMALIZE", "RESOLVE_ENTITY", "LINK", "ANALYZE", "CHALLENGE", "REVIEW", "EXPORT", "MONITOR"}
JOURNAL_RESULTS = {"FOUND", "NO_HIT", "BLOCKED", "CONFLICT", "ERROR", "CANCELLED", "REVIEWED"}
GAP_PRIORITIES = {"P0", "P1", "P2", "P3"}
GAP_STATES = {"NOT_CHECKED", "PLANNED", "IN_PROGRESS", "NO_HIT", "BLOCKED", "CONFLICT", "RESOLVED", "WAIVED"}
REPORT_EFFECTS = {"BLOCKS_REPORT", "LIMITS_REPORT", "NON_BLOCKING"}



class StoreError(RuntimeError):
    pass


class BaseStore:
    """File-backed evidence-first case store.

    The store is intentionally dependency-free and inspectable. JSON objects are
    written atomically. Raw captures are content-addressed and never overwritten.
    Search journal entries are append-only files with a canonical SHA-256 chain.
    """

    OBJECT_DIRS = {
        "query_plan": "query_plans",
        "source": "sources",
        "capture": "captures",
        "entity": "entities",
        "claim": "claims",
        "relation": "relations",
        "finding": "findings",
        "research_gap": "research_gaps",
        "entity_match": "entity_matches",
        "coverage": "coverage",
        "graph": "graphs",
        "transform": "transforms",
        "job": "jobs",
        "analysis_run": "analysis_runs",
        "analysis_opinion": "analysis_opinions",
        "consensus": "consensus",
        "monitor_snapshot": "monitoring",
        "journal": "journal",
    }
    ID_FIELDS = {
        "query_plan": "query_plan_id",
        "source": "source_id",
        "capture": "capture_id",
        "entity": "entity_id",
        "claim": "claim_id",
        "relation": "relation_id",
        "finding": "finding_id",
        "research_gap": "research_gap_id",
        "entity_match": "entity_match_id",
        "coverage": "coverage_id",
        "graph": "graph_view_id",
        "transform": "transform_id",
        "job": "job_id",
        "analysis_run": "run_id",
        "analysis_opinion": "opinion_id",
        "consensus": "consensus_id",
        "monitor_snapshot": "snapshot_id",
        "journal": "journal_id",
    }

    def __init__(self, root: str | Path = "data/osint-workbench") -> None:
        self.root = Path(root).expanduser().resolve()
        self.cases_dir = self.root / "cases"
        self.cases_dir.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise StoreError(f"object not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise StoreError(f"invalid JSON object: {path}: {exc}") from exc
        if not isinstance(value, dict):
            raise StoreError(f"expected JSON object: {path}")
        return value

    @staticmethod
    def _atomic_write_json(path: Path, payload: dict[str, Any], *, immutable: bool = False) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        if immutable and path.exists():
            if path.read_bytes() == encoded:
                return
            raise StoreError(f"immutable object already exists with different content: {path}")
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

    def case_dir(self, case_id: str) -> Path:
        case_id = safe_token(case_id, fallback="CASE")
        if not case_id.startswith("CASE-"):
            raise StoreError("case_id must start with CASE-")
        path = self.cases_dir / case_id
        if not path.is_dir():
            raise StoreError(f"case not found: {case_id}")
        return path

    def create_case(
        self,
        *,
        title: str,
        case_type: str,
        purpose: str,
        owner_role: str,
        legal_basis_or_usage_note: str,
        access_class: str = "PUBLIC",
        jurisdictions: Iterable[str] = ("UNSPECIFIED",),
        allowed: Iterable[str] = ("Passive public-source research",),
        excluded: Iterable[str] = ("Credential attacks", "Access-control bypass", "Active exploitation"),
        active_actions_allowed: bool = False,
        synthetic: bool = False,
        case_id: str | None = None,
    ) -> dict[str, Any]:
        case_type = case_type.upper()
        access_class = validate_access_class(access_class)
        if case_type not in CASE_TYPES:
            raise StoreError(f"unsupported case_type: {case_type}")
        if len(title.strip()) < 3 or len(purpose.strip()) < 10:
            raise StoreError("title and purpose are too short")
        if len(owner_role.strip()) < 3 or len(legal_basis_or_usage_note.strip()) < 10:
            raise StoreError("owner_role or legal basis is too short")
        if case_id is None:
            token = safe_token(title, fallback="OSINT", max_length=24)
            timestamp = utc_now_iso().replace("-", "").replace(":", "").replace("T", "-")[:15]
            case_id = f"CASE-{timestamp}-{token}"[:63].rstrip("-")
        else:
            case_id = safe_token(case_id, fallback="CASE")
            if not case_id.startswith("CASE-"):
                case_id = f"CASE-{case_id}"
        case_path = self.cases_dir / case_id
        with self._lock:
            if case_path.exists():
                raise StoreError(f"case already exists: {case_id}")
            case_path.mkdir(parents=True)
            for directory in (*self.OBJECT_DIRS.values(), "reports", "evidence/sha256"):
                (case_path / directory).mkdir(parents=True, exist_ok=True)
            payload: dict[str, Any] = {
                "schema_version": "father-osint.case.v0.1",
                "case_id": case_id,
                "title": title.strip(),
                "case_type": case_type,
                "purpose": purpose.strip(),
                "status": "AUTHORIZED" if legal_basis_or_usage_note.strip() else "DRAFT",
                "access_class": access_class,
                "legal_basis_or_usage_note": legal_basis_or_usage_note.strip(),
                "created_at_utc": utc_now_iso(),
                "owner_role": owner_role.strip(),
                "scope": {
                    "allowed": list(allowed),
                    "excluded": list(excluded),
                    "jurisdictions": list(jurisdictions) or ["UNSPECIFIED"],
                    "allowed_source_classes": [access_class] if access_class != "PUBLIC_WITH_PERSONAL_DATA" else ["PUBLIC", access_class],
                    "active_actions_allowed": bool(active_actions_allowed),
                },
                "retention_rule": "Review on case closure; preserve hashes and audit metadata according to policy.",
                "related_requirement_issues": [20, 21],
                "synthetic": bool(synthetic),
                "classification_decision": f"Case created with access class {access_class}; stricter child-object classes propagate.",
            }
            self._atomic_write_json(case_path / "case.json", payload, immutable=True)
            self._atomic_write_json(case_path / ".counters.json", {}, immutable=False)
        return payload

    def get_case(self, case_id: str) -> dict[str, Any]:
        return self._read_json(self.case_dir(case_id) / "case.json")

    def list_cases(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for path in sorted(self.cases_dir.glob("CASE-*/case.json")):
            try:
                result.append(self._read_json(path))
            except StoreError:
                continue
        return result

    def _allocate_id(self, case_id: str, prefix: str) -> str:
        case_path = self.case_dir(case_id)
        counters_path = case_path / ".counters.json"
        with self._lock:
            counters = self._read_json(counters_path)
            value = int(counters.get(prefix, 0)) + 1
            counters[prefix] = value
            self._atomic_write_json(counters_path, counters)
        return f"{prefix}-{value:04d}"

    def _object_path(self, case_id: str, kind: str, object_id: str) -> Path:
        if kind not in self.OBJECT_DIRS:
            raise StoreError(f"unsupported object kind: {kind}")
        return self.case_dir(case_id) / self.OBJECT_DIRS[kind] / f"{safe_token(object_id)}.json"

    def save_object(self, case_id: str, kind: str, payload: dict[str, Any], *, immutable: bool = True) -> dict[str, Any]:
        id_field = self.ID_FIELDS.get(kind)
        if id_field is None or not payload.get(id_field):
            raise StoreError(f"{kind} is missing {id_field}")
        if payload.get("case_id") not in {None, case_id}:
            raise StoreError("case lineage mismatch")
        self._atomic_write_json(self._object_path(case_id, kind, str(payload[id_field])), payload, immutable=immutable)
        return payload

    def get_object(self, case_id: str, kind: str, object_id: str) -> dict[str, Any]:
        return self._read_json(self._object_path(case_id, kind, object_id))

    def list_objects(self, case_id: str, kind: str) -> list[dict[str, Any]]:
        directory = self.case_dir(case_id) / self.OBJECT_DIRS[kind]
        return [self._read_json(path) for path in sorted(directory.glob("*.json"))]

