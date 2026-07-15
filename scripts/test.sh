#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
export PROJECT_ROOT="${PROJECT_ROOT:-${ROOT_DIR}}"
LOG_DIR="${ROOT_DIR}/tmp"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/test.log"

export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

{
  uv run python src/train.py \
    contrastive=train \
    classification=train \
    data=aapd \
    trainer=gpu \
    trainer.max_epochs=1 \
    classification.trainer.max_epochs=1
} 2>&1 | tee "${LOG_FILE}"
