from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.odt_extract import OdtExtractionError, extract_odt_text


DOCUMENT_ID = "DOC-RU-FZ-152-2006"
TARGET_NAME = f"{DOCUMENT_ID}.odt"
MARKERS = ("152-ФЗ", "О персональных данных")


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _identity_ok(text: str) -> bool:
    normalized = _norm(text)
    return all(_norm(marker) in normalized for marker in MARKERS)


def main() -> int:
    downloads = Path.home() / "Downloads"
    target_dir = REPO_ROOT / "data" / "operator_import" / "garant_timeline"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / TARGET_NAME

    candidates = sorted(
        (path for path in downloads.glob("*.odt") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        print(f"NO_ODT_FOUND: {downloads}")
        return 2

    diagnostics: list[str] = []
    for candidate in candidates[:20]:
        try:
            data = candidate.read_bytes()
            text = extract_odt_text(data)
        except (OSError, OdtExtractionError) as exc:
            diagnostics.append(f"{candidate.name}: parse_failed={exc}")
            continue
        if not _identity_ok(text):
            diagnostics.append(f"{candidate.name}: identity_failed")
            continue

        shutil.copyfile(candidate, target)
        copied = target.read_bytes()
        sha256 = hashlib.sha256(copied).hexdigest()
        print("GARANT_ODT_IMPORTED")
        print(f"source={candidate}")
        print(f"target={target}")
        print(f"bytes={len(copied)}")
        print(f"sha256={sha256}")
        print("identity_markers=PASS")
        return 0

    print("NO_IDENTITY_VALID_ODT_FOUND")
    for item in diagnostics:
        print(item)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
