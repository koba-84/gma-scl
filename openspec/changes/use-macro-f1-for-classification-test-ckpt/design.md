## Context

`src/train.py` の test 実行は `trainer.checkpoint_callback.best_model_path` を優先して読み込むため、
classification test の実質的な重み選択基準は callback 側 monitor metric で決まる。
現在の monitor は `classification/val/f1_micro` であり、要件の「macro-F1 基準」と不一致。

## Goals / Non-Goals

**Goals:**
- classification の checkpoint 選択基準を `classification/val/f1_macro` に統一する。
- 設定テストで monitor 値を固定し、将来の設定変更で回帰しないようにする。
- evaluation spec に test 用 best checkpoint の基準を明文化する。

**Non-Goals:**
- metric の計算ロジック変更（`FinetuneLitModule` の metric 実装変更は行わない）。
- test 実行フローや checkpoint 削除フローの変更。

## Decisions

- 変更点は `configs/callbacks/default.yaml` の `model_checkpoint.monitor` のみとする。
- テストでは `cfg_train.callbacks.model_checkpoint.monitor` を直接検証し、
  classification stage が参照する monitor 文字列を保証する。
- 仕様は evaluation spec の「test で使う重み」節に checkpoint monitor 基準として追記する。

## Risks / Trade-offs

- [Risk] macro-F1 最適化により micro-F1 がわずかに低下する可能性
  - Mitigation: 目的は test 用重み選択基準の変更であり、評価時は macro/micro の両方を記録して判断する。
- [Risk] callback 設定変更の意図が仕様に残らない
  - Mitigation: evaluation spec に monitor 基準を明文化して drift を防ぐ。
