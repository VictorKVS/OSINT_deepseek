from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import Material, MaterialPackage, ResearchTask


class MaterialStore:
    """Simple append-only store for the MVP.

    Metadata is stored as JSONL. Raw text payloads are persisted as UTF-8 files
    addressed by SHA-256 so obvious duplicates can be skipped cheaply.
    """

    def __init__(self, root: str | Path = "data/osint") -> None:
        self.root = Path(root)
        self.raw_dir = self.root / "raw"
        self.tasks_file = self.root / "tasks.jsonl"
        self.materials_file = self.root / "materials.jsonl"
        self.packages_file = self.root / "packages.jsonl"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.root.mkdir(parents=True, exist_ok=True)
        self._known_hashes = self._load_known_hashes()

    @staticmethod
    def hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _load_known_hashes(self) -> set[str]:
        hashes: set[str] = set()
        if not self.materials_file.exists():
            return hashes
        with self.materials_file.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    value = json.loads(line).get("content_hash")
                except json.JSONDecodeError:
                    continue
                if value:
                    hashes.add(value)
        return hashes

    @staticmethod
    def _append_jsonl(path: Path, payload: dict) -> None:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def save_task(self, task: ResearchTask) -> None:
        self._append_jsonl(self.tasks_file, task.to_dict())

    def save_material(self, material: Material) -> bool:
        """Persist a material. Return False when an obvious duplicate is skipped."""
        if material.raw_text is not None:
            material.content_hash = material.content_hash or self.hash_text(material.raw_text)
            if material.content_hash in self._known_hashes:
                return False
            raw_path = self.raw_dir / f"{material.content_hash}.txt"
            if not raw_path.exists():
                raw_path.write_text(material.raw_text, encoding="utf-8")
            material.local_path = str(raw_path)

        if material.content_hash and material.content_hash in self._known_hashes:
            return False

        self._append_jsonl(self.materials_file, material.to_dict())
        if material.content_hash:
            self._known_hashes.add(material.content_hash)
        return True

    def save_package(self, package: MaterialPackage) -> None:
        self._append_jsonl(self.packages_file, package.to_dict())

    def iter_materials(self) -> Iterable[dict]:
        if not self.materials_file.exists():
            return []
        with self.materials_file.open("r", encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
