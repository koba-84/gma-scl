## Context

現行の classification model 設定は encoder freeze の戦略と loss 種別を同じ config 群で扱っている。これにより組み合わせ実験を行う際に `linear_probe_asymmetric` のような直積設定が増えやすい。

## Goals / Non-Goals

**Goals:**

- strategy と loss を独立した Hydra config group に分離する。
- 既存の `FinetuneLitModule` 契約（`loss_name` / `loss_kwargs`）は維持する。

**Non-Goals:**

- モデル実装の再設計。
- 新しい loss や optimizer の追加。

## Decisions

- `configs/classification/strategy/{linear_probe,finetune}.yaml` で encoder_freeze と最適化設定を管理する。
- `configs/classification/loss/{bce,asymmetric,zlpr}.yaml` で loss 設定のみ上書きする。
- `configs/classification/train.yaml` は `strategy@model` と `loss@model` を順に合成する。

## Risks / Trade-offs

- [Risk] 既存の `classification/model=...` コマンドが壊れる。 → Mitigation: OpenSpec と main spec に breaking change を明記する。
- [Risk] 合成順序ミスで設定が上書きされる。 → Mitigation: `train.yaml` defaults 順序を固定し、設定解決テストを実施する。
