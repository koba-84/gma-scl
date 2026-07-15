## MODIFIED Requirements

### Requirement: Contrastive loss configuration must expose explicit runtime arguments

Contrastive loss configurations MUST declare every runtime initialization argument in Hydra config so reproducibility review does not require reading Python defaults. Supported contrastive loss configs MUST exclude removed MCACR and MCACRWONEG choices and include t-MXCLR and multi-scale MXCLR. NPMI-aware MXCLR agg configurations MUST expose `yule_q_lambda` as the explicit beta coefficient for corrected Yule's Q target similarity.

#### Scenario: Resolve contrastive loss configs without hidden defaults

- **WHEN** 開発者または coding agent が `configs/contrastive/model/*.yaml` を使って loss を解決する
- **THEN** each supported loss config contains every runtime initialization argument for its implementation
- **AND** `configs/contrastive/model/t_mxclr.yaml` exposes `data_dir`, `instance_temperature`, `graph_temperature`, `perplexity`, `exaggeration`, `degrees_of_freedom`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, and `agg`
- **AND** `configs/contrastive/model/multi_scale_mxclr.yaml` exposes `data_dir`, `perplexities`, `exaggeration`, `dataset_name`, `sbert_model_name`, `sbert_max_length`, and `agg`
- **AND** NPMI-aware MXCLR agg configs expose `yule_q_lambda`
- **AND** MCACR and MCACRWONEG configs are not supported choices
