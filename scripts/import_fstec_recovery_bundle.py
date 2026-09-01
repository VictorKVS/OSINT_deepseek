from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_OUT = ROOT / "reports" / "security_current_only" / "LATEST_FSTEC_RECOVERY_IMPORT.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Import FSTEC recovery bundle produced by GitHub Actions.")
    parser.add_argument("bundle", help="Path to fstec-official-recovery ZIP")
    args = parser.parse_args()

    bundle = Path(args.bundle).expanduser().resolve()
    if not bundle.is_file():
        raise SystemExit(f"bundle not found: {bundle}")

    imported: list[dict[str, object]] = []
    errors: list[str] = []

    with zipfile.ZipFile(bundle) as zf:
        report_name = "reports/security_current_only/LATEST_FSTEC_OFFICIAL_RECOVERY_RUN.json"
        if report_name not in zf.namelist():
            raise SystemExit("recovery report missing from bundle")
        report = json.loads(zf.read(report_name).decode("utf-8"))
        environment_id = str(report.get("execution_environment_id") or "")
        if environment_id != "GITHUB_ACTIONS_UBUNTU_LATEST":
            raise SystemExit(f"unexpected execution environment: {environment_id or '<missing>'}")

        for row in report.get("results", []) or []:
            if not isinstance(row, dict) or row.get("status") not in {"DOWNLOADED", "REUSED_EXACT"}:
                continue
            did = str(row.get("document_id") or "")
            digest = str(row.get("sha256") or "").lower()
            raw_ref = str(row.get("raw_path") or "")
            if len(digest) != 64 or not raw_ref:
                errors.append(f"{did}: missing sha256/raw_path")
                continue
            if raw_ref not in zf.namelist():
                errors.append(f"{did}: raw artifact missing from bundle: {raw_ref}")
                continue
            data = zf.read(raw_ref)
            actual = sha256_bytes(data)
            if actual != digest:
                errors.append(f"{did}: SHA-256 mismatch expected={digest} actual={actual}")
                continue
            if not data.startswith(b"%PDF-"):
                errors.append(f"{did}: artifact is not PDF")
                continue

            target = ROOT / raw_ref
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".fstec-import-", delete=False) as tmp:
                tmp.write(data)
                tmp_path = Path(tmp.name)
            if sha256_bytes(tmp_path.read_bytes()) != digest:
                tmp_path.unlink(missing_ok=True)
                errors.append(f"{did}: post-write SHA-256 mismatch")
                continue
            tmp_path.replace(target)

            meta_ref = f"data/security_current_only/metadata/{did}.json"
            if meta_ref in zf.namelist():
                meta = json.loads(zf.read(meta_ref).decode("utf-8"))
            else:
                meta = dict(row)
            meta["execution_environment_id"] = environment_id
            meta["imported_from_recovery_bundle"] = bundle.name
            meta["imported_at"] = utc_now()
            meta["artifact_pdf_magic_check"] = True
            meta["document_identity_confirmed"] = False
            meta["identity_status"] = "VISUAL_FIRST_PAGE_REVIEW_REQUIRED"
            meta["legal_truth_eligible"] = False
            meta["kb_auto_promotion"] = False
            meta_path = ROOT / meta_ref
            meta_path.parent.mkdir(parents=True, exist_ok=True)
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            imported.append({
                "document_id": did,
                "sha256": digest,
                "byte_length": len(data),
                "raw_path": raw_ref,
                "metadata_path": meta_ref,
            })

    summary = {
        "record_type": "FSTEC_RECOVERY_BUNDLE_IMPORT",
        "schema_version": "1.0",
        "status": "PASS" if imported and not errors else "PASS_WITH_GAPS" if imported else "FAIL",
        "execution_environment_id": "GITHUB_ACTIONS_UBUNTU_LATEST",
        "bundle": str(bundle),
        "imported_total": len(imported),
        "error_total": len(errors),
        "errors": errors,
        "imports": imported,
        "document_identity_confirmed": False,
        "identity_status": "VISUAL_FIRST_PAGE_REVIEW_REQUIRED",
        "legal_truth_eligible": False,
        "kb_auto_promotion": False,
        "observed_at": utc_now(),
    }
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if imported and not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
