from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "config" / "external_assets.seed.jsonl"

_ALLOWED_ROLES = {
    "PROOF_SOURCE",
    "BOOTSTRAP_CORPUS",
    "NAVIGATION_SOURCE",
    "REFERENCE_KB",
    "ALGORITHM_DONOR",
    "BENCHMARK_DATASET",
}
_ALLOWED_ADOPTIONS = {"REUSE", "WRAP", "FORK", "REFERENCE", "REJECT"}
_ALLOWED_CONTENT_MODES = {"NONE", "CANDIDATE_ONLY", "PROOF_ADAPTER"}
_ALLOWED_OPERATIONS = {
    "algorithm_reuse",
    "candidate_import",
    "proof_acquisition",
    "canonical_promotion",
}


class ExternalAssetPolicyError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ExternalAsset:
    asset_id: str
    name: str
    role: str
    adoption: str
    content_reuse_mode: str
    algorithm_reuse_allowed: bool
    legal_truth_promoted: bool
    status: str
    evidence: str

    @classmethod
    def from_dict(cls, row: dict[str, object]) -> "ExternalAsset":
        required = {
            "asset_id",
            "name",
            "role",
            "adoption",
            "content_reuse_mode",
            "algorithm_reuse_allowed",
            "legal_truth_promoted",
            "status",
            "evidence",
        }
        missing = sorted(required - set(row))
        if missing:
            raise ExternalAssetPolicyError(f"external asset missing fields: {missing}")
        asset = cls(
            asset_id=str(row["asset_id"]),
            name=str(row["name"]),
            role=str(row["role"]),
            adoption=str(row["adoption"]),
            content_reuse_mode=str(row["content_reuse_mode"]),
            algorithm_reuse_allowed=bool(row["algorithm_reuse_allowed"]),
            legal_truth_promoted=bool(row["legal_truth_promoted"]),
            status=str(row["status"]),
            evidence=str(row["evidence"]),
        )
        asset.validate()
        return asset

    def validate(self) -> None:
        if not self.asset_id.strip():
            raise ExternalAssetPolicyError("asset_id must be non-empty")
        if self.role not in _ALLOWED_ROLES:
            raise ExternalAssetPolicyError(f"unsupported external asset role: {self.role}")
        if self.adoption not in _ALLOWED_ADOPTIONS:
            raise ExternalAssetPolicyError(f"unsupported adoption decision: {self.adoption}")
        if self.content_reuse_mode not in _ALLOWED_CONTENT_MODES:
            raise ExternalAssetPolicyError(f"unsupported content reuse mode: {self.content_reuse_mode}")
        if self.legal_truth_promoted:
            raise ExternalAssetPolicyError("external asset registry cannot directly promote legal truth")
        if self.adoption == "REJECT" and self.content_reuse_mode != "NONE":
            raise ExternalAssetPolicyError("REJECT assets must have content_reuse_mode=NONE")
        if self.role == "ALGORITHM_DONOR" and self.content_reuse_mode != "NONE":
            raise ExternalAssetPolicyError("ALGORITHM_DONOR cannot authorize donor content reuse")


def load_external_assets(path: Path | None = None) -> dict[str, ExternalAsset]:
    registry = path or DEFAULT_REGISTRY
    if not registry.is_file():
        raise ExternalAssetPolicyError(f"external asset registry missing: {registry}")
    assets: dict[str, ExternalAsset] = {}
    with registry.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ExternalAssetPolicyError(f"invalid registry JSONL line {line_number}: {exc}") from exc
            if not isinstance(row, dict):
                raise ExternalAssetPolicyError(f"registry line {line_number} must be an object")
            asset = ExternalAsset.from_dict(row)
            if asset.asset_id in assets:
                raise ExternalAssetPolicyError(f"duplicate external asset_id: {asset.asset_id}")
            assets[asset.asset_id] = asset
    if not assets:
        raise ExternalAssetPolicyError("external asset registry is empty")
    return assets


def authorize_external_asset(asset_id: str, operation: str, *, path: Path | None = None) -> ExternalAsset:
    if operation not in _ALLOWED_OPERATIONS:
        raise ExternalAssetPolicyError(f"unsupported operation: {operation}")
    assets = load_external_assets(path)
    asset = assets.get(asset_id)
    if asset is None:
        raise ExternalAssetPolicyError(f"unregistered external asset: {asset_id}")

    if operation == "canonical_promotion":
        raise ExternalAssetPolicyError(
            f"external asset {asset_id} cannot directly authorize canonical promotion; FATHER review/promotion gates are required"
        )
    if operation == "algorithm_reuse":
        if not asset.algorithm_reuse_allowed:
            raise ExternalAssetPolicyError(f"algorithm reuse blocked for external asset {asset_id}")
        return asset
    if operation == "candidate_import":
        if asset.content_reuse_mode != "CANDIDATE_ONLY":
            raise ExternalAssetPolicyError(f"candidate content import blocked for external asset {asset_id}")
        return asset
    if operation == "proof_acquisition":
        if asset.content_reuse_mode != "PROOF_ADAPTER" or asset.role != "PROOF_SOURCE":
            raise ExternalAssetPolicyError(f"proof acquisition blocked for external asset {asset_id}")
        return asset

    raise ExternalAssetPolicyError(f"operation not authorized: {operation}")
