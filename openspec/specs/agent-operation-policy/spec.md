## Purpose

Define coding-agent operation policy for OpenSpec-driven implementation, verification, and reporting.
## Requirements
### Requirement: Agent work must be scoped to a single OpenSpec change

Coding agent MUST bind one implementation run to one OpenSpec change and MUST avoid mixing unrelated changes.

#### Scenario: Execute implementation for one change

- **WHEN** coding agent starts implementation from an OpenSpec change
- **THEN** edited files are limited to files directly required by that change
- **AND** unrelated local changes are not modified or committed

### Requirement: Agent completion must include verification and commit evidence

Coding agent MUST report verification results and commit boundaries when declaring completion.

#### Scenario: Report implementation completion

- **WHEN** coding agent reports that a change is complete
- **THEN** report includes executed verification commands and outcomes
- **AND** report includes commit units aligned to logical changes
- **AND** report includes any remaining uncommitted files and rationale

### Requirement: Agent must stop on unavoidable mixed-change state

Coding agent MUST stop and request user decision when unrelated pending changes cannot be safely separated from requested work.

#### Scenario: Mixed dirty tree blocks safe progress

- **WHEN** unrelated changes in working tree cannot be isolated without risky operations
- **THEN** agent stops further edits
- **AND** agent asks the user how to proceed before continuing

### Requirement: Agent autonomous commit execution

Coding agent MUST create commits autonomously when commit gates are satisfied, and MUST block commit creation when any mandatory gate fails.

#### Scenario: Autonomous commit on satisfied gates

- **WHEN** 単一 OpenSpec change の実装が完了し、必須検証が成功し、commit 単位が単一論理変更に分離されている
- **THEN** coding agent は追加のユーザー明示指示なしで commit を作成する
- **AND** report には commit hash と検証結果を含める

#### Scenario: Block autonomous commit on failed gates

- **WHEN** 必須検証が未実行または失敗、もしくは対象外差分の混在が解消できない
- **THEN** coding agent は commit を作成してはならない
- **AND** 失敗条件を報告して停止する

### Requirement: Agent must respect protected-branch review workflow

Coding agent MUST NOT bypass review controls by directly integrating to protected branches.

#### Scenario: Do not bypass protected branch controls

- **WHEN** リモート統合先が protected branch の制御対象である
- **THEN** coding agent は protected branch への直接 push や merge を行ってはならない
- **AND** review 可能な commit 境界または PR 情報を報告する

### Requirement: Agent must autonomously archive completed changes

Coding agent MUST execute OpenSpec archive transition autonomously after confirming completion and archive safety preconditions.

#### Scenario: Auto-archive after completion checks pass

- **WHEN** coding agent が change 完了（status complete かつ tasks 未完了なし）を確認した
- **THEN** coding agent は追加のユーザー明示指示なしで archive を実行する
- **AND** archive 後に移行先パスと事後確認結果を報告する

#### Scenario: Stop and report when archive cannot be safely executed

- **WHEN** 対象外差分混在や archive 先衝突により安全な archive 実行ができない
- **THEN** coding agent は archive 実行を中断する
- **AND** 停止理由とユーザーが選択すべき次アクションを報告する

### Requirement: Experimental hparams search workspace must not drive spec changes

Edits under configs/hparams_search MUST be treated as local experimental workspace updates and MUST NOT be used as direct evidence to add or alter OpenSpec requirements.

#### Scenario: Edit files under configs/hparams_search

- **WHEN** 開発者または coding agent が configs/hparams_search 配下ファイルを編集する
- **THEN** その編集は仕様変更として扱ってはならない
- **AND** OpenSpec main specs の requirement 追加/変更の根拠にしてはならない

#### Scenario: Promote reusable behavior from experimental workspace

- **WHEN** configs/hparams_search 由来の知見を恒久運用へ反映したい
- **THEN** 共有対象の設定を管理対象ディレクトリへ移動したうえで、別OpenSpec changeとして仕様化する
- **AND** configs/hparams_search 配下を直接仕様の正本として参照してはならない
