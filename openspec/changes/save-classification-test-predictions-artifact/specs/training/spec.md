## MODIFIED Requirements

### Requirement: Classification stage must log standard validation and test metrics

classification stage は val/test で閾値依存指標と順位依存指標の両方を epoch 単位で記録しなければならない。multilabel mAP は sigmoid 後の score を入力として記録し、既存の checkpoint monitor は維持する。

#### Scenario: Persist classification test score-target pairs as a W&B artifact

- **WHEN** 開発者または coding agent が W&B logger 付きで classification stage の test を実行する
- **THEN** test 中に計算した sigmoid score と正解ラベルの全ペアは単一の W&B artifact file として保存される
- **AND** artifact だけから `classification/test/map` などの test 指標を再計算できる

#### Scenario: Skip test prediction artifact logging without a W&B run

- **WHEN** 開発者または coding agent が W&B logger なしで classification stage の test を実行する
- **THEN** classification test metric logging は従来どおり完了する
- **AND** W&B artifact 保存処理は呼び出されない
