## 1. Config Restructure

- [x] 1.1 configs/classification/model を strategy/loss グループへ再編する
- [x] 1.2 classification/train.yaml の defaults を strategy/loss 2軸へ変更する

## 2. Verification

- [x] 2.1 classification/strategy=linear_probe classification/loss=asymmetric の設定解決を確認する
- [x] 2.2 classification/strategy=finetune classification/loss=zlpr の設定解決を確認する
- [x] 2.3 uv run pytest tests/configs.py -q を実行する

## 3. Spec Sync

- [x] 3.1 main spec (openspec/specs/training/spec.md) に 2軸構成を反映する
- [x] 3.2 tasks 完了チェックを更新する
