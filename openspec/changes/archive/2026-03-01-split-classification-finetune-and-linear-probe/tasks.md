## 1. OpenSpec Artifacts

- [x] 1.1 proposal を作成する
- [x] 1.2 training capability の delta spec を作成する
- [x] 1.3 design を作成する

## 2. Config Refactor

- [x] 2.1 `configs/classification/model/finetune.yaml` を `configs/classification/model/linear_probe.yaml` に改名する
- [x] 2.2 新規 `configs/classification/model/finetune.yaml` を作成し `encoder_freeze: false` を設定する
- [x] 2.3 設定解決で `classification/model=linear_probe` と既定 `finetune` の両方を確認する
