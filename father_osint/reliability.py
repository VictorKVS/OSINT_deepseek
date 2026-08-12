from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .models import Material


@dataclass(frozen=True, slots=True)
class SourceCheckpoint:
    source_type: str
    source_key: str
    cursor: str


class CheckpointStore(Protocol):
    def load(self, source_type: str, source_key: str) -> SourceCheckpoint | None: ...

    def commit(self, checkpoint: SourceCheckpoint) -> None: ...


class JsonCheckpointStore:
    """Small atomic local checkpoint store for DEV/M5 reliability proofs."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _key(source_type: str, source_key: str) -> str:
        return f"{source_type}:{source_key}"

    def _read_all(self) -> dict[str, dict[str, str]]:
        if not self.path.exists():
            return {}
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError("checkpoint file must contain a JSON object")
        return data

    def load(self, source_type: str, source_key: str) -> SourceCheckpoint | None:
        raw = self._read_all().get(self._key(source_type, source_key))
        if raw is None:
            return None
        return SourceCheckpoint(
            source_type=source_type,
            source_key=source_key,
            cursor=str(raw["cursor"]),
        )

    def commit(self, checkpoint: SourceCheckpoint) -> None:
        data = self._read_all()
        data[self._key(checkpoint.source_type, checkpoint.source_key)] = {
            "cursor": checkpoint.cursor,
        }

        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.flush()
        tmp.replace(self.path)


class MaterialPersister(Protocol):
    def save_material(self, material: Material) -> bool: ...


class DurableObservationWriter:
    """Enforce save-before-checkpoint for one source observation.

    The cursor is committed only after the Material observation has been durably
    accepted by the material store. Any persistence exception propagates and the
    checkpoint remains unchanged.
    """

    def __init__(self, material_store: MaterialPersister, checkpoint_store: CheckpointStore) -> None:
        self.material_store = material_store
        self.checkpoint_store = checkpoint_store

    def save_then_checkpoint(
        self,
        *,
        material: Material,
        source_key: str,
        cursor: str,
    ) -> bool:
        payload_reused = self.material_store.save_material(material)
        self.checkpoint_store.commit(
            SourceCheckpoint(
                source_type=material.source_type,
                source_key=source_key,
                cursor=str(cursor),
            )
        )
        return payload_reused
