from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "reports" / "knowledge_intake" / "LATEST_MODEL_WORK_QUEUE.json"
REGISTRY = ROOT / "config" / "local_model_capability_registry.json"
OUT = ROOT / "reports" / "knowledge_intake" / "LATEST_LOCAL_MODEL_ASSIGNMENTS.json"

MODEL_SUFFIXES = {".gguf", ".bin", ".safetensors"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_roots(extra: str | None) -> list[Path]:
    roots: list[Path] = []
    raw = extra or os.environ.get("FATHER_MODEL_ROOTS") or ""
    for part in raw.split(os.pathsep):
        part = part.strip()
        if part:
            roots.append(Path(part).expanduser())
    home = Path.home()
    roots.extend([
        home / "models",
        home / ".cache" / "huggingface" / "hub",
        Path("G:/models"),
        Path("G:/1/models"),
        Path("G:/LLM"),
        Path("G:/1/LLM"),
        Path("G:/1/Models"),
    ])
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root).casefold()
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def index_model_files(roots: list[Path], max_files: int = 10000) -> list[Path]:
    """Walk each configured root once, not once per model."""
    found: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        if not root.exists() or not root.is_dir():
            continue
        try:
            for path in root.rglob("*"):
                if len(found) >= max_files:
                    return found
                if not path.is_file() or path.suffix.lower() not in MODEL_SUFFIXES:
                    continue
                key = str(path).casefold()
                if key in seen:
                    continue
                seen.add(key)
                found.append(path)
        except (OSError, PermissionError):
            continue
    return found


def match_model_files(indexed: list[Path], aliases: list[str], max_files: int = 20) -> list[str]:
    aliases_cf = [a.casefold().replace("_", "-") for a in aliases]
    matches: list[str] = []
    for path in indexed:
        name = path.name.casefold().replace("_", "-")
        if any(alias in name for alias in aliases_cf):
            matches.append(str(path))
            if len(matches) >= max_files:
                break
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-discover local model files and route intake work into semifinal model assignments.")
    parser.add_argument("--model-roots", default=None, help="Additional model roots separated by OS path separator.")
    args = parser.parse_args()

    if not QUEUE.is_file():
        print(json.dumps({"status": "WORK_QUEUE_MISSING", "queue": str(QUEUE)}, ensure_ascii=False, indent=2))
        return 2

    queue = load_json(QUEUE)
    registry = load_json(REGISTRY)
    roots = candidate_roots(args.model_roots)
    indexed_files = index_model_files(roots)

    models: list[dict[str, Any]] = []
    for row in registry.get("models", []) or []:
        if not isinstance(row, dict):
            continue
        aliases = [str(x) for x in row.get("aliases") or []]
        paths = match_model_files(indexed_files, aliases)
        logical_available = bool(paths)
        models.append({
            **row,
            "availability": "DISCOVERED_LOCAL_FILE" if logical_available else "NOT_DISCOVERED",
            "discovered_paths": paths,
        })

    by_capability: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for model in models:
        if model.get("availability") != "DISCOVERED_LOCAL_FILE":
            continue
        for capability in model.get("capabilities") or []:
            by_capability[str(capability)].append(model)
    for capability in by_capability:
        by_capability[capability].sort(key=lambda m: (float(m.get("quality_score") or 0.0), str(m.get("model_id"))), reverse=True)

    stage_map = registry.get("stage_capability_map") or {}
    assignments: list[dict[str, Any]] = []
    unassigned: Counter[str] = Counter()
    model_load: Counter[str] = Counter()

    for item in queue.get("items", []) or []:
        if not isinstance(item, dict):
            continue
        for stage in item.get("stages") or []:
            stage = str(stage)
            if stage == "M0_EVIDENCE_IDENTITY":
                assignments.append({
                    "work_item_id": item.get("work_item_id"),
                    "source_id": item.get("source_id"),
                    "stage_id": stage,
                    "execution": "DETERMINISTIC_ONLY",
                    "models": [],
                    "output_state": "SEMIFABRICATE_ONLY",
                })
                continue
            capabilities = [str(x) for x in stage_map.get(stage) or []]
            eligible: dict[str, dict[str, Any]] = {}
            for capability in capabilities:
                for model in by_capability.get(capability, []):
                    eligible[str(model.get("model_id"))] = model
            ranked = sorted(eligible.values(), key=lambda m: (float(m.get("quality_score") or 0.0), str(m.get("model_id"))), reverse=True)
            if not ranked:
                unassigned[stage] += 1
                assignments.append({
                    "work_item_id": item.get("work_item_id"),
                    "source_id": item.get("source_id"),
                    "stage_id": stage,
                    "execution": "HOLD_NO_DISCOVERED_MODEL",
                    "models": [],
                    "required_capabilities": capabilities,
                    "output_state": "SEMIFABRICATE_ONLY",
                })
                continue

            selected = ranked[:3]
            model_rows = []
            for index, model in enumerate(selected):
                model_id = str(model.get("model_id"))
                model_load[model_id] += 1
                model_rows.append({
                    "model_id": model_id,
                    "role": "CHAMPION" if index == 0 else "CHALLENGER",
                    "quality_score": model.get("quality_score"),
                    "model_path": (model.get("discovered_paths") or [None])[0],
                })
            assignments.append({
                "work_item_id": item.get("work_item_id"),
                "source_id": item.get("source_id"),
                "source_sha256": item.get("source_sha256"),
                "document_kind": item.get("document_kind"),
                "domains": item.get("domains") or [],
                "object_path": item.get("object_path"),
                "stage_id": stage,
                "execution": "LOCAL_MODEL_CHAMPION_CHALLENGER",
                "models": model_rows,
                "required_capabilities": capabilities,
                "output_contract": item.get("output_contract") or {},
                "output_state": "SEMIFABRICATE_ONLY",
                "promotion_gate": "MAIN_ANALYST_REVIEW_REQUIRED",
            })

    detected = [m for m in models if m.get("availability") == "DISCOVERED_LOCAL_FILE"]
    payload = {
        "schema_version": "father-osint.local-model-assignments.v0.2",
        "record_type": "LOCAL_MODEL_SEMIFABRICATE_ASSIGNMENT_PLAN",
        "status": "READY" if detected else "NO_LOCAL_MODELS_DISCOVERED",
        "model_roots_checked": [str(p) for p in roots],
        "indexed_model_files_total": len(indexed_files),
        "models_registered_total": len(models),
        "models_discovered_total": len(detected),
        "models_discovered": [
            {"model_id": m.get("model_id"), "paths": m.get("discovered_paths"), "capabilities": m.get("capabilities")}
            for m in detected
        ],
        "assignments_total": len(assignments),
        "unassigned_stage_counts": dict(sorted(unassigned.items())),
        "model_assignment_counts": dict(sorted(model_load.items())),
        "assignments": assignments,
        "stage_registry": "config/model_stage_registry.yaml",
        "prompt_registry": "config/model_prompt_registry.json",
        "kb_auto_promotion": False,
        "note": "All discovered models participate only where their declared capability matches. Outputs remain semifinished candidates for main analyst review.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "assignments"}, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Assignments: {OUT.relative_to(ROOT).as_posix()}")
    return 0 if detected else 2


if __name__ == "__main__":
    raise SystemExit(main())
