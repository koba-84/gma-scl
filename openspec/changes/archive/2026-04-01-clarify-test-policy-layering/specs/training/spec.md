## ADDED Requirements

### Requirement: Sampler tests must separate shared integration from sampler-specific compatibility

Sampler validation MUST distinguish shared functional integration from sampler-specific compatibility regressions. Generic sampler switching and DataModule wiring MUST be checked in shared integration tests, while a regression that exists only for one sampler implementation MAY remain in a dedicated test.

#### Scenario: Keep sampler switching in shared integration

- **WHEN** 開発者または coding agent が `shuffle`, `gcbs`, `dpp` の sampler 切替や初期化順序を検証する
- **THEN** 検証は shared integration test で行う
- **AND** sampler 共通の functional contract は 1 か所で回帰検知できる

#### Scenario: Keep DPP-specific compatibility regression isolated

- **WHEN** DPP sampler だけが third-party `FiniteDPP` 初期化経路と stdout hygiene を持つ
- **THEN** その回帰検知は sampler 共通 integration test に吸収せず dedicated test として保持できる
- **AND** 当該 test は sampler 一般 contract ではなく DPP implementation-specific compatibility contract を表す

## MODIFIED Requirements

### Requirement: DPP sampler runtime output hygiene

When contrastive sampler type is DPP, the runtime SHALL suppress third-party informational stdout messages emitted during `FiniteDPP` initialization so training logs remain clean. This requirement is a DPP-specific compatibility contract and MUST NOT be used as a reason to merge all sampler tests into one parametrized stdout check.

#### Scenario: DPP sampler initialization does not print DPPy info lines

- **WHEN** DPP sampler iterates and constructs `FiniteDPP` using `L_gram_factor`
- **THEN** informational constructor prints from the third-party library are not emitted to standard output
- **AND** this regression may be guarded by a dedicated DPP-focused test rather than sampler-wide parametrization
