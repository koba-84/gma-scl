## MODIFIED Requirements

### Requirement: Contrastive loss naming and contract consistency

contrastive loss 実装は可読性のため簡潔で一貫した命名を使用し、`classification.py` を除く各 loss module は `nn.Module` wrapper と private 計算 helper の責務境界を共有しなければならない。単純な shape / config validation だけを行う private helper は主要関数から分離せず、`forward` や top-level helper の冒頭に保持しなければならない。

#### Scenario: Keep simple validation local to the main function

- **WHEN** 開発者または coding agent が loss module や周辺 helper の validation を更新する
- **THEN** 単純な shape / config / column existence の guard は主要関数の冒頭に直接記述される
- **AND** pytest で個別に守るほどの再利用価値がない `_validate_*` helper を新設または維持しない
