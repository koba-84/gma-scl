## MODIFIED Requirements

### Requirement: Contrastive loss naming and contract consistency

contrastive loss 実装は可読性のため簡潔で一貫した命名を使用し、`classification.py` を除く各 loss module は `nn.Module` wrapper と private 計算 helper の責務境界を共有しなければならない。MXCLR は similarity family と transport family の内部差を保持してもよいが、公開 graph builder 契約は単一の sample-pair score 行列へ統一しなければならない。

#### Scenario: Keep forward as validation and orchestration layer

- **WHEN** 開発者または coding agent が `classification.py` を除く `src/models/loss/*.py` を更新する
- **THEN** 各 `forward` は入力 shape 検証と state / buffer 解決を担当する
- **AND** loss 本体計算は module-level private helper へ委譲される

#### Scenario: Build one MXCLR score graph contract across agg families

- **WHEN** 開発者または coding agent が `src/models/loss/mxclr.py` の graph builder を更新する
- **THEN** `agg` ごとの差は instantiate 済み builder 設定で表現される
- **AND** builder は family ごとの matrix 構築と sample-pair 集約を内部で選択しつつ、最終的には MXCLR が直接使う共通 score 行列 `[N, N]` を返す
- **AND** top-level に family 別の公開 graph builder 関数を並立させない

#### Scenario: Expose MXCLR graph API as score graph

- **WHEN** 開発者または coding agent が MXCLR の labels-to-graph API を呼び出す
- **THEN** API は labels から score graph `[N, N]` を返す
- **AND** similarity family では共通集約契約の出力をそのまま score とする
- **AND** transport family では pairwise distance を MXCLR 用 score に写像してから返す
