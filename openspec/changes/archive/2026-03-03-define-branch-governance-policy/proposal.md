## Why

現在の OpenSpec にはブランチ命名・保護ブランチへの統合経路・ローカル/CI での強制方法が一箇所にまとまっておらず、運用判断が属人化しやすい。GitHub の rulesets / protected branches の推奨運用に合わせ、再現可能な最小ルールを明文化して強制する。

## What Changes

- ブランチ運用の新規 capability を追加し、命名規約・保護ブランチへの統合制約・PR 中心フローを定義する。
- version-control capability に、push 時のブランチ境界ルールを追加する。
- precommit-quality-gate-policy capability に、pre-push で branch policy を検証する必須ゲートを追加する。
- リポジトリ実装として pre-push branch policy 検証スクリプトとフック登録を追加する。

## Capabilities

### New Capabilities
- `branch-governance-policy`: ブランチ命名、保護ブランチ統合、PR 中心運用の必須要件を規定する

### Modified Capabilities
- `version-control`: push 時に protected branch へ直接統合しないルールを明文化する
- `precommit-quality-gate-policy`: pre-push で branch policy を検証するフック要件を追加する

## Impact

- 影響仕様: `openspec/specs/branch-governance-policy/spec.md` (新規), `openspec/specs/version-control.md`, `openspec/specs/precommit-quality-gate-policy/spec.md`
- 実装影響: `.pre-commit-config.yaml`, `scripts/validate_branch_policy.sh`
- 開発運用影響: feature/topic branch の命名規約順守、protected branch 直接 push の即時ブロック
