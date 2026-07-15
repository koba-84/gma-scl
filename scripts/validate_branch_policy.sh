#!/usr/bin/env bash
set -euo pipefail

PROTECTED_REF_REGEX='^refs/heads/(main|dev|release/.+)$'
PROTECTED_BRANCH_REGEX='^(main|dev|release/.+)$'
TOPIC_BRANCH_REGEX='^(feat|fix|refactor|docs|test|chore|exp|ops|hotfix)/[a-z0-9][a-z0-9._-]*$'
DEFAULT_HISTORY_BASE_REF='origin/main'

if [[ "${BRANCH_POLICY_BYPASS:-0}" == "1" ]]; then
  echo "[branch-policy] BRANCH_POLICY_BYPASS=1 のため検証をスキップします。"
  exit 0
fi

history_max_commits="${BRANCH_HISTORY_MAX_COMMITS:-}"
history_base_ref="${BRANCH_HISTORY_BASE_REF:-${DEFAULT_HISTORY_BASE_REF}}"

if [[ -n "${history_max_commits}" ]] && [[ ! "${history_max_commits}" =~ ^[0-9]+$ ]]; then
  echo "[branch-policy] BRANCH_HISTORY_MAX_COMMITS は 0 以上の整数で指定してください。"
  exit 1
fi

current_branch="$(git rev-parse --abbrev-ref HEAD)"

if [[ "${current_branch}" == "HEAD" ]]; then
  echo "[branch-policy] detached HEAD のため current branch 命名検証をスキップします。"
else
  if [[ "${current_branch}" =~ ${PROTECTED_BRANCH_REGEX} ]]; then
    echo "[branch-policy] protected branch '${current_branch}' からの push は禁止です。"
    echo "[branch-policy] topic branch を作成し、PR 経由で統合してください。"
    exit 1
  fi

  if [[ ! "${current_branch}" =~ ${TOPIC_BRANCH_REGEX} ]]; then
    echo "[branch-policy] branch 名 '${current_branch}' は許可形式ではありません。"
    echo "[branch-policy] 許可形式: <type>/<topic>"
    echo "[branch-policy] 許可 type: feat|fix|refactor|docs|test|chore|exp|ops|hotfix"
    exit 1
  fi
fi

while read -r _local_ref _local_sha remote_ref _remote_sha; do
  if [[ -z "${remote_ref:-}" ]]; then
    continue
  fi

  if [[ "${remote_ref}" =~ ${PROTECTED_REF_REGEX} ]]; then
    echo "[branch-policy] protected branch '${remote_ref#refs/heads/}' 宛の直接 push は禁止です。"
    echo "[branch-policy] topic branch へ push し、PR で統合してください。"
    exit 1
  fi
done

history_range=""
upstream_ref="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
if [[ -n "${upstream_ref}" ]]; then
  history_range="${upstream_ref}..HEAD"
elif git rev-parse --verify "${history_base_ref}" >/dev/null 2>&1; then
  history_range="${history_base_ref}..HEAD"
else
  echo "[branch-policy] upstream/base ref が見つからないため history 検証をスキップします。"
  exit 0
fi

merge_commit_count="$(git rev-list --count --merges "${history_range}")"
if (( merge_commit_count > 0 )); then
  echo "[branch-policy] topic branch の outgoing history に merge commit が ${merge_commit_count} 件あります。"
  echo "[branch-policy] push 前に rebase で線形履歴へ整理してください。"
  exit 1
fi

if [[ -n "${history_max_commits}" ]] && (( history_max_commits > 0 )); then
  outgoing_commit_count="$(git rev-list --count "${history_range}")"
  if (( outgoing_commit_count > history_max_commits )); then
    echo "[branch-policy] outgoing commit 数 ${outgoing_commit_count} が上限 ${history_max_commits} を超えています。"
    echo "[branch-policy] interactive rebase/autosquash で履歴を整理してから push してください。"
    echo "[branch-policy] この上限はローカル/チーム運用の override です。必要なら BRANCH_HISTORY_MAX_COMMITS=<n> を再設定してください。"
    exit 1
  fi
fi

exit 0
