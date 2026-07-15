## ADDED Requirements

### Requirement: Pre-tokenized dataset cache for training
The system MUST build train/dev/test tokenized datasets via Hugging Face Datasets batched map and MUST reuse on-disk cache when the preprocessing fingerprint is unchanged.

#### Scenario: Build tokenized splits from CSV
- **WHEN** 学習データディレクトリに `train.csv`, `dev.csv`, `test.csv` が存在する
- **THEN** システムは Hugging Face Datasets で3 splitを読み込み、指定 tokenizer と max_length で batched tokenization を実行する
- **AND** 出力には `input_ids`, `attention_mask`, `labels` が含まれる

#### Scenario: Reuse tokenized cache
- **WHEN** 同一 dataset_name と同一 tokenizer 設定で再実行する
- **THEN** システムは保存済み tokenized cache をロードして再トークナイズを省略する

### Requirement: Deterministic preprocessing metadata
The system MUST persist preprocessing metadata required for reproducibility, including tokenizer identifier, max_length, and label column order.

#### Scenario: Metadata is stored with cache
- **WHEN** tokenized cache が作成される
- **THEN** tokenizer 名、max_length、label順序を含むメタデータが保存される
- **AND** 以後の学習実行で同一メタデータを検証できる
