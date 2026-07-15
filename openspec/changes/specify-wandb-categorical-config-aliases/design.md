## Overview

W&B comparison 用 alias は、structured config を保持する nested subtree と衝突しない sibling leaf に統一する。有限選択肢は `*_name` 命名に揃え、数値 alias は既存の leaf key を維持する。

## Canonical Alias Paths

- `contrastive.model.loss_name`
- `contrastive.model.loss_fn.agg_name`
- `classification.model.loss_name`

`contrastive.model.loss_fn.tau_s` は数値比較用 alias なので現行 leaf を維持する。

## Source of Truth

- contrastive loss 名は `loss_fn._target_` の module 名から導出する
- MXCLR agg 名は `loss_fn.agg._target_` の module 名から導出する
- classification loss 名は criterion `_target_` から canonical short name へ写像する

## Validation

- `configs/contrastive/model/*.yaml` の support 対象 loss を総当たりで検証する
- `configs/contrastive/model/agg/*.yaml` の support 対象 agg を総当たりで検証する
- `configs/classification/loss/*.yaml` の support 対象 loss を総当たりで検証する
- logging helper と backfill helper の双方で同じ alias path が出ることを確認する
