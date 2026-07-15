## Why

現行の pytest は train/sweep 中心で、データ前処理やサンプラーの境界条件を素早く検知する単体テスト層が不足している。ML プロジェクトで推奨される「軽量 unit + 統合 + 実機」の階層を満たし、回帰検知速度を上げる。

## What Changes

- `src/data/components/gcbs.py` 末尾に、入力検証・出力 permutation 妥当性・Sampler 挙動を検証する自己テストを追加する。
- `src/data/components/dpp.py` 末尾に、初期化前エラー・embedding 形状検証・drop_last と k 制約を検証する自己テストを追加する。
- `src/data/components/classification_dataset.py` 末尾に、CSV 契約（必須列/値型/欠損）を検証する自己テストを追加する。
- `src/data/classification_datamodule.py` と `src/data/contrastive_datamodule.py` 末尾に、dataloader 構築と主要な異常系を検証する自己テストを追加する。
- `src/models/components/mlp_head.py` 末尾に、shape 契約と異常入力を検証する自己テストを追加する。
- 追加テストを `openspec/specs/training.md` のテスト階層仕様へ同期する。

## Capabilities

### Modified Capabilities

- `training`: データコンポーネント層の unit/data-contract テスト要件を追加する。

## Impact

- 影響コード: `src/data/components/gcbs.py`, `src/data/components/dpp.py`, `src/data/components/classification_dataset.py`, `src/data/classification_datamodule.py`, `src/data/contrastive_datamodule.py`, `src/models/components/mlp_head.py`
- 影響仕様: `openspec/changes/add-ml-test-granularity/specs/training/spec.md`, `openspec/specs/training.md`
- 影響運用: 変更時は既存統合テストに加え、データコンポーネント単体テストを常時実行する。
