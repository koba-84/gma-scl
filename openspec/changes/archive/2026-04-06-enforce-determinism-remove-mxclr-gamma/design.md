## Context

既存の trainer 既定値は `deterministic: False` であり、README でも手動 override を促すだけになっている。この状態では同一 seed を指定しても backend 非決定性が残り、研究コードとしての既定挙動が目的に一致しない。

一方 MXCLR は `gamma` による focal-style weighting を持つが、現行 sweep 設定でも既に未使用であり、標準学習経路の契約として残す理由が薄い。`gamma` を残すと loss 実装、Hydra 設定、main spec、テストが余計な分岐と説明を持ち続ける。

## Goals / Non-Goals

**Goals:**

- デフォルトの train 構成だけで deterministic 実行が有効になる。
- MXCLR 系 loss の公開初期化契約から `gamma` を完全に除去する。
- 仕様、設定、実装、テストが同じ契約を指す状態へ戻す。

**Non-Goals:**

- deterministic 化に伴う別種の runtime 最適化や速度改善。
- classification loss の `gamma_pos` / `gamma_neg` 契約の変更。
- MXCLR の `agg`、`tau`、`tau_s`、semantic 初期化経路の変更。

## Decisions

1. `configs/trainer/default.yaml` の既定値を `deterministic: True` に変更する。

- 理由: リポジトリの最重要要件は「明示 override なしで再現可能な標準経路」を持つことだから。
- 代替案: README と spec に override 必須とだけ書き、既定値は `False` のままにする。
  - 不採用理由: 手動運用に依存し、再現性要件を設定既定値で保証できない。

2. MXCLR の loss 本体は soft target cross entropy のみを残し、focal-style weighting を完全に削除する。

- 理由: 不要な scalar hyperparameter をなくし、Hydra 設定と loss 契約を単純化できる。
- 代替案: `gamma=0` を hidden default として内部実装だけ残す。
  - 不採用理由: ユーザー要求は `contrastive.model.loss_fn.gamma` の削除であり、死んだ分岐を残す意味がない。

3. MXCLRRank も親クラス契約に合わせて `gamma` 非依存へ揃える。

- 理由: rank variant だけ旧引数を残すと API が分岐し、将来の再利用や設定解決で混乱する。

## Risks / Trade-offs

- [Risk] deterministic 既定化により学習速度が低下する。
  Mitigation: 速度低下は仕様として受け入れ、既定再現性を優先する。必要な非決定実験は明示 override に限定する。

- [Risk] `gamma` を参照する既存 override や古い branch が解決エラーになる。
  Mitigation: 後方互換レイヤーは作らず、spec と config を更新して branch 側は rebase で追従させる。
