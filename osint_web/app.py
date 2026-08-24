from __future__ import annotations

import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
REPORTS = ROOT / "reports"
JOBS_PATH = REPORTS / "osint_control_center" / "jobs.json"
TRACE_PATH = REPORTS / "osint_control_center" / "trace_events.jsonl"
DOWNLOAD_PROGRESS_ROOT = REPORTS / "osint_control_center" / "downloads"
DOWNLOAD_RECEIPT_ROOT = REPORTS / "osint_control_center" / "download_receipts"
LIBRARY_ORDER_ROOT = REPORTS / "library_orders"
ROLE_REGISTRY = ROOT / "config" / "team_role_material_registry.json"
RU_BASELINE = ROOT / "config" / "role_ru_regulatory_baseline.json"
SAFE_ROLE = re.compile(r"^[A-Z0-9_]{2,64}$")
SAFE_TARGET = re.compile(r"^[A-Z0-9_]+-TOPIC-\d{2}$")
SAFE_CHAT = re.compile(r"^-?\d{1,24}$")
SAFE_USERNAME = re.compile(r"^[A-Za-z0-9_]{3,64}$")
TRACE_LOCK = threading.Lock()

ALLOWED_ACTIONS = {
    "PROGRAMMER_BIBLIOGRAPHY_PROBE": [str(ROOT / "RUN_PROGRAMMER_BIBLIOGRAPHY_PROBE.cmd")],
    "PROGRAMMER_BIBLIOGRAPHY_PLAN": [str(ROOT / "RUN_PROGRAMMER_BIBLIOGRAPHY_NEXT.cmd")],
    "REMAINING_P0_WINDOWS": [str(ROOT / "RUN_REMAINING_P0_SEARCH_WINDOWS.cmd")],
}
TELEGRAM_JOB_KINDS = {
    "TELEGRAM_QUERY_PROBE",
    "TELEGRAM_DOWNLOAD",
    "ROLE_ACQUISITION",
    "PROGRAMMER_BIBLIOGRAPHY_PROBE",
    "LIBRARY_ORDER_START",
}


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_trace(event: dict) -> None:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRACE_LOCK:
        with TRACE_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def load_traces(limit: int = 200) -> list[dict]:
    if not TRACE_PATH.exists():
        return []
    rows: list[dict] = []
    try:
        for line in TRACE_PATH.read_text(encoding="utf-8").splitlines()[-limit:]:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)
    except OSError:
        return []
    return rows


def load_jobs() -> list[dict]:
    payload = read_json(JOBS_PATH, {"jobs": []}) or {"jobs": []}
    return list(payload.get("jobs", []))[-100:]


def add_job(job: dict) -> None:
    jobs = load_jobs()
    jobs.append(job)
    write_json(JOBS_PATH, {"jobs": jobs[-100:]})


def update_job(job_id: str, **changes) -> None:
    jobs = load_jobs()
    for job in jobs:
        if job.get("id") == job_id:
            job.update(changes)
            break
    write_json(JOBS_PATH, {"jobs": jobs[-100:]})


def trace_event(job: dict, *, status: str, state_before: str, state_after: str, **extra) -> dict:
    event = {
        "trace_id": job["trace_id"],
        "correlation_id": job["correlation_id"],
        "project_id": job["project_id"],
        "task_id": job["task_id"],
        "command_id": job["command_id"],
        "parent_command_id": job.get("parent_command_id"),
        "actor_role": job.get("actor_role", "OSINT_UI"),
        "initiator": job.get("initiator", "OSINT_UI"),
        "executor": job.get("executor", job.get("kind")),
        "trigger": job.get("trigger", "USER_ACTION"),
        "command_name": job.get("kind"),
        "input_refs": job.get("input_refs", []),
        "state_before": state_before,
        "started_at": job.get("started_at_epoch"),
        "finished_at": job.get("finished_at_epoch"),
        "status": status,
        "output_refs": job.get("output_refs", []),
        "state_after": state_after,
        "evidence_refs": job.get("evidence_refs", []),
        "error_ref": job.get("error"),
        "retry_of": job.get("retry_of"),
        "rework_reason": job.get("rework_reason"),
        "human_approval_ref": job.get("human_approval_ref"),
        "next_command_ids": job.get("next_command_ids", []),
        "event_at_epoch": time.time(),
        **extra,
    }
    append_trace(event)
    return event


