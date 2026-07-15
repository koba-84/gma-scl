# Design

## Overview

MXCLR はすでに label description の構築を初期化時に行う。これと同じタイミングで、agg 実装が要求する train.csv 由来統計を自動ロードする。要求の所在は concrete agg module に寄せ、MXCLR は共通 contract のみを見る。

## Decisions

### Decision 1: agg module が必要統計量を宣言する

各 agg 実装に `required_label_stats()` を追加し、`npmi` `label_idf` `label_frequency` の必要集合を返す。

- Rationale: concrete agg ごとの差分を top-level loss module に持ち込まないため。

### Decision 2: MXCLR は宣言に基づいて統計量をロードする

`MXCLR.__init__` で agg の `required_label_stats()` を読み、未注入の統計量のみ `src/models/loss/components/label_stats.py` から計算して buffer に保持する。

- `idf_chamfer`: `npmi`, `label_idf`
- `distill_idf_chamfer`: `label_idf`
- `wmd`: `npmi`, `label_frequency`
- `wrd`, `uot`: `npmi`

### Decision 3: label_frequency helper を shared label_stats module に追加する

transport 系で必要な label frequency も train.csv から一貫した契約で取得できるよう、`compute_frequency()` を追加する。

- Rationale: frequency 計算を MXCLR 内へ重複実装しないため。

## Validation

- `uv run pytest tests/test_contrastive_losses.py -k "mxclr or idf_chamfer"`
- `PROJECT_ROOT=$(pwd) uv run python src/train.py hparams_search=contrastive_epoch --cfg hydra -p hydra.sweeper.params --resolve`
