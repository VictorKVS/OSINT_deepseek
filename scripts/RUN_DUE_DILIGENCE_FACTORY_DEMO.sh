#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m osint_factory demo --profile RU_ORG --root runtime/osint-factory-demo --workers 5
echo "Output: runtime/osint-factory-demo/cases/CASE-DEMO-RU_ORG"
