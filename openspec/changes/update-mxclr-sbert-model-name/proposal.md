## Why

MXCLR のラベル説明文エンコーダ既定値が `sentence-transformers/all-MiniLM-L6-v2` のままだと、現在の実験方針と設定管理の正本がずれる。再現時に Hydra 既定値と Python 側既定値が一致している必要があるため、既定の `sbert_model_name` を `sentence-transformers/all-roberta-large-v1` へ更新する。

## What Changes

- MXCLR の Hydra 既定設定で `sbert_model_name` を `sentence-transformers/all-roberta-large-v1` に変更する
- MXCLR 実装の Python 側既定値も同じモデル名へ揃える
- 既定値解決を固定する回帰テストを追加する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR の既定ラベル説明文エンコーダを `sentence-transformers/all-roberta-large-v1` に更新する

## Impact

- 影響コード: `configs/contrastive/model/mxclr.yaml`, `src/models/loss/mxclr.py`
- 影響テスト: `tests/test_configs.py`
- 運用影響: Hydra 既定の contrastive MXCLR 実験は新しい SBERT モデル名を解決する
