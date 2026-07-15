## MODIFIED Requirements

### Requirement: Tokenized CSV datamodules must share common setup and loader helpers

Tokenized CSV DataModule implementations MUST centralize tokenized split loading, label map derivation, shared collate behavior, `data_*` existence checks, and validation dataloader construction in one shared Lightning-oriented base implementation. Monolithic free functions that both build and load tokenized splits MUST NOT remain as the primary orchestration path.

#### Scenario: Reuse common tokenized data setup through a shared base datamodule

- **WHEN** 開発者または coding agent が classification / contrastive の tokenized CSV DataModule を整理する
- **THEN** tokenized split の prepare/load と `label2id` / `id2label` 構築は shared base datamodule が担う
- **AND** `prepare_data()` と `setup()` の Lightning hook から tokenized cache lifecycle を追える
- **AND** `build_or_load_tokenized_splits` のような monolithic orchestration function を残さない

#### Scenario: Keep sampler-specific logic in the contrastive module

- **WHEN** contrastive DataModule が GCBS / DPP を使う
- **THEN** sampler の初期化と更新は contrastive 側に残す
- **AND** shared base implementation は sampler 固有の分岐を持たない
