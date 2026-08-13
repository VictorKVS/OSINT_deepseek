from scripts import run_live_telegram_m5_full as runner


def test_full_live_runner_parser_exposes_integrated_controls():
    parser = runner.build_parser()
    help_text = parser.format_help()

    for flag in (
        "--max-items",
        "--recon-sample",
        "--sufficiency",
        "--term",
        "--hypothesis",
        "--resume",
        "--expect-reuse-min",
    ):
        assert flag in help_text


def test_full_live_runner_contains_all_g6_g10_layers():
    source = __import__("pathlib").Path("scripts/run_live_telegram_m5_full.py").read_text(encoding="utf-8")

    for symbol in (
        "DeterministicTelegramReconnaissance",
        "DeterministicEvidenceQualityAssessor",
        "DeterministicResearchSufficiencyAssessor",
        "DeterministicCounterEvidencePlanner",
        "DeterministicCounterEvidenceAssessor",
        "DeterministicAcquisitionReportBuilder",
    ):
        assert symbol in source


def test_full_live_runner_reports_requested_vs_achieved_and_no_truth_score():
    source = __import__("pathlib").Path("scripts/run_live_telegram_m5_full.py").read_text(encoding="utf-8")

    assert '"g8_requested_sufficiency"' in source
    assert '"g8_achieved_sufficiency"' in source
    assert '"g7_truth_probability": "NOT_CALCULATED"' in source
    assert '"g9_counter_evidence_status"' in source
    assert '"g10_acquisition_report_id"' in source


def test_full_live_runner_keeps_g9_incomplete_when_hypothesis_has_no_executed_challenge_search():
    request = runner.ResearchRequest(
        objective="test",
        research_questions=["q"],
        hypotheses=["leading hypothesis"],
    )
    directive = runner.DeterministicCounterEvidencePlanner().plan(request)
    assessment = runner.DeterministicCounterEvidenceAssessor().assess(directive.directive)

    assert directive.directive.status == "REQUIRED"
    assert assessment.assessment.status == "INCOMPLETE"
