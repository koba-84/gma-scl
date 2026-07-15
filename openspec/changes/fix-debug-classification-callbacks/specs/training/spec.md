## MODIFIED Requirements

### Requirement: Debug callback disabling must apply safely to classification stage

When a debug configuration disables global callbacks, the classification stage MUST also resolve without stage-local callback interpolation failures.

#### Scenario: debug=fdr resolves classification callbacks to null

- **WHEN** 開発者または coding agent が `uv run python src/train.py --config-name test --cfg job --resolve debug=fdr` を実行する
- **THEN** `classification.callbacks` は `null` として解決される
- **AND** `${callbacks.model_checkpoint}` のような global callback 参照解決で失敗しない

#### Scenario: debug=fdr completes both stages without callback interpolation failure

- **WHEN** 開発者または coding agent が Python 3.12 + GPU 環境で `uv run python src/train.py --config-name test debug=fdr` を実行する
- **THEN** contrastive stage は fast_dev_run で完了する
- **AND** classification stage も callback 補間エラーなく train/test を開始して完了できる
