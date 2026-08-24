from __future__ import annotations

import os
import sys
from http.server import ThreadingHTTPServer

from osint_web.app import Handler


EXPECTED_CLIENT_DISCONNECT_WINERRORS = {64, 10053, 10054}


class QuietThreadingHTTPServer(ThreadingHTTPServer):
    """HTTP server that keeps real failures visible but ignores normal client aborts."""

    daemon_threads = True

    def handle_error(self, request, client_address) -> None:  # noqa: ANN001
        _, exc, _ = sys.exc_info()
        if isinstance(exc, (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            return
        if isinstance(exc, OSError) and getattr(exc, "winerror", None) in EXPECTED_CLIENT_DISCONNECT_WINERRORS:
            return
        super().handle_error(request, client_address)


def main() -> int:
    host = os.getenv("OSINT_WEB_HOST", "127.0.0.1")
    port = int(os.getenv("OSINT_WEB_PORT", "8765"))
    print(f"FATHER OSINT Control Center: http://{host}:{port}")
    print("Local-only by default. Ctrl+C to stop.")
    QuietThreadingHTTPServer((host, port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
