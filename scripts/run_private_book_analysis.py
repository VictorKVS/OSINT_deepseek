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
        private_root.glob("*/structure_manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not manifests:
        raise FileNotFoundError("structure manifest not found; translate and run book_structure.py first")
    return manifests[0].parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze one structured translated private architecture book.")
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

    structure_manifest_path = workspace / "structure_manifest.json"
    if not structure_manifest_path.is_file():
        print("ERROR: structure_manifest.json missing; run OTUS tools/book_structure.py", file=sys.stderr)
        return 4
    structure_manifest = json.loads(structure_manifest_path.read_text(encoding="utf-8"))
    if structure_manifest.get("status") != "SEMANTIC_STRUCTURE_READY":
        print(
            f"ERROR: structure status is {structure_manifest.get('status')}; analysis blocked",
            file=sys.stderr,
        )
        return 5

    semantic_units_path = Path(structure_manifest["semantic_units_path"])
    semantic_units = load_jsonl(semantic_units_path)
    if not semantic_units:
        print("ERROR: semantic_units.jsonl is empty", file=sys.stderr)
        return 6

    source_manifest = json.loads((workspace / "source_manifest.json").read_text(encoding="utf-8"))
    item = source_manifest["item"]

    materials: list[Material] = []
    for unit in semantic_units:
        translated = str(unit.get("translated_text") or "").strip()
        if not translated:
            continue
        materials.append(
            Material(
                source_type="book",
                source_locator=(
                    f"private-library://{item['item_id']}"
                    f"#page={unit.get('source_page_start')}"
                    f"&semantic={unit.get('semantic_id')}"
                ),
                title=f"{item['normalized_title']} :: semantic {unit.get('order')}",
                raw_text=translated,
                local_path=str(semantic_units_path),
                metadata={
                    "book_id": item["item_id"],
                    "semantic_id": unit.get("semantic_id"),
                    "translation_unit_id": unit.get("source_unit_id"),
                    "source_text_sha256": unit.get("source_text_sha256"),
                    "source_page_start": unit.get("source_page_start"),
                    "source_page_end": unit.get("source_page_end"),
                    "source_char_start": unit.get("source_char_start"),
                    "source_char_end": unit.get("source_char_end"),
                    "heading_path": unit.get("heading_path") or [],
                    "unit_type": unit.get("unit_type") or "PARAGRAPH",
                    "translation_method": unit.get("translation_method"),
                    "translation_model": unit.get("translation_model"),
                    "semantic_review_status": unit.get("review_status") or "NEEDS_REVIEW",
                    "provenance_level": "TRANSLATED_SEMANTIC_BLOCK_TO_EXACT_SOURCE_PAGE_UNIT",
                },
            )
        )

    package = MaterialPackage(
        task_id=f"book:{item['item_id']}",
        materials=materials,
        notes="Private translated and semantically structured architecture book corpus.",
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
                "book_id": item["item_id"],
                "book_title": item["normalized_title"],
                "source_semantic_units": len(semantic_units),
                "materials_analyzed": len(materials),
                "counters": result.counters,
                "review_status": "NEEDS_REVIEW",
                "candidate_file": str(output_path),
                "structure_manifest": str(structure_manifest_path),
                "next_stage": "CROSS_SOURCE_REVIEW",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print("status=KNOWLEDGE_CANDIDATES_READY")
    print(f"book={item['normalized_title']}")
    print(f"semantic_units={len(semantic_units)}")
    print(f"materials_analyzed={len(materials)}")
    for key, value in sorted(result.counters.items()):
        print(f"{key}={value}")
    print(f"output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