def registry_payload() -> dict:
    return read_json(ROLE_REGISTRY, {}) or {}


def ru_baseline_payload() -> dict:
    return read_json(RU_BASELINE, {}) or {}


def role_ids() -> set[str]:
    return {str(row.get("role_id", "")).upper() for row in registry_payload().get("roles", [])}


def role_catalog() -> list[dict]:
    baseline_roles = ru_baseline_payload().get("roles") or {}
    rows: list[dict] = []
    for role in registry_payload().get("roles", []):
        role_id = str(role.get("role_id", "")).upper()
        if not role_id or role_id == "ARCHITECT":
            continue
        topics = []
        for index, topic in enumerate(role.get("topics", []), start=1):
            target_id = f"{role_id}-TOPIC-{index:02d}"
            topics.append({
                "target_id": target_id,
                "label": str(topic),
                "destination": f"data/team_role_telegram/{role_id.casefold()}/{target_id.casefold()}",
            })
        ru_role = baseline_roles.get(role_id) or {}
        rows.append({
            "role_id": role_id,
            "knowledge_base_id": role.get("knowledge_base_id"),
            "priority": role.get("priority"),
            "stream_id": role.get("stream_id"),
            "topics": topics,
            "ru_regulatory_state": ru_role.get("baseline_state") or "RESEARCH_REQUIRED",
            "ru_regulatory_documents_total": len(ru_role.get("documents") or []),
        })
    return rows


def resolve_role_target(role_id: str, target_id: str) -> tuple[dict, dict]:
    role_id = role_id.strip().upper().replace("-", "_")
    target_id = target_id.strip().upper()
    if not SAFE_ROLE.fullmatch(role_id) or not SAFE_TARGET.fullmatch(target_id):
        raise ValueError("invalid role or target format")
    for role in role_catalog():
        if role["role_id"] != role_id:
            continue
        for topic in role["topics"]:
            if topic["target_id"] == target_id:
                return role, topic
        raise ValueError("target does not belong to selected role")
    raise ValueError("unknown role")


def latest_role_reports() -> list[dict]:
    out = []
    root = REPORTS / "team_role_telegram"
    if not root.exists():
        return out
    for path in sorted(root.glob("LATEST_*_TELEGRAM_RUN.json")):
        payload = read_json(path)
        if isinstance(payload, dict):
            out.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), **payload})
    return out


def load_library_orders(limit: int = 50) -> list[dict]:
    if not LIBRARY_ORDER_ROOT.exists():
        return []
    rows: list[dict] = []
    paths = [p for p in LIBRARY_ORDER_ROOT.glob("LIB-*.json") if "_STAGE2_HANDOFF" not in p.name]
    for path in sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
        payload = read_json(path)
        if not isinstance(payload, dict) or payload.get("record_type") != "FATHER_LIBRARY_ORDER":
            continue
        rows.append({
            "order_id": payload.get("order_id"),
            "role_id": payload.get("role_id"),
            "knowledge_base_id": payload.get("knowledge_base_id"),
            "maturity_target": payload.get("maturity_target"),
            "execution_mode": payload.get("execution_mode"),
            "state": payload.get("state"),
            "current_stage": payload.get("current_stage"),
            "stages": payload.get("stages") or {},
            "metrics": payload.get("metrics") or {},
            "gaps": payload.get("gaps") or [],
            "ru_regulatory_baseline": payload.get("ru_regulatory_baseline") or {},
            "requested_sources": payload.get("requested_sources") or [],
            "updated_at_epoch": payload.get("updated_at_epoch"),
        })
    return rows


