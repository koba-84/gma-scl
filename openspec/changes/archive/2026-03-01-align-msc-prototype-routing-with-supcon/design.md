## Context

`supcon` 側では prototype はモデル内の学習可能パラメータとして保持され、trainer が正規化して各 loss に明示供給している。一方 `multi-label` の MSC は `prototype=None` 時にバッチから内部生成するため、同一 loss 名でも供給契約が異なる。

## Goals / Non-Goals

**Goals:**

- MSC の prototype 供給契約を `supcon` と同じ「外部明示供給」に揃える。
- Lightning 側で学習可能 prototype を optimizer 対象に含める。
- MSC の fail-fast を導入して暗黙分岐を除去する。

**Non-Goals:**

- base/ml_supcon/mcacr など他 loss の入出力契約変更。
- prototype を queue や datamodule で再設計する大規模改修。

## Decisions

- `ContrastiveLitModule` に `use_learnable_prototype` フラグと prototype パラメータを追加する。
- prototype 初期化は `setup(stage="fit")` で datamodule の `num_classes` と projection 出力次元から行う。
  - 理由: optimizer 構築前に parameter を確実に生成するため。
- MSC 使用時のみ `loss_fn(z, labels, prototype=normalized_prototype)` で呼び出す。
  - 理由: 他 loss のシグネチャ互換を壊さず変更影響を局所化するため。
- MSC loss では `prototype` を必須化し、自動生成関数を削除する。

## Risks / Trade-offs

- [Risk] datamodule が `num_classes` を返せない場合に初期化失敗する
  → Mitigation: fit 開始前に明示エラーで停止し、原因をログメッセージで示す。
- [Risk] projection 出力次元の推定失敗
  → Mitigation: `projection_head.model[-1].out_features` を優先し、取得不能時は例外にする。
- [Trade-off] MSC 経路の互換性を切る
  → 研究用途の方針に沿って互換レイヤーは持たない。
