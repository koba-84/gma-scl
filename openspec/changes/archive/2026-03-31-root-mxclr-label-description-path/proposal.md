## Why

MXCLR の label description path を `data/...` の相対パスで持つと、GitHub Actions の test 実行 cwd では解決できず instantiate が失敗します。既定 config は cwd に依存せず、リポジトリルート基準で安定して解決される必要があります。

## What Changes

- MXCLR config の `label_description_path` を `${paths.root_dir}` 基準の絶対解決へ変更する。
- training spec の path 要件を `${paths.root_dir}` 基準へ更新する。

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: MXCLR の既定 label description path が cwd 非依存で解決されるよう更新する

## Impact

- 影響コード: `configs/contrastive/model/mxclr.yaml`
- 影響 spec: `openspec/specs/training/spec.md`, `openspec/specs/training.md`
