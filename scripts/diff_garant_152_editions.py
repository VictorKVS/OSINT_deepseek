from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.document_compiler import parse_legal_structure
from father_osint.garant_timeline import parse_garant_timeline_text
from father_osint.legal_core import (
    LegalCoreExtractionError,
    extract_152_fz_core_text,
    is_152_fz_primary_document,
)
from father_osint.odt_extract import OdtExtractionError, extract_odt_text


DOCUMENT_ID = "DOC-RU-FZ-152-2006"
SOURCE_URL = "https://base.garant.ru/12148567/"
ARCHIVE = REPO_ROOT / "data" / "knowledge_factory" / "garant_editions" / DOCUMENT_ID
REPORT_DIR = REPO_ROOT / "reports" / "pdn_timelines"
_MIN_ARTICLE_LOCATORS = 20
_MAX_ARTICLE_LOCATORS = 80


def _structure_fingerprint(core_text: str, core_sha: str) -> dict[str, str]:
    nodes, _ = parse_legal_structure(DOCUMENT_ID, core_sha[:24], core_text)
    article_nodes = [node for node in nodes if node.node_type == "ARTICLE"]
    selected = article_nodes or [node for node in nodes if node.node_type == "BODY"]
    return {node.locator: node.content_sha256 for node in selected}


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.is_dir():
        print(f"ARCHIVE_NOT_FOUND: {ARCHIVE}")
        return 2

    parse_failed = 0
    identity_failed = 0
    scope_failed = 0
    by_core_sha: dict[str, dict[str, object]] = {}
    exact_aliases: defaultdict[str, list[str]] = defaultdict(list)

    archived_paths = list(sorted(ARCHIVE.glob("*.odt")))
    for path in archived_paths:
        try:
            data = path.read_bytes()
            text = extract_odt_text(data)
        except (OSError, OdtExtractionError):
            parse_failed += 1
            continue
        if not is_152_fz_primary_document(text):
            identity_failed += 1
            continue

        try:
            core_text = extract_152_fz_core_text(text)
        except LegalCoreExtractionError:
            scope_failed += 1
            continue

        capture_sha = hashlib.sha256(data).hexdigest()
        full_text_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        core_sha = hashlib.sha256(core_text.encode("utf-8")).hexdigest()
        exact_aliases[core_sha].append(capture_sha)
        if core_sha in by_core_sha:
            continue

        capture = parse_garant_timeline_text(
            document_id=DOCUMENT_ID,
            source_url=SOURCE_URL,
            observed_on="LOCAL_ARCHIVE",
            text=core_text,
        )
        hints = [item.amendment_date for item in capture.amendment_date_hints]
        structure = _structure_fingerprint(core_text, core_sha)
        locator_count = len(structure)
        if not (_MIN_ARTICLE_LOCATORS <= locator_count <= _MAX_ARTICLE_LOCATORS):
            scope_failed += 1
            continue

        by_core_sha[core_sha] = {
            "core_text_sha256": core_sha,
            "full_extracted_text_sha256": full_text_sha,
            "representative_capture_sha256": capture_sha,
            "latest_amendment_hint": hints[-1] if hints else None,
            "amendment_hint_count": len(hints),
            "structure_locator_count": locator_count,
            "structure": structure,
        }

    editions = list(by_core_sha.values())
    for edition in editions:
        edition["exact_capture_count"] = len(exact_aliases[str(edition["core_text_sha256"])])

    editions.sort(
        key=lambda item: (
            str(item.get("latest_amendment_hint") or ""),
            int(item.get("amendment_hint_count") or 0),
            str(item["core_text_sha256"]),
        )
    )

    comparisons: list[dict[str, object]] = []
    for index in range(len(editions) - 1):
        left = editions[index]
        right = editions[index + 1]
        left_map = dict(left["structure"])
        right_map = dict(right["structure"])
        left_keys = set(left_map)
        right_keys = set(right_map)

        added = sorted(right_keys - left_keys)
        removed = sorted(left_keys - right_keys)
        common = sorted(left_keys & right_keys)
        modified = sorted(locator for locator in common if left_map[locator] != right_map[locator])
        unchanged = sorted(locator for locator in common if left_map[locator] == right_map[locator])
        same_hint = left.get("latest_amendment_hint") == right.get("latest_amendment_hint")

        comparisons.append({
            "record_type": "GARANT_EDITION_STRUCTURAL_DIFF",
            "document_id": DOCUMENT_ID,
            "sequence_index": index + 1,
            "from_core_text_sha256": left["core_text_sha256"],
            "to_core_text_sha256": right["core_text_sha256"],
            "from_capture_sha256": left["representative_capture_sha256"],
            "to_capture_sha256": right["representative_capture_sha256"],
            "from_latest_amendment_hint": left.get("latest_amendment_hint"),
            "to_latest_amendment_hint": right.get("latest_amendment_hint"),
            "from_structure_locator_count": left["structure_locator_count"],
            "to_structure_locator_count": right["structure_locator_count"],
            "ordering_basis": "A2_LATEST_AMENDMENT_HINT_ONLY",
            "ordering_confidence": "LOW" if same_hint else "MEDIUM",
            "added_locators": added,
            "removed_locators": removed,
            "modified_locators": modified,
            "unchanged_locator_count": len(unchanged),
            "added_count": len(added),
            "removed_count": len(removed),
            "modified_count": len(modified),
            "semantic_text_mirrored": False,
            "scope": "PRIMARY_152_FZ_CORE_ONLY",
            "evidence_state": "A2_WORKING_DIFF_ONLY",
        })

    summary = {
        "record_type": "GARANT_EDITION_DIFF_SUMMARY",
        "document_id": DOCUMENT_ID,
        "archived_odt": len(archived_paths),
        "unique_core_editions": len(editions),
        "unique_text_editions": len(editions),
        "comparisons": len(comparisons),
        "parse_failed": parse_failed,
        "identity_failed": identity_failed,
        "scope_failed": scope_failed,
        "semantic_text_mirrored": False,
        "scope_semantics": "only the primary 152-FZ body from exact header through article 25, before presidential signature, is compared",
        "ordering_semantics": "edition order is based on GARANT A2 latest-amendment navigation hints and is not an A0/A1 proven effective-date order",
    }

    jsonl = REPORT_DIR / "garant_152_edition_diffs.jsonl"
    with jsonl.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n")
        for comparison in comparisons:
            handle.write(json.dumps(comparison, ensure_ascii=False, sort_keys=True) + "\n")

    md = REPORT_DIR / "GARANT_152_EDITION_DIFFS.md"
    lines = [
        "# GARANT 152-FZ structural edition diffs",
        "",
        "Policy: **GARANT working copies navigate; A0/A1 sources prove legal effect.**",
        "",
        f"- unique core editions: {summary['unique_core_editions']}",
        f"- adjacent comparisons: {summary['comparisons']}",
        f"- parse failed: {summary['parse_failed']}",
        f"- identity failed: {summary['identity_failed']}",
        f"- scope failed: {summary['scope_failed']}",
        "- compared scope: **primary 152-FZ legal body only**",
        "- GARANT semantic text mirrored to Git: **no**",
        "",
        "| # | From latest hint | To latest hint | From locators | To locators | Added | Removed | Modified | Unchanged | Order confidence |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in comparisons:
        lines.append(
            f"| {item['sequence_index']} | {item.get('from_latest_amendment_hint') or '—'} | "
            f"{item.get('to_latest_amendment_hint') or '—'} | {item['from_structure_locator_count']} | "
            f"{item['to_structure_locator_count']} | {item['added_count']} | {item['removed_count']} | "
            f"{item['modified_count']} | {item['unchanged_locator_count']} | {item['ordering_confidence']} |"
        )
    lines += [
        "",
        "Only primary-law article locators and content hashes are compared; no GARANT legal text is exported.",
        "A structural diff is an A2 working result until the corresponding amendment act and effective rule are reconciled to A0/A1 evidence.",
        f"Sanity gate: accepted structure locator count must be between {_MIN_ARTICLE_LOCATORS} and {_MAX_ARTICLE_LOCATORS}.",
    ]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"summary": summary, "diff_jsonl": str(jsonl), "diff_md": str(md)}, ensure_ascii=False, indent=2))
    if scope_failed:
        print("SCOPE_GATE_FAILED: at least one archived capture could not be safely reduced to the primary 152-FZ body.")
        return 2
    if len(editions) < 2:
        print("NEED_MORE_SEMANTIC_EDITIONS: download a historical edition from GARANT Redaktsii and rerun inventory/diff.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
