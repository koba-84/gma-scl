## Why

現在の `idf_chamfer` は双方向の IDF 重み付き score を単純平均しており、BERTScore の本来の集約である Precision/Recall からの F1 と一致していません。`idf_chamfer` はそのまま残しつつ、元論文準拠の集約を比較可能にするため、新しい agg `BERTScore_F1` を追加します。

## What Changes

- MXCLR 用 agg に新規 `BERTScore_F1` を追加する。
- `BERTScore_F1` は `idf_chamfer` と同じ semantic similarity と NPMI 混合、および IDF 重み付けを使い、方向別 score を Precision/Recall として `2PR/(P+R)` で集約する。
- `idf_chamfer` は既存の算術平均 agg として残し、後方互換の alias や置換分岐は追加しない。
- Hydra config から `contrastive/model/agg@contrastive.model.loss_fn=BERTScore_F1` を選択可能にする。
- W&B comparison alias `contrastive.model.loss_fn.agg_name` に canonical 名 `BERTScore_F1` を記録する。
- MXCLR の score graph、config instantiate、W&B alias の pytest を追加・更新する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MXCLR が BERTScore 論文準拠の F1 集約 agg `BERTScore_F1` を選択でき、比較 alias に同名を記録できるようにする

## Impact

- 影響コード: `src/models/loss/agg/`, `configs/contrastive/model/agg/`, `src/utils/wandb_config_aliases.py`, `tests/`
- 影響 spec: `openspec/specs/training/spec.md`
- 追加依存なし
