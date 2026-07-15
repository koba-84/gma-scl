## MODIFIED Requirements

### Requirement: Prediction analysis script must use 6-22-38 as the default four rank-band boundaries for AAPD

The repository MUST use rank boundaries `[6, 22, 38]` as the default configuration for the four rank-based frequency bands in the AAPD prediction analysis script.

#### Scenario: Recompute AAPD Macro-F1 with default rank bands

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** 既定の rank boundaries は `[6, 22, 38]` である
- **AND** 頻度帯は rank `1-6`, `7-22`, `23-38`, `39-54` として構築される
