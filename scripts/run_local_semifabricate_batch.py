from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import intake_downloads_knowledge_factory as intake  # noqa: E402

ASSIGNMENTS = ROOT / "reports" / "knowledge_intake" / "LATEST_LOCAL_MODEL_ASSIGNMENTS.json"
PROMPTS = ROOT / "config" / "model_prompt_registry.json"
OUT_ROOT = ROOT / "_LOCAL_DOWNLOADS_KB_INTAKE" / "semifabricates"
REPORT = ROOT / "reports" / "knowledge_intake" / "LATEST_LOCAL_SEMIFABRICATE_BATCH.json"
MAIN_QUEUE = ROOT / "reports" / "knowledge_intake" / "LATEST_MAIN_ANALYST_SEMIFABRICATE_QUEUE.json"
DEFAULT_STAGES = {"M5_TERMINOLOGY", "M6_KNOWLEDGE_EXTRACTION"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_llama_cli() -> str | None:
    env = os.environ.get("FATHER_LLAMA_CLI")
    if env and Path(env).is_file():
        return str(Path(env))
    for name in ("llama-cli", "llama-cli.exe", "main", "main.exe", "llama", "llama.exe"):
        found = shutil.which(name)
        if found:
            return found
    candidates = [
        Path("G:/llama.cpp/build/bin/Release/llama-cli.exe"),
        Path("G:/1/llama.cpp/build/bin/Release/llama-cli.exe"),
        Path("G:/llama.cpp/llama-cli.exe"),
        Path("G:/1/llama.cpp/llama-cli.exe"),
    ]
    for path in candidates:
        if path.is_file():
            return str(path)
    return None


def evidence_spans(text: str, span_chars: int = 1800, max_chars: int = 12000) -> list[dict[str, str]]:
    text = text[:max_chars]
    spans: list[dict[str, str]] = []
    start = 0
    index = 1
    while start < len(text):
        chunk = text[start : start + span_chars].strip()
        if chunk:
            spans.append({"span_id": f"SPAN-{index:04d}", "text": chunk})
            index += 1
        start += span_chars
    return spans


def prompt_key(stage_id: str) -> str:
    return stage_id


def expected_shape(stage_id: str) -> dict[str, Any]:
    if stage_id == "M5_TERMINOLOGY":
        return {
            "term_candidates": [
                {
                    "term": "string",
                    "candidate_type": "TERM_CANDIDATE|DEFINITION_CANDIDATE|ALIAS_CANDIDATE|ABBREVIATION_CANDIDATE",
                    "definition": "string_or_null",
                    "aliases": ["string"],
                    "evidence_span_ids": ["SPAN-0001"],
                    "confidence": "LOW|MEDIUM|HIGH",
                }
            ]
        }
    return {
        "knowledge_candidates": [
            {
                "candidate_type": "CLAIM_CANDIDATE|REQUIREMENT_CANDIDATE|PRINCIPLE_CANDIDATE|PATTERN_CANDIDATE|TRADEOFF_CANDIDATE|DECISION_CRITERION_CANDIDATE|FAILURE_MODE_CANDIDATE|APPLICABILITY_CANDIDATE|EXAMPLE_CANDIDATE|DEFINITION_CANDIDATE",
                "statement": "string",
                "conditions": ["string"],
                "exceptions": ["string"],
                "scope": "string_or_null",
                "evidence_span_ids": ["SPAN-0001"],
                "confidence": "LOW|MEDIUM|HIGH",
                "review_status": "MAIN_ANALYST_REVIEW_REQUIRED",
            }
        ]
    }


def build_prompt(stage: dict[str, Any], packet: dict[str, Any], stage_id: str) -> str:
    schema = expected_shape(stage_id)
    return (
        stage.get("system_prompt", "")
        + "\n\nSTRICT OUTPUT RULES:\n"
        + "Return exactly one valid JSON object and no markdown. Every material item must cite one or more supplied span_id values. "
        + "If evidence is insufficient, return an empty candidate list. Do not invent sources, hashes, definitions, requirements or relations.\n\n"
        + "EXPECTED JSON SHAPE:\n"
        + json.dumps(schema, ensure_ascii=False, indent=2)
        + "\n\nEVIDENCE PACKET:\n"
        + json.dumps(packet, ensure_ascii=False, indent=2)
    )


def extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else None
    except Exception:
        pass
    starts = [m.start() for m in re.finditer(r"\{", text)]
    for start in starts:
        depth = 0
        in_string = False
        escape = False
        for index in range(start, len(text)):
            ch = text[index]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : index + 1]
                    try:
                        value = json.loads(candidate)
                        if isinstance(value, dict):
                            return value
                    except Exception:
                        break
    return None


