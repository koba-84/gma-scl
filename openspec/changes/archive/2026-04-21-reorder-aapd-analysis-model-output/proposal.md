## Why

AAPD 分析表のモデル行順は比較時の見やすさに直接影響する。既定の行順を `bce`, `base`, `mulsupcon` に揃えたい。

## What Changes

- `scripts/a.py` の prediction file 列挙順を `bce`, `base`, `mulsupcon` に変更する

## Capabilities

### New Capabilities

### Modified Capabilities
- `prediction-analysis`: AAPD 分析表の既定モデル表示順を変更する

## Impact

- 影響コード: scripts/a.py
- 影響仕様: openspec/specs/prediction-analysis/spec.md
