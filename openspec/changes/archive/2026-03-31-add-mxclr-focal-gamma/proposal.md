## Why

MXCLR の loss は batch 内候補に対する分類として InfoNCE を cross entropy で最適化している一方、難易度の低い候補も一様に扱っています。classification 側で実績のある focal loss 的な重み付けを同じ CE 解釈へ持ち込み、容易な候補の寄与を制御できるようにします。

## What Changes

- MXCLR 初期化引数に focal-style weighting 用の `gamma` を追加する。
- MXCLR の InfoNCE loss 計算で、soft target 分布に対する各 batch 内候補の負対数尤度へ `(1 - p)^gamma` の重みを掛ける。
- `gamma=0` を既定値として現行 loss と一致させ、正値時のみ focal loss 的な挙動を有効化する。
- `configs/contrastive/model/mxclr.yaml` に `gamma` を追加し、Hydra 設定から再現可能にする。
- MXCLR テストを更新し、`gamma` の値検証と `gamma>0` 時の forward の有限性・非退行を確認する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MXCLR の loss 設定と forward 契約に `gamma` による focal-style weighting 要件を追加する。

## Impact

- 影響コード: `src/models/loss/mxclr.py`, `configs/contrastive/model/mxclr.yaml`, `tests/test_contrastive_losses.py`, `tests/property_based.py`
- 影響仕様: `openspec/specs/training/spec.md`
- 追加依存はなし
