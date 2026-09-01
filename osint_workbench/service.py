from __future__ import annotations

import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlsplit

from . import __version__
from .store import StoreError, WorkbenchStore

_LOG = logging.getLogger("osint_workbench.service")


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _sanitize_object(kind: str, payload: dict[str, Any], *, expose_local_paths: bool) -> dict[str, Any]:
    result = dict(payload)
    if kind == "capture" and not expose_local_paths:
        result["storage_uri"] = f"evidence://sha256/{payload.get('sha256', 'unknown')}"
    return result


def make_handler(store: WorkbenchStore, *, expose_local_paths: bool = False) -> type[BaseHTTPRequestHandler]:
    class ReadOnlyWorkbenchHandler(BaseHTTPRequestHandler):
        server_version = "FATHER-OSINT-Workbench/0.1"
        protocol_version = "HTTP/1.1"

        def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            try:
                self._route_get()
            except StoreError as exc:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "NOT_FOUND", "detail": str(exc)})
            except (ValueError, KeyError) as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "BAD_REQUEST", "detail": str(exc)})
            except PermissionError as exc:
                self._send_json(HTTPStatus.FORBIDDEN, {"error": "FORBIDDEN", "detail": str(exc)})
            except Exception as exc:  # pragma: no cover - defensive HTTP boundary
                _LOG.exception("unhandled service error")
                self._send_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": "INTERNAL_ERROR", "detail": f"{type(exc).__name__}: {exc}"},
                )

        def do_HEAD(self) -> None:  # noqa: N802
            if urlsplit(self.path).path == "/health":
                self._send_json(HTTPStatus.OK, {}, head_only=True)
            else:
                self._send_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "HEAD_NOT_SUPPORTED"}, head_only=True)

        def do_POST(self) -> None:  # noqa: N802
            self._method_not_allowed()

        def do_PUT(self) -> None:  # noqa: N802
            self._method_not_allowed()

        def do_PATCH(self) -> None:  # noqa: N802
            self._method_not_allowed()

        def do_DELETE(self) -> None:  # noqa: N802
            self._method_not_allowed()

        def _method_not_allowed(self) -> None:
            self._send_json(
                HTTPStatus.METHOD_NOT_ALLOWED,
                {
                    "error": "READ_ONLY_API",
                    "detail": "M1A exposes read-only case, graph, evidence-metadata and report views.",
                },
                extra_headers={"Allow": "GET, HEAD"},
            )

        def _route_get(self) -> None:
            parsed = urlsplit(self.path)
            parts = [unquote(part) for part in parsed.path.split("/") if part]
            if not parts:
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "service": "FATHER OSINT Workbench read-only API",
                        "version": __version__,
                        "links": ["/health", "/api/v1/cases"],
                    },
                )
                return
            if parts == ["health"]:
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "status": "ok",
                        "service": "osint-workbench-read-only",
                        "version": __version__,
                        "case_count": len(store.list_cases()),
                        "write_methods_enabled": False,
                    },
                )
                return
            if parts[:3] != ["api", "v1", "cases"]:
                raise StoreError("route not found")
            if len(parts) == 3:
                self._send_json(HTTPStatus.OK, {"items": store.list_cases()})
                return
            case_id = parts[3]
            if len(parts) == 4:
                self._send_json(HTTPStatus.OK, store.get_case(case_id))
                return
            action = parts[4]
            if action == "summary" and len(parts) == 5:
                self._send_json(HTTPStatus.OK, store.summary(case_id))
                return
            if action == "objects":
                self._objects(case_id, parts[5:])
                return
            if action == "reports":
                self._reports(case_id, parts[5:])
                return
            if action == "evidence" and len(parts) == 7 and parts[6] == "metadata":
                capture = store.get_object(case_id, "capture", parts[5])
                self._send_json(HTTPStatus.OK, _sanitize_object("capture", capture, expose_local_paths=expose_local_paths))
                return
            if action == "graph" and len(parts) == 6 and parts[5] == "latest":
                graphs = store.list_objects(case_id, "graph")
                if not graphs:
                    raise StoreError("no graph view exists for case")
                self._send_json(HTTPStatus.OK, graphs[-1])
                return
            raise StoreError("route not found")

        def _objects(self, case_id: str, tail: list[str]) -> None:
            if not tail:
                self._send_json(HTTPStatus.OK, {"kinds": sorted(store.OBJECT_DIRS)})
                return
            kind = tail[0]
            if kind not in store.OBJECT_DIRS:
                raise StoreError(f"unsupported object kind: {kind}")
            if len(tail) == 1:
                objects = [
                    _sanitize_object(kind, item, expose_local_paths=expose_local_paths)
                    for item in store.list_objects(case_id, kind)
                ]
                self._send_json(HTTPStatus.OK, {"kind": kind, "items": objects})
                return
            if len(tail) == 2:
                payload = store.get_object(case_id, kind, tail[1])
                self._send_json(HTTPStatus.OK, _sanitize_object(kind, payload, expose_local_paths=expose_local_paths))
                return
            raise StoreError("object route not found")

        def _reports(self, case_id: str, tail: list[str]) -> None:
            report_dir = store.case_dir(case_id) / "reports"
            if not tail:
                items = [
                    {
                        "name": path.name,
                        "byte_size": path.stat().st_size,
                    }
                    for path in sorted(report_dir.iterdir())
                    if path.is_file() and path.suffix in {".md", ".sha256"}
                ]
                self._send_json(HTTPStatus.OK, {"items": items})
                return
            if len(tail) != 1:
                raise StoreError("report route not found")
            name = Path(tail[0]).name
            if name != tail[0] or not (name.endswith(".md") or name.endswith(".sha256")):
                raise StoreError("invalid report filename")
            path = report_dir / name
            if not path.is_file():
                raise StoreError(f"report not found: {name}")
            content_type = "text/markdown; charset=utf-8" if name.endswith(".md") else "text/plain; charset=utf-8"
            self._send_bytes(HTTPStatus.OK, path.read_bytes(), content_type=content_type)

        def _send_json(
            self,
            status: HTTPStatus,
            payload: Any,
            *,
            head_only: bool = False,
            extra_headers: dict[str, str] | None = None,
        ) -> None:
            data = _json_bytes(payload)
            self._send_bytes(status, b"" if head_only else data, content_type="application/json; charset=utf-8", declared_length=len(data), extra_headers=extra_headers)

        def _send_bytes(
            self,
            status: HTTPStatus,
            data: bytes,
            *,
            content_type: str,
            declared_length: int | None = None,
            extra_headers: dict[str, str] | None = None,
        ) -> None:
            self.send_response(int(status))
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data) if declared_length is None else declared_length))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
            if extra_headers:
                for key, value in extra_headers.items():
                    self.send_header(key, value)
            self.end_headers()
            if data:
                self.wfile.write(data)

        def log_message(self, fmt: str, *args: Any) -> None:
            _LOG.info("%s - %s", self.address_string(), fmt % args)

    return ReadOnlyWorkbenchHandler


def serve(
    store: WorkbenchStore,
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    expose_local_paths: bool = False,
    ready_callback: Callable[[ThreadingHTTPServer], None] | None = None,
) -> None:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError("M1A read-only API binds to loopback only by policy")
    server = ThreadingHTTPServer((host, int(port)), make_handler(store, expose_local_paths=expose_local_paths))
    if ready_callback:
        ready_callback(server)
    _LOG.info("OSINT Workbench read-only API listening on http://%s:%s", host, port)
    try:
        server.serve_forever()
    finally:
        server.server_close()
