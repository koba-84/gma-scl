## ADDED Requirements

### Requirement: Commit timing must follow completion and validation boundaries

開発者と coding agent は MUST 単一論理変更が完了し、当該変更の必須検証が成功した時点で commit を作成しなければならない。

#### Scenario: Commit after logical unit completion

- **WHEN** 単一トピックの実装と関連ドキュメント更新が完了している
- **THEN** その単位で commit を作成する
- **AND** 未完了の別トピック変更は同一 commit に含めない

#### Scenario: Commit only after required checks pass

- **WHEN** 開発者または coding agent が commit を作成する
- **THEN** `uv run pre-commit run -a` が成功している
- **AND** Python 変更を含む場合は mypy フックが成功している

### Requirement: Dirty tree must be handled explicitly before agent edits

coding agent は MUST 作業開始時に未コミット差分を確認し、対象外差分を commit に混在させてはならない。

#### Scenario: Start work with unrelated local changes present

- **WHEN** 作業開始時の `git status --short` に対象外差分が含まれる
- **THEN** agent は対象外差分を編集・revert・commit しない
- **AND** 対象差分との混在回避が困難な場合は作業を停止してユーザー確認を要求する
