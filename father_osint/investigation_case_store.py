from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from secrets import randbelow
from typing import Any


CASE_STATUSES = {"DRAFT", "ACTIVE", "REVIEW", "CLOSED", "ARCHIVED"}
QUESTION_STATUSES = {"OPEN", "PARTIAL", "ANSWERED", "BLOCKED"}
HYPOTHESIS_STATUSES = {"OPEN", "SUPPORTED", "WEAKENED", "REJECTED", "UNRESOLVED"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
INVESTIGATION_MODES = {
    "PERSON",
    "ORGANIZATION",
    "INFRASTRUCTURE",
    "TELEGRAM_SOCIAL",
    "CRYPTO",
    "DOCUMENT_REGULATORY",
    "MEDIA_NARRATIVE",
    "GEO",
    "INCIDENT_CAMPAIGN",
    "CUSTOM",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class InvestigationCaseStore:
    """Small local JSON case store for Investigation Workspace v1.

    Each case is stored in a separate atomically replaced JSON file. The store
    is intentionally conservative: it validates case identity/status and keeps
    analyst objects inside the case until the graph/evidence stores are split
    into their own persistence layer.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        tmp.replace(path)

    @staticmethod
    def _read(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _path(self, case_id: str) -> Path:
        safe = case_id.strip().upper()
        if not safe.startswith("CASE-") or any(ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in safe):
            raise ValueError("invalid case_id")
        return self.root / f"{safe}.json"

    def _new_case_id(self) -> str:
        year = datetime.now(timezone.utc).year
        for _ in range(32):
            candidate = f"CASE-{year}-{randbelow(100_000_000):08d}"
            if not self._path(candidate).exists():
                return candidate
        raise RuntimeError("unable to allocate unique case_id")

    def create_case(
        self,
        *,
        title: str,
        purpose: str,
        investigation_modes: list[str] | tuple[str, ...],
        in_scope: list[str] | None = None,
        out_of_scope: list[str] | None = None,
        constraints: list[str] | None = None,
        status: str = "DRAFT",
    ) -> dict[str, Any]:
        clean_title = title.strip()
        clean_purpose = purpose.strip()
        if not clean_title:
            raise ValueError("case title is required")
        if not clean_purpose:
            raise ValueError("case purpose is required")

        clean_status = status.strip().upper()
        if clean_status not in CASE_STATUSES:
            raise ValueError("invalid case status")

        modes = [str(mode).strip().upper() for mode in investigation_modes]
        if not modes or any(mode not in INVESTIGATION_MODES for mode in modes):
            raise ValueError("invalid investigation mode")
        if len(modes) != len(set(modes)):
            raise ValueError("duplicate investigation mode")

        now = utc_now_iso()
        payload: dict[str, Any] = {
            "schema_version": "1.0",
            "case_id": self._new_case_id(),
            "title": clean_title,
            "status": clean_status,
            "investigation_modes": modes,
            "scope": {
                "purpose": clean_purpose,
                "in_scope": list(in_scope or []),
                "out_of_scope": list(out_of_scope or []),
                "constraints": list(constraints or []),
            },
            "questions": [],
            "hypotheses": [],
            "entities": [],
            "relations": [],
            "findings": [],
            "evidence": [],
            "claims": [],
            "timeline": [],
            "conclusions": [],
            "created_at": now,
            "updated_at": now,
        }
        self._atomic_write(self._path(payload["case_id"]), payload)
        return deepcopy(payload)

    def list_cases(self, *, include_archived: bool = False) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for path in self.root.glob("CASE-*.json"):
            try:
                case = self._read(path)
            except (OSError, json.JSONDecodeError):
                continue
            if not include_archived and case.get("status") == "ARCHIVED":
                continue
            rows.append(case)
        rows.sort(key=lambda row: str(row.get("updated_at", "")), reverse=True)
        return rows

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        path = self._path(case_id)
        if not path.exists():
            return None
        return deepcopy(self._read(path))

    def save_case(self, case: dict[str, Any]) -> dict[str, Any]:
        case_id = str(case.get("case_id", "")).strip().upper()
        if not case_id:
            raise ValueError("case_id is required")
        status = str(case.get("status", "")).strip().upper()
        if status not in CASE_STATUSES:
            raise ValueError("invalid case status")
        updated = deepcopy(case)
        updated["case_id"] = case_id
        updated["status"] = status
        updated["updated_at"] = utc_now_iso()
        self._atomic_write(self._path(case_id), updated)
        return deepcopy(updated)

    def add_question(
        self,
        case_id: str,
        *,
        text: str,
        priority: str = "P1",
        status: str = "OPEN",
    ) -> dict[str, Any]:
        case = self.get_case(case_id)
        if case is None:
            raise KeyError(case_id)
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("question text is required")
        clean_priority = priority.strip().upper()
        clean_status = status.strip().upper()
        if clean_priority not in PRIORITIES:
            raise ValueError("invalid question priority")
        if clean_status not in QUESTION_STATUSES:
            raise ValueError("invalid question status")

        questions = list(case.get("questions") or [])
        question_id = f"Q-{len(questions) + 1:03d}"
        question = {
            "question_id": question_id,
            "text": clean_text,
            "status": clean_status,
            "priority": clean_priority,
        }
        questions.append(question)
        case["questions"] = questions
        self.save_case(case)
        return deepcopy(question)

    def add_hypothesis(
        self,
        case_id: str,
        *,
        text: str,
        status: str = "OPEN",
    ) -> dict[str, Any]:
        case = self.get_case(case_id)
        if case is None:
            raise KeyError(case_id)
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("hypothesis text is required")
        clean_status = status.strip().upper()
        if clean_status not in HYPOTHESIS_STATUSES:
            raise ValueError("invalid hypothesis status")

        hypotheses = list(case.get("hypotheses") or [])
        hypothesis_id = f"H-{len(hypotheses) + 1:03d}"
        hypothesis = {
            "hypothesis_id": hypothesis_id,
            "text": clean_text,
            "status": clean_status,
            "supporting_evidence_ids": [],
            "counter_evidence_ids": [],
            "gap_ids": [],
            "confidence_rationale": "",
        }
        hypotheses.append(hypothesis)
        case["hypotheses"] = hypotheses
        self.save_case(case)
        return deepcopy(hypothesis)

    def set_status(self, case_id: str, status: str) -> dict[str, Any]:
        case = self.get_case(case_id)
        if case is None:
            raise KeyError(case_id)
        clean_status = status.strip().upper()
        if clean_status not in CASE_STATUSES:
            raise ValueError("invalid case status")
        case["status"] = clean_status
        return self.save_case(case)