def download_overview() -> dict:
    live: list[dict] = []
    if DOWNLOAD_PROGRESS_ROOT.exists():
        for path in sorted(DOWNLOAD_PROGRESS_ROOT.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            payload = read_json(path)
            if not isinstance(payload, dict):
                continue
            items = list((payload.get("items") or {}).values())
            live.append({
                "registry_file": path.name,
                "role_id": payload.get("role_id"),
                "stage": payload.get("stage"),
                "state": payload.get("state"),
                "context": payload.get("context") or {},
                "overall_progress_pct": payload.get("overall_progress_pct"),
                "items_total": payload.get("items_total"),
                "queued_total": payload.get("queued_total"),
                "downloading_total": payload.get("downloading_total"),
                "hashing_total": payload.get("hashing_total"),
                "downloaded_total": payload.get("downloaded_total"),
                "reused_total": payload.get("reused_total"),
                "failed_total": payload.get("failed_total"),
                "bytes_received_total": payload.get("bytes_received_total"),
                "bytes_expected_total": payload.get("bytes_expected_total"),
                "updated_at_epoch": payload.get("updated_at_epoch"),
                "items": items,
            })

    history: list[dict] = []
    sources: list[tuple[str, dict]] = []
    architect = read_json(REPORTS / "architect_telegram" / "LATEST_ARCHITECT_TELEGRAM_RUN.json", {}) or {}
    if architect:
        sources.append(("ARCHITECT", architect))
    for report in latest_role_reports():
        sources.append((str(report.get("role_id") or "UNKNOWN"), report))
    for role_id, report in sources:
        for status_key, status in (("downloads", "DOWNLOADED"), ("reused", "REUSED")):
            for row in report.get(status_key, []) or []:
                history.append({
                    "role_id": role_id,
                    "stage": "STAGE_1_ACQUISITION",
                    "status": status,
                    "target_id": (row.get("matched_target_ids") or [None])[0],
                    "file_name": row.get("file_name"),
                    "file_size": row.get("file_size"),
                    "progress_pct": 100.0,
                    "sha256": row.get("sha256"),
                    "local_path": row.get("local_path"),
                    "source_url": row.get("source_url"),
                    "chat_id": row.get("chat_id"),
                    "message_id": row.get("message_id"),
                })

    if DOWNLOAD_RECEIPT_ROOT.exists():
        for path in sorted(DOWNLOAD_RECEIPT_ROOT.glob("*.json"), key=lambda p: p.stat().st_mtime):
            row = read_json(path)
            if not isinstance(row, dict):
                continue
            if row.get("status") not in {"DOWNLOADED", "REUSED", "FAILED"}:
                continue
            history.append({
                "role_id": row.get("role_id"),
                "stage": "STAGE_1_ACQUISITION",
                "status": row.get("status"),
                "target_id": row.get("target_id"),
                "topic": row.get("topic"),
                "file_name": row.get("file_name"),
                "file_size": row.get("file_size"),
                "progress_pct": 100.0 if row.get("status") in {"DOWNLOADED", "REUSED"} else 0.0,
                "sha256": row.get("sha256"),
                "local_path": row.get("local_path"),
                "source_url": row.get("source_url"),
                "chat_id": row.get("chat_id"),
                "message_id": row.get("message_id"),
                "command_id": row.get("command_id"),
                "error": row.get("error"),
            })

    return {
        "stage": "STAGE_1_ACQUISITION",
        "live": live[:100],
        "history": history[-300:],
        "live_roles_total": len(live),
        "historical_items_total": len(history),
    }


def overview() -> dict:
    registry = registry_payload()
    architect = read_json(REPORTS / "architect_telegram" / "LATEST_ARCHITECT_TELEGRAM_RUN.json", {}) or {}
    bibliography = read_json(REPORTS / "team_role_telegram" / "LATEST_PROGRAMMER_BIBLIOGRAPHY_PROBE.json", {}) or {}
    acquisition_plan = read_json(REPORTS / "team_role_telegram" / "LATEST_PROGRAMMER_BIBLIOGRAPHY_ACQUISITION_PLAN.json", {}) or {}
    network = read_json(REPORTS / "architect_telegram" / "LATEST_TELEGRAM_NETWORK_DIAGNOSTIC.json", {}) or {}
    roles = latest_role_reports()
    total_hits = sum(int(r.get("search_hits_total") or 0) for r in roles) + int(architect.get("search_hits_total") or 0)
    downloaded = sum(int(r.get("downloaded_total") or 0) for r in roles) + int(architect.get("downloaded_total") or 0)
    reused = sum(int(r.get("payload_reused_total") or 0) for r in roles) + int(architect.get("payload_reused_total") or 0)
    return {
        "generated_at_epoch": time.time(),
        "network": network,
        "architect": architect,
        "bibliography": bibliography,
        "acquisition_plan": acquisition_plan,
        "roles": registry.get("roles", []),
        "role_catalog": role_catalog(),
        "streams": registry.get("streams", []),
        "role_reports": roles,
        "library_orders": load_library_orders(30),
        "jobs": load_jobs(),
        "trace_events": load_traces(50),
        "downloads": download_overview(),
        "metrics": {
            "search_hits_total": total_hits,
            "downloaded_total": downloaded,
            "payload_reused_total": reused,
            "bibliography_availability_ratio": bibliography.get("availability_ratio"),
            "speedup_vs_1_stream_pct": None,
        },
    }


def _source_session_file() -> tuple[Path, Path]:
    raw = os.getenv("TELEGRAM_SESSION_PATH", "").strip()
    base = Path(raw) if raw else ROOT / "legacy" / "telegram" / "reader_session"
    if not base.is_absolute():
        base = ROOT / base
    if base.suffix == ".session":
        return base, base.with_suffix("")
    return base.with_suffix(".session"), base


def child_env(job: dict) -> dict[str, str]:
    env = os.environ.copy()
    env["FATHER_TRACE_ID"] = str(job["trace_id"])
    env["FATHER_CORRELATION_ID"] = str(job["correlation_id"])
    env["FATHER_TASK_ID"] = str(job["task_id"])
    env["FATHER_COMMAND_ID"] = str(job["command_id"])
    if job.get("parent_command_id"):
        env["FATHER_PARENT_COMMAND_ID"] = str(job["parent_command_id"])

    if job.get("kind") in TELEGRAM_JOB_KINDS:
        source_file, _ = _source_session_file()
        if source_file.is_file():
            target_dir = ROOT / ".runtime" / "telegram" / "sessions"
            target_dir.mkdir(parents=True, exist_ok=True)
            target_base = target_dir / f"ui_{job['id']}"
            shutil.copy2(source_file, target_base.with_suffix(".session"))
            env["TELEGRAM_SESSION_PATH"] = str(target_base)
    return env


def spawn_job(kind: str, command: list[str], meta: dict | None = None) -> dict:
    uid = uuid.uuid4().hex[:10]
    meta = dict(meta or {})
    job = {
        "id": uid,
        "trace_id": f"TRACE-{uuid.uuid4().hex[:12]}",
        "correlation_id": str(meta.pop("correlation_id", f"CORR-{uuid.uuid4().hex[:12]}")),
        "project_id": "FATHER-OSINT",
        "task_id": str(meta.pop("task_id", f"TASK-{uuid.uuid4().hex[:10]}")),
        "command_id": str(meta.pop("command_id", f"CMD-{uuid.uuid4().hex[:10]}")),
        "parent_command_id": meta.pop("parent_command_id", None),
        "actor_role": str(meta.pop("actor_role", "OSINT_UI")),
        "initiator": str(meta.pop("initiator", "OSINT_UI")),
        "executor": str(meta.pop("executor", kind)),
        "trigger": str(meta.pop("trigger", "USER_ACTION")),
        "kind": kind,
        "state": "QUEUED",
        "created_at_epoch": time.time(),
        "input_refs": meta.pop("input_refs", []),
        "output_refs": [],
        "evidence_refs": [],
        **meta,
    }
    add_job(job)
    trace_event(job, status="QUEUED", state_before="PLANNED", state_after="QUEUED")

    def worker():
        try:
            flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            proc = subprocess.Popen(command, cwd=str(ROOT), creationflags=flags, env=child_env(job))
            started = time.time()
            update_job(job["id"], state="RUNNING", pid=proc.pid, started_at_epoch=started)
            running = {**job, "state": "RUNNING", "pid": proc.pid, "started_at_epoch": started}
            trace_event(running, status="RUNNING", state_before="QUEUED", state_after="RUNNING", pid=proc.pid)
            rc = proc.wait()
            finished = time.time()
            final_state = "PASS" if rc == 0 else "FAILED"
            update_job(job["id"], state=final_state, exit_code=rc, finished_at_epoch=finished)
            final = {**running, "state": final_state, "exit_code": rc, "finished_at_epoch": finished}
            trace_event(final, status=final_state, state_before="RUNNING", state_after=final_state, exit_code=rc)
        except Exception as exc:
            finished = time.time()
            error = f"{type(exc).__name__}: {exc}"
            update_job(job["id"], state="FAILED", error=error, finished_at_epoch=finished)
            failed = {**job, "state": "FAILED", "error": error, "finished_at_epoch": finished}
            trace_event(failed, status="FAILED", state_before="RUNNING", state_after="FAILED")

    threading.Thread(target=worker, daemon=True).start()
    return job


def _python() -> str:
    py = ROOT / ".venv" / "Scripts" / "python.exe"
    return str(py if py.exists() else Path(sys.executable))


def action_command(payload: dict) -> tuple[str, list[str], dict]:
    action = str(payload.get("action", "")).upper().strip()
    common = {
        "correlation_id": payload.get("correlation_id") or None,
        "parent_command_id": payload.get("parent_command_id") or None,
        "initiator": "OSINT_UI",
        "actor_role": "OSINT_UI",
        "trigger": "USER_ACTION",
    }
    common = {k: v for k, v in common.items() if v is not None}

    if action == "LIBRARY_ORDER_START":
        role = str(payload.get("role", "")).upper().strip().replace("-", "_")
        maturity = str(payload.get("maturity", "MIN")).upper().strip()
        mode = str(payload.get("mode", "AUTO_BOUNDED")).upper().strip()
        if not SAFE_ROLE.fullmatch(role) or role not in role_ids() or role == "ARCHITECT":
            raise ValueError("unknown or unsupported role")
        if maturity not in {"MIN", "MEDIUM", "MAX"}:
            raise ValueError("unsupported maturity")
        if mode not in {"AUTO_BOUNDED", "REVIEW_EACH_STAGE"}:
            raise ValueError("unsupported library order mode")
        command = [
            _python(),
            str(ROOT / "scripts" / "start_library_order.py"),
            "--role", role,
            "--maturity", maturity,
            "--mode", mode,
        ]
        return action, command, {
            **common,
            "role": role,
            "maturity": maturity,
            "mode": mode,
            "executor": "LIBRARY_ORDER_ORCHESTRATOR",
            "input_refs": [f"role:{role}", f"maturity:{maturity}", "policy:RU_REGULATORY_FIRST"],
        }

    if action == "ROLE_ACQUISITION":
        role = str(payload.get("role", "")).upper().strip().replace("-", "_")
        if not SAFE_ROLE.fullmatch(role) or role not in role_ids() or role == "ARCHITECT":
            raise ValueError("unknown or unsupported role")
        return action, [str(ROOT / "RUN_TEAM_ROLE_ACQUISITION.cmd"), role], {
            **common,
            "role": role,
            "executor": "ROLE_ACQUISITION_WORKER",
            "input_refs": [f"role:{role}"],
        }

    if action == "TELEGRAM_QUERY_PROBE":
        query = " ".join(str(payload.get("query", "")).split()).strip()
        if not query or len(query) > 240:
            raise ValueError("query must contain 1..240 characters")
        role_id = str(payload.get("role", "")).upper().strip().replace("-", "_")
        target_id = str(payload.get("target_id", "")).upper().strip()
        role, topic = resolve_role_target(role_id, target_id)
        command = [
            _python(),
            str(ROOT / "scripts" / "probe_osint_query.py"),
            "--query", query,
            "--role", role_id,
            "--target-id", target_id,
        ]
        return action, command, {
            **common,
            "role": role_id,
            "target_id": target_id,
            "topic": topic["label"],
            "query": query,
            "executor": "TELEGRAM_COLLECTOR",
            "input_refs": [f"role:{role_id}", f"target:{target_id}", f"query:{query}"],
        }

    if action == "TELEGRAM_DOWNLOAD":
        role_id = str(payload.get("role", "")).upper().strip().replace("-", "_")
        target_id = str(payload.get("target_id", "")).upper().strip()
        _, topic = resolve_role_target(role_id, target_id)
        chat_id = str(payload.get("chat_id", "")).strip()
        if not SAFE_CHAT.fullmatch(chat_id):
            raise ValueError("invalid Telegram chat_id")
        try:
            message_id = int(payload.get("message_id"))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid Telegram message_id") from exc
        if message_id <= 0:
            raise ValueError("invalid Telegram message_id")
        username = str(payload.get("chat_username", "") or "").strip().lstrip("@")
        if username and not SAFE_USERNAME.fullmatch(username):
            raise ValueError("invalid Telegram username")
        expected_file_name = str(payload.get("file_name", "") or "").strip()[:260]
        command = [
            _python(),
            str(ROOT / "scripts" / "download_osint_telegram_item.py"),
            "--role", role_id,
            "--target-id", target_id,
            "--chat-id", chat_id,
            "--message-id", str(message_id),
        ]
        if username:
            command.extend(["--chat-username", username])
        if expected_file_name:
            command.extend(["--expected-file-name", expected_file_name])
        return action, command, {
            **common,
            "role": role_id,
            "target_id": target_id,
            "topic": topic["label"],
            "chat_id": chat_id,
            "message_id": message_id,
            "file_name": expected_file_name,
            "executor": "TELEGRAM_DOWNLOAD_WORKER",
            "input_refs": [f"role:{role_id}", f"target:{target_id}", f"telegram:{chat_id}:{message_id}"],
        }

    if action in ALLOWED_ACTIONS:
        return action, ALLOWED_ACTIONS[action], {**common, "executor": action}
    raise ValueError("action is not allowed")


class Handler(BaseHTTPRequestHandler):
    server_version = "FATHER-OSINT-ControlCenter/0.3"

    def log_message(self, fmt, *args):
        return

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/overview":
            return self.send_json(overview())
        if parsed.path == "/api/jobs":
            return self.send_json({"jobs": load_jobs()})
        if parsed.path == "/api/traces":
            return self.send_json({"trace_events": load_traces(500)})
        if parsed.path == "/api/downloads":
            return self.send_json(download_overview())
        if parsed.path == "/api/catalog":
            return self.send_json({"roles": role_catalog()})
        if parsed.path == "/api/library-orders":
            return self.send_json({"orders": load_library_orders(100)})
        if parsed.path == "/api/search-results":
            root = REPORTS / "osint_control_center" / "searches"
            rows = []
            if root.exists():
                for path in sorted(root.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:30]:
                    payload = read_json(path)
                    if isinstance(payload, dict):
                        rows.append(payload)
            return self.send_json({"searches": rows})
        path = parsed.path or "/"
        if path == "/":
            file_path = STATIC / "index.html"
        else:
            file_path = (STATIC / path.lstrip("/")).resolve()
            if STATIC.resolve() not in file_path.parents:
                return self.send_error(HTTPStatus.FORBIDDEN)
        if not file_path.is_file():
            return self.send_error(HTTPStatus.NOT_FOUND)
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(file_path.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if urlparse(self.path).path != "/api/action":
            return self.send_error(HTTPStatus.NOT_FOUND)
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 32_768)
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            kind, command, meta = action_command(payload)
            job = spawn_job(kind, command, meta)
            return self.send_json({"status": "STARTED", "job": job}, 202)
        except (ValueError, json.JSONDecodeError) as exc:
            return self.send_json({"status": "ERROR", "error": str(exc)}, 400)


def main() -> int:
    host = os.getenv("OSINT_WEB_HOST", "127.0.0.1")
    port = int(os.getenv("OSINT_WEB_PORT", "8765"))
    print(f"FATHER OSINT Control Center: http://{host}:{port}")
    print("Local-only by default. Ctrl+C to stop.")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
