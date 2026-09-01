from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from osint_workbench.demo import run_demo


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the fully synthetic FATHER OSINT Workbench core demo")
    parser.add_argument("--root", default="data/osint-workbench-demo")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = run_demo(Path(args.root), force=args.force)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
