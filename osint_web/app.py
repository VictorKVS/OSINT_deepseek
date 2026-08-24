from __future__ import annotations

import json
import mimetypes
import os
import re
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
ROLE_REGISTRY = ROOT / "config" / "team_role_material_registry.json"
SAFE_ROLE = re.compile(r"^[A-Z0-9_]{2,64}$")
TRACE_LOCK = threading.Lock()

ALLOWED_ACTIONS = {
    "PROGRAMMER_BIBLIOGRAPHY_PROBE": [str(ROOT / "RUN_PROGRAMMER_BIBLIOGRAPHY_PROBE.cmd")],
    "PROGRAMMER_BIBLIOGRAPHY_PLAN": [str(ROOT / "RUN_PROGRAMMER_BIBLIOGRAPHY_NEXT.cmd")],
    "REMAINING_P0_WINDOWS": [str(ROOT / "RUN_REMAINING_P0_SEARCH_WINDOWS.cmd")],
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


def role_ids() -> set[str]:
    registry = read_json(ROLE_REGISTRY, {}) or {}
    return {str(row.get("role_id", "")).upper() for row in registry.get("roles", [])}


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


def download_overview() -> dict:
    live: list[dict] = []
    if DOWNLOAD_PROGRESS_ROOT.exists():
        for path in sorted(DOWNLOAD_PROGRESS_ROOT.glob("*.json")):
            payload = read_json(path)
            if not isinstance(payload, dict):
                continue
            items = list((payload.get("items") or {}).values())
            live.append({
                "role_id": payload.get("role_id"),
                "stage": payload.get("stage"),
                "state": payload.get("state"),
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
                    "file_name": row.get("file_name"),
                    "file_size": row.get("file_size"),
                    "progress_pct": 100.0,
                    "sha256": row.get("sha256"),
                    "local_path": row.get("local_path"),
                    "source_url": row.get("source_url"),
                    "chat_id": row.get("chat_id"),
                    "message_id": row.get("message_id"),
                })
    return {
        "stage": "STAGE_1_ACQUISITION",
        "live": live,
        "history": history[-200:],
        "live_roles_total": len(live),
        "historical_items_total": len(history),
    }


def overview() -> dict:
    registry = read_json(ROLE_REGISTRY, {}) or {}
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
        "streams": registry.get("streams", []),
        "role_reports": roles,
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
            proc = subprocess.Popen(command, cwd=str(ROOT), creationflags=flags)
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
    if action == "ROLE_ACQUISITION":
        role = str(payload.get("role", "")).upper().strip().replace("-", "_")
        if not SAFE_ROLE.fullmatch(role) or role not in role_ids() or role == "ARCHITECT":
            raise ValueError("unknown or unsupported role")
        return action, [str(ROOT / "RUN_TEAM_ROLE_ACQUISITION.cmd"), role], {**common, "role": role, "executor": "ROLE_ACQUISITION_WORKER", "input_refs": [f"role:{role}"]}
    if action == "TELEGRAM_QUERY_PROBE":
        query = " ".join(str(payload.get("query", "")).split()).strip()
        if not query or len(query) > 240:
            raise ValueError("query must contain 1..240 characters")
        py = ROOT / ".venv" / "Scripts" / "python.exe"
        python_exe = str(py if py.exists() else Path(sys.executable))
        return action, [python_exe, str(ROOT / "scripts" / "probe_osint_query.py"), "--query", query], {**common, "query": query, "executor": "TELEGRAM_COLLECTOR", "input_refs": [f"query:{query}"]}
    if action in ALLOWED_ACTIONS:
        return action, ALLOWED_ACTIONS[action], {**common, "executor": action}
    raise ValueError("action is not allowed")


class Handler(BaseHTTPRequestHandler):
    server_version = "FATHER-OSINT-ControlCenter/0.1"

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
