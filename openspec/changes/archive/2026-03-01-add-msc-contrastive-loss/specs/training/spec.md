## MODIFIED Requirements

### Requirement: Contrastive loss 実装の命名

- contrastive loss 実装は可読性のため簡潔で一貫した命名を使用する。
- loss 実装ファイル名は src/models/loss/\<loss_name>.py の形式に統一し、loss\_ などの冗長な接頭辞を付けない。
- base loss の公開クラス名は Base とする。
- supcon loss の公開クラス名は MulSupCon とする。
- MCACR 派生 loss の公開クラス名として MCACR_WONEG を提供する。
- MSC loss の公開クラス名として MSC を提供する。
- MCACRLoss は data_dir と dataset_name を受け取り、内部で \<data_dir>/\<dataset_name>/train.csv を解決して初期化時に毎回 NPMI 行列を直接計算する。
- contrastive loss へ渡す埋め込みの L2 正規化は src/models/contrastive_module.py の ContrastiveLitModule.\_project で実施する。
- loss 実装側（例: src/models/loss/mxclr.py）は埋め込み正規化を重複実装しない。
- MCACR 系 loss（MCACR / MCACR_WONEG）は、アンカーに正例が存在しない場合にのみ repulsion 項を 0 化する。
- configs/contrastive/model/base.yaml の loss_fn._target_ は src.models.loss.base.Base を参照する。
- configs/contrastive/model/ml_supcon.yaml の loss_fn._target_ は src.models.loss.ml_supcon.MulSupCon を参照する。
- configs/contrastive/model/mcacr_woneg.yaml の loss_fn._target_ は src.models.loss.mcacr_woneg.MCACR_WONEG を参照する。
- configs/contrastive/model/mxclr.yaml の loss_fn._target_ は src.models.loss.mxclr.MXCLR を参照する。
- configs/contrastive/model/msc.yaml の loss_fn._target_ は src.models.loss.msc.MSC を参照する。
- MXCLR は標準経路で loss_fn(z, labels) を受け取り、内部で similarity_graph(labels) を使って類似度行列へ変換する。
- MSC は標準経路で loss_fn(z, labels) を受け取り、prototype 未指定時は labels と z から内部で prototype を構築して計算する。

#### Scenario: base loss クラスを構成から解決する

- **WHEN** configs/contrastive/model/base.yaml の loss_fn._target_ を使ってインスタンス化する
- **THEN** src.models.loss.base.Base が解決され、学習時に利用できる

#### Scenario: base loss をパッケージから参照する

- **WHEN** src.models.loss から base loss を import する
- **THEN** Base が公開され、旧クラス名は公開されない

#### Scenario: supcon loss クラスを構成から解決する

- **WHEN** configs/contrastive/model/ml_supcon.yaml の loss_fn._target_ を使ってインスタンス化する
- **THEN** src.models.loss.ml_supcon.MulSupCon が解決され、学習時に利用できる

#### Scenario: supcon loss をパッケージから参照する

- **WHEN** src.models.loss から supcon loss を import する
- **THEN** MulSupCon が公開され、旧クラス名は公開されない

#### Scenario: mcacr woneg loss クラスを構成から解決する

- **WHEN** configs/contrastive/model/mcacr_woneg.yaml の loss_fn._target_ を使ってインスタンス化する
- **THEN** src.models.loss.mcacr_woneg.MCACR_WONEG が解決され、学習時に利用できる

#### Scenario: mcacr woneg loss をパッケージから参照する

- **WHEN** src.models.loss から mcacr woneg loss を import する
- **THEN** MCACR_WONEG が公開される

#### Scenario: msc loss クラスを構成から解決する

- **WHEN** configs/contrastive/model/msc.yaml の loss_fn._target_ を使ってインスタンス化する
- **THEN** src.models.loss.msc.MSC が解決され、学習時に利用できる

#### Scenario: msc loss を標準経路で実行する

- **WHEN** ContrastiveLitModule.model_step が loss_fn(z, labels) を呼び出す
- **THEN** MSC は追加引数なしで有限スカラー損失を返す
