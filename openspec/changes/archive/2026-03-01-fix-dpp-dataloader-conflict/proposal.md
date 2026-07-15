## Why

DPPサンプラ利用時にDataLoaderへ排他的な引数を同時に渡しており、学習ジョブが起動直後に失敗する。ハイパーパラメータ探索で `sampler_type=dpp` を含む設定があるため、早急に修正が必要である。

## What Changes

- contrastive用DataLoaderの生成を `sampler_type` ごとに分岐し、DPP時は `batch_sampler` のみを渡す。
- GCBS/通常shuffle時の既存挙動は維持し、`batch_size` と `sampler` の組み合わせを継続利用する。
- DPP時の排他条件を満たすことを確認する実行検証手順を追加する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: contrastive train_dataloader の sampler 設定仕様を修正し、DPP利用時の DataLoader 引数衝突を防止する。

## Impact

- 影響コード: `src/data/contrastive_datamodule.py`
- 影響範囲: contrastive 学習の train dataloader 構築時のみ
- 外部API/依存ライブラリ変更: なし
