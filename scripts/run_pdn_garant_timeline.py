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
from father_osint.legal_core import (
    LegalCoreExtractionError,
    extract_152_fz_core_text,
    is_152_fz_primary_document,
)
from father_osint.legal_source_bundle import LegalSourceBundle
from father_osint.odt_extract import OdtExtractionError, extract_odt_text


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
    candidates: list[Path] = []
    for suffix in (".odt", ".txt", ".html", ".htm"):
        candidate = input_dir / f"{document_id}{suffix}"
        if candidate.is_file():
            candidates.append(candidate)
    return tuple(candidates)


def _mime_for(path: Path) -> str:
    if path.suffix.casefold() in {".html", ".htm"}:
        return "text/html"
    return "text/plain"


def _extract_candidate_text(path: Path, data: bytes) -> str:
    if path.suffix.casefold() == ".odt":
        return extract_odt_text(data)
    return extract_visible_text(data, _mime_for(path))


def _empty_basis_counts() -> dict[str, int]:
    return {key: 0 for key in _BASIS_KEYS}


def _normalized(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _missing_identity_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    normalized_text = _normalized(text)
    return [marker for marker in markers if _normalized(marker) not in normalized_text]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract only amendment/version metadata from operator-saved GARANT working copies"
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
                "expected_input": str(input_dir / f"{bundle.document_id}.odt"),
            })
            continue

        selected_path: Path | None = None
        source_bytes: bytes | None = None
        source_capture_sha256: str | None = None
        text: str | None = None
        selected_scope = "FULL_CAPTURE"
        candidate_diagnostics: list[dict[str, object]] = []
        extraction_failures = 0
        scope_failures = 0

        for candidate in source_paths:
            try:
                candidate_bytes = candidate.read_bytes()
                candidate_text = _extract_candidate_text(candidate, candidate_bytes)
            except (DocumentCompilerError, OdtExtractionError, ValueError) as exc:
                extraction_failures += 1
                candidate_diagnostics.append({
                    "file": candidate.name,
                    "status": "PARSE_FAILED",
                    "reason": str(exc),
                })
                continue

            if bundle.document_id == "DOC-RU-FZ-152-2006":
                if not is_152_fz_primary_document(candidate_text):
                    candidate_diagnostics.append({
                        "file": candidate.name,
                        "status": "IDENTITY_FAILED",
                        "reason": "capture contains no primary 152-FZ header/title pair near document start",
                    })
                    continue
                try:
                    candidate_text = extract_152_fz_core_text(candidate_text)
                except LegalCoreExtractionError as exc:
                    scope_failures += 1
                    candidate_diagnostics.append({
                        "file": candidate.name,
                        "status": "SCOPE_FAILED",
                        "reason": str(exc),
                    })
                    continue
                selected_scope = "PRIMARY_152_FZ_CORE_ONLY"

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
            if scope_failures:
                status = "SCOPE_FAILED"
            elif extraction_failures == len(source_paths):
                status = "PARSE_FAILED"
            else:
                status = "IDENTITY_FAILED"
            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": status,
                "source_id": provider.source_id,
                "source_url": provider.url,
                "candidate_files": [path.name for path in source_paths],
                "candidate_diagnostics": candidate_diagnostics,
                "reason": {
                    "IDENTITY_FAILED": "no local capture passed document identity markers",
                    "PARSE_FAILED": "no local capture could be parsed as visible text",
                    "SCOPE_FAILED": "no primary-document capture could be safely scoped for temporal parsing",
                }[status],
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

        local_path = local_root / f"{bundle.document_id}.timeline.json"
        local_payload = capture.to_dict()
        local_payload["source_capture_sha256"] = source_capture_sha256
        local_payload["source_capture_bytes"] = len(source_bytes)
        local_payload["selected_input"] = selected_path.name
        local_payload["selected_scope"] = selected_scope
        local_path.write_text(
            json.dumps(local_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        if not capture.events:
            if capture.amendment_date_hints:
                records.append({
                    "record_type": "TIMELINE_CAPTURE",
                    "document_id": bundle.document_id,
                    "status": "TIMELINE_HINTS_READY",
                    "source_id": provider.source_id,
                    "source_url": provider.url,
                    "selected_input": selected_path.name,
                    "selected_scope": selected_scope,
                    "source_capture_sha256": source_capture_sha256,
                    "source_capture_bytes": len(source_bytes),
                    "events": 0,
                    "amendment_date_hints": len(capture.amendment_date_hints),
                    "official_evidence_requests": 0,
                    "reason": "compact GARANT amendment-date list extracted; act identity/effective-rule evidence still pending",
                    "semantic_text_mirrored": False,
                })
                continue

            records.append({
                "record_type": "TIMELINE_CAPTURE",
                "document_id": bundle.document_id,
                "status": "TIMELINE_EMPTY",
                "source_id": provider.source_id,
                "source_url": provider.url,
                "selected_input": selected_path.name,
                "selected_scope": selected_scope,
                "source_capture_sha256": source_capture_sha256,
                "source_capture_bytes": len(source_bytes),
                "reason": "document identity passed but no amendment events or compact amendment-date hints were extracted",
                "semantic_text_mirrored": False,
            })
            continue

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
            "selected_scope": selected_scope,
            "source_capture_sha256": source_capture_sha256,
            "source_capture_bytes": len(source_bytes),
            "events": len(capture.events),
            "amendment_date_hints": len(capture.amendment_date_hints),
            "future_edition_signalled": capture.future_edition_signalled,
            "semantic_text_mirrored": False,
            "official_evidence_requests": len(requests),
            "effective_date_basis_counts": record_basis_counts,
        })

    summary = {
        "record_type": "TIMELINE_SUMMARY",
        "bundles": len(bundles),
        "timeline_metadata_ready": sum(item.get("status") == "TIMELINE_METADATA_READY" for item in records),
        "timeline_hints_ready": sum(item.get("status") == "TIMELINE_HINTS_READY" for item in records),
        "timeline_empty": sum(item.get("status") == "TIMELINE_EMPTY" for item in records),
        "identity_failed": sum(item.get("status") == "IDENTITY_FAILED" for item in records),
        "scope_failed": sum(item.get("status") == "SCOPE_FAILED" for item in records),
        "input_pending": sum(item.get("status") == "INPUT_PENDING" for item in records),
        "parse_failed": sum(item.get("status") == "PARSE_FAILED" for item in records),
        "amendment_date_hints": sum(int(item.get("amendment_date_hints", 0)) for item in records),
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
        f"- timeline hints ready: {summary['timeline_hints_ready']}",
        f"- timeline empty: {summary['timeline_empty']}",
        f"- identity failed: {summary['identity_failed']}",
        f"- scope failed: {summary['scope_failed']}",
        f"- input pending: {summary['input_pending']}",
        f"- parse failed: {summary['parse_failed']}",
        f"- compact amendment-date hints: {summary['amendment_date_hints']}",
        f"- official evidence requests: {summary['official_evidence_requests']}",
        f"- explicit calendar-date rules: {basis_counts['EXPLICIT_CALENDAR_DATE']}",
        f"- publication-relative rules: {basis_counts['RELATIVE_TO_OFFICIAL_PUBLICATION']}",
        f"- other non-calendar rules: {basis_counts['NON_CALENDAR_RULE']}",
        "- semantic/full legal text mirrored from GARANT: **no**",
        "",
        "## Documents",
        "",
        "| Document | Status | Scope | Timeline source | Events | Date hints | Evidence requests |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for record in records:
        lines.append(
            f"| `{record['document_id']}` | {record['status']} | {record.get('selected_scope', '—')} | "
            f"{record.get('source_id', '—')} | {record.get('events', '—')} | "
            f"{record.get('amendment_date_hints', '—')} | {record.get('official_evidence_requests', '—')} |"
        )
    lines += [
        "",
        "Every detailed amendment event stays `OFFICIAL_EVIDENCE_PENDING` until an A0/A1 publication/effectiveness anchor is attached.",
        "A compact `С изменениями и дополнениями от:` list is stored only as `A2_NAVIGATION_HINT_ONLY`; dates alone do not identify an amending act.",
        "152-FZ captures are temporally parsed only inside the primary law body, excluding surrounding GARANT material.",
        "Publication-relative rules explicitly request an A0/A1 official-publication date; no calendar date is inferred from GARANT alone.",
        "Every timeline capture must pass document identity markers before amendment parsing.",
        "Multiple local capture formats may coexist; the runner chooses the first identity-valid capture, preferring GARANT-downloaded ODT, then rendered .txt, then saved HTML.",
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

    hard_failures = (
        summary["parse_failed"]
        + summary["timeline_empty"]
        + summary["identity_failed"]
        + summary["scope_failed"]
    )
    return 2 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
