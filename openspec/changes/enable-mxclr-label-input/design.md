## Context

`ContrastiveLitModule.model_step` は `self.loss_fn(z, labels)` を一貫して呼び出す。一方、MXCLR は現状 `forward(z, g_soft)` であり、この差分のため設定上は選択可能でも実学習で未接続になる。

## Goals / Non-Goals

**Goals:**

- MXCLR の入力契約を他 loss と揃える。
- `contrastive/model=mxclr` で標準学習経路を通せるようにする。
- 類似度グラフ生成を暫定実装し、自己テストで動作を検証する。

**Non-Goals:**

- MXCLR 論文再現の厳密な類似度設計。
- `ContrastiveLitModule` 側の分岐追加。

## Decisions

- `forward(self, z, target)` の `target` を shape ベースで分岐する。
  - \[N, N\]: 既に `g_soft` とみなしてそのまま使用。
  - \[N, L\]: labels とみなし `similarity_graph(labels)` で変換。
- `similarity_graph` は labels 二値化後の cosine 類似度（[0,1] へ clamp）を採用する。
  - 非 Jaccard であり、暫定実装として単純・安定。
- 正規化責務は既存仕様どおり `ContrastiveLitModule._project` に維持する。

## Risks / Trade-offs

- [Risk] cosine 類似度は最終的な研究設計と一致しない可能性がある。
  - Mitigation: 実装を `similarity_graph` に閉じ、将来差し替え可能にする。
- [Risk] shape 判定分岐で誤入力を見落とす可能性がある。
  - Mitigation: [N, D] と [N, N]/[N, L] の検証を厳密化し、例外メッセージを明確化する。
