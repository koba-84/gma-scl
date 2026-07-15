## Context

既存の W&B alias 導出は `loss_name` の一部を明示 map に依存している。一方で contrastive loss は `_target_` の module 名がそのまま比較用キーとして使えるため、module 名導出へ寄せた方が新規 loss 追加時に保守しやすい。`agg` も同じく `_target_` の module 名から導出できる。`tau_s` だけは MXCLR_PROTO schedule 版で leaf が存在しないため、比較用 alias として `tau_s_schedule.start` を使う。

## Decisions

- contrastive loss 名は `_target_.split(".")[-2]` で導出する
- contrastive agg 名も `loss_fn.agg._target_.split(".")[-2]` で導出する
- classification loss 名だけは既存比較キー互換のため明示 map を維持する
- logging と backfill は共通 helper `derive_wandb_config_aliases` を使用する

## Risks

- 既存 run の contrastive loss alias が新ルールと不一致になる
  - W&B Public API で既存 run を変換して揃える
