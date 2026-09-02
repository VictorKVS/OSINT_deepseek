#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "============================================================"
echo "FATHER OSINT - Screening Factory M3 offline demo"
echo "============================================================"
python -m pytest -q tests/test_screening_factory_m3.py
python scripts/run_screening_factory_demo.py
