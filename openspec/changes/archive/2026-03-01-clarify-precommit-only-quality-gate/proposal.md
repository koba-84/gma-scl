## Why

個人開発運用では CI を必須とせず、ローカル pre-commit を品質ゲートの中心に据えたい。一方で現行仕様には push 前 pytest 必須要件が残っており、運用方針と不整合がある。

## What Changes

- 品質ゲートの必須要件を「pre-commit 実行成功」に明確化する。
- push 前の `uv run pytest -m "not slow"` 必須要件を仕様から外し、任意の追加検証として扱う。
- commit 粒度の規約（単一論理変更）は維持する。

## Capabilities

### New Capabilities

- `precommit-quality-gate-policy`: pre-commit を必須品質ゲートとする運用要件を定義する。

### Modified Capabilities

- `version-control`: push 前検証要件を pre-commit 前提へ更新する。
- `training`: pre-push fast test 必須の要件を運用方針に合わせて更新する。

## Impact

- 影響ファイル: `openspec/specs/version-control.md`, `openspec/specs/training/spec.md`, `openspec/specs/training.md`, `openspec/specs/dev-quality-tooling/spec.md`
- 実装コードの挙動変更: なし
- 開発フロー: push 前 pytest は推奨に変更し、pre-commit 成功を必須とする
