from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from osint_workbench.workflow import PassiveOSINTWorkbench


class WorkbenchTestCase(TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def bootstrap(self, *, approve: bool = True) -> tuple[PassiveOSINTWorkbench, object]:
        workbench = PassiveOSINTWorkbench(self.root)
        boot = workbench.bootstrap_case(
            title="Synthetic core test",
            seed_type="ORGANIZATION",
            seed_value="Example Test LLC",
            purpose="Exercise the passive evidence-first OSINT core without network access.",
            legal_basis_or_usage_note="Fully synthetic unit-test data used only for deterministic verification.",
            case_type="SYNTHETIC_TRAINING",
            jurisdictions=("SYNTHETIC",),
            objective="Resolve the synthetic organization and retain complete evidence lineage.",
            approve_plan=approve,
            reviewer_id="unit-reviewer" if approve else None,
            synthetic=True,
            case_id="CASE-UNIT-0001",
        )
        return workbench, boot
