## Why

classification stage の validation/test metric は個別 `self.log()` 呼び出しに分散しており、TorchMetrics/Lightning の推奨パターンである `MetricCollection` と `self.log_dict()` に揃っていない。metric 定義をまとまりとして扱える形へ寄せ、実装と回帰テストの両方を整理する必要がある。

## What Changes

- classification validation/test の epoch 指標を `MetricCollection` にまとめる
- `self.log_dict()` で一括記録できる metric は epoch end にまとめて出力する
- loss と epoch axis のような collection 化しない項目だけ個別 `self.log()` に残す
- finetune metric logging 契約を spec と pytest で固定する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: classification metric logging の実装契約を `MetricCollection` ベースへ更新する

## Impact

- 影響コード:
  - `src/models/finetune_module.py`
- 影響テスト:
  - `tests/test_finetune_module_artifact.py`
  - `tests/integration/data/test_data_integration.py`
- 影響仕様:
  - `openspec/specs/training/spec.md`
