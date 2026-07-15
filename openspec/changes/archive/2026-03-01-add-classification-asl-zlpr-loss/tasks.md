## 1. OpenSpec and Configuration

- [x] 1.1 classification loss 追加要件を OpenSpec artifacts（proposal/design/specs）に定義する
- [x] 1.2 classification model 設定に loss_name/loss_kwargs を追加する

## 2. Implementation

- [x] 2.1 src/models/loss/classification.py に AsymmetricLoss と ZLPRLoss を実装する
- [x] 2.2 src/models/finetune_module.py で loss_name による criterion 解決を実装する

## 3. Verification

- [x] 3.1 uv run python src/models/loss/classification.py で自己テストを実行する
- [x] 3.2 uv run pytest tests/configs.py -q で設定解決を検証する
- [x] 3.3 tasks の完了チェックを更新する
