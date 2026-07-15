## Context

現在の W&B hyperparameter logging は `base_cfg` 全体を `OmegaConf.to_container(..., resolve=True)` で plain dict 化し、そのまま `contrastive` / `classification` を送っています。一方、実行時の trainer は `_run_stage()` 内で `stage_cfg.trainer` と top-level `trainer` を merge して生成しており、stage ごとの実効設定は logging 側に戻されていません。そのため、partial override や runtime 補完が入ったキーが W&B config では欠損し得ます。

さらに、直近 2 run は既に W&B 上に存在するため、コード修正だけでは履歴の再現性が回復しません。既存 run に対する限定的な config backfill が必要です。

## Goals / Non-Goals

**Goals:**

- stage 実行時の実効 `contrastive` / `classification` config を W&B に記録する
- stage override を含む logging regression test を追加する
- 直近 2 run の欠損 config を API で安全に補完する

**Non-Goals:**

- W&B run の metrics/history を書き換えること
- 任意 run を包括的に修正する汎用 migration 基盤を導入すること
- 実験設定そのものを変更すること

## Decisions

1. logging 入力に stage 実効 config を明示的に渡す。
   `_run_stage()` で trainer merge 後の stage config を plain dict 化し、`log_hyperparameters()` に `stage_cfg_resolved` として渡します。logging 側で base config を再構築するより、実行地点で確定した値を渡す方が責務が明確です。

2. W&B へ送る top-level `contrastive` / `classification` のうち、現在の stage だけを実効 config で置き換える。
   共有 run で両 stage を記録する構造は維持しつつ、実行中 stage の値だけを確定値で上書きします。これにより既存 UI 構造を崩さず欠損を防げます。

3. nested config に加えて leaf の flat alias を追加する。
   W&B の比較列では dot-path key を直接選ぶことが多いため、`contrastive.model.loss_fn.gamma` のような leaf alias を同時に保存します。既存の nested 表現は残し、参照性だけを補強します。

4. 既存 run backfill は小さな専用スクリプトで実施する。
   run ID を明示した限定更新にし、欠損した flat alias と推定可能な runtime 値だけを補完します。学習コードに migration 処理を混ぜず、監査しやすくします。

## Risks / Trade-offs

- [Risk] stage config の dict 化で補間や Hydra object 構造が壊れる → Mitigation: `resolve=True` の plain container に限定し、既存 interpolation テストを維持する
- [Risk] backfill 対象 run を取り違える → Mitigation: スクリプトは run ID 明示入力に限定し、更新前後の差分を表示する
- [Risk] W&B API 更新で想定外のキーを上書きする → Mitigation: 欠損キーのみ更新し、既存値があるキーは変更しない
- [Risk] flat alias が多すぎて config を読みにくくする → Mitigation: leaf 値のみ追加し、nested dict は既存構造を維持する
