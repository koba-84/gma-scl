## ADDED Requirements

### Requirement: Commit message language convention

Commit message subject MUST keep the structured format `<Type>: <summary>` with English `Type` tokens, and behavior-changing commits MUST preserve English section headers `Why`, `Validation`, and `Reproducibility` when required. Section contents MAY be written in Japanese or English.

#### Scenario: Subject uses required English type token

- **WHEN** 開発者または coding agent が commit を作成する
- **THEN** 件名は `Feat` `Fix` `Refactor` `Docs` `Test` `Chore` のいずれかを先頭に使用する
- **AND** 件名フォーマットは `<Type>: <summary>` を満たす

#### Scenario: Required body headers remain English while explanation language is flexible

- **WHEN** commit が機能・設定・学習挙動に影響し、本文が必要になる
- **THEN** 本文の必須見出しは `Why` `Validation` `Reproducibility` の英語表記を使用する
- **AND** 各見出し配下の説明文は日本語または英語を使用できる
