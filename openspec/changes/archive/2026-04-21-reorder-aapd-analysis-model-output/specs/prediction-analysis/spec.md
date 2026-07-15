## MODIFIED Requirements

### Requirement: Prediction analysis script must print AAPD model rows in bce-base-mulsupcon order

The repository MUST print AAPD prediction analysis rows in the order `bce`, `base`, `mulsupcon`.

#### Scenario: Print AAPD analysis rows in expected order

- **WHEN** 開発者または coding agent が `uv run python scripts/a.py` を実行する
- **THEN** モデル行は `bce`, `base`, `mulsupcon` の順で表示される
