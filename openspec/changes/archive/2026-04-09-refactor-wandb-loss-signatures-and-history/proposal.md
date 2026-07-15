## Why

W&B config logging の比較キーが実験運用に対して不安定で、必要な alias が stage ごとに欠損するケースがある。加えて loss 実装が未使用引数を受け取る設計になっており、設定・実装・テストの対応関係が曖昧になっているため、仕様と実装を同時に整理する。

## What Changes

- W&B へ記録する config alias の必須項目を仕様化し、training logging と backfill の両方で同一導出ロジックを使うようにテスト要件を明確化する。
- contrastive loss の public 引数を実運用で使用するものに限定し、未使用引数の受け渡しを廃止する。**BREAKING**
- text encoder の tokenization `max_length` を 512 に統一し、設定と datamodule 既定値を一致させる。
- topic branch の commit history 整理ルール（線形履歴・過剰コミット抑制）を version-control 仕様へ追加し、pre-push で自動検証する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `training`: W&B alias 記録要件、loss 引数契約、tokenization 長の既定値要件を更新する
- `version-control`: push 前の commit history 整理ルールと自動検証要件を追加する

## Impact

- 影響コード:
  - `src/utils/logging_utils.py`
  - `src/utils/wandb_config_aliases.py`
  - `scripts/backfill_wandb_config.py`
  - `src/models/loss/mxclr.py`
  - `src/models/loss/msc.py`
  - `src/models/loss/agg/*.py`
  - `src/data/contrastive_datamodule.py`
  - `src/data/classification_datamodule.py`
  - `scripts/validate_branch_policy.sh`
- 影響設定:
  - `configs/contrastive/data/default.yaml`
  - `configs/classification/data/*.yaml`
- 影響テスト:
  - `tests/test_logging_utils.py`
  - `tests/test_wandb_config_aliases.py`
  - `tests/test_backfill_wandb_config.py`
  - `tests/losses/test_mxclr_loss.py`
  - `tests/losses/test_msc_loss.py`
  - `tests/property/test_mxclr_properties.py`
- 影響仕様:
  - `openspec/specs/training/spec.md`
  - `openspec/specs/version-control.md`
- 追加依存はなし
