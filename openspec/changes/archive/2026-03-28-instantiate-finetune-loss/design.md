## Context

現在の classification loss は config で `loss_name` と `loss_kwargs` を与え、`FinetuneLitModule` 内の `_build_criterion` が文字列ごとに実装を選択している。一方で本リポジトリの model / optimizer / scheduler は Hydra instantiate で解決しており、loss だけが例外になっている。

## Goals / Non-Goals

**Goals:**
- classification loss 解決を Hydra instantiate に統一する
- loss 追加時に module 側の if 分岐を増やさない
- 既存の BCE / Asymmetric / ZLPR を config 差し替えだけで使える状態を維持する

**Non-Goals:**
- classification の学習挙動自体を変えること
- loss 実装そのものの数式や既定値を変えること

## Decisions

- `FinetuneLitModule` は `criterion: torch.nn.Module` を直接受け取り、`self.criterion` に保持する
- `configs/classification/loss/*.yaml` は `_target_` 付き config に変換し、strategy config から compose された `criterion` を module instantiate 時にそのまま生成する
- 既存テストは `criterion._target_` と variant ごとのパラメータ差し替えを確認する形へ更新する

## Risks / Trade-offs

- config key 名が変わるため既存 override が壊れる → OpenSpec とテストを同時更新し、後方互換 layer は持たない
- `torch.nn.BCEWithLogitsLoss` と custom loss の config 記法が混在する → 全 loss config を `_target_` 形式に揃える
