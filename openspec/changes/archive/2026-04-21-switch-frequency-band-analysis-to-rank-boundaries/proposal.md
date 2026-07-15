## Why

頻度帯分析で比較したいのは frequency 値しきいではなく、頻度順位で上位何ラベルまでかという区切りである。研究用途では「上位 10 ラベル」「次の 20 ラベル」のように順位ベースで帯を固定できる契約が必要である。

## What Changes

- `scripts/a.py` の頻度帯指定を frequency 値境界から rank 境界へ変更する
- 公開 CLI は `--rank-boundaries` を受け取り、頻度降順の上位何ラベルまでで帯を切る
- 未指定時はラベル数に対する順位四分位を既定値として使う
- prediction analysis spec を frequency-value boundary 前提から rank-boundary 前提へ更新する

## Capabilities

### New Capabilities

### Modified Capabilities
- `prediction-analysis`: 頻度帯別 Macro-F1 分析を rank-based banding 契約へ変更する

## Impact

- 影響コード: scripts/a.py
- 影響仕様: openspec/specs/prediction-analysis/spec.md
- 依存追加なし
