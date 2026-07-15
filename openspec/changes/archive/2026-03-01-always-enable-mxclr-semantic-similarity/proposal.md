## Why

MXCLR の semantic 類似度利用がオプションになっていると、設定差分で実験条件がぶれやすい。AAPD での運用を明確化するため、semantic 類似度を常時有効の契約へ固定する。

## What Changes

- `src/models/loss/mxclr.py` から `use_label_semantic_similarity` 引数と分岐を削除する。
- MXCLR 初期化時は常に `dataset_name=aapd` と `label_description_path` を必須とし、Sentence-BERT でラベル間類似度を構築する。
- semantic 無効時 fallback 計算経路を削除する。
- `configs/contrastive/model/mxclr.yaml` から `use_label_semantic_similarity` 設定を削除する。
- OpenSpec training 要件を「常時利用」へ更新する。
- **BREAKING**: semantic 類似度を無効化する既存設定は利用できなくなる。

## Capabilities

### New Capabilities

- `mxclr-always-semantic-init`: MXCLR は常にラベル説明由来の semantic 類似度で初期化される。

### Modified Capabilities

- `training`: MXCLR 初期化契約を optional semantic から mandatory semantic へ変更する。
- `mxclr-label-semantic-similarity`: fallback なしの常時 semantic 計算に変更する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `configs/contrastive/model/mxclr.yaml`, `openspec/specs/training.md`, `openspec/specs/training/spec.md`
- 影響運用: AAPD 説明ファイルが必須になる
