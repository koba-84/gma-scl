## Why

commit message policy は定義されているが、自動検証がないため運用逸脱が発生する。再現性重視の履歴品質を担保するため、commit 作成時と push 前の両方で機械的に検証する必要がある。

## What Changes

- commit-msg フックで件名形式と必須本文（Why/Validation/Reproducibility）を自動検証する。
- pre-push フックで push 対象コミット群の commit message を再検証する。
- 検証ロジックをスクリプト化し、仕様に沿ったエラーメッセージで修正可能性を上げる。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `commit-message-policy`: 仕様準拠を自動検証する実行ゲートを追加する
- `precommit-quality-gate-policy`: commit-msg/pre-push 段の品質ゲート要件を追加する

## Impact

- 影響ファイル: `.pre-commit-config.yaml`, `scripts/`
- 影響仕様: `openspec/specs/commit-message-policy/spec.md`, `openspec/specs/precommit-quality-gate-policy/spec.md`
- 影響運用: commit/push 時にメッセージ不整合は即時失敗する
