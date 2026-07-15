## Why

version-control 仕様の `BRANCH_HISTORY_MAX_COMMITS=30` 既定値は、一次資料にある Git / GitHub / GitLab の推奨を直接根拠にしたものではない。根拠の薄い固定値を必須ルールとして運用すると、仕様の説明責任が弱くなるため、source-backed な履歴整理ポリシーへ改める。

## What Changes

- topic branch 履歴整理の必須条件を「線形履歴」「単一トピック」「small and focused PR」「squash/rebase merge 前提」に揃える。
- `BRANCH_HISTORY_MAX_COMMITS` は既定値付きの hard gate ではなく、必要なときに明示設定する任意 override に変更する。
- `scripts/validate_branch_policy.sh` から commit 数 30 の既定 enforcement を削除し、merge commit 禁止と protected branch 直 push 禁止を主 gate にする。

## Capabilities

### Modified Capabilities

- `version-control`: topic branch history の必須条件と pre-push 自動検証の仕様を source-backed な内容へ更新する

## Impact

- 影響仕様:
  - `openspec/specs/version-control.md`
- 影響実装:
  - `scripts/validate_branch_policy.sh`
