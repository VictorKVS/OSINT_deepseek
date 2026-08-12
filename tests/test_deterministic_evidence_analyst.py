from father_osint.models import Material, MaterialPackage
from father_osint.reasoning import DeterministicEvidenceAnalyst, DeterministicSocrates


def test_analyst_builds_one_observation_claim_per_text_material():
    materials = [
        Material(
            source_type="telegram",
            source_locator="telegram://100/1",
            title="Channel A",
            raw_text="First observed message",
        ),
        Material(
            source_type="web",
            source_locator="https://example.test/item",
            title="Web source",
            raw_text="Second observed document",
        ),
    ]
    package = MaterialPackage(task_id="task-1", materials=materials)

    analysis = DeterministicEvidenceAnalyst().analyze(package)

    assert len(analysis.claims) == 2
    assert analysis.claims[0].evidence_ids == [materials[0].material_id]
    assert analysis.claims[1].evidence_ids == [materials[1].material_id]
    assert all(claim.confidence == 1.0 for claim in analysis.claims)
    assert DeterministicSocrates().critique(package, analysis).verdict == "PASS"


def test_analyst_does_not_claim_truth_beyond_observation():
    material = Material(
        source_type="telegram",
        source_locator="telegram://100/2",
        title="Channel",
        raw_text="The moon is made of cheese.",
    )
    package = MaterialPackage(task_id="task-2", materials=[material])

    claim = DeterministicEvidenceAnalyst().analyze(package).claims[0]

    assert claim.statement.startswith("Observed telegram source")
    assert "The moon is made of cheese." in claim.statement
    assert claim.evidence_ids == [material.material_id]
