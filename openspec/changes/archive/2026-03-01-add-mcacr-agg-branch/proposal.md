## Why

MCACR の負例重み計算は集約式が固定で、MXCLR と同様に集約方式の比較実験を同一実装で切り替えできない。agg 引数で切り替え可能にして、条件差分を設定で明示できるようにする。

## What Changes

- MCACRLoss に agg 引数を追加し、負例側の類似度集約式を分岐可能にする。
- repulse_weight 計算の集約を agg に応じて `mean` / `self_norm` で切り替える。
- `configs/contrastive/model/mcacr.yaml` に agg 設定を追加する。
- MCACR 自己テストに agg 分岐と不正値検証を追加する。

## Capabilities

### New Capabilities

- `mcacr-aggregation-selection`: MCACR が agg 引数で負例重み集約方式を選択できることを定義する。

### Modified Capabilities

- `training`: MCACR 初期化契約に agg 設定を追加する。

## Impact

- 影響コード: src/models/loss/mcacr.py, configs/contrastive/model/mcacr.yaml
- 影響仕様: openspec/specs/training.md, openspec/specs/training/spec.md
- 影響検証: uv run python src/models/loss/mcacr.py
