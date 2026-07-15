## Why

MCACR の NPMI を外部ファイルに依存させる運用は、前処理手順を増やし実験実行を煩雑化する。loss 初期化時に毎回 `train.csv` から直接計算することで、前処理不要かつ手順固定の実行フローへ揃える。

## What Changes

- MCACR 系 loss 初期化時に、毎回 `train.csv` から NPMI 行列を計算する。
- 既存の NPMI 計算式と同一の統計量定義（ラベル出現頻度と共起頻度）を使う。
- `npmi.npy` の読み込み・生成・保存を行わない。
- 入力 CSV が不足または不正な場合は、原因がわかる例外メッセージで失敗させる。
- MCACR の自己テストに CSV 直計算経路の検証を追加する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MCACR 系 loss が NPMI 依存ファイルを使わず、`train.csv` から直接計算する要件を追加する。

## Impact

- 影響コード: `src/models/loss/mcacr.py`, `src/models/loss/mcacr_woneg.py`
- 影響テスト: `src/models/loss/mcacr.py` の自己テスト、必要に応じて config 解決テスト
- 運用影響: MCACR 実行時の NPMI 前処理は不要になる
