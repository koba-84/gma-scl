## Why

現状の学習エントリーポイントでは seed が 0 のときに乱数シード初期化が実行されず、同一設定でも再現性が崩れる。
研究コードとして「同じ commit + 同じ設定 + 同じ seed」で再現できる前提を満たすため、seed=0 を有効な固定値として扱う必要がある。

## What Changes

- 学習開始時のシード初期化条件を真偽値判定から未設定判定へ変更し、seed=0 でも `lightning.seed_everything` を実行する。
- seed が未設定の場合のみ既存通りシード初期化をスキップする。
- 変更仕様を OpenSpec training spec に反映し、seed 指定時の挙動を明文化する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `training`: train エントリーポイントにおける seed 指定時の再現性要件（seed=0 含む）を変更する。

## Impact

- 影響コード: `src/train.py`
- 影響仕様: `openspec/specs/training/spec.md`
- API や依存追加はなし
