## Why

Hypothesis は導入済みだが、探索設定と再現手順がテストコード内に分散しており、ローカル実行と CI 実行の運用基準が固定されていない。profile と実行手順を明文化して、探索強度と再現性を一貫運用できるようにする。

## What Changes

- pytest 起動時に Hypothesis profile を登録・読込する共通設定を追加する。
- property-based test を profile ベース運用に揃え、局所 `deadline=None` 指定を廃止する。
- README に seed/profile を使った再現実行手順を追記する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- dev-quality-tooling: Hypothesis の探索設定と再現実行手順を標準化する。

## Impact

- テスト設定: tests/conftest.py
- テスト実装: tests/property_based.py
- ドキュメント: README.md
- 仕様: openspec/specs/dev-quality-tooling/spec.md
