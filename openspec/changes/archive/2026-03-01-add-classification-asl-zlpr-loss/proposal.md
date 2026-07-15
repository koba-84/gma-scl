## Why

classification ステージの損失関数が BCEWithLogitsLoss 固定のため、クラス不均衡やランキング重視の設定を比較検証できない。研究再現性を維持したまま ASL と ZLPR を同一学習経路で選択可能にする必要がある。

## What Changes

- classification 損失に `bce` / `asymmetric` / `zlpr` の選択肢を追加する。
- ASL を `gamma_pos`, `gamma_neg`, `margin` で設定可能にし、指定値 `gamma_pos=0`, `gamma_neg=1`, `margin=0` を再現できるようにする。
- linear_probe/finetune の分類モデル設定に loss 設定ブロックを追加する。
- 損失実装の最小自己テストと設定解決テストを追加する。

## Capabilities

### New Capabilities

- `classification-losses`: classification 用の損失関数切り替えと ASL/ZLPR 実装。

### Modified Capabilities

- `training`: classification ステージが複数損失関数を設定から解決できるように要件を拡張。

## Impact

- 影響コード: `src/models/finetune_module.py`, `src/models/loss/`, `configs/classification/model/*.yaml`, `tests/`
- 学習挙動: loss 選択により最適化対象が変化。
- 後方互換: 互換レイヤーは追加せず、既定値 `bce` で既存運用を維持する。
