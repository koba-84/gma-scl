## Context

`IdfChamferGraph` は `transport_lambda` 引数を受け取り、semantic similarity と NPMI の混合重みとして使う。一方、Hydra config の `idf_chamfer.yaml` は `_target_` しか定義していないため、struct mode 下では `contrastive.model.loss_fn.agg.transport_lambda=...` の通常 override が失敗する。

## Goals / Non-Goals

**Goals:**

- `idf_chamfer` config で `transport_lambda` を通常 override できるようにする
- 現行の実装既定値 `5e-1` と config 既定値を一致させる

**Non-Goals:**

- `IdfChamferGraph` の計算式変更
- 他 agg family の既定値変更

## Decisions

- Decision 1: `configs/contrastive/model/agg/idf_chamfer.yaml` に `transport_lambda: 5e-1` を追加する
  - Rationale: 実装の既定値と揃えつつ、Hydra struct error を最小変更で解消できる
  - Alternative considered: `+contrastive.model.loss_fn.agg.transport_lambda=...` を毎回使う
  - Rejected because: 恒久設定や sweeper 定義で毎回 `+` を要求するのは扱いづらい

## Risks / Trade-offs

- [Risk] config 既定値と Python 既定値が将来ずれる → Mitigation: 既定値を同じ `5e-1` に固定し、spec にも明記する
