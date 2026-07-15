## MODIFIED Requirements

### Requirement: Classification stage must log standard validation and test metrics

classification stage は val/test で閾値依存指標と順位依存指標の両方を epoch 単位で記録しなければならない。multilabel mAP は sigmoid 後の score を入力として記録し、既存の checkpoint monitor は維持する。

#### Scenario: Log validation metrics including mAP

- **WHEN** 開発者または coding agent が classification stage の validation を実行する
- **THEN** `classification/val/f1_macro`, `classification/val/f1_micro`, `classification/val/hamming_loss`, `classification/val/map` が epoch metric として記録される
- **AND** `classification/val/map` は二値化後予測ではなく sigmoid score から計算される

#### Scenario: Log test metrics including mAP

- **WHEN** 開発者または coding agent が classification stage の test を実行する
- **THEN** `classification/test/f1_macro`, `classification/test/f1_micro`, `classification/test/hamming_loss`, `classification/test/map` が epoch metric として記録される
- **AND** 空テキスト補正は F1/hamming loss 用の二値予測にだけ適用され、mAP 用 score は順位情報を保持する
