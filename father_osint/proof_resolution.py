from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from .document_compiler import DocumentCompilerError, extract_visible_text


IDENTITY_METHOD = "EXTRACT_VISIBLE_TEXT__PRIMARY_AND_SECONDARY__NORMALIZED"
EVIDENCE_KIND = "OPERATOR_BROWSER_CAPTURE_OF_A0_PUBLICATION_PAGE"


def _normalize(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class LocalProofResult:
    document_id: str
    proof_available: bool
    resolution: str
    local_path: str
    bytes: int | None
    sha256: str | None
    expected_sha256: str | None
    sha256_match: bool
    identity_method: str
    primary_identity_markers: dict[str, bool]
    secondary_identity_markers: dict[str, bool]
    identity_error: str | None
    identity_pass: bool
    publication_anchor: dict[str, Any] | None
    evidence_kind: str
    network_used: bool = False
    api_required_for_serving: bool = False
    new_d2_d3_promotion: bool = False
    legal_truth_promoted: bool = False
    elapsed_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def resolve_local_official_proof(
    *,
    repo_root: Path,
    review_item: dict[str, Any],
    source_item: dict[str, Any],
    local_path: Path,
) -> LocalProofResult:
    started = time.perf_counter()
    document_id = str(source_item.get("document_id") or review_item.get("document_id") or "")
    expected_sha = str(review_item.get("artifact_sha256") or "") or None
    primary = [str(value) for value in source_item.get("primary_identity_markers", [])]
    secondary = [str(value) for value in source_item.get("identity_markers", [])]
    publication_anchor = source_item.get("publication_anchor")

    if not local_path.is_file():
        return LocalProofResult(
            document_id=document_id,
            proof_available=False,
            resolution="BLOCKED_LOCAL_EVIDENCE_MISSING",
            local_path=local_path.relative_to(repo_root).as_posix(),
            bytes=None,
            sha256=None,
            expected_sha256=expected_sha,
            sha256_match=False,
            identity_method=IDENTITY_METHOD,
            primary_identity_markers={marker: False for marker in primary},
            secondary_identity_markers={marker: False for marker in secondary},
            identity_error="local capture is missing",
            identity_pass=False,
            publication_anchor=publication_anchor,
            evidence_kind=EVIDENCE_KIND,
            elapsed_seconds=time.perf_counter() - started,
        )

    actual_sha = _sha256(local_path)
    sha_match = bool(expected_sha) and actual_sha == expected_sha
    primary_results = {marker: False for marker in primary}
    secondary_results = {marker: False for marker in secondary}
    identity_error: str | None = None

    try:
        visible = extract_visible_text(local_path.read_bytes(), "text/html")
        normalized = _normalize(visible)
        primary_results = {marker: _normalize(marker) in normalized for marker in primary}
        secondary_results = {marker: _normalize(marker) in normalized for marker in secondary}
    except (OSError, DocumentCompilerError, ValueError) as exc:
        identity_error = f"{type(exc).__name__}: {exc}"

    identity_pass = (
        identity_error is None
        and bool(primary_results)
        and all(primary_results.values())
        and all(secondary_results.values())
    )
    proof_available = sha_match and identity_pass

    return LocalProofResult(
        document_id=document_id,
        proof_available=proof_available,
        resolution="LOCAL_A0_VERIFIED_CACHE" if proof_available else "BLOCKED_LOCAL_A0_VERIFICATION_FAILED",
        local_path=local_path.relative_to(repo_root).as_posix(),
        bytes=local_path.stat().st_size,
        sha256=actual_sha,
        expected_sha256=expected_sha,
        sha256_match=sha_match,
        identity_method=IDENTITY_METHOD,
        primary_identity_markers=primary_results,
        secondary_identity_markers=secondary_results,
        identity_error=identity_error,
        identity_pass=identity_pass,
        publication_anchor=publication_anchor,
        evidence_kind=EVIDENCE_KIND,
        elapsed_seconds=time.perf_counter() - started,
    )


def resolve_pack_from_files(
    *,
    repo_root: Path,
    review_path: Path,
    source_pack_path: Path,
    local_dir: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    review = json.loads(review_path.read_text(encoding="utf-8"))
    source_pack = json.loads(source_pack_path.read_text(encoding="utf-8"))
    review_by_id = {str(item.get("document_id")): item for item in review.get("documents", [])}

    results: list[dict[str, Any]] = []
    for source_item in source_pack.get("documents", []):
        document_id = str(source_item.get("document_id") or "")
        review_item = review_by_id.get(document_id)
        if review_item is None:
            results.append({
                "document_id": document_id,
                "proof_available": False,
                "resolution": "BLOCKED_REVIEW_RECORD_MISSING",
                "network_used": False,
                "api_required_for_serving": False,
                "new_d2_d3_promotion": False,
                "legal_truth_promoted": False,
            })
            continue
        local_path = local_dir / f"{document_id}.html"
        results.append(resolve_local_official_proof(
            repo_root=repo_root,
            review_item=review_item,
            source_item=source_item,
            local_path=local_path,
        ).to_dict())

    verified = sum(bool(item.get("proof_available")) for item in results)
    total = len(results)
    elapsed = time.perf_counter() - started
    return {
        "record_type": "LOCAL_OFFICIAL_PROOF_PACK_RESOLUTION",
        "pack_id": source_pack.get("pack_id"),
        "documents_total": total,
        "proof_available": verified,
        "proof_blocked": total - verified,
        "all_proofs_available": total > 0 and verified == total,
        "network_used": False,
        "api_required_for_serving": False,
        "new_d2_d3_promotion": False,
        "legal_truth_promoted": False,
        "evidence_kind": EVIDENCE_KIND,
        "documents": results,
        "total_seconds": elapsed,
        "throughput_docs_per_second": (total / elapsed) if elapsed > 0 else None,
    }
