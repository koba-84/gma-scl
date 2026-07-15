## Overview

既定の実験設定で GPU 利用時の待ち時間を減らすため、設定層と dataset 実装層の両方を更新する。変更は学習ロジック自体には触れず、同一入力に対する出力意味を維持したまま runtime overhead を下げる。

## Goals

- dataloader 既定値で pinned host memory を使えるようにする
- tokenized split から sample を取得するたびに Python list -> tensor 変換を繰り返さない
- 既定 config で encoder / head compile を有効化する

## Non-Goals

- sampler 更新頻度や loss 実装の最適化
- batch size や epoch 数など探索計画の変更
- compile 非対応演算への個別回避ロジック追加

## Design Decisions

### 1. pin_memory は data config の既定値で有効化する

contrastive / classification の各 data config で `pin_memory: True` に変更する。DataModule 実装は既に config 値を DataLoader に渡しているため、コード変更は不要とする。

### 2. tokenized split は torch format で事前整形する

`build_or_load_tokenized_splits` で load/build 後の `DatasetDict` に対して `set_format(type=\"torch\", columns=[...], output_all_columns=True)` を適用する。これにより `input_ids`, `attention_mask`, `labels`, `is_empty_text` は dataset access 時点で tensor として返る。

`TokenizedTorchDataset.__getitem__` は受け取った row が tensor を返す前提に寄せ、必要最低限の dtype 正規化のみを行う。すでに tensor の場合は再生成せず `.to(dtype=...)` / `bool()` 相当で整える。

### 3. compile は model config の既定値で有効化する

contrastive / classification ともに config の `compile` default を `true` に変更する。実装側では既に `setup(stage=\"fit\")` 内で compile 分岐を持つため、新しい互換レイヤーは追加しない。

## Risks and Mitigations

- compile により初回 epoch の立ち上がりが遅くなる可能性
  → 既定値変更のみとし、必要なら override で無効化できる既存契約を維持する。
- HF dataset の format 変更で text 列が欠落する可能性
  → `output_all_columns=True` を使い、text column の読み出しを維持する。
- bool / float dtype が意図せず変わる可能性
  → `__getitem__` 側で `labels=float32`, `empty_text_mask=bool`, token ids/attention mask=long` を明示する。

## Validation Plan

- `uv run python src/train.py --cfg job --resolve` で compile / pin_memory の既定値を確認する
- tokenized dataset 関連 pytest を実行して `__getitem__` の形状と dtype を確認する
- 必要なら既存の train fast path 向け pytest を追加実行する
