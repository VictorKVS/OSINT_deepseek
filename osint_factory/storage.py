from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class CaseStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def case_dir(self, case_id: str) -> Path:
        path = self.root / "cases" / case_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_json(self, case_id: str, relative_path: str, payload: dict[str, Any]) -> Path:
        target = self.case_dir(case_id) / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, target)
        return target
