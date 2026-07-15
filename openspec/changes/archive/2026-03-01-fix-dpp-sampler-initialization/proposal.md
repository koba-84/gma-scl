## Why

DPP利用時、最初のDataLoader反復開始時点で `DPPBatchSampler` の埋め込みが未設定のままとなり、学習開始前に `RuntimeError` で停止する。これにより二次的に Lightning の teardown で `combined_loader` 例外が発生し、原因特定を難しくしている。

## What Changes

- DPPサンプラの初期化状態を判定できるAPIを追加する。
- 学習開始時にDPP埋め込みを事前初期化し、最初の DataLoader 反復前に `set_embeddings` が完了するようにする。
- 各epoch開始時の既存更新は維持し、epochごとの再計算動作は継続する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: DPP sampler の初期化タイミング要件を追加し、fit開始時に未初期化例外を発生させない。

## Impact

- 影響コード: `src/models/contrastive_module.py`, `src/data/components/dpp.py`
- 影響範囲: contrastive 学習の DPP サンプラ利用時のみ
- 外部依存/API変更: なし
