## 1. OpenSpec artifacts

- [x] 1.1 proposal を作成し、対象範囲と影響範囲を定義する
- [x] 1.2 design を作成し、追加テストの設計判断と非目標を定義する
- [x] 1.3 training delta spec を作成し、unit/data-contract テスト要件を追加する

## 2. Test implementation

- [x] 2.1 `gcbs` 実装ファイル末尾に自己テストを追加する（入力検証・permutation 不変条件・Sampler）
- [x] 2.2 `dpp` 実装ファイル末尾に自己テストを追加する（初期化前エラー・入力検証・k 制約・drop_last）
- [x] 2.3 `classification_dataset` 実装ファイル末尾に自己テストを追加する（CSV 契約・異常系）
- [x] 2.4 `classification_datamodule` 実装ファイル末尾に自己テストを追加する（prepare/setup/dataloader/num_classes 異常系）
- [x] 2.5 `contrastive_datamodule` 実装ファイル末尾に自己テストを追加する（sampler 切替・初期化前エラー）
- [x] 2.6 `mlp_head` 実装ファイル末尾に自己テストを追加する（shape 契約・異常系）

## 3. Verification and spec sync

- [x] 3.1 追加自己テストを `uv run python src/data/components/<file>.py` / `src/data/<file>.py` / `src/models/components/<file>.py` で実行し、通過を確認する
- [x] 3.2 `openspec/specs/training.md` に本変更の確定仕様を同期する
