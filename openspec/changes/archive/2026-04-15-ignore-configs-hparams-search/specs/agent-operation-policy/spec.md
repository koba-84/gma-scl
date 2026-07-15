## ADDED Requirements

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
