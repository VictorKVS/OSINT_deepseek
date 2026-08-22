from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.document_compiler import DocumentCompilerError, extract_visible_text
from father_osint.garant_timeline import official_evidence_requests, parse_garant_timeline_text
from father_osint.legal_source_bundle import LegalSourceBundle


DEFAULT_BUNDLES = REPO_ROOT / "config" / "pdn_source_bundles.json"
DEFAULT_INPUT = REPO_ROOT / "data" / "operator_import" / "garant_timeline"
DEFAULT_LOCAL = REPO_ROOT / "data" / "knowledge_factory" / "pdn_timelines"
DEFAULT_EXPORT = REPO_ROOT / "reports" / "pdn_timelines"

_BASIS_KEYS = (
    "EXPLICIT_CALENDAR_DATE",
    "RELATIVE_TO_OFFICIAL_PUBLICATION",
    "NON_CALENDAR_RULE",
)


def _load_bundles(path: Path) -> tuple[LegalSourceBundle, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(LegalSourceBundle.from_dict(item) for item in payload["bundles"])


def _candidate_input(input_dir: Path, document_id: str) -> Path | None:
    for suffix in (".html", ".htm", ".txt"):
        candidate = input_dir / f"{document_id}{suffix}"
        if candidate.is_file():
            return candidate
    return None


def _mime_for(path: Path) -> str:
    if path.suffix.casefold() in {".html", ".htm"}:
        return "text/html"
    return "text/plain"


def _empty_basis_counts() -> dict[str, int]:
    return {key: 0 for key in _BASIS_KEYS}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract only amendment/version metadata from operator-saved GARANT pages"
    )
    parser.add_argument("--bundles", default=str(DEFAULT_BUNDLES))
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT))
    parser.add_argument("--local-root", default=str(DEFAULT_LOCAL))
    parser.add_argument("--export-dir", default=str(DEFAULT_EXPORT))
    parser.add_argument("--observed-on", default="2026-08-22")
    args = parser.parse_args()

    bundles = _load_bundles(Path(args.bundles))
    input_dir = Path(args.input_dir)
    local_root = Path(args.local_root)
    export_dir = Path(args.export_dir)
    local_root.mkdir(parents=True, exist_ok=True)
    export_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    evidence_requests: list[dict[str, object]] = []
    basis_counts = _empty_basis_counts()

    for bundle in bundles:
        provider = bundle.preferred_timeline_provider()
        if provider is None:
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "TIMELINE_PROVIDER_PENDING",
            })
            continue

        source_path = _candidate_input(input_dir, bundle.document_id)
        if source_path is None:
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "INPUT_PENDING",
                "source_id": provider.source_id,
                "source_url": provider.url,
                "expected_input": str(input_dir / f"{bundle.document_id}.html"),
            })
            continue

        try:
            source_bytes = source_path.read_bytes()
            source_capture_sha256 = hashlib.sha256(source_bytes).hexdigest()
            text = extract_visible_text(source_bytes, _mime_for(source_path))
            capture = parse_garant_timeline_text(
                document_id=bundle.document_id,
                source_url=provider.url,
                observed_on=args.observed_on,
                text=text,
            )
        except (DocumentCompilerError, ValueError) as exc:
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "PARSE_FAILED",
                "source_id": provider.source_id,
                "source_url": provider.url,
                "reason": str(exc),
            })
            continue

        local_path = local_root / f"{bundle.document_id}.timeline.json"
        local_payload = capture.to_dict()
        local_payload["source_capture_sha256"] = source_capture_sha256
        local_payload["source_capture_bytes"] = len(source_bytes)
        local_path.write_text(
            json.dumps(local_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        requests = list(
            official_evidence_requests(
                capture,
                source_capture_sha256=source_capture_sha256,
            )
        )
        evidence_requests.extend(requests)

        record_basis_counts = _empty_basis_counts()
        for event in capture.events:
            record_basis_counts[event.effective_date_basis] += 1
            basis_counts[event.effective_date_basis] += 1

        records.append({
            "record_type": "TIMELINE_CAPTURE",
            "document_id": bundle.document_id,
            "status": "TIMELINE_METADATA_READY",
            "source_id": provider.source_id,
            "source_url": provider.url,
            "source_capture_sha256": source_capture_sha256,
            "source_capture_bytes": len(source_bytes),
            "events": len(capture.events),
            "future_edition_signalled": capture.future_edition_signalled,
            "semantic_text_mirrored": False,
            "official_evidence_requests": len(requests),
            "effective_date_basis_counts": record_basis_counts,
        })

    summary = {
        "record_type": "TIMELINE_SUMMARY",
        "bundles": len(bundles),
        "timeline_metadata_ready": sum(item.get("status") == "TIMELINE_METADATA_READY" for item in records),
        "input_pending": sum(item.get("status") == "INPUT_PENDING" for item in records),
        "parse_failed": sum(item.get("status") == "PARSE_FAILED" for item in records),
        "official_evidence_requests": len(evidence_requests),
        "effective_date_basis_counts": basis_counts,
        "semantic_text_mirrored": False,
        "timeline_policy": "GARANT_NAVIGATES_A0_A1_PROVES",
    }

    jsonl = export_dir / "timeline_metadata.jsonl"
    with jsonl.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n")
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        for request in evidence_requests:
            payload = {"record_type": "OFFICIAL_EVIDENCE_REQUEST", **request}
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    plan = export_dir / "PLAN.md"
    lines = [
        "# PDn legal version timeline plan",
        "",
        "Policy: **GARANT navigates the version timeline; A0/A1 sources prove publication/effectiveness.**",
        "",
        f"- bundles: {summary['bundles']}",
        f"- timeline metadata ready: {summary['timeline_metadata_ready']}",
        f"- input pending: {summary['input_pending']}",
        f"- parse failed: {summary['parse_failed']}",
        f"- official evidence requests: {summary['official_evidence_requests']}",
        f"- explicit calendar-date rules: {basis_counts['EXPLICIT_CALENDAR_DATE']}",
        f"- publication-relative rules: {basis_counts['RELATIVE_TO_OFFICIAL_PUBLICATION']}",
        f"- other non-calendar rules: {basis_counts['NON_CALENDAR_RULE']}",
        "- semantic/full legal text mirrored from GARANT: **no**",
        "",
        "## Documents",
        "",
        "| Document | Status | Timeline source | Events | Evidence requests |",
        "|---|---|---|---:|---:|",
    ]
    for record in records:
        lines.append(
            f"| `{record['document_id']}` | {record['status']} | {record.get('source_id', '—')} | "
            f"{record.get('events', '—')} | {record.get('official_evidence_requests', '—')} |"
        )
    lines += [
        "",
        "Every amendment event stays `OFFICIAL_EVIDENCE_PENDING` until an A0/A1 publication/effectiveness anchor is attached.",
        "Publication-relative rules explicitly request an A0/A1 official-publication date; no calendar date is inferred from GARANT alone.",
        "Each local GARANT capture is linked by SHA-256 only; no full GARANT text is exported or mirrored.",
    ]
    plan.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({
        "summary": summary,
        "input_dir": str(input_dir),
        "local_root": str(local_root),
        "export_jsonl": str(jsonl),
        "export_plan": str(plan),
    }, ensure_ascii=False, indent=2))

    return 2 if summary["parse_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
