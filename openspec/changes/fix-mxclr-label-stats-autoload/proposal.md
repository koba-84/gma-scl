# Proposal

## Summary

`configs/hparams_search/contrastive_epoch.yaml` は `contrastive/model=mxclr` と `contrastive/model/agg@contrastive.model.loss_fn=idf_chamfer` を解決するが、実行時の `MXCLR` は `idf_chamfer` に必要な `npmi` と `label_idf` を自動初期化していない。そのため `score_graph()` で `ValueError("npmi is required for idf_chamfer.")` が発生し、設定が実行不能になっている。

## Problem

- `MXCLR` は agg 実装に応じた label statistics の必要量を知らず、明示注入がない限り `label_npmi` / `label_idf` / `label_frequency` を空のまま保持する。
- `idf_chamfer` 系や transport 系 agg は train.csv 由来統計を必須とするため、Hydra で設定解決できても学習開始時に失敗する。
- 現在の main spec には「MXCLR が agg ごとに必要な train.csv 統計を自動ロードする」契約がない。

## Goals

- MXCLR が選択された agg 実装の要求に応じて train.csv 由来統計を初期化時に自動ロードする。
- `contrastive_epoch.yaml` の `mxclr + idf_chamfer` preset を instantiate 可能にする。
- agg ごとの統計要件を concrete agg module 側で宣言し、`src/models/loss/mxclr.py` に concrete agg 分岐を増やさない。

## Non-Goals

- `idf_chamfer` や transport agg の数式変更。
- Hydra sweep 空間や学習 hyperparameter の変更。
