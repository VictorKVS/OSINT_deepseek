from __future__ import annotations

import ipaddress
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from .extractor import DeterministicIdentifierExtractor, ExtractionResult
from .jobs import PassiveAcquisitionOrchestrator
from .store import WorkbenchStore


class URLPolicyError(ValueError):
    pass


class CollectionError(RuntimeError):
    pass


@dataclass(slots=True)
class HTTPCollectionResult:
    source: dict[str, Any] | None
    capture: dict[str, Any] | None
    job: dict[str, Any]
    extraction: ExtractionResult | None
    status_code: int | None
    final_url: str | None


class PublicURLPolicy:
    """Strict single-URL passive collection policy with SSRF-oriented checks."""

    version = "public-url-policy/0.1.0"
    allowed_schemes = {"http", "https"}
    allowed_ports = {80, 443}
    blocked_host_suffixes = (".local", ".localhost", ".internal", ".home", ".lan")

    def validate(self, url: str, *, resolve: bool = True) -> urllib.parse.SplitResult:
        try:
            parsed = urllib.parse.urlsplit(url)
        except ValueError as exc:
            raise URLPolicyError(f"invalid URL: {exc}") from exc
        if parsed.scheme.lower() not in self.allowed_schemes:
            raise URLPolicyError("only http/https URLs are allowed")
        if parsed.username or parsed.password:
            raise URLPolicyError("credentials in URLs are prohibited")
        host = (parsed.hostname or "").rstrip(".").lower()
        if not host:
            raise URLPolicyError("URL hostname is missing")
        if host == "localhost" or host.endswith(self.blocked_host_suffixes):
            raise URLPolicyError("local/internal hostnames are prohibited")
        try:
            port = parsed.port
        except ValueError as exc:
            raise URLPolicyError(f"invalid port: {exc}") from exc
        effective_port = port or (443 if parsed.scheme.lower() == "https" else 80)
        if effective_port not in self.allowed_ports:
            raise URLPolicyError("only ports 80 and 443 are allowed in the passive public collector")
        if resolve:
            self._validate_resolution(host, effective_port)
        return parsed

    @staticmethod
    def _validate_resolution(host: str, port: int) -> None:
        addresses: set[str] = set()
        try:
            for item in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM):
                addresses.add(item[4][0].split("%")[0])
        except socket.gaierror as exc:
            raise URLPolicyError(f"hostname resolution failed: {host}: {exc}") from exc
        if not addresses:
            raise URLPolicyError(f"hostname produced no addresses: {host}")
        blocked: list[str] = []
        for raw in addresses:
            try:
                address = ipaddress.ip_address(raw)
            except ValueError:
                blocked.append(raw)
                continue
            if not address.is_global:
                blocked.append(raw)
        if blocked:
            raise URLPolicyError(f"hostname resolves to non-public address(es): {', '.join(sorted(blocked))}")


