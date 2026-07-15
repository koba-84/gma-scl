## 1. OpenSpec artifacts

- [x] 1.1 proposal/design/specs をレビューし、branch policy の必須要件と適用範囲を確定する

## 2. Spec sync

- [x] 2.1 main specs に branch-governance-policy を新規追加する
- [x] 2.2 main specs の version-control と precommit-quality-gate-policy に branch policy 要件を同期する

## 3. Enforcement implementation

- [x] 3.1 pre-push branch policy 検証スクリプトを追加し、protected branch 直接 push と命名違反を拒否する
- [x] 3.2 pre-commit 設定へ branch policy pre-push フックを登録する
- [x] 3.3 branch policy 検証スクリプトを shellcheck 警告ゼロに調整する

## 4. Verification

- [x] 4.1 branch policy 検証スクリプトの正常系/異常系をローカルで実行確認する
- [x] 4.2 OpenSpec status で artifacts 完了を確認し、検証結果を tasks.md に記録する

検証メモ（2026-03-03）:

- branch policy script:
  - 正常系: `feat/branch-policy-check` から `refs/heads/feat/branch-policy-check` へ push 想定入力で終了コード 0
  - 異常系1: `invalidbranch` は命名規約違反として失敗
  - 異常系2: `refs/heads/main` 宛 push は protected branch 宛として失敗
  - ログ: `tmp/branch-policy-check.log`
  - 品質ゲート: `uv run pre-commit run shellcheck --files scripts/validate_branch_policy.sh` が成功
- OpenSpec status:
  - `uv run openspec status --change define-branch-governance-policy --json` で artifacts `proposal/design/specs/tasks` がすべて `done`
