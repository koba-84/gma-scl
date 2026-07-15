## Why

マルチラベルデータセットでのDPPサンプリングで `ValueError: probabilities do not sum to 1` が発生し、学習が停止する。現状の `float32 + GS` 設定は大規模データで数値誤差に弱いため、安定性を上げる必要がある。

## What Changes

- DPP埋め込み行列の内部表現を `float64` で扱う。
- DPP sampling mode の既定値を `GS_bis` に変更する。
- DPPy内部の標準出力メッセージが学習ログへ混入しないよう、DPPサンプリング時の不要出力を抑止する。
- aapdで1epoch実行し、当該エラーが再現しないことを確認する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: DPPバッチサンプリングの数値安定性要件を強化し、aapdでの `probabilities do not sum to 1` を回避する。
- `training`: DPPサンプリング実行時に第三者ライブラリ由来の不要な標準出力が混入しない。

## Impact

- 影響コード: `src/data/components/dpp.py`, `src/data/contrastive_datamodule.py`
- 影響範囲: `sampler_type=dpp` のみ
- 外部API変更: なし
