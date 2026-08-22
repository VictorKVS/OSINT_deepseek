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
from father_osint.odt_extract import OdtExtractionError, extract_odt_text


DOCUMENT_ID = "DOC-RU-FZ-152-2006"
SOURCE_URL = "https://base.garant.ru/12148567/"
MARKERS = ("152-ФЗ", "О персональных данных")
ARCHIVE = REPO_ROOT / "data" / "knowledge_factory" / "garant_editions" / DOCUMENT_ID
REPORT_DIR = REPO_ROOT / "reports" / "pdn_timelines"


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _identity_ok(text: str) -> bool:
    normalized = _norm(text)
    return all(_norm(marker) in normalized for marker in MARKERS)


def _structure_fingerprint(text: str, text_sha: str) -> dict[str, str]:
    nodes, _ = parse_legal_structure(DOCUMENT_ID, text_sha[:24], text)
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
    by_text_sha: dict[str, dict[str, object]] = {}
    exact_aliases: defaultdict[str, list[str]] = defaultdict(list)

    for path in sorted(ARCHIVE.glob("*.odt")):
        try:
            data = path.read_bytes()
            text = extract_odt_text(data)
        except (OSError, OdtExtractionError):
            parse_failed += 1
            continue
        if not _identity_ok(text):
            identity_failed += 1
            continue

        capture_sha = hashlib.sha256(data).hexdigest()
        text_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        exact_aliases[text_sha].append(capture_sha)
        if text_sha in by_text_sha:
            continue

        capture = parse_garant_timeline_text(
            document_id=DOCUMENT_ID,
            source_url=SOURCE_URL,
            observed_on="LOCAL_ARCHIVE",
            text=text,
        )
        hints = [item.amendment_date for item in capture.amendment_date_hints]
        by_text_sha[text_sha] = {
            "text_sha256": text_sha,
            "representative_capture_sha256": capture_sha,
            "latest_amendment_hint": hints[-1] if hints else None,
            "amendment_hint_count": len(hints),
            "structure": _structure_fingerprint(text, text_sha),
        }

    editions = list(by_text_sha.values())
    for edition in editions:
        edition["exact_capture_count"] = len(exact_aliases[str(edition["text_sha256"])])

    editions.sort(
        key=lambda item: (
            str(item.get("latest_amendment_hint") or ""),
            int(item.get("amendment_hint_count") or 0),
            str(item["text_sha256"]),
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
            "from_text_sha256": left["text_sha256"],
            "to_text_sha256": right["text_sha256"],
            "from_capture_sha256": left["representative_capture_sha256"],
            "to_capture_sha256": right["representative_capture_sha256"],
            "from_latest_amendment_hint": left.get("latest_amendment_hint"),
            "to_latest_amendment_hint": right.get("latest_amendment_hint"),
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
            "evidence_state": "A2_WORKING_DIFF_ONLY",
        })

    summary = {
        "record_type": "GARANT_EDITION_DIFF_SUMMARY",
        "document_id": DOCUMENT_ID,
        "archived_odt": len(list(ARCHIVE.glob("*.odt"))),
        "unique_text_editions": len(editions),
        "comparisons": len(comparisons),
        "parse_failed": parse_failed,
        "identity_failed": identity_failed,
        "semantic_text_mirrored": False,
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
        f"- unique semantic editions: {summary['unique_text_editions']}",
        f"- adjacent comparisons: {summary['comparisons']}",
        f"- parse failed: {summary['parse_failed']}",
        f"- identity failed: {summary['identity_failed']}",
        "- GARANT semantic text mirrored to Git: **no**",
        "",
        "| # | From latest hint | To latest hint | Added | Removed | Modified | Unchanged | Order confidence |",
        "|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for item in comparisons:
        lines.append(
            f"| {item['sequence_index']} | {item.get('from_latest_amendment_hint') or '—'} | "
            f"{item.get('to_latest_amendment_hint') or '—'} | {item['added_count']} | {item['removed_count']} | "
            f"{item['modified_count']} | {item['unchanged_locator_count']} | {item['ordering_confidence']} |"
        )
    lines += [
        "",
        "Only article/body locators and content hashes are compared; no GARANT legal text is exported.",
        "A structural diff is an A2 working result until the corresponding amendment act and effective rule are reconciled to A0/A1 evidence.",
    ]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"summary": summary, "diff_jsonl": str(jsonl), "diff_md": str(md)}, ensure_ascii=False, indent=2))
    if len(editions) < 2:
        print("NEED_MORE_SEMANTIC_EDITIONS: download a historical edition from GARANT Redaktsii and rerun inventory/diff.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
