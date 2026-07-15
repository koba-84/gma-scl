## ADDED Requirements

### Requirement: Agent work must be scoped to a single OpenSpec change

coding agent は MUST 1 回の実装作業を単一 OpenSpec change に紐づけ、別 change の差分を混在させてはならない。

#### Scenario: Implement change with clear scope

- **WHEN** coding agent が OpenSpec change に基づいて実装する
- **THEN** 変更ファイルは当該 change の目的に直接関係するものに限定される
- **AND** 範囲外差分を検出した場合は対象から除外する

### Requirement: Agent completion must include spec alignment and verification evidence

coding agent は MUST 作業完了時に spec 反映、検証実行結果、commit 境界を報告しなければならない。

#### Scenario: Report completion for a change

- **WHEN** coding agent が変更完了を報告する
- **THEN** proposal/spec/design/tasks と実装の整合を示す
- **AND** 実行した検証コマンドと成否を示す
- **AND** commit 粒度が単一論理変更であることを示す
