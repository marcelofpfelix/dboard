#!/bin/bash

set -euo pipefail
  # change to app directory
cd "$(dirname "$0")/.." || exit

service=dboard

echo
echo "Format"
echo "################################################################################"
uv run ruff format $service/* --check tests || exit

echo
echo "Linter"
echo "################################################################################"
uv run ruff check $service/* tests  || exit

echo
echo "Type Checking"
echo "################################################################################"
uv run mypy --namespace-packages --explicit-package-bases --strict $service  tests || exit
