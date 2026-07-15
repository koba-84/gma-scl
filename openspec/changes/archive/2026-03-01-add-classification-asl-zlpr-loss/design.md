## Context

現行 `FinetuneLitModule` は `BCEWithLogitsLoss` を直接保持しており、classification ステージで損失関数を差し替える拡張点がない。OpenSpec 運用上、損失の追加は設定解決可能性と最小自己テストを同時に満たす必要がある。

## Goals / Non-Goals

**Goals:**

- classification で `bce` / `asymmetric` / `zlpr` を設定選択できる。
- ASL のハイパーパラメータ（`gamma_pos`, `gamma_neg`, `margin`）を設定可能にする。
- 追加実装の自己テストと設定テストを通す。

**Non-Goals:**

- contrastive 損失実装の変更。
- 新しい評価指標や推論ロジックの追加。

## Decisions

- 損失実装を `src/models/loss/classification.py` に集約する。
  - 理由: 既存の loss 実装配置と整合し、自己テスト運用を統一できる。
- `FinetuneLitModule` には `loss_name` と `loss_kwargs` を追加し、内部ファクトリで `criterion` を解決する。
  - 理由: Hydra 側で簡潔に切り替え可能で、既存学習フローへの影響を最小化できる。
- ZLPR は log-sum-exp ベースの pairwise ranking 損失として実装する。
  - 理由: マルチラベル分類の正負ラベル分離を直接最適化できる。

## Risks / Trade-offs

- [Risk] ZLPR の定義差分（文献実装差）で期待値とズレる可能性。 → Mitigation: 実装式をコードコメントとテストで固定し、有限値と勾配計算を検証する。
- [Risk] loss 設定追加で設定ミスが増える可能性。 → Mitigation: 未知 loss 名は `ValueError` で即時失敗させる。
