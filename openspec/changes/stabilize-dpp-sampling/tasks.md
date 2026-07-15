## 1. Artifacts

- [x] 1.1 Create proposal/design/spec/tasks for DPP numerical stability change
- [x] 1.2 Verify artifact status is apply-ready

## 2. Implementation

- [x] 2.1 Change DPP embedding dtype handling to float64
- [x] 2.2 Change default DPP mode from GS to GS_bis in datamodule
- [x] 2.3 Run aapd one-epoch DPP training and confirm probability-sum error is gone

## 3. Follow-up Implementation

- [x] 3.1 Suppress third-party stdout noise during FiniteDPP initialization and validate with targeted pytest

検証メモ（2026-03-02）:

- 実行コマンド:
  - `uv run pytest tests/test_dpp_sampler_stdout.py`
- 結果:
  - `1 passed`（DPP sampler 実行時に標準出力へノイズが出ないことを確認）

検証メモ（2026-03-01）:

- 実行コマンド:
  - `PROJECT_ROOT=$(pwd) uv run python src/train.py contrastive/sampler@contrastive.data=dpp contrastive.trainer.max_epochs=1 classification.model=null logger=csv`
- 結果:
  - `Trainer.fit` が `max_epochs=1` で正常終了（exit code 0）
  - 実行中に `ValueError: probabilities do not sum to 1` は発生しないことを確認
