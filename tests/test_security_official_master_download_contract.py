import json
from pathlib import Path


def test_master_security_plan_combines_core_departmental_and_secure_development():
    plan = json.loads(Path("config/security_official_master_download_plan.json").read_text(encoding="utf-8"))
    paths = {row["path"] for row in plan["source_registries"]}
    assert "config/pdn_current_only_registry.json" in paths
    assert "config/security_departmental_acquisition_map.json" in paths
    extras = {row["document_id"]: row for row in plan["extra_documents"]}
    for document_id in (
        "DOC-RU-FZ-187-2017",
        "DOC-RU-FSTEC-235-2017",
        "DOC-RU-FSTEC-239-2017",
        "DOC-RU-FSTEC-240-2023",
        "DOC-RU-FSTEC-230-2025",
        "DOC-RU-GOST-R-56939-2024",
        "DOC-RU-GOST-R-58412-2019",
    ):
        assert document_id in extras
    allowed_maturity = {"MIN", "MEDIUM", "MAX"}
    allowed_importance = {"NECESSARY", "DESIRABLE", "INTERESTING_LATER"}
    for row in extras.values():
        assert row["maturity_level"] in allowed_maturity
        assert row["importance_class"] in allowed_importance
    overrides = plan["official_route_overrides"]
    for document_id in (
        "DOC-RU-FSTEC-117-2025",
        "DOC-RU-FSTEC-137-2026",
        "DOC-RU-FSTEC-230-2025",
        "DOC-RU-FSTEC-235-2017",
        "DOC-RU-FSTEC-239-2017",
        "DOC-RU-FSTEC-240-2023",
        "DOC-RU-FZ-187-2017",
    ):
        assert overrides[document_id].startswith("https://publication.pravo.gov.ru/document/")
    assert plan["rules"]["default_execute_all_unique_documents"] is True
    assert plan["rules"]["reference_hosts_are_never_used_as_official_fallback"] is True
    assert plan["rules"]["prefer_official_publication_route_over_secondary_official_landing_page"] is True


def test_master_runner_is_reuse_first_official_only_bounded_and_traceable():
    text = Path("scripts/run_security_official_master_download.py").read_text(encoding="utf-8")
    assert "build_global_document_registry.py" in text
    assert "DownloadProgressRegistry" in text
    assert "ThreadPoolExecutor(max_workers=WORKERS" in text
    assert "WORKERS = 5" in text
    assert "RobustOfficialArtifactFetcher" in text
    assert "minimum_timeout_seconds=45.0" in text
    assert "ROBUST_OFFICIAL_TRANSPORT" in text
    assert '"REUSED_EXACT"' in text
    assert '"REUSED_DECLARED_LOCAL_A0"' in text
    assert '"NEED_OFFICIAL_SOURCE"' in text
    assert "hashlib.sha256(raw_path.read_bytes()).hexdigest()" in text
    assert 'base.OFFICIAL_HOSTS.add("protect.gost.ru")' in text
    assert "status_reference_url" not in text
    assert "consultant.ru" not in text.casefold()
    assert "normativ.kontur.ru" not in text.casefold()
    assert '"failed_error_classes"' in text
    assert '"speedup_vs_1_stream_pct": None' in text
    assert '"eta_seconds": None' in text
    assert '"kb_auto_promotion": False' in text


def test_one_click_master_security_launcher_exists():
    text = Path("RUN_SECURITY_OFFICIAL_MASTER_DOWNLOAD.cmd").read_text(encoding="utf-8")
    assert "run_security_official_master_download_multiroute.py" in text
    assert "LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json" in text
    assert "reuse-first" in text
    assert "official-only" in text
    assert "advisory per-route" in text
