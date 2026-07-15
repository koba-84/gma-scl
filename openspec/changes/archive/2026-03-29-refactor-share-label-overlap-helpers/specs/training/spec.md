## MODIFIED Requirements

### Requirement: Contrastive loss naming and contract consistency

contrastive loss 実装は可読性のため簡潔で一貫した命名を使用し、`classification.py` を除く各 loss module は `nn.Module` wrapper と private 計算 helper の責務境界を共有しなければならない。label overlap の OR-count / union-count のような複数 loss で再利用される計算は top-level loss module に重複実装してはならず、shared components に集約しなければならない。

#### Scenario: Keep forward as validation and orchestration layer

- **WHEN** 開発者または coding agent が `classification.py` を除く `src/models/loss/*.py` を更新する
- **THEN** 各 `forward` は入力 shape 検証と state / buffer 解決を担当する
- **AND** loss 本体計算は module-level private helper へ委譲される

#### Scenario: Share label overlap helpers across contrastive losses

- **WHEN** 開発者または coding agent が multi-label overlap 計算を更新する
- **THEN** `Base` `MSC` `MCACR` 系で共通に使う OR-count / union-count は `src/models/loss/components` の shared helper で実装される
- **AND** top-level loss module ごとに同等の式を重複実装しない
