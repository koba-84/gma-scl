## MODIFIED Requirements

### Requirement: Contrastive temperature parameters must use canonical naming

Contrastive loss implementations and configs MUST use `temperature`-based names for public temperature parameters instead of mixed aliases such as `temp` or `tau`.

#### Scenario: Resolve single-temperature losses with canonical key

- **WHEN** 開発者が Base、MulSupCon、MSC の config を解決する
- **THEN** 公開温度キーは `temperature` である
- **AND** `temp` や `tau` は公開 config key として使われない

#### Scenario: Resolve multi-temperature losses with role-specific keys

- **WHEN** 開発者が MXCLR、MCACR、MCACRWONEG、MXCLR_PROTO の config を解決する
- **THEN** 複数温度は `instance_temperature`、`graph_temperature`、`positive_temperature`、`negative_temperature` のような役割付き `temperature` 名で公開される
- **AND** `tau_s`、`tau_s_schedule`、`temp_attract`、`temp_repulse` のような旧キーは公開 config key として使われない

#### Scenario: Validate canonical temperature keys across all supported losses

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を対象に温度キー検証テストを実行する
- **THEN** 各 loss config の温度関連キーは対応する loss 実装の runtime 初期化引数と一致する
- **AND** 旧キー（`temp`, `tau`, `tau_s`, `temp_attract`, `temp_repulse`）はどのサポート loss でも公開 config key として現れない
