## Why

`debug=default` は global `callbacks: null` を設定するが、`configs/classification/train.yaml` は stage-local の `classification.callbacks.*` から `${callbacks.*}` を再参照している。そのため `debug=fdr` で classification stage に入ると、contrastive stage 完了後に `callbacks` 補間が解決できず fast_dev_run が停止する。Python 3.12 + GPU 移行後の end-to-end smoke を成立させるには、debug config でも classification stage が callback 無効化を安全に継承できる必要がある。

## What Changes

- `configs/debug/default.yaml` で classification stage の callbacks も明示的に `null` にする。
- training spec に、debug config で global callbacks を無効化した際も classification stage が補間エラーなしで実行できる要件を追加する。
- Python 3.12 + GPU 環境で `debug=fdr` の fast_dev_run を再実行して、contrastive / classification の両 stage が完走することを確認する。

## Capabilities

### Modified Capabilities
- `training`: debug config で callbacks を無効化しても classification stage が Hydra 補間エラーなしで起動できる。

## Impact

- 影響範囲: `configs/debug/default.yaml`, `openspec/specs/training/spec.md`
- 実行影響: debug/fdr と debug/default で callback 無効化が stage 間で一貫する
- 非対象: 通常学習時の callback 構成、trainer 実装、モデル実装
