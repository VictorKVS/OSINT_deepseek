"""Evidence-first passive OSINT workbench.

The package is deliberately separate from the frozen ``father_osint`` DEV v1
runtime. It implements the first operational slice of ``docs/osint-platform``
without enabling intrusive collection or autonomous FACT promotion.
"""

from .planner import CoreQueryPlanner
from .store import WorkbenchStore
from .workflow import PassiveOSINTWorkbench

__all__ = ["CoreQueryPlanner", "PassiveOSINTWorkbench", "WorkbenchStore"]
__version__ = "0.1.0"
