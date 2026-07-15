## Why

統合テストは増えてきたが、ML ベストプラクティスに照らすと fast integration の網羅と命名規約がまだ一貫していない。特に tests ディレクトリ配下で `test_` 接頭辞に依存した命名は冗長であり、可読性と運用統一の観点で改善余地がある。

## What Changes

- Data 品質観点（簡易 skew 検知）を fast integration に追加する。
- 再現性観点（固定 seed での sampler 経路の再現）を fast integration に追加する。
- tests 配下のファイル名から `test` 語を除去し、機能名ベースへリネームする。
- OpenSpec の training spec と change artifacts の実行コマンド表記を新命名へ同期する。

## Capabilities

### Modified Capabilities

- `training`: fast integration 粒度に data quality/reproducibility を追加し、tests 配下で `test` 語を使わない命名規約へ統一する。

## Impact

- 影響コード: `tests/*.py` 一式、`openspec/specs/training.md`
- 影響運用: pytest 収集設定を調整し、`test` 語に依存しない命名で統一する。
