#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: bash scripts/ci_pytest.sh <fast|slow> [extra pytest args...]" >&2
  exit 1
fi

SUITE="$1"
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

case "${SUITE}" in
  fast)
    MARK_EXPR="not slow and not integration and not gpu"
    HYPOTHESIS_PROFILE="ci_fast"
    DOCTEST_ARGS=()
    OUT_DIR="${ROOT_DIR}/tmp/github-actions/fast-tests"
    ;;
  slow)
    MARK_EXPR="(slow or integration) and not gpu"
    HYPOTHESIS_PROFILE="ci_slow"
    DOCTEST_ARGS=(--doctest-modules)
    OUT_DIR="${ROOT_DIR}/tmp/github-actions/slow-tests"
    ;;
  *)
    echo "Unknown suite: ${SUITE}" >&2
    exit 1
    ;;
esac

mkdir -p "${OUT_DIR}"
cd "${ROOT_DIR}"

export HYPOTHESIS_PROFILE
export CUDA_VISIBLE_DEVICES=""

LOG_FILE="${OUT_DIR}/pytest.log"
JUNIT_FILE="${OUT_DIR}/junit.xml"

: > "${LOG_FILE}"
printf 'Running: uv run pytest -m %q' "${MARK_EXPR}" \
  | tee -a "${LOG_FILE}"
for arg in "${DOCTEST_ARGS[@]}"; do
  printf ' %q' "${arg}" | tee -a "${LOG_FILE}"
done
printf ' --junitxml %q -q' "${JUNIT_FILE}" | tee -a "${LOG_FILE}"
for arg in "$@"; do
  printf ' %q' "${arg}" | tee -a "${LOG_FILE}"
done
printf '\n' | tee -a "${LOG_FILE}"

uv run pytest -m "${MARK_EXPR}" "${DOCTEST_ARGS[@]}" --junitxml "${JUNIT_FILE}" -q "$@" 2>&1 | tee -a "${LOG_FILE}"
