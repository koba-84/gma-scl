## ADDED Requirements

### Requirement: Commit subject must be concise and structured

Commit 件名は MUST 1行で変更主題を示し、読み手が変更種別を即時把握できる形式でなければならない。

#### Scenario: Write structured commit subject

- **WHEN** 開発者が commit 件名を作成する
- **THEN** 件名は `<Type>: <summary>` 形式で記述される
- **AND** Type は `Feat` `Fix` `Refactor` `Docs` `Test` `Chore` のいずれかを使う
- **AND** summary は命令形で簡潔に記述される

### Requirement: Behavioral changes must include rationale and validation in body

挙動変更を含む commit は MUST 本文に変更理由と検証方法を記載し、レビュー時に再確認できる状態を作らなければならない。

#### Scenario: Record rationale and validation for behavior change

- **WHEN** commit が機能、設定、学習挙動に影響する
- **THEN** 本文に `Why` と `Validation` の情報が記載される
- **AND** Validation には実行したコマンドまたは確認手順が含まれる

### Requirement: ML-related commits must include reproducibility context

ML 関連変更（model/loss/sampler/data/hparams）を含む commit は MUST 本文に再現に必要な設定コンテキストを記録しなければならない。

#### Scenario: Record reproducibility context for ML change

- **WHEN** commit が学習結果や評価値へ影響しうる設定を変更する
- **THEN** 本文に対象設定キー、設定ファイル、またはデータ契約変更のいずれかが記載される
- **AND** 関連する OpenSpec change ID がある場合は本文に記載される
