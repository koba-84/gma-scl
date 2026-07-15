## Context

現状の `MCACRLoss` は、負例項で NPMI 由来のラベル類似度重み（`repulse_weight`）と距離分布を組み合わせている。ユーザー要件は、同一の MCACR 枠組みを保ちつつ、負例側のラベル重みだけを除いた比較系を導入すること。既存実装の挙動は維持し、Hydra 設定で安全に切り替えられる必要がある。

## Goals / Non-Goals

**Goals:**

- `MCACR_WONEG` クラスを追加し、負例項は距離ベース重みのみ（ラベル重みなし）で計算できるようにする。
- 既存 `MCACRLoss` のロジックを壊さず、共有可能な計算部分は共通化する。
- Hydra 設定から `contrastive/model=mcacr_woneg` で解決できるようにする。
- 最小限の単体テストで import/forward/設定解決を検証する。

**Non-Goals:**

- 既存 `MCACRLoss` のアルゴリズム変更。
- 学習パイプライン全体（trainer/datamodule/sampler）の仕様変更。
- 新しい外部依存の導入。

## Decisions

1. `mcacr_woneg.py` を新設して `MCACR_WONEG` を追加し、`mcacr.py` は既存 `MCACRLoss` 専用のまま維持する。
   理由: 比較実験でクラス境界を明確にでき、`mcacr.py` に条件分岐を持ち込まずに保守できる。
   代替案: `mcacr.py` に同居。却下理由: 派生実装の意図が分岐に埋もれやすい。

2. `MCACR_WONEG` 側に専用計算関数を持ち、repulsion の重みを距離ベースのみに固定する。
   理由: `MCACRLoss` の挙動不変を担保しやすく、仕様差分を局所化できる。
   代替案: 共通関数にフラグ追加。却下理由: `mcacr.py` 側の分岐増加で可読性が下がる。

3. 設定ファイル `configs/contrastive/model/mcacr_woneg.yaml` を追加し、既存 `mcacr.yaml` と同等パラメータで `_target_` のみ差し替える。
   理由: 実験比較で設定差分を最小化できる。
   代替案: `mcacr.yaml` にフラグ追加。却下理由: 既存実験設定の意味が変わりやすい。

4. テストは GPU 不要の loss 単体テストを追加し、`MCACR_WONEG` の計算が有効値を返すことと API 公開を検証する。
   理由: 変更点に対して最短で回帰検知できる。
   代替案: 学習統合テストのみ。却下理由: 実行コストが高く原因切り分けが難しい。

## Risks / Trade-offs

- [Risk] 負例ラベル重み除外で loss スケールが変化し、既存ハイパーパラメータで不安定化する可能性
  → Mitigation: 実装は新規クラスとして分離し、既存設定を不変に保つ。比較実験は別設定で実施する。

- [Risk] 共通化時の分岐ミスで `MCACRLoss` 側の挙動が変わる可能性
  → Mitigation: 既存クラスのテスト経路を維持し、新規クラスのみ追加差分を検証する。
