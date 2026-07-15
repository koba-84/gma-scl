## Why

ユーザー要件は rank ベースで 4 つの頻度帯へ分けて比較することにある。任意個数の帯を許すと出力契約がぶれ、比較条件が揃わないため、4 帯固定へ制約する必要がある。

## What Changes

- `scripts/a.py` の rank-based 分析を 4 帯固定にする
- `--rank-boundaries` は 3 個の境界だけを受け付ける
- 未指定時は既定の順位四分位境界を使って常に 4 帯を出力する
- prediction analysis spec を「可変本数の rank bands」から「4 rank bands 固定」へ更新する

## Capabilities

### New Capabilities

### Modified Capabilities
- `prediction-analysis`: rank-based frequency-band analysis の出力帯数を 4 固定へ変更する

## Impact

- 影響コード: scripts/a.py
- 影響仕様: openspec/specs/prediction-analysis/spec.md
- 依存追加なし
