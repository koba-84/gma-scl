## Context

現在の設定は `configs/contrastive/train.yaml` で `contrastive.trainer.max_epochs=1`、一方で `configs/hparams_search/contrastive_epoch.yaml` では 80 を指定しており、通常実行と探索設定の前提が分離している。実験再現時に「標準設定」がどちらか曖昧になるため、contrastive 学習の epoch を仕様として単一値に固定する。

## Goals / Non-Goals

**Goals:**

- contrastive ステージの既定 epoch を 80 に統一する。
- OpenSpec の training 仕様で「contrastive epoch は 80 固定」を明文化する。
- 既存の設定解決フロー (`--cfg job --resolve`) で整合性を確認する。

**Non-Goals:**

- classification ステージの epoch や最適化設定の変更。
- loss 実装やモデル構造の変更。
- 新しい探索軸（複数 epoch 値）の導入。

## Decisions

- Decision 1: `configs/contrastive/train.yaml` の `trainer.max_epochs` を 80 に更新する。

  - Rationale: 通常実行の既定値を仕様値に一致させることで、実験条件を明確化できる。
  - Alternative: 実行時 override のみで 80 を指定する。却下理由: 指定漏れによる条件ブレを防げない。

- Decision 2: `configs/hparams_search/contrastive_epoch.yaml` は固定値 80 を保持し、再現用プリセットとして扱う。

  - Rationale: 既存運用ファイルを維持しつつ、仕様と実装の不整合を解消できる。
  - Alternative: 当該ファイルを削除する。却下理由: 既存の実験起動手順への影響が大きい。

- Decision 3: training spec の epoch sweep 記述を削除し、固定 epoch ルールへ置換する。

  - Rationale: ドキュメントと設定値の乖離を解消する。
  - Alternative: 旧記述を注記付きで残す。却下理由: 仕様としての規範性が下がる。

## Risks / Trade-offs

- [Risk] 学習時間が従来の既定値 (1 epoch) より増加する。→ Mitigation: 短時間検証は `configs/test.yaml` などの専用設定を使用する。
- [Trade-off] epoch 比較実験の手軽さは下がる。→ Mitigation: 比較実験が必要な場合は別 change で探索専用設定を再定義する。
