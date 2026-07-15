## Purpose

Tokenized CSV DataModule の共通処理を 1 箇所へ集約し、classification / contrastive の両方で同じ準備・検証・共通 dataloader を再利用できるようにする。

## Requirements

### Requirement: Tokenized CSV datamodules must share common setup and loader helpers

Tokenized CSV DataModule implementations MUST centralize tokenized split loading, label map derivation, shared collate behavior, `data_*` existence checks, and DataLoader construction helpers in one shared Lightning-oriented base implementation. Monolithic free functions that both build and load tokenized splits MUST NOT remain as the primary orchestration path.

#### Scenario: Reuse common tokenized data setup through a shared base datamodule

- **WHEN** 開発者または coding agent が classification / contrastive の tokenized CSV DataModule を整理する
- **THEN** tokenized split の prepare/load と `label2id` / `id2label` 構築は shared base datamodule が担う
- **AND** `prepare_data()` と `setup()` の Lightning hook から tokenized cache lifecycle を追える
- **AND** `data_train` / `data_val` / `data_test` の存在確認は共有実装を使う
- **AND** DataLoader 組み立ての共通 helper は共有実装を使う
- **AND** `build_or_load_tokenized_splits` のような monolithic orchestration function を残さない

#### Scenario: Keep public dataloader hooks in each concrete datamodule

- **WHEN** 開発者または coding agent が concrete datamodule の公開 API を読む
- **THEN** `ClassificationDataModule` は `train_dataloader` `val_dataloader` `test_dataloader` を同じ module 内に持つ
- **AND** `ContrastiveDataModule` も `train_dataloader` `val_dataloader` `test_dataloader` を同じ module 内に持つ
- **AND** shared base datamodule は concrete stage 用の公開 dataloader hook を持たない

#### Scenario: Keep sampler-specific logic in the contrastive module

- **WHEN** contrastive DataModule が GCBS / DPP を使う
- **THEN** sampler の初期化と更新は contrastive 側に残す
- **AND** shared implementation は sampler 固有の分岐を持たない

#### Scenario: Preserve public module behavior

- **WHEN** 共有実装へ移行した後に既存の integration test が実行される
- **THEN** classification / contrastive の入力・出力形状と stage の振る舞いは従来どおりである

### Requirement: Tokenized dataset caches must be reproducible and reusable

Tokenized dataset preparation MUST build train/dev/test splits via Hugging Face Datasets batched map and MUST reuse the on-disk cache when the preprocessing fingerprint is unchanged.

#### Scenario: Build tokenized splits from CSV

- **WHEN** 学習データディレクトリに `train.csv`, `dev.csv`, `test.csv` が存在する
- **THEN** システムは Hugging Face Datasets で 3 split を読み込み、指定 tokenizer と max_length で batched tokenization を実行する
- **AND** 出力には `input_ids`, `attention_mask`, `labels` が含まれる

#### Scenario: Reuse tokenized cache

- **WHEN** 同一 dataset_name と同一 tokenizer 設定で再実行する
- **THEN** システムは保存済み tokenized cache をロードして再トークナイズを省略する

### Requirement: CSV-based datasets must share the AAPD file contract

CSV-based multi-label datasets prepared for the training pipeline MUST provide `train.csv`, `dev.csv`, and `test.csv` files whose header starts with `abstract` followed by label columns, and whose label values are numeric binary floats compatible with AAPD (`0.0` or `1.0`). Dataset configs for such datasets MUST be selectable through Hydra for both contrastive and classification stages when the corresponding CSV files exist.

#### Scenario: WoS preprocessing emits AAPD-compatible splits

- **WHEN** `uv run python data/wos/preprocess.py` is executed
- **THEN** it writes `data/wos/train.csv`, `data/wos/dev.csv`, and `data/wos/test.csv`
- **AND** each file header starts with `abstract`
- **AND** label columns are numeric strings in deterministic order
- **AND** each row encodes the existing WoS document labels as `0.0`/`1.0` values

