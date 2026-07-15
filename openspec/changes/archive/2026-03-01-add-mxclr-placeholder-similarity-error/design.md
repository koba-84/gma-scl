## Context

現状の mxclr 実装は `similarity_graph` を提供し、将来の類似度定義で `g_soft` を構築する想定です。一方で正式仕様は後続導入予定であり、現時点では確定していません。また contrastive 学習では `ContrastiveLitModule._project` が投影後埋め込みの正規化を実施しており、loss 側で同処理を持つと責務が重複します。

## Goals / Non-Goals

**Goals:**

- Jaccard 由来の暫定挙動を即時に無効化する。
- 実装未完了であることを `NotImplementedError` で明示する。
- 自己テストで未実装状態を明確に検証する。
- 埋め込み正規化の処理場所を `ContrastiveLitModule._project` に一本化する。
- Hydra 設定から `contrastive/model=mxclr` を解決可能にする。

**Non-Goals:**

- 新しい類似度アルゴリズムの導入。
- Hydra 設定や学習フローへの mxclr 統合。

## Decisions

- `MXCLR.similarity_graph` は常に `NotImplementedError` を送出する。
  - 理由: 暫定挙動の実行を確実に防ぎ、誤実験を回避するため。
- `forward` 本体は維持する。
  - 理由: 将来、外部で生成した `g_soft` を使う経路を残し、差分を最小化するため。
- `MXCLR.forward` から埋め込み正規化を除去する。
  - 理由: 正規化責務を `ContrastiveLitModule._project` に集約し、処理場所を一意化するため。
- `configs/contrastive/model/mxclr.yaml` を追加し、`loss_fn._target_` は `src.models.loss.mxclr.MXCLR` を参照する。
  - 理由: 既存 loss 設定と同じ経路で選択可能にし、設定運用を統一するため。
- `__main__` 自己テストは「未実装エラーが発生すること」を成功条件にする。
  - 理由: 仕様どおり未実装状態であることを自動検証できるため。

## Risks / Trade-offs

- [Risk] 既存の `similarity_graph` 利用コードが失敗する。
  - Mitigation: 例外メッセージで未実装であることと実装予定の意図を明示する。
- [Risk] `MXCLR.forward` を単独利用する呼び出しで入力正規化が前提になる。
  - Mitigation: OpenSpec と docstring に入力前提を明記する。
- [Trade-off] 現時点では mxclr の即時利用性が下がる。
  - Mitigation: 誤った暫定仕様での実験を防ぐことを優先する。
