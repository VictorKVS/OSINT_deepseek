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


def _candidate_inputs(input_dir: Path, document_id: str) -> tuple[Path, ...]:
    # Prefer a rendered-text capture over browser-saved HTML, but inspect all
    # available candidates so stale shell HTML cannot mask a valid .txt file.
    candidates: list[Path] = []
    for suffix in (".txt", ".html", ".htm"):
        candidate = input_dir / f"{document_id}{suffix}"
        if candidate.is_file():
            candidates.append(candidate)
    return tuple(candidates)


def _mime_for(path: Path) -> str:
    if path.suffix.casefold() in {".html", ".htm"}:
        return "text/html"
    return "text/plain"


def _empty_basis_counts() -> dict[str, int]:
    return {key: 0 for key in _BASIS_KEYS}


def _normalized(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _missing_identity_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    normalized_text = _normalized(text)
    return [marker for marker in markers if _normalized(marker) not in normalized_text]


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

        source_paths = _candidate_inputs(input_dir, bundle.document_id)
        if not source_paths:
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "INPUT_PENDING",
                "source_id": provider.source_id,
                "source_url": provider.url,
                "expected_input": str(input_dir / f"{bundle.document_id}.txt"),
            })
            continue

        selected_path: Path | None = None
        source_bytes: bytes | None = None
        source_capture_sha256: str | None = None
        text: str | None = None
        candidate_diagnostics: list[dict[str, object]] = []
        extraction_failures = 0

        for candidate in source_paths:
            try:
                candidate_bytes = candidate.read_bytes()
                candidate_text = extract_visible_text(candidate_bytes, _mime_for(candidate))
            except (DocumentCompilerError, ValueError) as exc:
                extraction_failures += 1
                candidate_diagnostics.append({
                    "file": candidate.name,
                    "status": "PARSE_FAILED",
                    "reason": str(exc),
                })
                continue

            missing_markers = _missing_identity_markers(candidate_text, provider.identity_markers)
            if missing_markers:
                candidate_diagnostics.append({
                    "file": candidate.name,
                    "status": "IDENTITY_FAILED",
                    "missing_identity_markers": missing_markers,
                })
                continue

            selected_path = candidate
            source_bytes = candidate_bytes
            source_capture_sha256 = hashlib.sha256(candidate_bytes).hexdigest()
            text = candidate_text
            break

        if selected_path is None or source_bytes is None or source_capture_sha256 is None or text is None:
            status = "PARSE_FAILED" if extraction_failures == len(source_paths) else "IDENTITY_FAILED"
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": status,
                "source_id": provider.source_id,
                "source_url": provider.url,
                "candidate_files": [path.name for path in source_paths],
                "candidate_diagnostics": candidate_diagnostics,
                "reason": (
                    "no local capture passed document identity markers"
                    if status == "IDENTITY_FAILED"
                    else "no local capture could be parsed as visible text"
                ),
                "semantic_text_mirrored": False,
            })
            continue

        try:
            capture = parse_garant_timeline_text(
                document_id=bundle.document_id,
                source_url=provider.url,
                observed_on=args.observed_on,
                text=text,
            )
        except ValueError as exc:
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "PARSE_FAILED",
                "source_id": provider.source_id,
                "source_url": provider.url,
                "selected_input": selected_path.name,
                "reason": str(exc),
            })
            continue

        if not capture.events:
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "TIMELINE_EMPTY",
                "source_id": provider.source_id,
                "source_url": provider.url,
                "selected_input": selected_path.name,
                "source_capture_sha256": source_capture_sha256,
                "source_capture_bytes": len(source_bytes),
                "reason": "document identity passed but no amendment events were extracted",
                "semantic_text_mirrored": False,
            })
            continue

        local_path = local_root / f"{bundle.document_id}.timeline.json"
        local_payload = capture.to_dict()
        local_payload["source_capture_sha256"] = source_capture_sha256
        local_payload["source_capture_bytes"] = len(source_bytes)
        local_payload["selected_input"] = selected_path.name
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
            "selected_input": selected_path.name,
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
        "timeline_empty": sum(item.get("status") == "TIMELINE_EMPTY" for item in records),
        "identity_failed": sum(item.get("status") == "IDENTITY_FAILED" for item in records),
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
        f"- timeline empty: {summary['timeline_empty']}",
        f"- identity failed: {summary['identity_failed']}",
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
        "Every timeline capture must pass document identity markers before amendment parsing.",
        "Multiple local capture formats may coexist; the runner chooses the first identity-valid capture, preferring rendered .txt over saved HTML.",
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

    hard_failures = summary["parse_failed"] + summary["timeline_empty"] + summary["identity_failed"]
    return 2 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
