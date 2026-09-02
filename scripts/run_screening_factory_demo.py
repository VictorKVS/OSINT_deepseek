from __future__ import annotations

import json
from pathlib import Path

from screening_factory.demo import build_demo


if __name__ == "__main__":
    output = Path("runtime/screening-factory-demo")
    print(json.dumps(build_demo(output), ensure_ascii=False, indent=2))
