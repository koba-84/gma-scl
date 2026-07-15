## ADDED Requirements

### Requirement: Public class naming for contrastive loss implementations
The training specification MUST define the canonical public class names for built-in contrastive losses.

#### Scenario: Resolve canonical class names for built-in losses
- **WHEN** 開発者または coding agent が built-in contrastive loss 実装の公開名を確認する
- **THEN** canonical class names は `Base`, `MulSupCon`, `MCACR_WONEG`, `MXCLR`, `MSC` である
- **AND** loss 実装ファイル名は `src/models/loss/<loss_name>.py` 形式を維持する
