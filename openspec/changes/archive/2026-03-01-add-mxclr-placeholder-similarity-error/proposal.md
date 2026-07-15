## Why

mxclr は追加済みですが、類似度グラフ生成が暫定的に Jaccard 固定のままです。研究コードとして意図しない暫定仕様で実験が進むことを避けるため、未実装であることを明示的に失敗させます。あわせて埋め込み正規化の責務を明示し、処理場所の重複を防ぎます。

## What Changes

- `src/models/loss/mxclr.py` の Jaccard ベース類似度グラフ生成を明示的な未実装エラーに変更する。
- mxclr の自己テストを、未実装エラーを期待する検証に更新する。
- MXCLR の埋め込み正規化を loss 側で行わず、`ContrastiveLitModule._project` に一本化する。
- Hydra で MXCLR を選択できるよう `configs/contrastive/model/mxclr.yaml` を追加する。
- OpenSpec に、埋め込み正規化の処理場所を明記する。
- **BREAKING**: 既存の `MXCLR.similarity_graph(...)` 呼び出しは成功せず `NotImplementedError` を送出する。

## Capabilities

### New Capabilities

- `mxclr-loss`: mxclr の類似度グラフ生成が未実装時に必ず明示的なエラーを返し、暫定 Jaccard 実装を使用不能にする。

### Modified Capabilities

- `training`: contrastive loss 入力前の埋め込み正規化を `ContrastiveLitModule._project` に固定し、loss 側重複正規化を禁止する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `src/models/contrastive_module.py`, `configs/contrastive/model/mxclr.yaml`, `openspec/specs/training.md`
- 影響運用: similarity_graph を使う呼び出しは停止し、将来の正式実装が入るまで利用不可となる
