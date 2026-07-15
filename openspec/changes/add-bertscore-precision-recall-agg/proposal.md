## Why

現在の MXCLR には `BERTScore_F1` はありますが、方向別 score をそのまま観測する `BERTScore_Precision` と `BERTScore_Recall` がありません。BERTScore 由来の集約を精度方向・再現方向に分けて比較できないため、F1 との関係やラベル集合方向性の影響を切り分けられるようにする必要があります。

## What Changes

- MXCLR 用 agg に新規 `BERTScore_Precision` と `BERTScore_Recall` を追加する。
- 両 agg は `BERTScore_F1` と同じ semantic similarity、NPMI 混合、IDF 重み付けを使い、方向別 score をそのまま返す。
- `BERTScore_Precision(i, j)` は source=`i` target=`j` の方向 score を返し、`BERTScore_Recall(i, j)` はその逆方向 score を返す。
- Hydra config から `contrastive/model/agg@contrastive.model.loss_fn=BERTScore_Precision` と `BERTScore_Recall` を選択可能にする。
- W&B comparison alias `contrastive.model.loss_fn.agg_name` に canonical 名 `BERTScore_Precision` と `BERTScore_Recall` を記録する。
- MXCLR の score graph、config instantiate、W&B alias の pytest を追加・更新する。

## Capabilities

### Modified Capabilities

- `training`: MXCLR が BERTScore 由来の Precision/Recall 集約 agg を選択でき、比較 alias に canonical 名を記録できるようにする

## Impact

- 影響コード: `src/models/loss/agg/`, `configs/contrastive/model/agg/`, `src/utils/wandb_config_aliases.py`, `tests/`
- 影響 spec: `openspec/specs/training/spec.md`
- 追加依存なし
