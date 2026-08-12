from father_osint.models import Material, MaterialPackage
from father_osint.reasoning import AnalysisResult, DeterministicSocrates, EvidenceClaim


def package_with_one_material():
    material = Material(
        source_type="telegram",
        source_locator="telegram://100/1",
        title="Evidence",
        raw_text="Observed evidence",
    )
    return MaterialPackage(task_id="task-1", materials=[material]), material


def test_socrates_accepts_claim_citing_material_from_package():
    package, material = package_with_one_material()
    claim = EvidenceClaim(
        statement="The package contains the observed evidence.",
        evidence_ids=[material.material_id],
        confidence=0.9,
    )
    analysis = AnalysisResult(
        task_id=package.task_id,
        package_id=package.package_id,
        claims=[claim],
    )

    critique = DeterministicSocrates().critique(package, analysis)

    assert critique.verdict == "PASS"
    assert critique.challenged_claim_ids == []


def test_socrates_challenges_claim_with_foreign_evidence_id():
    package, _ = package_with_one_material()
    claim = EvidenceClaim(
        statement="Unsupported claim",
        evidence_ids=["material-not-in-package"],
        confidence=0.8,
    )
    analysis = AnalysisResult(
        task_id=package.task_id,
        package_id=package.package_id,
        claims=[claim],
    )

    critique = DeterministicSocrates().critique(package, analysis)

    assert critique.verdict == "CHALLENGE"
    assert claim.claim_id in critique.challenged_claim_ids


def test_socrates_rejects_analysis_for_different_package():
    package, material = package_with_one_material()
    analysis = AnalysisResult(
        task_id="other-task",
        package_id="other-package",
        claims=[
            EvidenceClaim(
                statement="Claim",
                evidence_ids=[material.material_id],
                confidence=0.5,
            )
        ],
    )

    critique = DeterministicSocrates().critique(package, analysis)
    assert critique.verdict == "INSUFFICIENT"


def test_socrates_rejects_empty_analysis():
    package, _ = package_with_one_material()
    analysis = AnalysisResult(
        task_id=package.task_id,
        package_id=package.package_id,
        claims=[],
    )

    critique = DeterministicSocrates().critique(package, analysis)
    assert critique.verdict == "INSUFFICIENT"
