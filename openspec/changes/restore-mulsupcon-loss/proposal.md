## Why

`src/models/loss/ml_supcon.py` の現行実装は、各サンプル対の Jaccard 重みを使う `Base` loss と実質的に同じ計算になっている。これでは `contrastive/model=ml_supcon` を選んでも MulSupCon 固有の「各正ラベルを個別アンカーとして展開し、そのラベルを含むサンプル群に対して supervised contrastive を計算する」挙動にならず、既存比較実験の前提が崩れる。

## What Changes

- `MulSupCon` を、各アンカーの正ラベルごとに contrastive row を展開する MulSupCon の計算へ戻す。
- `Base` と `MulSupCon` の挙動差が pytest で検出できるようにする。
- training spec に MulSupCon 固有の計算契約を追記する。

## Capabilities

### Modified Capabilities
- `training`: `contrastive/model=ml_supcon` が、label-wise expanded supervised contrastive loss として動作する。

## Impact

- 影響範囲: `src/models/loss/ml_supcon.py`, `tests/losses/test_ml_supcon_loss.py`, `openspec/specs/training/spec.md`
- 実行影響: `ml_supcon` を用いた contrastive 学習の loss 値と最適化挙動が変わる。
- 非対象: `Base`, `MCACR`, `MXCLR`, `MSC` の計算式
