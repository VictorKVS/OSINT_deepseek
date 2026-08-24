from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from father_osint.architecture_book_analyst import ArchitectureBookAnalyst
from father_osint.models import Material, MaterialPackage


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def find_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    manifests = sorted(
        private_root.glob("*/translation_manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not manifests:
        raise FileNotFoundError("translation manifest not found")
    return manifests[0].parent


def classify_unit(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "EMPTY"
    if len(stripped) <= 140 and (
        stripped.isupper()
        or stripped.casefold().startswith(("глава ", "часть ", "chapter ", "part "))
    ):
        return "HEADING"
    return "PARAGRAPH"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze one fully translated private architecture book.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    args = parser.parse_args()

    try:
        workspace = find_workspace(Path(args.private_root), args.workspace)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    translation_manifest_path = workspace / "translation_manifest.json"
    translation_manifest = json.loads(translation_manifest_path.read_text(encoding="utf-8"))
    if translation_manifest.get("status") != "TRANSLATION_COMPLETE":
        print(
            f"ERROR: translation status is {translation_manifest.get('status')}; analysis blocked",
            file=sys.stderr,
        )
        return 3

    source_manifest = json.loads((workspace / "source_manifest.json").read_text(encoding="utf-8"))
    units = load_jsonl(Path(translation_manifest["units_path"]))

    materials: list[Material] = []
    current_heading: list[str] = []
    for unit in units:
        translated = str(unit.get("translated_text") or "").strip()
        if not translated:
            print(f"ERROR: untranslated unit {unit.get('unit_id')}", file=sys.stderr)
            return 4
        unit_type = classify_unit(translated)
        if unit_type == "HEADING":
            current_heading = [translated]
        materials.append(
            Material(
                source_type="book",
                source_locator=f"private-library://{source_manifest['item']['item_id']}#unit={unit['unit_id']}",
                title=f"{source_manifest['item']['normalized_title']} :: {unit['order']}",
                raw_text=translated,
                local_path=str(workspace / "translation_units.jsonl"),
                metadata={
                    "book_id": source_manifest["item"]["item_id"],
                    "translation_unit_id": unit["unit_id"],
                    "source_text_sha256": unit["source_text_sha256"],
                    "source_page_start": unit.get("source_page_start"),
                    "source_page_end": unit.get("source_page_end"),
                    "heading_path": list(current_heading),
                    "unit_type": unit_type,
                    "translation_method": unit.get("translation_method"),
                    "translation_model": unit.get("translation_model"),
                },
            )
        )

    package = MaterialPackage(
        task_id=f"book:{source_manifest['item']['item_id']}",
        materials=materials,
        notes="Private translated architecture book corpus.",
    )
    result = ArchitectureBookAnalyst().analyze(package)

    output_path = workspace / "architecture_knowledge_candidates.json"
    output_path.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_path = workspace / "architecture_knowledge_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "schema_version": result.schema_version,
                "task_id": result.task_id,
                "book_id": source_manifest["item"]["item_id"],
                "book_title": source_manifest["item"]["normalized_title"],
                "counters": result.counters,
                "review_status": "NEEDS_REVIEW",
                "candidate_file": str(output_path),
                "next_stage": "CROSS_SOURCE_REVIEW",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print("status=KNOWLEDGE_CANDIDATES_READY")
    print(f"book={source_manifest['item']['normalized_title']}")
    for key, value in sorted(result.counters.items()):
        print(f"{key}={value}")
    print(f"output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
