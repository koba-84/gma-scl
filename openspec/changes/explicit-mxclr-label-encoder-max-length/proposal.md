## Why

MXCLR のラベル説明文エンコードは現状で SentenceTransformer のモデル既定長に暗黙依存しており、設定ファイルから最大トークン長を確認できません。再現性と設定可読性のため、最大トークン長を明示設定できるようにします。

## What Changes

- MXCLR 初期化引数にラベル説明文エンコード用の `sbert_max_length` を追加する。
- `SentenceTransformer` 初期化後に `max_seq_length` へ明示代入してトークナイズ上限を固定する。
- `configs/contrastive/model/mxclr.yaml` に `sbert_max_length` を追加し、現行運用値を明示する。
- MXCLR 自己テストを更新し、引数変更後も初期化と forward が成立することを確認する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MXCLR の semantic 初期化設定にラベル説明文エンコード最大長の明示指定要件を追加する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `configs/contrastive/model/mxclr.yaml`
- 影響仕様: `openspec/specs/training/spec.md`
- 追加依存はなし
