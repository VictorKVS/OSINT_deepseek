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
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
REPORTS = ROOT / "reports"
JOBS_PATH = REPORTS / "osint_control_center" / "jobs.json"
ROLE_REGISTRY = ROOT / "config" / "team_role_material_registry.json"
SAFE_ROLE = re.compile(r"^[A-Z0-9_]{2,64}$")

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
        "metrics": {
            "search_hits_total": total_hits,
            "downloaded_total": downloaded,
            "payload_reused_total": reused,
            "bibliography_availability_ratio": bibliography.get("availability_ratio"),
            "speedup_vs_1_stream_pct": None,
        },
    }


def spawn_job(kind: str, command: list[str], meta: dict | None = None) -> dict:
    job_id = uuid.uuid4().hex[:10]
    job = {"id": job_id, "kind": kind, "state": "STARTING", "created_at_epoch": time.time(), **(meta or {})}
    add_job(job)

    def worker():
        try:
            flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            proc = subprocess.Popen(command, cwd=str(ROOT), creationflags=flags)
            update_job(job_id, state="RUNNING", pid=proc.pid, started_at_epoch=time.time())
            rc = proc.wait()
            update_job(job_id, state="PASS" if rc == 0 else "FAILED", exit_code=rc, finished_at_epoch=time.time())
        except Exception as exc:
            update_job(job_id, state="FAILED", error=f"{type(exc).__name__}: {exc}", finished_at_epoch=time.time())

    threading.Thread(target=worker, daemon=True).start()
    return job


def action_command(payload: dict) -> tuple[str, list[str], dict]:
    action = str(payload.get("action", "")).upper().strip()
    if action == "ROLE_ACQUISITION":
        role = str(payload.get("role", "")).upper().strip().replace("-", "_")
        if not SAFE_ROLE.fullmatch(role) or role not in role_ids() or role == "ARCHITECT":
            raise ValueError("unknown or unsupported role")
        return action, [str(ROOT / "RUN_TEAM_ROLE_ACQUISITION.cmd"), role], {"role": role}
    if action == "TELEGRAM_QUERY_PROBE":
        query = " ".join(str(payload.get("query", "")).split()).strip()
        if not query or len(query) > 240:
            raise ValueError("query must contain 1..240 characters")
        py = ROOT / ".venv" / "Scripts" / "python.exe"
        python_exe = str(py if py.exists() else Path(sys.executable))
        return action, [python_exe, str(ROOT / "scripts" / "probe_osint_query.py"), "--query", query], {"query": query}
    if action in ALLOWED_ACTIONS:
        return action, ALLOWED_ACTIONS[action], {}
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
