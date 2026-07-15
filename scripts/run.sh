#!/usr/bin/env bash
set -euo pipefail

# Run from repository root:
#   bash scripts/run_test1_to_test4.sh

if [ -z "${PROJECT_ROOT:-}" ]; then
  PROJECT_ROOT="$(pwd)"
  export PROJECT_ROOT
fi

for cfg in test1 test2 test3 test4; do
  echo "[RUN] hparams_search=${cfg}"
  uv run python src/train.py -m hparams_search="${cfg}"
done
