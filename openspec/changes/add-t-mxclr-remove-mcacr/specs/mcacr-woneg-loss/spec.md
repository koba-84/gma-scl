## REMOVED Requirements

### Requirement: MCACRWONEG availability

The repository MUST provide MCACRWONEG as a selectable loss implementation for contrastive training.

#### Scenario: Resolve MCACRWONEG target from config

- **WHEN** 開発者が `configs/contrastive/model/mcacr_woneg.yaml` を利用する
- **THEN** `src.models.loss.mcacr_woneg.MCACRWONEG` が解決できる
