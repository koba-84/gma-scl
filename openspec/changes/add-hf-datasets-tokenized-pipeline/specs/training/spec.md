## ADDED Requirements

### Requirement: Tokenized batch contract between DataModule and model
Training data modules and model modules MUST exchange tokenized tensor batches instead of raw text lists.

#### Scenario: Classification training step receives tokenized batch
- **WHEN** classification stage の `training_step` が呼び出される
- **THEN** バッチには `input_ids`, `attention_mask`, `labels` が含まれる
- **AND** モデルは追加トークナイズを行わず forward を実行する

#### Scenario: Contrastive training step receives tokenized batch
- **WHEN** contrastive stage の `training_step` が呼び出される
- **THEN** バッチには `input_ids`, `attention_mask`, `labels` が含まれる
- **AND** モデルは tokenized tensors を直接 encoder へ渡す

### Requirement: HF Datasets as standard training input path
The training pipeline MUST use Hugging Face Datasets as the standard preprocessing path for CSV-based text-label data.

#### Scenario: Datamodule setup constructs HF datasets
- **WHEN** datamodule `setup("fit")` が実行される
- **THEN** datamodule は HF Datasets ベースの tokenized split を構築またはロードする
- **AND** DataLoader は tokenized split からバッチを返す
