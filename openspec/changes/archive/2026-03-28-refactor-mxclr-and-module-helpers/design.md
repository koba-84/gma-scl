## Context

直近の refactor で label stats, aggregation, transport の shared helper は導入済みですが、呼び出し側にはまだ重複 loader や trivial helper が残っています。特に MXCLR は agg 文字列ごとの分岐が集中しており、transport family と similarity family の差分が読み取りにくい状態です。

## Goals / Non-Goals

**Goals:**

- MXCLR の label description / agg dispatch を 1 箇所ずつの canonical 実装に寄せる
- MCACR が shared `label_stats` helper を直接使う形に揃える
- module/datamodule の trivial helper を削除して、値取得は使用箇所に inline 化する

**Non-Goals:**

- 損失関数の数式や学習挙動の変更
- config schema の大幅変更
- tokenized datamodule 共通基盤の再設計

## Decisions

- MXCLR の agg dispatch は Hydra instantiate で partial callable を生成する registry に寄せる。これにより `agg` 文字列ごとの top-level `if` を減らし、family 差分は registry 定義で管理する。
- `mcacr.py` の `_load_npmi` は削除し、`compute_npmi` を直接使う。shared helper が既に canonical contract を持っているため、薄い wrapper を残す理由がない。
- `_projection_output_dim` と `_batch_size_from_batch` は再利用性より局所可読性が勝るため、使用箇所に inline 化する。

## Risks / Trade-offs

- [Hydra instantiate の設定ミス] → self-test と config resolve を実行して registry 解決を確認する
- [helper 削除で見落とした参照] → `rg` で参照確認後に削除し、対象 module の self-test を実行する