class _ValidatedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, policy: PublicURLPolicy) -> None:
        super().__init__()
        self.policy = policy

    def redirect_request(self, req: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> urllib.request.Request | None:
        absolute = urllib.parse.urljoin(req.full_url, newurl)
        self.policy.validate(absolute)
        return super().redirect_request(req, fp, code, msg, headers, absolute)


class PassiveHTTPCollector:
    """One-URL-at-a-time public HTTP GET collector.

    No authentication, cookie replay, JavaScript automation, CAPTCHA handling,
    robots bypass, port probing or crawling is implemented. The collector requires
    an approved query plan and stores the exact response bytes with SHA-256.
    """

    version = "passive-http-collector/0.1.0"

    def __init__(
        self,
        store: WorkbenchStore,
        *,
        timeout_seconds: int = 20,
        max_bytes: int = 10 * 1024 * 1024,
        user_agent: str = "FATHER-OSINT-Workbench/0.1 (+evidence-preserving passive research)",
    ) -> None:
        self.store = store
        self.timeout_seconds = max(1, int(timeout_seconds))
        self.max_bytes = max(1, int(max_bytes))
        self.user_agent = user_agent
        self.url_policy = PublicURLPolicy()
        self.jobs = PassiveAcquisitionOrchestrator(store)

    def fetch(
        self,
        case_id: str,
        *,
        query_plan_id: str,
        pivot_id: str,
        url: str,
        title: str | None = None,
        publisher: str = "Unknown",
        source_type: str = "WEB_PAGE",
        primary_level: str = "UNKNOWN",
        jurisdiction: str = "UNSPECIFIED",
        language: str = "und",
        reliability_grade: str = "D_LEAD",
        what_it_supports: tuple[str, ...] = ("The public page was retrieved and preserved.",),
        what_it_does_not_support: tuple[str, ...] = ("The truth of every statement on the page without separate review.",),
        access_class: str = "PUBLIC",
        legal_basis_or_usage_note: str = "Passive GET of a lawfully accessible public URL within approved case scope.",
        republication_status: str = "METADATA_ONLY",
        extract_identifiers: bool = True,
    ) -> HTTPCollectionResult:
        case = self.store.get_case(case_id)
        plan = self.store.get_object(case_id, "query_plan", query_plan_id)
        if plan["status"] != "APPROVED" or plan["human_approval"]["status"] != "APPROVED":
            raise PermissionError("HTTP collection requires an approved human-reviewed query plan")
        pivot = next((item for item in plan["pivots"] if item["pivot_id"] == pivot_id), None)
        if pivot is None:
            raise ValueError(f"pivot not found: {pivot_id}")
        if pivot["access_class"] not in {"PUBLIC", "PUBLIC_WITH_PERSONAL_DATA"}:
            raise PermissionError("public HTTP collector cannot process internal/restricted pivot data")
        if case["scope"]["active_actions_allowed"] and pivot["stream"] == "DIGITAL_FOOTPRINT":
            # Active scope does not turn a passive transform into a scanner; this
            # guard documents that the collector remains one GET only.
            pass

        try:
            self.url_policy.validate(url)
        except URLPolicyError as exc:
            job = self._record_terminal(
                case_id,
                query_plan_id=query_plan_id,
                pivot_id=pivot_id,
                stream=pivot["stream"],
                url=url,
                result_code="BLOCKED",
                summary=f"URL policy blocked collection: {exc}",
                error_code="URL_POLICY_BLOCKED",
            )
            return HTTPCollectionResult(None, None, job, None, None, None)

        request = urllib.request.Request(
            url,
            method="GET",
            headers={
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/json,application/xml,text/plain,application/pdf;q=0.9,*/*;q=0.1",
                "Accept-Encoding": "identity",
                "Connection": "close",
            },
        )
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            _ValidatedRedirectHandler(self.url_policy),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        )
        try:
            with opener.open(request, timeout=self.timeout_seconds) as response:
                final_url = response.geturl()
                self.url_policy.validate(final_url)
                status_code = int(getattr(response, "status", response.getcode()))
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > self.max_bytes:
                    raise CollectionError(f"response exceeds max_bytes={self.max_bytes}")
                data = response.read(self.max_bytes + 1)
                if len(data) > self.max_bytes:
                    raise CollectionError(f"response exceeds max_bytes={self.max_bytes}")
                content_type = response.headers.get_content_type() or "application/octet-stream"
                charset = response.headers.get_content_charset()
                mime_type = f"{content_type}; charset={charset}" if charset else content_type
                effective_title = title or final_url
        except urllib.error.HTTPError as exc:
            body = exc.read(min(self.max_bytes, 65536)) if getattr(exc, "fp", None) else b""
            code = int(exc.code)
            result_code = "NO_HIT" if code in {404, 410} else "ERROR"
            job = self._record_terminal(
                case_id,
                query_plan_id=query_plan_id,
                pivot_id=pivot_id,
                stream=pivot["stream"],
                url=url,
                result_code=result_code,
                summary=f"HTTP {code}: {exc.reason}",
                error_code=f"HTTP_{code}",
                raw_output=body,
            )
            return HTTPCollectionResult(None, None, job, None, code, exc.geturl())
        except (urllib.error.URLError, TimeoutError, OSError, CollectionError, URLPolicyError, ValueError) as exc:
            job = self._record_terminal(
                case_id,
                query_plan_id=query_plan_id,
                pivot_id=pivot_id,
                stream=pivot["stream"],
                url=url,
                result_code="ERROR",
                summary=f"Public HTTP collection failed: {type(exc).__name__}: {exc}",
                error_code=type(exc).__name__.upper(),
            )
            return HTTPCollectionResult(None, None, job, None, None, None)

        source = self.store.register_source(
            case_id,
            url=final_url,
            title=effective_title,
            publisher=publisher,
            source_type=source_type,
            primary_level=primary_level,
            jurisdiction=jurisdiction,
            language=language,
            affiliation="Publisher/source identity as declared; further assessment may be required.",
            bias_or_interest="Not automatically assessed by HTTP retrieval.",
            reliability_grade=reliability_grade,
            what_it_supports=what_it_supports,
            what_it_does_not_support=what_it_does_not_support,
            access_class=access_class,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
            republication_status=republication_status,
        )
        capture = self.store.capture_bytes(
            case_id,
            source_id=source["source_id"],
            data=data,
            capture_method="HTTP_GET",
            mime_type=mime_type,
            filename_hint=self._filename_hint(final_url, content_type),
            collector_id="passive-http-collector",
            collector_version=self.version,
            access_class=access_class,
            legal_basis_or_usage_note=legal_basis_or_usage_note,
        )
        extraction: ExtractionResult | None = None
        textual = content_type.startswith("text/") or content_type in {"application/json", "application/xml", "application/xhtml+xml"}
        if extract_identifiers and textual:
            extraction = DeterministicIdentifierExtractor(self.store).extract_capture(
                case_id,
                source_id=source["source_id"],
                capture_id=capture["capture_id"],
                query_plan_id=query_plan_id,
            )
        normalized = {
            "status_code": status_code,
            "final_url": final_url,
            "source_id": source["source_id"],
            "capture_id": capture["capture_id"],
            "content_type": content_type,
            "byte_size": len(data),
            "extraction": extraction.indicators if extraction else [],
        }
        job = self.jobs.record_completed_job(
            case_id,
            query_plan_id=query_plan_id,
            pivot_id=pivot_id,
            stream=pivot["stream"],
            input_type="URL",
            input_reference=url,
            raw_output=data,
            normalized_output=normalized,
            result_code="FOUND",
            summary=f"Retrieved HTTP {status_code}; bytes={len(data)}; preserved as {capture['capture_id']}.",
            source_id=source["source_id"],
            source_ids=[source["source_id"]],
            capture_ids=[capture["capture_id"]],
            entity_ids=extraction.entity_ids if extraction else [],
            relation_ids=extraction.relation_ids if extraction else [],
            claim_ids=extraction.claim_ids if extraction else [],
            execution_profile="WINDOWS_NATIVE",
            safety_class="PASSIVE_PUBLIC",
            network_policy="INTERNET_READ_ONLY",
            parser_name="deterministic-identifier-extractor" if extraction else "capture-only",
            parser_version=DeterministicIdentifierExtractor.version if extraction else self.version,
        )
        return HTTPCollectionResult(source, capture, job, extraction, status_code, final_url)

    def _record_terminal(
        self,
        case_id: str,
        *,
        query_plan_id: str,
        pivot_id: str,
        stream: str,
        url: str,
        result_code: str,
        summary: str,
        error_code: str,
        raw_output: bytes = b"",
    ) -> dict[str, Any]:
        return self.jobs.record_completed_job(
            case_id,
            query_plan_id=query_plan_id,
            pivot_id=pivot_id,
            stream=stream,
            input_type="URL",
            input_reference=url,
            raw_output=raw_output,
            normalized_output={"result_code": result_code, "summary": summary, "url": url},
            result_code=result_code,
            summary=summary,
            execution_profile="WINDOWS_NATIVE",
            safety_class="PASSIVE_PUBLIC",
            network_policy="INTERNET_READ_ONLY",
            parser_name="passive-http-collector",
            parser_version=self.version,
            error_code=error_code,
        )

    @staticmethod
    def _filename_hint(url: str, content_type: str) -> str:
        path = urllib.parse.urlsplit(url).path
        name = path.rsplit("/", 1)[-1] or "index"
        if "." not in name:
            suffix = {
                "text/html": ".html",
                "application/json": ".json",
                "application/xml": ".xml",
                "application/pdf": ".pdf",
                "text/plain": ".txt",
            }.get(content_type, ".bin")
            name += suffix
        return name[:120]
