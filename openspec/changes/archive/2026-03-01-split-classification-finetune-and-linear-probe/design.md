## Context

現行の classification model 設定ファイル `finetune.yaml` は `encoder_freeze: true` となっており、実質的には linear probe 構成である。ファイル名と挙動の不一致が設定選択時の認知負荷につながっている。

## Goals / Non-Goals

**Goals:**

- freeze あり設定を `linear_probe` として明示化する。
- 既定の `finetune` 設定を非 freeze にして、名前と挙動を一致させる。
- Hydra の model group で両設定を明示的に選択できる状態にする。

**Non-Goals:**

- optimizer/scheduler や encoder モデル種別の変更。
- classification 以外のステージ設定変更。

## Decisions

- Decision 1: 既存 `finetune.yaml` の内容を `linear_probe.yaml` へ移す。

  - Rationale: 既存 freeze 設定をそのまま保持しつつ、用途を名前で明確化できる。
  - Alternative: `finetune.yaml` をそのまま残して別名を追加。却下理由: 名称と実態の不整合が残る。

- Decision 2: 新規 `finetune.yaml` は `linear_probe` をベースに `encoder_freeze: false` のみ変更する。

  - Rationale: 差分を最小に保ち、比較実験の再現性を担保できる。
  - Alternative: 他ハイパーパラメータも再設計。却下理由: 今回の要求範囲を超える。

## Risks / Trade-offs

- [Risk] 既存の `classification/model=finetune` 利用時に挙動が freeze ありからなしへ変わる。→ Mitigation: freeze が必要な実験は `classification/model=linear_probe` を明示指定する。
- [Trade-off] model 設定ファイルが 2 つに増える。→ Mitigation: 命名を用途ベースで固定し、役割を明確化する。
