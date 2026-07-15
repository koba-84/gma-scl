## Why

contrastive loss ごとに温度パラメータ名が temp、temperature、tau で揺れており、設定比較と実装読解の両方で認知負荷が高い。加えて、loss 初期化に使う引数の一部が Python 側既定値にのみ存在し config からは見えないため、再現時に確認すべき場所が分散している。

## What Changes

- contrastive loss の温度パラメータ名を `temperature` 系へ統一し、Hydra config でも同じキーを使う。
- contrastive loss の初期化で使用する引数を config に明示し、Python 側既定値だけに依存しない構成へ揃える。
- loss config の解決値とインスタンス化を検証するテストを追加し、表記揺れや config 欠落の再発を防ぐ。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: contrastive loss の温度引数命名規則と config 完全性要件を追加する

## Impact

- Affected code: `src/models/loss/*.py`, `configs/contrastive/model/*.yaml`, `tests/losses/*.py`, `tests/test_configs.py`
- Affected systems: Hydra config 解決、contrastive loss 初期化、W&B に出る loss config の可読性
- Breaking surface: loss config key の `temp` / `tau` / `tau_s` を `temperature` 系へ置換する
