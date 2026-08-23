from pathlib import Path


def test_100_law_donor_audit_is_bounded_parallel_and_fail_closed():
    script = Path("scripts/audit_prebuilt_db_100_source_identity.py").read_text(encoding="utf-8")
    cmd = Path("RUN_AUDIT_PREBUILT_DB_100_SOURCE_IDENTITY.cmd").read_text(encoding="utf-8")

    assert "SAMPLE_SIZE = 100" in script
    assert "MAX_WORKERS = 5" in script
    assert "ThreadPoolExecutor" in script
    assert "pravo.gov.ru" in script
    assert "ALLOWED_HOSTS" in script
    assert "MAX_BYTES" in script
    assert "RETRIES = 2" in script
    assert "VERIFIED_MATCH" in script
    assert "IDENTITY_COLLISION" in script
    assert "AMBIGUOUS" in script
    assert "UNVERIFIED_TRANSPORT" in script
    assert '"content_reuse_allowed": False' in script
    assert '"legal_truth_promoted": False' in script
    assert "collision_rate_observed" in script
    assert "duplicate_nd_groups_in_full_eligible_set" in script
    assert "scripts\\audit_prebuilt_db_100_source_identity.py" in cmd
