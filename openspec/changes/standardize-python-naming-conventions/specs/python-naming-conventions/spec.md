## ADDED Requirements

### Requirement: Python symbol naming conventions
Python implementation names MUST follow repository-wide conventions aligned with PEP 8.

#### Scenario: Name functions and methods with snake_case
- **WHEN** 開発者または coding agent が新規関数・メソッドを追加する
- **THEN** 識別子は `snake_case` を使用する
- **AND** 先頭大文字や混在ケースを使用しない

#### Scenario: Name classes with CapWords
- **WHEN** 開発者または coding agent が新規クラスを追加する
- **THEN** 識別子は `CapWords` を使用する
- **AND** 単語区切りにアンダースコアを使用しない

#### Scenario: Name variables and attributes with snake_case
- **WHEN** 開発者または coding agent が変数・属性・引数を追加する
- **THEN** 識別子は `snake_case` を使用する
- **AND** 定数でない値に `UPPER_CASE` を使用しない

### Requirement: File-level naming conventions
Python modules under `src`, `tests`, and `scripts` MUST use lowercase snake_case file names.

#### Scenario: Add Python file under managed directories
- **WHEN** 開発者または coding agent が `src` `tests` `scripts` 配下に Python ファイルを追加する
- **THEN** ファイル名は小文字 `snake_case` を使用する
- **AND** `tests` 配下は既存仕様に従い `test_` 接頭辞を付けない

### Requirement: Domain-specific naming exceptions must be explicit
If domain-specific or paper-aligned naming exceptions are required, they MUST be explicitly declared in lint configuration and documented in specs.

#### Scenario: Keep MCACR_WONEG as explicit exception
- **WHEN** 開発者または coding agent が命名規約を lint 設定へ反映する
- **THEN** `MCACR_WONEG` のみを例外名として明示する
- **AND** 例外理由を仕様に記録する
