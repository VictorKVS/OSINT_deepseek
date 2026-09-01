from __future__ import annotations

import mimetypes
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable

from .canonical import sha256_bytes, utc_now_iso
from .policy import PolicyError, strictest_access_class, validate_access_class
from .store_base import (
    CLAIM_REPRESENTATIONS, ENTITY_STATUSES, ENTITY_TYPES, EVIDENCE_GRADES,
    PRIMARY_LEVELS, RELATION_TYPES, REPUBLICATION_STATUSES, SOURCE_TYPES,
    StoreError,
)


class EvidenceStoreMixin:
    def register_source(
        self,
        case_id: str,
        *,
        url: str,
        title: str,
        publisher: str,
        source_type: str = "WEB_PAGE",
        primary_level: str = "UNKNOWN",
        jurisdiction: str = "UNSPECIFIED",
        language: str = "und",
        affiliation: str = "Unknown or not assessed",
        bias_or_interest: str = "Not assessed",
        reliability_grade: str = "D_LEAD",
        what_it_supports: Iterable[str] = ("The source was located and registered.",),
        what_it_does_not_support: Iterable[str] = ("Any factual conclusion not separately captured and reviewed.",),
        access_class: str = "PUBLIC",
        legal_basis_or_usage_note: str = "Lawfully accessible source registered for the stated case purpose.",
        republication_status: str = "METADATA_ONLY",
        published_at: str | None = None,
    ) -> dict[str, Any]:
        access_class = validate_access_class(access_class)
        source_type = source_type.upper()
        primary_level = primary_level.upper()
        reliability_grade = reliability_grade.upper()
        republication_status = republication_status.upper()
        if access_class == "PROHIBITED":
            raise PolicyError("PROHIBITED sources cannot enter the evidence workflow")
        if source_type not in SOURCE_TYPES:
            raise StoreError(f"unsupported source_type: {source_type}")
        if primary_level not in PRIMARY_LEVELS:
            raise StoreError(f"unsupported primary_level: {primary_level}")
        if reliability_grade not in EVIDENCE_GRADES:
            raise StoreError(f"unsupported reliability_grade: {reliability_grade}")
        if republication_status not in REPUBLICATION_STATUSES:
            raise StoreError(f"unsupported republication_status: {republication_status}")
        if not url.strip() or not title.strip() or not publisher.strip():
            raise StoreError("source URL, title and publisher must not be empty")
        if len(jurisdiction.strip()) < 2 or not (2 <= len(language.strip()) <= 6):
            raise StoreError("source jurisdiction or language is invalid")
        supports = list(what_it_supports)
        limitations = list(what_it_does_not_support)
        if not supports or not limitations:
            raise StoreError("source requires support and limitation statements")
        source_id = self._allocate_id(case_id, "SRC")
        payload = {
            "schema_version": "father-osint.source.v0.1",
            "source_id": source_id,
            "case_id": case_id,
            "url": url,
            "title": title.strip() or url,
            "publisher": publisher.strip() or "Unknown",
            "source_type": source_type,
            "primary_level": primary_level,
            "accessed_at_utc": utc_now_iso(),
            "published_at": published_at,
            "jurisdiction": jurisdiction,
            "language": language,
            "affiliation": affiliation,
            "bias_or_interest": bias_or_interest,
            "reliability_grade": reliability_grade,
            "what_it_supports": supports,
            "what_it_does_not_support": limitations,
            "access_class": access_class,
            "legal_basis_or_usage_note": legal_basis_or_usage_note,
            "republication_status": republication_status,
            "status": "ACTIVE",
        }
        return self.save_object(case_id, "source", payload)

    def capture_bytes(
        self,
        case_id: str,
        *,
        source_id: str,
        data: bytes,
        capture_method: str = "MANUAL_UPLOAD",
        mime_type: str | None = None,
        filename_hint: str = "capture.bin",
        collector_id: str = "osint-workbench",
        collector_version: str = "0.1.0",
        access_class: str | None = None,
        legal_basis_or_usage_note: str = "Captured for evidentiary preservation within approved case scope.",
    ) -> dict[str, Any]:
        source = self.get_object(case_id, "source", source_id)
        access_class = validate_access_class(access_class or source["access_class"])
        if access_class == "PROHIBITED":
            raise PolicyError("PROHIBITED data cannot be captured")
        digest = sha256_bytes(data)
        suffix = Path(filename_hint).suffix.lower()
        if not suffix:
            suffix = mimetypes.guess_extension(mime_type or "application/octet-stream") or ".bin"
        evidence_path = self.case_dir(case_id) / "evidence" / "sha256" / f"{digest}{suffix}"
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            if evidence_path.exists() and evidence_path.read_bytes() != data:
                raise StoreError("content-addressed evidence collision")
            if not evidence_path.exists():
                fd, temp_name = tempfile.mkstemp(prefix=".capture.", suffix=".tmp", dir=evidence_path.parent)
                try:
                    with os.fdopen(fd, "wb") as handle:
                        handle.write(data)
                        handle.flush()
                        os.fsync(handle.fileno())
                    os.replace(temp_name, evidence_path)
                finally:
                    if os.path.exists(temp_name):
                        os.unlink(temp_name)
        capture_id = self._allocate_id(case_id, "CAP")
        payload = {
            "schema_version": "father-osint.source-capture.v0.1",
            "capture_id": capture_id,
            "source_id": source_id,
            "case_id": case_id,
            "captured_at_utc": utc_now_iso(),
            "capture_method": capture_method.upper(),
            "mime_type": mime_type or mimetypes.guess_type(filename_hint)[0] or "application/octet-stream",
            "byte_size": len(data),
            "sha256": digest,
            "storage_uri": evidence_path.as_uri(),
            "immutable": True,
            "collector_id": collector_id,
            "collector_version": collector_version,
            "access_class": access_class,
            "legal_basis_or_usage_note": legal_basis_or_usage_note,
            "raw_preserved": True,
            "integrity_verified": sha256_bytes(evidence_path.read_bytes()) == digest,
            "quarantine_status": "NOT_REQUIRED" if (mime_type or "").startswith("text/") else "PENDING",
        }
        return self.save_object(case_id, "capture", payload)

    def capture_text(self, case_id: str, *, source_id: str, text: str, filename_hint: str = "capture.txt", **kwargs: Any) -> dict[str, Any]:
        return self.capture_bytes(
            case_id,
            source_id=source_id,
            data=text.encode("utf-8"),
            mime_type="text/plain; charset=utf-8",
            filename_hint=filename_hint,
            **kwargs,
        )

    def read_capture_bytes(self, case_id: str, capture_id: str) -> bytes:
        capture = self.get_object(case_id, "capture", capture_id)
        uri = capture["storage_uri"]
        if not uri.startswith("file:"):
            raise StoreError("only local file captures can be read by the passive MVP")
        from urllib.parse import unquote, urlparse
        from urllib.request import url2pathname
        parsed = urlparse(uri)
        path = Path(url2pathname(unquote(parsed.path)))
        data = path.read_bytes()
        if sha256_bytes(data) != capture["sha256"]:
            raise StoreError(f"capture integrity failure: {capture_id}")
        return data

    def create_entity(
        self,
        case_id: str,
        *,
        entity_type: str,
        display_name: str,
        source_ids: Iterable[str],
        aliases: Iterable[str] = (),
        identifiers: Iterable[dict[str, Any]] = (),
        attributes: dict[str, Any] | None = None,
        access_class: str = "PUBLIC",
        status: str = "CANDIDATE",
        synthetic: bool | None = None,
    ) -> dict[str, Any]:
        entity_type = entity_type.upper()
        if entity_type not in ENTITY_TYPES:
            raise StoreError(f"unsupported entity_type: {entity_type}")
        status = status.upper()
        if status not in ENTITY_STATUSES:
            raise StoreError(f"unsupported entity status: {status}")
        if not display_name.strip():
            raise StoreError("entity display_name must not be empty")
        source_ids = list(dict.fromkeys(source_ids))
        if not source_ids:
            raise StoreError("entity requires at least one source_id")
        for source_id in source_ids:
            self.get_object(case_id, "source", source_id)
        entity_id = self._allocate_id(case_id, "ENT")
        payload = {
            "schema_version": "father-osint.entity.v0.1",
            "entity_id": entity_id,
            "case_id": case_id,
            "entity_type": entity_type,
            "display_name": display_name.strip(),
            "aliases": list(dict.fromkeys(alias for alias in aliases if alias.strip())),
            "identifiers": list(identifiers),
            "attributes": dict(attributes or {}),
            "access_class": validate_access_class(access_class),
            "source_ids": source_ids,
            "status": status,
            "synthetic": self.get_case(case_id)["synthetic"] if synthetic is None else bool(synthetic),
        }
        return self.save_object(case_id, "entity", payload)

    def create_claim(
        self,
        case_id: str,
        *,
        source_ids: Iterable[str],
        statement: str,
        locator: str,
        subject_entity_ids: Iterable[str],
        representation: str = "STRUCTURED_EXTRACTION",
        predicate: str | None = None,
        object_entity_ids: Iterable[str] = (),
        object_text: str | None = None,
        access_class: str = "PUBLIC",
        limitations: Iterable[str] = ("Source claim is not automatically an established fact.",),
    ) -> dict[str, Any]:
        source_ids = list(dict.fromkeys(source_ids))
        subjects = list(dict.fromkeys(subject_entity_ids))
        objects = list(dict.fromkeys(object_entity_ids))
        representation = representation.upper()
        if representation not in CLAIM_REPRESENTATIONS:
            raise StoreError(f"unsupported claim representation: {representation}")
        if not source_ids or not subjects:
            raise StoreError("claim requires source_ids and subject_entity_ids")
        if len(statement.strip()) < 3 or not locator.strip():
            raise StoreError("claim statement or locator is too short")
        for source_id in source_ids:
            self.get_object(case_id, "source", source_id)
        for entity_id in subjects + objects:
            self.get_object(case_id, "entity", entity_id)
        claim_id = self._allocate_id(case_id, "CLM")
        payload: dict[str, Any] = {
            "schema_version": "father-osint.claim.v0.1",
            "claim_id": claim_id,
            "case_id": case_id,
            "source_ids": source_ids,
            "statement": statement.strip(),
            "representation": representation,
            "locator": locator,
            "subject_entity_ids": subjects,
            "status": "SOURCE_CLAIM",
            "access_class": validate_access_class(access_class),
            "limitations": list(limitations),
        }
        if predicate is not None:
            payload["predicate"] = predicate
        if objects:
            payload["object_entity_ids"] = objects
        if object_text is not None:
            payload["object_text"] = object_text
        return self.save_object(case_id, "claim", payload)

    def create_relation(
        self,
        case_id: str,
        *,
        from_entity_id: str,
        relation_type: str,
        to_entity_id: str,
        source_ids: Iterable[str],
        claim_ids: Iterable[str],
        evidence_grade: str = "D_LEAD",
        status: str = "CANDIDATE",
        valid_from: str | None = None,
        valid_to: str | None = None,
        not_implying: Iterable[str] = ("Causation, control or wrongdoing beyond the cited evidence.",),
    ) -> dict[str, Any]:
        relation_type = relation_type.upper()
        evidence_grade = evidence_grade.upper()
        if relation_type not in RELATION_TYPES:
            raise StoreError(f"unsupported relation_type: {relation_type}")
        if evidence_grade not in EVIDENCE_GRADES:
            raise StoreError(f"unsupported evidence_grade: {evidence_grade}")
        status = status.upper()
        if status not in ENTITY_STATUSES:
            raise StoreError(f"unsupported relation status: {status}")
        self.get_object(case_id, "entity", from_entity_id)
        self.get_object(case_id, "entity", to_entity_id)
        source_ids = list(dict.fromkeys(source_ids))
        claim_ids = list(dict.fromkeys(claim_ids))
        if not source_ids or not claim_ids:
            raise StoreError("relation requires source_ids and claim_ids")
        for source_id in source_ids:
            self.get_object(case_id, "source", source_id)
        for claim_id in claim_ids:
            self.get_object(case_id, "claim", claim_id)
        relation_id = self._allocate_id(case_id, "REL")
        payload = {
            "schema_version": "father-osint.relation.v0.1",
            "relation_id": relation_id,
            "case_id": case_id,
            "from_entity_id": from_entity_id,
            "relation_type": relation_type,
            "to_entity_id": to_entity_id,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "source_ids": source_ids,
            "claim_ids": claim_ids,
            "evidence_grade": evidence_grade,
            "status": status,
            "not_implying": list(not_implying),
        }
        return self.save_object(case_id, "relation", payload)

