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
    def hash_file(path: str | Path) -> str:
        digest = hashlib.sha256()
        with Path(path).open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _append_jsonl(path: Path, payload: dict) -> None:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def save_task(self, task: ResearchTask) -> None:
        self._append_jsonl(self.tasks_file, task.to_dict())

    def save_material(self, material: Material) -> bool:
        """Persist one source observation and report raw-payload reuse.

        Returns True only when an equal raw-text payload already existed in the
        content-addressed raw store and its bytes were reused. The Material
        observation itself is still appended and is never skipped for that reason.

        File-only observations are hashed from the original file bytes. DEV v1
        preserves the original path rather than silently copying/normalizing files.
        """
        payload_reused = False

        if material.raw_text is not None:
            material.content_hash = self.hash_text(material.raw_text)
            raw_path = self.raw_dir / f"{material.content_hash}.txt"
            payload_reused = raw_path.exists()
            if not payload_reused:
                raw_path.write_text(material.raw_text, encoding="utf-8")
            material.local_path = str(raw_path)
        elif material.local_path is not None:
            source_path = Path(material.local_path)
            if not source_path.is_file():
                raise FileNotFoundError(f"Material local_path not found: {source_path}")
            material.content_hash = self.hash_file(source_path)

        self._append_jsonl(self.materials_file, material.to_dict())
        return payload_reused

    def save_package(self, package: MaterialPackage) -> None:
        self._append_jsonl(self.packages_file, package.to_dict())

    def iter_materials(self) -> Iterable[dict]:
        if not self.materials_file.exists():
            return []
        with self.materials_file.open("r", encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
