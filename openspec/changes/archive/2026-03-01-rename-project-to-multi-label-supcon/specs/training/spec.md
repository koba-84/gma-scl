## MODIFIED Requirements

### Requirement: Canonical training project name

This requirement MUST set the default wandb project name in training config to multi-label-supcon.

#### Scenario: Default wandb project name

- WHEN 開発者が `configs/logger/wandb.yaml` の既定設定を使う
- THEN `project` は `multi-label-supcon` である
