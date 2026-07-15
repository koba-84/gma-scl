## Context

今回の不整合は 2 系統ある。1 つ目は既存 run の `contrastive.model.loss_name` 欠損で、比較列に必要な alias が backfill 対象 run に揃っていないこと。2 つ目は contrastive stage 側で `define_metric("contrastive/train/*", step_metric="contrastive/epoch")` を定義している一方、Lightning の `WandbLogger` が既定で `* -> trainer/global_step` を定義するため、同じ metric が 2 本の x 軸定義に一致して UI 上で重複系列として見えることだ。

既存 run の欠損は運用上すでに発生しているため、今後の logging 実装修正だけでは比較可能性が回復しない。backfill 実行と今後の metric 契約整理を同時に扱う必要がある。

## Goals / Non-Goals

**Goals:**

- 既存の対象 run に対して `contrastive.model.loss_name` を backfill で補完する
- 学習時 logging で比較用 alias を安定して記録する
- contrastive train/val metric が W&B 上で単一の x 軸定義だけに一致するようにする
- 上記契約を pytest で固定し、再発を防ぐ

**Non-Goals:**

- W&B 上の過去 run 全件を自動列挙して一括更新すること
- classification metric の軸定義ルールを全面的に作り直すこと
- W&B 以外の logger の挙動を変更すること

## Decisions

- `contrastive.model.loss_name` の backfill は既存の `scripts/backfill_wandb_config.py` を使い、対象 run id を明示指定して更新する
  - 代替案: 新しい専用 backfill script を追加する
  - 不採用理由: 既存 helper と alias 導出を再利用した方が保守点が増えない
- contrastive stage の `define_metric` は wildcard ではなく、必要な metric 名だけを個別に `contrastive/epoch` 軸へ結び付ける
  - 代替案: `WandbLogger` 側の既定 `*` 定義を無効化または上書きする
  - 不採用理由: Lightning 側既定挙動への依存が強く、局所修正では安全に制御しづらい
- `contrastive/train/loss` と `contrastive/val/loss` のみを stage 軸へ明示定義し、他の metric は logger 既定の `trainer/global_step` に委ねる
  - 代替案: contrastive 系 metric 全体を個別定義へ展開する
  - 不採用理由: 現時点で重複が問題化しているのは epoch 集約 loss 系だけで、必要最小限の整理に留める
- テストでは alias 導出結果だけでなく、`define_metric` 呼び出し内容そのものを検証する
  - 代替案: W&B UI の見え方だけを手動確認する
  - 不採用理由: 実装契約がコード上で固定されず再発防止にならない

## Risks / Trade-offs

- [Risk] backfill 対象 run を誤ると不要な config 更新が入る
  - Mitigation: 更新対象 run id を明示し、dry-run 出力を確認してから `--apply` を実行する
- [Risk] wildcard をやめることで将来追加される contrastive metric が epoch 軸に乗らない
  - Mitigation: 今回は重複が問題化した loss metric のみを契約化し、新規 epoch metric を追加する際は requirement とテストを更新する
- [Risk] Lightning/W&B の内部仕様変更で `define_metric` の順序や既定定義が変わる
  - Mitigation: 既定 wildcard と衝突しない個別 metric 名定義を使い、呼び出し内容をテストで監視する
