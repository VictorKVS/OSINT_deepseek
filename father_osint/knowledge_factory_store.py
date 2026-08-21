from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .knowledge_factory import AuditEvent, DocumentRecord, OfficialSource


class KnowledgeFactoryStore:
    """Small append/audit-safe JSONL store for the M1 Knowledge Factory vertical.

    Registry records are upserted by stable IDs. Audit records are append-only.
    The implementation is intentionally simple for M1 and keeps the storage
    contract explicit so it can later move to PostgreSQL without changing the
    domain objects.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.sources_file = self.root / "official_sources.jsonl"
        self.documents_file = self.root / "documents.jsonl"
        self.audit_file = self.root / "audit.jsonl"
        self.originals_dir = self.root / "originals"
        self.originals_dir.mkdir(exist_ok=True)

    @staticmethod
    def _read_jsonl(path: Path) -> list[dict]:
        if not path.exists():
            return []
        rows: list[dict] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    @staticmethod
    def _write_jsonl(path: Path, rows: Iterable[dict]) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        tmp.replace(path)

    @staticmethod
    def _append_jsonl(path: Path, row: dict) -> None:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    def save_source(self, source: OfficialSource) -> None:
        rows = self._read_jsonl(self.sources_file)
        payload = source.to_dict()
        replaced = False
        for index, row in enumerate(rows):
            if row.get("source_id") == source.source_id:
                rows[index] = payload
                replaced = True
                break
        if not replaced:
            rows.append(payload)
        self._write_jsonl(self.sources_file, rows)

    def save_document(self, document: DocumentRecord) -> None:
        rows = self._read_jsonl(self.documents_file)
        payload = document.to_dict()
        replaced = False
        for index, row in enumerate(rows):
            if row.get("document_id") == document.document_id:
                rows[index] = payload
                replaced = True
                break
        if not replaced:
            rows.append(payload)
        self._write_jsonl(self.documents_file, rows)

    def append_audit(self, event: AuditEvent) -> None:
        self._append_jsonl(self.audit_file, event.to_dict())

    def list_sources(self) -> list[dict]:
        return self._read_jsonl(self.sources_file)

    def list_documents(self) -> list[dict]:
        return self._read_jsonl(self.documents_file)

    def list_audit(self) -> list[dict]:
        return self._read_jsonl(self.audit_file)

    def get_source(self, source_id: str) -> dict | None:
        return next((row for row in self.list_sources() if row.get("source_id") == source_id), None)

    def get_document(self, document_id: str) -> dict | None:
        return next((row for row in self.list_documents() if row.get("document_id") == document_id), None)
