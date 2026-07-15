## Overview

validation/test の multilabel metrics は、閾値依存指標群と順位依存指標群で入力が異なるため、2 つの `MetricCollection` に分ける。各 step では collection を update し、epoch end で `compute()` した dict を `self.log_dict()` へ渡す。

## Metric Layout

- validation threshold metrics:
  - `classification/val/f1_macro`
  - `classification/val/f1_micro`
  - `classification/val/hamming_loss`
- validation ranking metrics:
  - `classification/val/map`
- test 側も同じ粒度で `classification/test/*` を定義する

## Logging Policy

- `classification/epoch` と `classification/val/loss` は個別 `self.log()` を維持する
- MetricCollection から compute した dict は `on_validation_epoch_end` / `on_test_epoch_end` で `self.log_dict()` する
- collection は epoch end で reset する

## Validation

- unit test で validation/test epoch end が `self.log_dict()` に期待 key をまとめて渡すことを確認する
- 既存 integration test で classification test metric が引き続き train entrypoint から取得できることを確認する
