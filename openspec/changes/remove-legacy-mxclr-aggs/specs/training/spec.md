## ADDED Requirements

### Requirement: MXCLR-family agg choices must exclude removed legacy aggregations

MXCLR-family loss configurations MUST support only the active agg choices `BERTScore_F1`, `BERTScore_Precision`, and `BERTScore_Recall`. The removed `mean`, `wmd`, `wrd`, `uot`, `chamfer`, and `idf_chamfer` agg choices MUST NOT be exposed through Hydra config files or runtime agg modules.

#### Scenario: Resolve MXCLR default with a supported agg

- **WHEN** 開発者または coding agent が `contrastive/model=mxclr` を compose する
- **THEN** `contrastive.model.loss_fn.agg._target_` は残存サポート対象の agg 実装を参照する
- **AND** removed agg choices `mean`, `wmd`, `wrd`, `uot`, `chamfer`, and `idf_chamfer` are not used as defaults

#### Scenario: Removed agg configs are unavailable

- **WHEN** 開発者または coding agent が `configs/contrastive/model/agg/` の support 対象を確認する
- **THEN** `mean.yaml`, `wmd.yaml`, `wrd.yaml`, `uot.yaml`, `chamfer.yaml`, and `idf_chamfer.yaml` は存在しない
- **AND** remaining agg config files resolve to concrete supported agg implementations

#### Scenario: Removed agg runtime modules are unavailable

- **WHEN** 開発者または coding agent が `src/models/loss/agg/` の public agg modules を確認する
- **THEN** `mean.py`, `wmd.py`, `wrd.py`, `uot.py`, `chamfer.py`, and `idf_chamfer.py` は存在しない
- **AND** tests do not instantiate removed agg implementations

### Requirement: t-MXCLR must be removed from supported contrastive losses

Contrastive loss configurations MUST NOT expose `t_mxclr` as a supported choice. The `t_mxclr` runtime implementation, tests, hparam-search config, and dedicated spec MUST be removed.

#### Scenario: t-MXCLR config and runtime are unavailable

- **WHEN** 開発者または coding agent が supported contrastive model configs and loss modules を確認する
- **THEN** `configs/contrastive/model/t_mxclr.yaml` は存在しない
- **AND** `src/models/loss/t_mxclr.py` は存在しない
- **AND** tests and hparam search configs do not reference `t_mxclr`
