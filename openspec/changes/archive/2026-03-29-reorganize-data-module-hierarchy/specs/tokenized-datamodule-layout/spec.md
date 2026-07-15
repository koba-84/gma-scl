## MODIFIED Requirements

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
