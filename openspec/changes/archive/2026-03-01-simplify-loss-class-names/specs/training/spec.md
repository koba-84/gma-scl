## MODIFIED Requirements

### Requirement: Contrastive loss 実装の命名

The contrastive loss 実装は可読性のため簡潔で一貫したクラス名を MUST 使用する。base loss 実装の公開クラス名は `Base`、supcon loss 実装の公開クラス名は `MulSupCon` とし、設定から同名で解決されなければならない。

#### Scenario: base loss クラスを構成から解決する

- **WHEN** `configs/contrastive/model/base.yaml` の `loss_fn._target_` を使ってインスタンス化する
- **THEN** `src.models.loss.base.Base` が解決され、学習時に利用できる

#### Scenario: base loss をパッケージから参照する

- **WHEN** `src.models.loss` から base loss を import する
- **THEN** `Base` が公開され、旧クラス名は公開されない

#### Scenario: supcon loss クラスを構成から解決する

- **WHEN** `configs/contrastive/model/ml_supcon.yaml` の `loss_fn._target_` を使ってインスタンス化する
- **THEN** `src.models.loss.ml_supcon.MulSupCon` が解決され、学習時に利用できる

#### Scenario: supcon loss をパッケージから参照する

- **WHEN** `src.models.loss` から supcon loss を import する
- **THEN** `MulSupCon` が公開され、旧クラス名は公開されない
