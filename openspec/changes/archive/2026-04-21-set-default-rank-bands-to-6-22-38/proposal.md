## Why

デフォルト帯は四分位ではなく、研究比較で使いたい `1-6`, `7-22`, `23-38`, `39-54` の 4 帯に固定したい。既定実行の比較条件を明示値に合わせるため、default rank boundaries を変更する必要がある。

## What Changes

- `scripts/a.py` の default rank boundaries を `[6, 22, 38]` に変更する
- prediction analysis spec の default rank bands を `1-6`, `7-22`, `23-38`, `39-54` へ更新する

## Capabilities

### New Capabilities

### Modified Capabilities
- `prediction-analysis`: default four-rank-band definition を `[6, 22, 38]` へ変更する

## Impact

- 影響コード: scripts/a.py
- 影響仕様: openspec/specs/prediction-analysis/spec.md
- 依存追加なし
