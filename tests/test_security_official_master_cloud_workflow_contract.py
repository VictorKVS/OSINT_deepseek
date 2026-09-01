from pathlib import Path


def test_cloud_master_workflow_is_scheduled_traceable_and_partial_success_safe():
    text = Path(".github/workflows/security-official-master-cloud.yml").read_text(encoding="utf-8")
    assert "Security Official Master Cloud Recovery" in text
    assert 'cron: "15 17 * * *"' in text
    assert "run_security_official_master_download_multiroute.py" in text
    assert "stamp_security_master_cloud_environment.py" in text
    assert "GITHUB_ACTIONS_UBUNTU_LATEST" in text
    assert "continue-on-error: true" in text
    assert "actions/upload-artifact@v4" in text
    assert "security-official-master-cloud-${{ github.run_id }}" in text
    assert "Preserve partial-success semantics" in text


def test_cloud_master_stamper_preserves_legal_review_gate():
    text = Path("scripts/stamp_security_master_cloud_environment.py").read_text(encoding="utf-8")
    assert '"execution_environment_id"' in text
    assert '"CLOUD_CI"' in text
    assert 'meta["legal_truth_eligible"] = False' in text
    assert 'meta["kb_auto_promotion"] = False' in text
    assert "LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json" in text
