## Purpose

Define evaluation-stage behavior, checkpoint usage, and execution contracts for model assessment.

## Requirements

### Requirement: Evaluation target stage

Evaluation flow MUST execute test for the classification stage in default configuration and MUST expose the standard classification test metrics including multilabel mAP.

#### Scenario: Run default evaluation path

- **WHEN** 開発者が既定設定で train/eval 経路を実行する
- **THEN** classification stage の test が実行される
- **AND** 出力 metric には `classification/test/f1_micro` と `classification/test/map` が含まれる

# 評価仕様（Evaluation Spec）

## 1. 評価（test）の対象（設定で確定）

- デフォルト設定では：
  - contrastive：`test: false`（評価しない）
  - classification：`test: True`（評価する）

根拠：

- `configs/contrastive/train.yaml`: `test: false`
- `configs/classification/train.yaml`: `test: True`

補足（運用方針）：

- contrastive は表現学習のため、標準の test は実施しない。

## 2. test 実行条件（コードで確定）

- `src/train.py` はステージごとに `stage_cfg.get("test", False)` を見て test を実行する。

## 3. test で使う重み（ckpt_path の決め方：コードで確定）

test 実行時、`ckpt_path` は以下の優先順で決まる：

1. `trainer.checkpoint_callback.best_model_path` があればそれを使用
2. best が無い（または checkpoint_callback が無い）場合：
   - `ckpt_path=None` のまま `trainer.test(...)` を実行
   - つまり「現在の重み」で test を行う

呼び出し形（確定）：

- `trainer.test(model=model, datamodule=datamodule, ckpt_path=ckpt_path)`

checkpoint callback を使う場合の選択基準（設定で確定）：

- `configs/callbacks/default.yaml` の `model_checkpoint.monitor` は `classification/val/f1_macro`
- したがって classification test は、validation macro-F1 最大の checkpoint を優先して評価する

## 4. test 後の ckpt 削除（コードで確定）

test 実行後、以下の削除を試みる：

- best ckpt（`ckpt_path` があれば）
- `last.ckpt`（`checkpoint_callback.dirpath/last.ckpt` が組める場合）

## 5. パス仕様（確定）

- `root_dir = ${oc.env:PROJECT_ROOT}`
- `data_dir = ${paths.root_dir}/data/`
- `log_dir  = ${paths.root_dir}/logs/`
- `output_dir = ${hydra:runtime.output_dir}`（Hydra により動的生成）
- `work_dir = ${hydra:runtime.cwd}`

## 6. wandb（確定）

- `configs/logger/wandb.yaml` より：
  - `project: multi-label-supcon`
  - `save_dir: ${paths.output_dir}`
  - `group` と `tags` はデフォルト空（必要なら override で指定）

## 7. 評価系テストの位置づけ

- 単体レベルの検証は `tests/test_contrastive_losses.py` などの pytest で扱い、評価仕様では統合経路を対象にする。
- 評価フローの統合検証は `tests/test_eval.py` を標準とし、`train -> ckpt 作成 -> eval` の接続を確認する。
- 実機 GPU 前提の包括確認は `scripts/test.sh` で行う（ローカルマシン実行）。
