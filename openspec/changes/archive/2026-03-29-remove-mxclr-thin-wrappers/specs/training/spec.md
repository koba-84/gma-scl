## MODIFIED Requirements

### Requirement: Contrastive loss naming and contract consistency

contrastive loss 実装は可読性のため簡潔で一貫した命名を使用し、`classification.py` を除く各 loss module は `nn.Module` wrapper と private 計算 helper の責務境界を共有しなければならない。MXCLR score graph pipeline では、1 箇所からしか呼ばれない薄い wrapper を top-level helper として残してはならない。

#### Scenario: Keep MXCLR score graph pipeline direct

- **WHEN** 開発者または coding agent が `src/models/loss/mxclr.py` を更新する
- **THEN** MXCLR score graph pipeline は matrix 構築、sample-pair 集約、score 化を主要関数へ直接記述する
- **AND** 単なる転送だけを行う薄い wrapper helper を top-level に追加しない
