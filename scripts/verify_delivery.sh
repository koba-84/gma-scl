#!/usr/bin/env bash
set -euo pipefail

CHANGES=()
RUN_CMDS=()
COMMITS=5

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/verify_delivery.sh --changes <change1,change2> --run "<cmd>" [--run "<cmd>"] [--commits N]

Options:
  --changes   Comma-separated OpenSpec change names to verify as complete.
  --run       Verification command to execute. Can be specified multiple times.
  --commits   Number of recent commits to display (default: 5).
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --changes)
      IFS=',' read -r -a CHANGES <<< "${2:-}"
      shift 2
      ;;
    --run)
      RUN_CMDS+=("${2:-}")
      shift 2
      ;;
    --commits)
      COMMITS="${2:-5}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ ${#CHANGES[@]} -eq 0 ]]; then
  echo "--changes is required" >&2
  usage
  exit 2
fi
if [[ ${#RUN_CMDS[@]} -eq 0 ]]; then
  echo "At least one --run command is required" >&2
  usage
  exit 2
fi

echo "== Delivery Self Check =="
echo "Timestamp: $(date -Iseconds)"
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "HEAD: $(git rev-parse --short HEAD)"
echo

echo "[1/4] Recent commits (latest ${COMMITS})"
git log --oneline -n "$COMMITS"
echo

echo "[2/4] OpenSpec change completion"
for change in "${CHANGES[@]}"; do
  echo "- checking: $change"
  out="$(uv run openspec status --change "$change" --json)"
  if ! echo "$out" | uv run python -c 'import json,sys; data=json.load(sys.stdin); sys.exit(0 if data.get("isComplete") else 1)'; then
    echo "  ERROR: change '$change' is not complete" >&2
    exit 1
  fi
  echo "  OK"
done
echo

echo "[3/4] Verification commands"
for cmd in "${RUN_CMDS[@]}"; do
  echo "+ $cmd"
  eval "$cmd"
done
echo

echo "[4/4] Working tree state"
if [[ -n "$(git status --short)" ]]; then
  echo "Working tree is not clean. Current changes:"
  git status --short
else
  echo "Working tree is clean"
fi
echo

echo "== Report Template =="
cat <<'TEMPLATE'
変更概要:
-

commit 粒度:
- commit 1:
- commit 2:

実行検証:
-

OpenSpec:
- change:
- status: complete

未実施/既知リスク:
-
TEMPLATE
