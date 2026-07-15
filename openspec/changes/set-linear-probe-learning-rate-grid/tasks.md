## 1. Sweep 設定更新

- [x] 1.1 `configs/hparams_search/contrastive_epoch.yaml` の `contrastive.model.optimizer.lr` を `5e-5,1e-4` に更新する
- [x] 1.2 同ファイルの `classification.model.optimizer.lr` を `1e-3,5e-4` に更新する

## 2. 仕様同期

- [x] 2.1 `openspec/specs/training/spec.md` に linear_probe の learning-rate grid 要件を反映する
- [x] 2.2 `openspec/specs/training.md` の該当節を更新して設定値と一致させる

## 3. 検証

- [x] 3.1 `PROJECT_ROOT=$(pwd) uv run python src/train.py --cfg job --resolve hparams_search=contrastive_epoch` で設定解決を確認する
