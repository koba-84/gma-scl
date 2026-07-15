## 1. Default Loss Switch

- [x] 1.1 `configs/contrastive/train.yaml` の既定 model を `base` に変更する
- [x] 1.2 `contrastive/model=ml_supcon` の明示指定で loss を切り替えられることを確認する
- [x] 1.3 `configs/contrastive/train_ml_supcon.yaml` を削除し、model 指定運用へ統一する

## 2. Epoch Sweep Configuration

- [x] 2.1 `configs/hparams_search/contrastive_epoch.yaml` を追加し `contrastive.trainer.max_epochs: 1,5,10,20` を定義する
- [x] 2.2 sweep 設定で classification 設定は既定（train/test true）を使用する
- [x] 2.3 `uv run python src/train.py --cfg job --resolve hparams_search=contrastive_epoch` で設定解決を確認する

## 3. Spec Sync

- [x] 3.1 `openspec/specs/training.md` に default loss と epoch sweep の運用ルールを反映する
