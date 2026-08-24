from scripts.analyze_team_role_telegram_coverage import analyze


def _report():
    return {
        "status": "PASS",
        "role_id": "PROGRAMMER",
        "knowledge_base_id": "PROGRAMMING_KB",
        "targets": [
            {"target_id": "PROGRAMMER-TOPIC-01", "query": "Python"},
            {"target_id": "PROGRAMMER-TOPIC-02", "query": "pytest"},
            {"target_id": "PROGRAMMER-TOPIC-03", "query": "OpenTelemetry"},
        ],
        "downloads": [
            {
                "matched_target_ids": ["PROGRAMMER-TOPIC-01", "PROGRAMMER-TOPIC-02"],
                "sha256": "a" * 64,
            }
        ],
        "reused": [
            {
                "matched_target_ids": ["PROGRAMMER-TOPIC-02"],
                "sha256": "b" * 64,
            }
        ],
        "queries_total": 3,
        "search_hits_total": 20,
        "media_candidates_total": 2,
        "downloaded_total": 1,
        "payload_reused_total": 1,
        "errors_total": 0,
        "speedup_vs_1_stream_pct": None,
    }


def test_topic_coverage_exposes_real_gaps_without_claiming_overall_min():
    result = analyze(_report())
    assert result["telegram_gate"] == "SECOND_PASS_REQUIRED"
    assert result["overall_min_gate"] == "NOT_PROVEN_BY_TELEGRAM_ALONE"
    assert result["topics_total"] == 3
    assert result["topics_covered"] == 2
    assert result["topics_gap"] == 1
    assert result["topic_coverage_ratio"] == 2 / 3
    assert result["gap_target_ids"] == ["PROGRAMMER-TOPIC-03"]
    assert result["topics_with_multiple_payloads"] == 1


def test_all_topics_covered_means_telegram_ready_not_global_kb_ready():
    report = _report()
    report["reused"].append(
        {
            "matched_target_ids": ["PROGRAMMER-TOPIC-03"],
            "sha256": "c" * 64,
        }
    )
    result = analyze(report)
    assert result["telegram_gate"] == "TELEGRAM_COVERAGE_READY"
    assert result["topics_gap"] == 0
    assert result["overall_min_gate"] == "NOT_PROVEN_BY_TELEGRAM_ALONE"


def test_coverage_preserves_unknown_one_stream_speedup():
    result = analyze(_report())
    assert result["observed_acquisition_metrics"]["speedup_vs_1_stream_pct"] is None


def test_one_click_coverage_runner_is_local_only():
    from pathlib import Path

    text = Path("RUN_TEAM_ROLE_COVERAGE.cmd").read_text(encoding="utf-8")
    assert "analyze_team_role_telegram_coverage.py" in text
    assert "No Telegram connection or new download is performed." in text
    assert "RUN_TEAM_ROLE_ACQUISITION" not in text
