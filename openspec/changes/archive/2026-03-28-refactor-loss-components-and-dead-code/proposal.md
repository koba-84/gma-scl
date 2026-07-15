## Why

loss 周辺の責務配置が崩れており、同種の helper が複数箇所に分散しています。加えて未使用関数の機械的な洗い出し手段がないため、不要コードが残りやすい状態です。

## What Changes

- dev dependency に vulture を追加し、pyproject.toml で検出設定を管理する
- vulture と既存参照調査を使って未使用関数を削除する
- label-set aggregation helper を `src/models/loss/components/` に統一し、top-level の `src/models/loss/aggregation.py` を廃止する
- MCACR から label frequency / NPMI 計算を分離し、再利用可能な helper module に移す
- MXCLR transport helper を 1 つの公開 entrypoint に統一し、family 別の薄い公開 wrapper を削除する

## Capabilities

### New Capabilities

### Modified Capabilities

- training: loss component と label statistics helper の配置および transport helper 公開契約を更新する
- dev-quality-tooling: 未使用コード検出に vulture を使う運用を追加する

## Impact

- pyproject.toml
- uv.lock
- src/models/loss/mcacr.py
- src/models/loss/mxclr.py
- src/models/loss/components/aggregation.py
- src/models/loss/components/transport.py
- src/models/loss/components/label_stats.py
- src/models/loss/aggregation.py
- openspec/specs/training/spec.md
- openspec/specs/dev-quality-tooling/spec.md
