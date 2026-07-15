## Why

現在の MXCLR は `forward(z, g_soft)` 前提で、contrastive 学習の標準経路 `loss_fn(z, labels)` とインターフェースが一致していません。このままでは他 loss と同じ設定運用で利用できないため、入力契約を揃える必要があります。

## What Changes

- `src/models/loss/mxclr.py` を修正し、`forward` が `labels` 入力（[N, L]）を受け取れるようにする。
- `MXCLR.similarity_graph` を未実装エラーから暫定実装へ変更し、ラベル二値ベクトルの cosine 類似度で `g_soft` を生成する。
- `forward` では `target` が [N, N] の場合は `g_soft` として扱い、[N, L] の場合は `similarity_graph` で変換する。
- MXCLR 自己テストを、標準経路（labels 入力）と直接経路（g_soft 入力）の両方を検証する内容へ更新する。
- OpenSpec の training 仕様に、MXCLR の標準入力が labels であることを明記する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MXCLR を他 contrastive loss と同じ `loss_fn(z, labels)` 契約で利用できるようにする。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `openspec/specs/training.md`
- 影響運用: `contrastive/model=mxclr` で他 loss と同様に学習経路へ接続可能になる
