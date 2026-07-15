## ADDED Requirements

### Requirement: Agent must autonomously execute archive after change completion

Coding agent MUST execute archive transition autonomously once the active change is complete and archive safety checks pass.

#### Scenario: Execute archive without explicit follow-up request

- **WHEN** coding agent が単一 change の全 tasks 完了と archive 前提条件成立を確認した
- **THEN** coding agent はユーザーの追加依頼を待たずに archive を実行する
- **AND** 実行結果として移行先パスと事後確認結果を報告する

#### Scenario: Do not auto-archive in unresolved mixed-change state

- **WHEN** 対象外差分の混在で安全な archive 実行可否を判定できない
- **THEN** coding agent は archive 実行を中断する
- **AND** ユーザーへ確認事項と推奨対応を報告する
