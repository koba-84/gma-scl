## MODIFIED Requirements

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
