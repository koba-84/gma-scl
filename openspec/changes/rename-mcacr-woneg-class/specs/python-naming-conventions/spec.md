## MODIFIED Requirements

### Requirement: Domain-specific naming exceptions must be explicit

If domain-specific naming exceptions are required, they MUST be explicitly declared in lint configuration and documented in specs.

#### Scenario: Keep exception list empty by default

- **WHEN** 開発者または coding agent が命名規約を lint 設定へ反映する
- **THEN** 仕様で明示された根拠がない限り、命名例外を追加しない
- **AND** 標準規約を全クラス名へ適用する
