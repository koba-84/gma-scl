## MODIFIED Requirements

### Requirement: Contrastive loss configuration must expose explicit runtime arguments

Contrastive loss configurations MUST declare every runtime initialization argument in Hydra config so reproducibility review does not require reading Python defaults.

#### Scenario: Resolve contrastive loss configs without hidden defaults

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を使って loss を解決する
- **THEN** 各 loss config には対応する loss 実装の runtime 初期化引数がすべて明示される
- **AND** 既定 train 構成で使う loss 引数の確認のために Python 実装既定値だけを参照する必要がない

### Requirement: Contrastive temperature parameters must use canonical naming

Contrastive loss implementations and configs MUST use `temperature`-based names for public temperature parameters instead of mixed aliases such as `temp` or `tau`.

#### Scenario: Resolve single-temperature losses with canonical key

- **WHEN** 開発者が Base、MulSupCon、MSC の config を解決する
- **THEN** 公開温度キーは `temperature` である
- **AND** `temp` や `tau` は公開 config key として使われない

#### Scenario: Resolve multi-temperature losses with role-specific keys

- **WHEN** 開発者が MXCLR、MCACR、MCACRWONEG の config を解決する
- **THEN** 複数温度は `instance_temperature`、`graph_temperature`、`positive_temperature`、`negative_temperature` のような役割付き `temperature` 名で公開される
- **AND** `tau_s` や `temp_attract` のような旧キーは公開 config key として使われない
