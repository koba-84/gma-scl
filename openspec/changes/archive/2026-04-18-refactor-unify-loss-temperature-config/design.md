## Overview

本変更は、contrastive loss 実装と Hydra config の公開契約を `temperature` 系命名へ揃え、同時に loss 初期化引数を config 上へ出し切る。対象は Base、MulSupCon、MSC、MXCLR、MCACR、MCACRWONEG とし、内部補助関数も同じ命名に合わせて更新する。

## Design Decisions

### 1. 温度引数は `temperature` を基底名に統一する

- 単一温度の loss は `temperature` を使う
- 役割が分かれる loss は `positive_temperature`、`negative_temperature`、`graph_temperature` のように役割接頭辞を付ける
- `tau`、`tau_s`、`temp`、`temp_attract`、`temp_repulse` は公開 config と公開コンストラクタから除外する

### 2. config を初期化契約の正本にする

- 各 loss の `__init__` で受ける runtime 引数は config に全て明示する
- 既定値は Python 実装にも残すが、標準 train config では省略しない
- `eps` のような数値安定化引数も対象に含める

### 3. 既存の stage wiring は変えない

- `ContrastiveLitModule` の loss 呼び出し経路は変えない
- Hydra の `_target_` とネスト構造は維持し、キー名だけを整理する
- W&B alias 実装は leaf 値をそのまま拾うため、主に config key 更新とテスト更新で追従する

## Validation

- `uv run pytest tests/test_configs.py tests/losses/test_base_loss.py tests/losses/test_ml_supcon_loss.py tests/losses/test_msc_loss.py tests/losses/test_mxclr_loss.py tests/losses/test_mcacr_losses.py`
- `uv run python src/train.py --cfg job --resolve > multi-label/tmp/refactor-unify-loss-temperature-config-resolved.yaml`
- 必要に応じて `uv run pre-commit run -a`
