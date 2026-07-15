## Purpose

Define commit message standards for this ML repository so history remains reviewable and reproducible.

## Requirements

### Requirement: Commit subject must be concise and structured

Commit subject MUST use one-line structured format that makes change intent immediately clear.

#### Scenario: Write structured commit subject

- **WHEN** 開発者または coding agent が commit を作成する
- **THEN** 件名は `<Type>: <summary>` 形式である
- **AND** Type は `Feat` `Fix` `Refactor` `Docs` `Test` `Chore` のいずれかを使う
- **AND** summary は命令形で簡潔に記載される

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

### Requirement: Behavior-changing commits must include rationale and validation

Commits that can change behavior MUST include rationale and validation evidence in the body.

#### Scenario: Record rationale and validation

- **WHEN** commit が機能・設定・学習挙動に影響する
- **THEN** 本文に `Why` と `Validation` の情報が含まれる
- **AND** Validation には実行したコマンドまたは確認手順が含まれる

### Requirement: ML-impacting commits must include reproducibility context

Commits that can affect ML outcomes MUST include reproducibility context in the body.

#### Scenario: Record reproducibility context for ML changes

- **WHEN** commit が model/loss/sampler/data/hparams のいずれかを変更する
- **THEN** 本文に対象設定キー、設定ファイル、またはデータ契約変更が記録される
- **AND** 関連 OpenSpec change がある場合は change ID を記録する

### Requirement: Lightweight commits may use minimal body

Pure documentation, comment-only, and non-behavioral cleanups MAY use minimal body text.

#### Scenario: Keep minimal body for non-behavioral updates

- **WHEN** commit が docs/test/chore の非挙動変更のみを含む
- **THEN** 本文は 1 行要約または省略を許容する
- **AND** 件名要件は維持する

### Requirement: Commit message policy must be enforced automatically

Project MUST enforce commit message policy through executable gates at commit time and push time.

#### Scenario: Validate message on commit

- **WHEN** 開発者または coding agent が commit を作成する
- **THEN** commit-msg フックで件名形式と必須本文項目を検証する
- **AND** 不一致時は commit を失敗させる

#### Scenario: Validate outgoing commits on push

- **WHEN** 開発者または coding agent が push を実行する
- **THEN** pre-push フックで push 対象コミット群の message 要件を再検証する
- **AND** 不一致時は push を失敗させる
