## 1. Config Update

- [x] 1.1 `configs/contrastive/train.yaml` の `trainer.max_epochs` を 80 に変更する
- [x] 1.2 `configs/hparams_search/contrastive_epoch.yaml` の意図を固定 80 前提で確認し、必要なら文言を更新する

## 2. Spec Sync

- [x] 2.1 `openspec/specs/training/spec.md` に contrastive epoch 80 固定ルールを追記する
- [x] 2.2 `openspec/specs/training/spec.md` から epoch sweep（1,5,10,20）運用記述を削除または置換する

## 3. Validation

- [x] 3.1 `uv run python src/train.py --cfg job --resolve` で `contrastive.trainer.max_epochs=80` を確認する
- [x] 3.2 変更差分を確認し、OpenSpec change artifact と実装が一致していることを確認する
