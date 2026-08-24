from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_ROOT = REPO_ROOT / "reports" / "team_role_telegram"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "reports" / "team_role_telegram"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized_role(value: str) -> str:
    return value.strip().upper().replace("-", "_")


def _default_report(role_id: str) -> Path:
    return DEFAULT_REPORT_ROOT / f"LATEST_{role_id}_TELEGRAM_RUN.json"


def _target_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = report.get("targets") or []
    if not isinstance(rows, list):
        raise RuntimeError("report.targets must be a list")
    return [row for row in rows if isinstance(row, dict) and row.get("target_id")]


def _evidence_rows(report: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for state, key in (("DOWNLOADED", "downloads"), ("REUSED", "reused")):
        payload = report.get(key) or []
        if not isinstance(payload, list):
            raise RuntimeError(f"report.{key} must be a list")
        for row in payload:
            if isinstance(row, dict):
                rows.append((state, row))
    return rows


def analyze(report: dict[str, Any]) -> dict[str, Any]:
    role_id = _normalized_role(str(report.get("role_id") or ""))
    if not role_id:
        raise RuntimeError("report.role_id is required")
    if report.get("status") not in {"PASS", "PASS_WITH_ERRORS"}:
        raise RuntimeError(f"cannot assess non-passing acquisition report: {report.get('status')}")

    targets = _target_rows(report)
    target_by_id = {str(row["target_id"]): row for row in targets}
    evidence = _evidence_rows(report)

    counts: dict[str, Counter[str]] = defaultdict(Counter)
    payloads_by_target: dict[str, set[str]] = defaultdict(set)
    unmatched_evidence = 0

    for state, row in evidence:
        matched = row.get("matched_target_ids") or []
        if not isinstance(matched, list) or not matched:
            unmatched_evidence += 1
            continue
        digest = str(row.get("sha256") or row.get("local_path") or f"{row.get('chat_id')}:{row.get('message_id')}")
        for target_id in matched:
            target_id = str(target_id)
            if target_id not in target_by_id:
                continue
            counts[target_id][state] += 1
            payloads_by_target[target_id].add(digest)

    topic_rows: list[dict[str, Any]] = []
    covered = 0
    gaps: list[str] = []
    for target in targets:
        target_id = str(target["target_id"])
        downloaded = counts[target_id]["DOWNLOADED"]
        reused = counts[target_id]["REUSED"]
        unique_payloads = len(payloads_by_target[target_id])
        status = "COVERED" if unique_payloads > 0 else "GAP"
        if status == "COVERED":
            covered += 1
        else:
            gaps.append(target_id)
        topic_rows.append(
            {
                "target_id": target_id,
                "query": target.get("query"),
                "status": status,
                "downloaded_refs": downloaded,
                "reused_refs": reused,
                "unique_payloads": unique_payloads,
            }
        )

    topics_total = len(targets)
    coverage_ratio = (covered / topics_total) if topics_total else None
    evidence_distribution = [row["unique_payloads"] for row in topic_rows]
    max_topic_payloads = max(evidence_distribution, default=0)
    topics_with_multiple_payloads = sum(1 for value in evidence_distribution if value >= 2)

    # This gate evaluates only Telegram acquisition coverage. Overall FATHER MIN
    # additionally requires authoritative-source seeds, which this Telegram report
    # cannot prove and must not silently infer.
    if topics_total == 0:
        telegram_gate = "BLOCKED_NO_TOPICS"
    elif covered == topics_total:
        telegram_gate = "TELEGRAM_COVERAGE_READY"
    else:
        telegram_gate = "SECOND_PASS_REQUIRED"

    return {
        "record_type": "TEAM_ROLE_TELEGRAM_TOPIC_COVERAGE",
        "schema_version": "1.0",
        "role_id": role_id,
        "knowledge_base_id": report.get("knowledge_base_id"),
        "source_report_status": report.get("status"),
        "telegram_gate": telegram_gate,
        "overall_min_gate": "NOT_PROVEN_BY_TELEGRAM_ALONE",
        "overall_min_note": "FATHER MIN also requires authoritative-source seeds per P0 topic cluster; Telegram acquisition is candidate/supporting evidence only.",
        "topics_total": topics_total,
        "topics_covered": covered,
        "topics_gap": topics_total - covered,
        "topic_coverage_ratio": coverage_ratio,
        "topics_with_multiple_payloads": topics_with_multiple_payloads,
        "max_unique_payloads_on_one_topic": max_topic_payloads,
        "unmatched_evidence_rows": unmatched_evidence,
        "gap_target_ids": gaps,
        "topics": topic_rows,
        "observed_acquisition_metrics": {
            key: report.get(key)
            for key in (
                "queries_total",
                "search_hits_total",
                "media_candidates_total",
                "downloaded_total",
                "payload_reused_total",
                "skipped_type_total",
                "skipped_size_total",
                "errors_total",
                "bytes_downloaded",
                "elapsed_seconds",
                "throughput_files_per_second",
                "throughput_megabytes_per_second",
                "useful_candidate_ratio",
                "speedup_vs_1_stream_pct",
            )
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Assess per-topic coverage from an existing team-role Telegram run")
    parser.add_argument("--role", required=True)
    parser.add_argument("--report", default=None)
    parser.add_argument("--output", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    role_id = _normalized_role(args.role)
    report_path = Path(args.report).resolve() if args.report else _default_report(role_id)
    if not report_path.is_file():
        raise SystemExit(f"acquisition report not found: {report_path}")
    report = _load(report_path)
    if _normalized_role(str(report.get("role_id") or "")) != role_id:
        raise SystemExit(f"report role mismatch: expected {role_id}, got {report.get('role_id')}")

    result = analyze(report)
    output_path = Path(args.output).resolve() if args.output else (DEFAULT_OUTPUT_ROOT / f"LATEST_{role_id}_COVERAGE.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    compact = {
        key: result[key]
        for key in (
            "role_id",
            "knowledge_base_id",
            "telegram_gate",
            "overall_min_gate",
            "topics_total",
            "topics_covered",
            "topics_gap",
            "topic_coverage_ratio",
            "topics_with_multiple_payloads",
            "max_unique_payloads_on_one_topic",
            "gap_target_ids",
        )
    }
    compact["report_path"] = str(output_path.relative_to(REPO_ROOT)).replace("\\", "/") if output_path.is_relative_to(REPO_ROOT) else str(output_path)
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
