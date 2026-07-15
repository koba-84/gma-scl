## 1. OpenSpec仕様反映

- [x] 1.1 `mcacr-woneg-loss` capability の要件を満たす実装方針を最終確認する
- [x] 1.2 `training` capability の命名・設定解決要件に `MCACR_WONEG` を反映する

## 2. Loss実装

- [x] 2.1 `src/models/loss/mcacr_woneg.py` を追加し `MCACR_WONEG` を実装する
- [x] 2.2 負例項でラベル重みを使わない専用計算を実装し、`MCACRLoss` 既存挙動を維持する
- [x] 2.3 `src/models/loss/__init__.py` に公開シンボルを追加する

## 3. 設定と検証

- [x] 3.1 `configs/contrastive/model/mcacr_woneg.yaml` を追加し Hydra から解決可能にする
- [x] 3.2 loss 単体テストを追加し `MCACR_WONEG` の forward と公開 API を検証する
- [x] 3.3 `uv run pytest` で追加テストを実行し、結果を確認する
