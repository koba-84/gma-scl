## MODIFIED Requirements

### Requirement: Classification stage must log standard validation and test metrics

classification stage は val/test で閾値依存指標と順位依存指標の両方を epoch 単位で記録しなければならない。multilabel mAP は sigmoid 後の score を入力として記録し、既存の checkpoint monitor は維持する。

#### Scenario: Log classification epoch metrics via MetricCollection

- **WHEN** 開発者または coding agent が classification stage の validation/test metric 実装を更新する
- **THEN** 同一入力を共有する epoch 指標群は `torchmetrics.MetricCollection` として管理される
- **AND** epoch end の記録は `self.log_dict()` でまとめて行われる

#### Scenario: Keep non-collection metrics on explicit `self.log()`

- **WHEN** 開発者または coding agent が classification stage の metric logging を実装する
- **THEN** `classification/epoch` や validation loss のような collection 化しない値だけ個別 `self.log()` を使う
- **AND** collection 化できる metric は個別 `self.log()` に戻さない
