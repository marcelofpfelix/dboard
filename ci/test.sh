#!/bin/bash

set -euo pipefail
  # change to app directory
cd "$(dirname "$0")/.." || exit

service=dboard
MIN_COVERAGE=0

echo
echo "Tests"
echo "################################################################################"
uv run pytest -n auto --cov=$service --cov-fail-under=$MIN_COVERAGE --cov-report=term tests || exit
