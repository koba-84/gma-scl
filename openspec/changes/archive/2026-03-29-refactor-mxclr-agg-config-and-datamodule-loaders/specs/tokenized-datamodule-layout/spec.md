## MODIFIED Requirements

### Requirement: Tokenized CSV datamodules must share common setup and loader helpers

Tokenized CSV DataModule implementations MUST centralize tokenized split loading, label map derivation, shared collate behavior, `data_*` existence checks, and DataLoader construction helpers in one shared Lightning-oriented base implementation. Monolithic free functions that both build and load tokenized splits MUST NOT remain as the primary orchestration path.

#### Scenario: Reuse common tokenized data setup through a shared base datamodule

- **WHEN** 開発者または coding agent が classification / contrastive の tokenized CSV DataModule を整理する
- **THEN** tokenized split の prepare/load と `label2id` / `id2label` 構築は shared base datamodule が担う
- **AND** `prepare_data()` と `setup()` の Lightning hook から tokenized cache lifecycle を追える
- **AND** `data_train` / `data_val` / `data_test` の存在確認は共有実装を使う
- **AND** DataLoader 組み立ての共通 helper は共有実装を使う

#### Scenario: Keep public dataloader hooks in each concrete datamodule

- **WHEN** 開発者または coding agent が concrete datamodule の公開 API を読む
- **THEN** `ClassificationDataModule` は `train_dataloader` `val_dataloader` `test_dataloader` を同じ module 内に持つ
- **AND** `ContrastiveDataModule` も `train_dataloader` `val_dataloader` `test_dataloader` を同じ module 内に持つ
- **AND** shared base datamodule は concrete stage 用の公開 dataloader hook を持たない
