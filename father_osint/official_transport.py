from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from .acquisition import AcquisitionError, ArtifactFetcher, FetchedArtifact, UrllibArtifactFetcher


class CurlArtifactFetcher:
    """TLS-verifying curl transport fallback for hostile/slow official sites.

    The command is executed without a shell. TLS verification remains enabled;
    this class intentionally never passes curl's insecure/-k option.

    Some public publication archives behave differently for HEAD vs GET and
    may require ordinary redirect-cookie handling. The fallback therefore uses
    curl's cookie engine for redirects, but does not inject authentication or
    bypass access control. It also leaves curl's normal User-Agent unchanged so
    sites that reject project-specific crawler identifiers can still return the
    same public document a normal curl client receives.
    """

    def __init__(self, executable: str | None = None) -> None:
        self.executable = executable or shutil.which("curl.exe") or shutil.which("curl")

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        if not self.executable:
            raise AcquisitionError("curl executable is unavailable")

        timeout = max(1, int(timeout_seconds))
        connect_timeout = max(1, min(timeout, 15))
        tmp_name: str | None = None
        cookie_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile(prefix="father-kf-", suffix=".artifact", delete=False) as tmp:
                tmp_name = tmp.name
            with tempfile.NamedTemporaryFile(prefix="father-kf-", suffix=".cookies", delete=False) as cookie:
                cookie_name = cookie.name

            command = [
                self.executable,
                "--fail",
                "--location",
                "--silent",
                "--show-error",
                "--compressed",
                "--connect-timeout",
                str(connect_timeout),
                "--max-time",
                str(timeout),
                "--retry",
                "2",
                "--retry-delay",
                "1",
                "--retry-max-time",
                str(timeout),
                "--max-filesize",
                str(max_bytes),
                "--cookie",
                cookie_name,
                "--cookie-jar",
                cookie_name,
                "--header",
                "Accept: text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                "--header",
                "Accept-Language: ru-RU,ru;q=0.9,en;q=0.7",
                "--output",
                tmp_name,
                "--write-out",
                "FATHER_FINAL_URL=%{url_effective}\nFATHER_CONTENT_TYPE=%{content_type}\n",
                url,
            ]
            try:
                completed = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds + 10,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise AcquisitionError(f"curl fetch timed out after {timeout_seconds}s") from exc
            except OSError as exc:
                raise AcquisitionError(f"curl execution failed: {exc}") from exc

            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout or "curl returned non-zero status").strip()
                raise AcquisitionError(f"curl fetch failed ({completed.returncode}): {detail[:500]}")

            data = Path(tmp_name).read_bytes()
            if not data:
                raise AcquisitionError("curl returned an empty artifact")
            if len(data) > max_bytes:
                raise AcquisitionError(f"artifact exceeds max_bytes={max_bytes}")

            final_url: str | None = None
            mime_type: str | None = None
            for line in completed.stdout.splitlines():
                if line.startswith("FATHER_FINAL_URL="):
                    final_url = line.partition("=")[2].strip() or None
                elif line.startswith("FATHER_CONTENT_TYPE="):
                    mime_type = line.partition("=")[2].strip() or None

            return FetchedArtifact(data=data, mime_type=mime_type, final_url=final_url or url)
        finally:
            if tmp_name:
                Path(tmp_name).unlink(missing_ok=True)
            if cookie_name:
                Path(cookie_name).unlink(missing_ok=True)


class RobustOfficialArtifactFetcher:
    """Bounded official-source transport: urllib first, TLS-verifying curl fallback.

    It exists for environments where Python's certificate store or HTTP stack
    cannot reach an otherwise valid official site. It does not weaken TLS or
    source-policy validation. AcquisitionService still validates the final host,
    exact bytes, SHA-256, size and provenance after this transport returns.
    """

    def __init__(
        self,
        *,
        primary: ArtifactFetcher | None = None,
        fallback: ArtifactFetcher | None = None,
        minimum_timeout_seconds: float = 45.0,
    ) -> None:
        if minimum_timeout_seconds <= 0:
            raise ValueError("minimum_timeout_seconds must be > 0")
        self.primary = primary or UrllibArtifactFetcher()
        self.fallback = fallback or CurlArtifactFetcher()
        self.minimum_timeout_seconds = float(minimum_timeout_seconds)

    @staticmethod
    def _failure_text(exc: Exception) -> str:
        return str(exc) if isinstance(exc, AcquisitionError) else f"{type(exc).__name__}: {exc}"

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        effective_timeout = max(float(timeout_seconds), self.minimum_timeout_seconds)
        try:
            return self.primary.fetch(
                url,
                timeout_seconds=effective_timeout,
                max_bytes=max_bytes,
            )
        except Exception as primary_exc:
            primary_reason = self._failure_text(primary_exc)

        try:
            return self.fallback.fetch(
                url,
                timeout_seconds=effective_timeout,
                max_bytes=max_bytes,
            )
        except Exception as fallback_exc:
            fallback_reason = self._failure_text(fallback_exc)
            raise AcquisitionError(
                "official transport failed; "
                f"primary=[{primary_reason}]; fallback=[{fallback_reason}]"
            ) from fallback_exc
