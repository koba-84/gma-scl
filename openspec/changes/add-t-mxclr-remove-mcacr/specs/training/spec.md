## MODIFIED Requirements

### Requirement: Contrastive loss configuration must expose explicit runtime arguments

Contrastive loss configurations MUST declare every runtime initialization argument in Hydra config so reproducibility review does not require reading Python defaults. Supported contrastive loss configs MUST exclude removed MCACR and MCACRWONEG choices and include t-MXCLR.

#### Scenario: Resolve contrastive loss configs without hidden defaults

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を使って loss を解決する
- **THEN** each supported loss config contains every runtime initialization argument for its implementation
- **AND** `configs/contrastive/model/t_mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `perplexity`, `exaggeration`, `degrees_of_freedom`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, and `agg`
- **AND** MCACR and MCACRWONEG configs are not supported choices

### Requirement: Contrastive temperature parameters must use canonical naming

Contrastive loss implementations and configs MUST use `temperature`-based names for public temperature parameters instead of mixed aliases such as `temp` or `tau`.

#### Scenario: Resolve multi-temperature losses with role-specific keys

- **WHEN** 開発者が MXCLR, MXCLRKendall, or t-MXCLR config を解決する
- **THEN** multiple temperatures are exposed with role-specific `temperature` names such as `instance_temperature` and `graph_temperature`
- **AND** removed MCACR/MCACRWONEG temperature keys are not retained through compatibility layers
