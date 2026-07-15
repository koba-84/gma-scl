## Why

現在のテストは例ベース中心で、境界値や入力組み合わせの網羅が人手に依存している。Hypothesis を導入して不変条件を自動探索し、回帰の早期検出を強化する。

## What Changes

- 開発依存に Hypothesis を追加する。
- 既存の純関数に対して、Hypothesis を用いた property-based test を追加する。
- README の品質チェック手順に、Hypothesis を含む実行例を追記する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- dev-quality-tooling: Hypothesis による property-based test を開発品質ワークフローに追加する。

## Impact

- 依存: pyproject.toml, uv.lock
- テスト: tests/ 配下に property-based test を追加
- ドキュメント: README.md の品質チェック手順を更新
- 仕様: openspec/specs/dev-quality-tooling/spec.md を更新
