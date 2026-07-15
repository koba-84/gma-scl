## Context

このリポジトリの train config は contrastive と classification の 2 段階を既定で含む。classification の trainer は stage-local config を持つため、既定 epoch 数の変更は `configs/classification/train.yaml` を更新すれば足りる。一方 `configs/hparams_search/contrastive_epoch.yaml` は探索専用 preset であり、ここに model family と loss hyperparameter を明示すれば、Hydra の `--cfg job --resolve` で再現条件を直接確認できる。

## Goals / Non-Goals

**Goals:**

- classification の既定 epoch 数を 40 に短縮する
- contrastive_epoch を MXCLR + `idf_chamfer` preset として固定する
- MXCLR sweep preset の主要値を spec と config で一致させる

**Non-Goals:**

- 新しい loss 実装や agg 実装の追加
- canonical な learning-rate grid 自体の変更
- 既存の default MXCLR config の既定 agg の変更

## Decisions

- Decision 1: classification の既定 epoch は stage-local trainer で 40 に固定する
  - Rationale: 現行実装は各段階が個別 trainer を持つため、global trainer ではなく classification stage だけを変えるのが最小変更になる
  - Alternative considered: global trainer の `max_epochs` を変更する
  - Rejected because: contrastive stage まで影響し、2 段階構成の意図に反する
- Decision 2: contrastive_epoch は `contrastive/model: mxclr` と `contrastive/model/agg@contrastive.model.loss_fn: idf_chamfer` を明示する
  - Rationale: 現行 config group 名は `idf_chamfer` であり、Hydra override と整合する正式名を使う必要がある
  - Alternative considered: `chamfer_idf` という別名を追加する
  - Rejected because: 後方互換レイヤー追加になり、このリポジトリ方針に反する
- Decision 3: NPMI 混合重みは agg config の `transport_lambda: 5e-1`、focal 強度は `contrastive.model.loss_fn.gamma: 2` で指定する
  - Rationale: 実装上の受け口は `IdfChamferGraph.transport_lambda` と `MXCLR.gamma` であり、設定キーをそのまま使うのが最も明確

## Risks / Trade-offs

- [Risk] classification の既定 epoch 短縮で長め学習前提の比較結果と直接比較しづらくなる → Mitigation: 変更を spec と OpenSpec change に残し、必要時は override で個別に延長する
- [Risk] sweep preset の model family 変更で従来の base 探索前提を誤読する可能性がある → Mitigation: training spec に MXCLR preset であることを明記する
