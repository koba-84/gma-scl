## MODIFIED Requirements

### Requirement: Contrastive loss naming and contract consistency

contrastive loss 実装は可読性のため簡潔で一貫した命名を使用し、`classification.py` を除く各 loss module は `nn.Module` wrapper と private 計算 helper の責務境界を共有しなければならない。

#### Scenario: Keep public class names and Hydra targets stable

- **WHEN** 開発者または coding agent が contrastive loss 実装を更新する
- **THEN** `Base` `MulSupCon` `MCACRWONEG` `MXCLR` `MSC` と `MCACRLoss` の公開 class 名は維持される
- **AND** `configs/contrastive/model/*.yaml` の `loss_fn._target_` は既存 target を継続して解決できる

#### Scenario: Keep forward as validation and orchestration layer

- **WHEN** 開発者または coding agent が `classification.py` を除く `src/models/loss/*.py` を更新する
- **THEN** 各 `forward` は入力 shape 検証と state / buffer 解決を担当する
- **AND** loss 本体計算は module-level private helper へ委譲される

#### Scenario: Use consistent private helper naming

- **WHEN** 開発者または coding agent が contrastive loss module に private 計算 helper を追加または更新する
- **THEN** loss 本体 helper は `_compute_<loss>_loss` の命名を使用する
- **AND** helper は公開 API として export しない

### Requirement: Loss unit verification must use pytest

`src/models/loss` 配下の contrastive loss 実装の単体検証は pytest を標準経路とし、ソースファイル末尾の `__main__` 自己テストを要求してはならない。

#### Scenario: Verify loss modules through pytest

- **WHEN** 開発者または coding agent が loss 単体検証を実行する
- **THEN** 検証は `uv run pytest ...` で実行される
- **AND** `uv run python src/models/loss/<loss_file>.py` を標準検証手順として要求しない

#### Scenario: Cover normal and invalid-input cases in pytest

- **WHEN** 開発者または coding agent が contrastive loss 向け pytest を追加または更新する
- **THEN** 各対象 loss は有限スカラーを返す正常系を少なくとも 1 つ持つ
- **AND** 主要な入力不正または設定不正に対する異常系を少なくとも 1 つ持つ

#### Scenario: Keep temporary dataset artifacts under repository tmp

- **WHEN** `MCACR` 系など train.csv を要する loss 向け pytest が一時ファイルを作成する
- **THEN** 一時ファイルは `multi-label/tmp` 配下を使う
- **AND** test 終了時にクリーンアップされる
