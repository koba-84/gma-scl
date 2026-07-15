#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_DIR="${ROOT_DIR}/tmp/github-actions/code-quality"
LOG_FILE="${LOG_DIR}/pre-commit.log"

mkdir -p "${LOG_DIR}"
cd "${ROOT_DIR}"

run_with_log() {
  : > "${LOG_FILE}"
  printf 'Running:' | tee -a "${LOG_FILE}"
  printf ' %q' "$@" | tee -a "${LOG_FILE}"
  printf '\n' | tee -a "${LOG_FILE}"
  "$@" 2>&1 | tee -a "${LOG_FILE}"
}

if [ "$#" -eq 0 ]; then
  run_with_log uv run pre-commit run -a
  exit 0
fi

existing_files=()
for path in "$@"; do
  if [ -e "${path}" ]; then
    existing_files+=("${path}")
  fi
done

if [ "${#existing_files[@]}" -eq 0 ]; then
  : > "${LOG_FILE}"
  echo "No existing changed files require code-quality checks." | tee -a "${LOG_FILE}"
  exit 0
fi

run_with_log uv run pre-commit run --files "${existing_files[@]}"