#### Scenario: Resolve Reuters-21578 data configs

- **WHEN** 開発者または coding agent が `data=reuters21578` を指定して train config を compose する
- **THEN** `contrastive.data.dataset_name` と `classification.data.dataset_name` は `reuters21578` として解決される
- **AND** `classification.data.num_classes` は Reuters-21578 CSV ヘッダのラベル列数と一致する `90` として解決される

#### Scenario: Resolve UK-LEX data configs

- **WHEN** 開発者または coding agent が `data=uklex` を指定して train config を compose する
- **THEN** `contrastive.data.dataset_name` と `classification.data.dataset_name` は `uklex` として解決される
- **AND** `classification.data.num_classes` は UK-LEX CSV ヘッダのラベル列数と一致する `69` として解決される

### Requirement: Tokenized preprocessing metadata must be persisted for reproducibility

Tokenized preprocessing MUST persist metadata required for reproducibility, including tokenizer identifier, max_length, and label column order.

#### Scenario: Metadata is stored with cache

- **WHEN** tokenized cache が作成される
- **THEN** tokenizer 名、max_length、label順序を含むメタデータが保存される
- **AND** 以後の学習実行で同一メタデータを検証できる

### Requirement: Tokenized dataset access must reuse tensor-backed rows

Tokenized dataset access MUST avoid rebuilding tensors for model-facing columns on every `__getitem__` call once the cached split has been prepared.

#### Scenario: Reuse tensor-backed tokenized columns during item access

- **WHEN** 開発者または coding agent が tokenized cache を読み込んだ split から sample を取得する
- **THEN** `input_ids`, `attention_mask`, `labels`, `is_empty_text` は tensor-backed row として取得される
- **AND** `__getitem__` は Python list から新しい tensor を都度構築しない
- **AND** 返却される dtype は `input_ids` / `attention_mask` が `torch.long`, `labels` が `torch.float32`, `empty_text_mask` が `torch.bool` を維持する

### Requirement: Tokenized dataset wrapper and cache orchestration must live in separate modules

The tokenized dataset wrapper module MUST expose only the dataset-facing bundle and torch dataset wrapper types. Tokenized cache materialization and cache loading helpers MUST live in a separate module, and shared datamodule code MUST import them explicitly from that cache-oriented module.

#### Scenario: Keep hf_tokenized_dataset focused on dataset-facing types

- **WHEN** 開発者または coding agent が tokenized dataset component modules を整理する
- **THEN** `hf_tokenized_dataset.py` は `TokenizedDatasetBundle` と `TokenizedTorchDataset` のみを公開する
- **AND** cache key / metadata / materialize / load helper は別 module に存在する

#### Scenario: Shared datamodule imports cache helpers from a cache-oriented module

- **WHEN** shared tokenized datamodule base が tokenized cache を prepare/load する
- **THEN** cache helper は dataset wrapper module ではなく cache-oriented module から import される
- **AND** datamodule の runtime behavior は従来どおり維持される

### Requirement: Data hierarchy must separate datamodule-level modules from low-level components

Modules that implement Lightning datamodule base behavior or tokenized cache orchestration MUST live under `src/data/` rather than `src/data/components/`. The `components` directory MUST remain reserved for lower-level reusable dataset and sampler building blocks.

#### Scenario: Keep datamodule base out of components

- **WHEN** 開発者または coding agent が tokenized datamodule 基盤を配置する
- **THEN** shared datamodule base は `src/data/` 直下に存在する
- **AND** `src/data/components/` には置かれない

#### Scenario: Keep tokenized cache orchestration out of components

- **WHEN** 開発者または coding agent が tokenized cache materialize/load helper を配置する
- **THEN** cache orchestration module は `src/data/` 直下に存在する
- **AND** `src/data/components/` には dataset wrapper や sampler のような低レベル部品だけが残る