def run_model(*, cli: str, model_path: str, prompt: str, timeout: int) -> tuple[int, str, str, float]:
    started = time.perf_counter()
    command = [
        cli,
        "-m", model_path,
        "-p", prompt,
        "-n", "2048",
        "-c", "4096",
        "--temp", "0.1",
    ]
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr, time.perf_counter() - started


def candidate_count(stage_id: str, payload: dict[str, Any] | None) -> int:
    if not payload:
        return 0
    key = "term_candidates" if stage_id == "M5_TERMINOLOGY" else "knowledge_candidates"
    value = payload.get(key) or []
    return len(value) if isinstance(value, list) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute a small local M5/M6 semifinal extraction batch using discovered llama.cpp models.")
    parser.add_argument("--max-items", type=int, default=2)
    parser.add_argument("--models-per-stage", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    if not ASSIGNMENTS.is_file():
        print(json.dumps({"status": "ASSIGNMENTS_MISSING", "path": str(ASSIGNMENTS)}, ensure_ascii=False, indent=2))
        return 2
    cli = find_llama_cli()
    if not cli:
        print(json.dumps({"status": "LLAMA_CLI_NOT_FOUND", "hint": "Set FATHER_LLAMA_CLI or install llama-cli in PATH."}, ensure_ascii=False, indent=2))
        return 2

    plan = load_json(ASSIGNMENTS)
    prompts = load_json(PROMPTS)
    stage_defs = prompts.get("stages") or {}

    chosen_work_items: list[str] = []
    for row in plan.get("assignments", []) or []:
        wid = str(row.get("work_item_id") or "")
        if wid and wid not in chosen_work_items and str(row.get("stage_id")) in DEFAULT_STAGES and row.get("execution") == "LOCAL_MODEL_CHAMPION_CHALLENGER":
            chosen_work_items.append(wid)
        if len(chosen_work_items) >= max(0, args.max_items):
            break
    selected_ids = set(chosen_work_items)

    runs: list[dict[str, Any]] = []
    analyst_queue: list[dict[str, Any]] = []
    for assignment in plan.get("assignments", []) or []:
        if not isinstance(assignment, dict):
            continue
        wid = str(assignment.get("work_item_id") or "")
        stage_id = str(assignment.get("stage_id") or "")
        if wid not in selected_ids or stage_id not in DEFAULT_STAGES:
            continue
        if assignment.get("execution") != "LOCAL_MODEL_CHAMPION_CHALLENGER":
            continue

        object_path = ROOT / str(assignment.get("object_path") or "")
        if not object_path.is_file():
            runs.append({"work_item_id": wid, "stage_id": stage_id, "status": "OBJECT_MISSING", "object_path": str(object_path)})
            continue
        text = intake.sample_text(object_path, limit=14000)
        spans = evidence_spans(text)
        if not spans:
            runs.append({"work_item_id": wid, "stage_id": stage_id, "status": "NO_TEXT_EVIDENCE"})
            continue

        stage = stage_defs.get(prompt_key(stage_id)) or {}
        packet = {
            "work_item_id": wid,
            "source_id": assignment.get("source_id"),
            "source_sha256": assignment.get("source_sha256"),
            "document_kind": assignment.get("document_kind"),
            "domains": assignment.get("domains") or [],
            "evidence_spans": spans,
        }
        full_prompt = build_prompt(stage, packet, stage_id)

        for model in (assignment.get("models") or [])[: max(1, args.models_per_stage)]:
            model_id = str(model.get("model_id") or "")
            model_path = str(model.get("model_path") or "")
            if not model_path or not Path(model_path).is_file():
                runs.append({"work_item_id": wid, "stage_id": stage_id, "model_id": model_id, "status": "MODEL_PATH_MISSING"})
                continue
            out_path = OUT_ROOT / wid / stage_id / f"{model_id}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if out_path.is_file():
                try:
                    prior = load_json(out_path)
                    if prior.get("status") == "SEMIFABRICATE_READY" and prior.get("source_sha256") == assignment.get("source_sha256"):
                        runs.append({"work_item_id": wid, "stage_id": stage_id, "model_id": model_id, "status": "REUSED_SEMIFABRICATE", "output": out_path.relative_to(ROOT).as_posix()})
                        analyst_queue.append(prior)
                        continue
                except Exception:
                    pass
            try:
                rc, stdout, stderr, elapsed = run_model(cli=cli, model_path=model_path, prompt=full_prompt, timeout=args.timeout_seconds)
            except subprocess.TimeoutExpired:
                runs.append({"work_item_id": wid, "stage_id": stage_id, "model_id": model_id, "status": "TIMEOUT"})
                continue
            parsed = extract_json(stdout)
            status = "SEMIFABRICATE_READY" if rc == 0 and parsed is not None else "MODEL_OUTPUT_REVIEW_REQUIRED"
            record = {
                "schema_version": "father-osint.model-semifabricate.v0.1",
                "record_type": "MODEL_SEMIFABRICATE",
                "status": status,
                "work_item_id": wid,
                "stage_id": stage_id,
                "model_id": model_id,
                "model_role": model.get("role"),
                "model_path": model_path,
                "source_id": assignment.get("source_id"),
                "source_sha256": assignment.get("source_sha256"),
                "document_kind": assignment.get("document_kind"),
                "domains": assignment.get("domains") or [],
                "evidence_span_ids": [span["span_id"] for span in spans],
                "parsed_output": parsed,
                "candidate_count": candidate_count(stage_id, parsed),
                "returncode": rc,
                "elapsed_seconds": elapsed,
                "stderr_tail": stderr[-2000:],
                "raw_output_tail": stdout[-6000:] if parsed is None else None,
                "review_status": "MAIN_ANALYST_REVIEW_REQUIRED",
                "kb_auto_promotion": False,
            }
            out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            runs.append({"work_item_id": wid, "stage_id": stage_id, "model_id": model_id, "status": status, "candidate_count": record["candidate_count"], "elapsed_seconds": elapsed, "output": out_path.relative_to(ROOT).as_posix()})
            if status == "SEMIFABRICATE_READY":
                analyst_queue.append(record)

    counters = Counter(str(row.get("status") or "UNKNOWN") for row in runs)
    payload = {
        "schema_version": "father-osint.local-semifabricate-batch.v0.1",
        "record_type": "LOCAL_SEMIFABRICATE_BATCH_RUN",
        "status": "PASS" if analyst_queue else "PASS_WITH_GAPS" if runs else "NO_WORK",
        "llama_cli": cli,
        "work_items_selected_total": len(selected_ids),
        "runs_total": len(runs),
        "status_counts": dict(sorted(counters.items())),
        "semifabricates_ready_total": len(analyst_queue),
        "candidate_objects_total": sum(int(row.get("candidate_count") or 0) for row in analyst_queue),
        "main_analyst_queue": MAIN_QUEUE.relative_to(ROOT).as_posix(),
        "kb_auto_promotion": False,
        "runs": runs,
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MAIN_QUEUE.write_text(json.dumps({
        "schema_version": "father-osint.main-analyst-semifabricate-queue.v0.1",
        "record_type": "MAIN_ANALYST_SEMIFABRICATE_QUEUE",
        "state": "MAIN_ANALYST_REVIEW_REQUIRED",
        "items_total": len(analyst_queue),
        "items": analyst_queue,
        "kb_auto_promotion": False,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "runs"}, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Main analyst queue: {MAIN_QUEUE.relative_to(ROOT).as_posix()}")
    print(f"Report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if analyst_queue else 2


if __name__ == "__main__":
    raise SystemExit(main())
