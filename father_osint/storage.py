from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import Material, MaterialPackage, ResearchTask


class MaterialStore:
    """Simple append-only DEV store.

    Material records represent source observations and are always preserved.
    Raw text payloads are stored separately as SHA-256-addressed UTF-8 blobs, so
    identical payload bytes may be reused without collapsing provenance.
    """

    def __init__(self, root: str | Path = "data/osint") -> None:
        self.root = Path(root)
        self.raw_dir = self.root / "raw"
        self.tasks_file = self.root / "tasks.jsonl"
        self.materials_file = self.root / "materials.jsonl"
        self.packages_file = self.root / "packages.jsonl"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def _append_jsonl(path: Path, payload: dict) -> None:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def save_task(self, task: ResearchTask) -> None:
        self._append_jsonl(self.tasks_file, task.to_dict())

    def save_material(self, material: Material) -> bool:
        """Persist one source observation.

        Equal payload hashes do not make two source observations identical.
        Raw payload bytes may be reused, while each Material record remains in
        materials.jsonl for provenance. Exact observation-level deduplication is
        intentionally not defined in DEV v1.
        """
        if material.raw_text is not None:
            material.content_hash = material.content_hash or self.hash_text(material.raw_text)
            raw_path = self.raw_dir / f"{material.content_hash}.txt"
            if not raw_path.exists():
                raw_path.write_text(material.raw_text, encoding="utf-8")
            material.local_path = str(raw_path)

        self._append_jsonl(self.materials_file, material.to_dict())
        return True

    def save_package(self, package: MaterialPackage) -> None:
        self._append_jsonl(self.packages_file, package.to_dict())

    def iter_materials(self) -> Iterable[dict]:
        if not self.materials_file.exists():
            return []
        with self.materials_file.open("r", encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
