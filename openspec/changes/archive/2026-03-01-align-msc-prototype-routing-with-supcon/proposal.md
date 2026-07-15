## Why

現行の multi-label では MSC が prototype 未指定時にバッチ内から自動生成するため、supcon 側の「学習可能 prototype を trainer から明示供給する」運用と一致していない。運用と比較実験の整合性を確保するため、MSC の prototype 供給経路を supcon と同じ方針に揃える必要がある。

## What Changes

- contrastive 学習で `contrastive/model=msc` のとき、`ContrastiveLitModule` が学習可能 prototype パラメータを保持し、正規化して MSC loss に明示的に渡す。
- `src/models/loss/msc.py` の prototype 自動生成分岐を削除し、prototype 未指定時は例外で fail-fast する。
- `configs/contrastive/model/msc.yaml` に MSC 向け prototype 供給を有効化する設定を追加する。
- MSC 自己テストを外部 prototype 前提へ更新し、設定解決テストとあわせて検証する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: MSC の標準学習経路を `loss_fn(z, labels, prototype)` 契約へ変更し、prototype 未指定時の内部自動生成を廃止する。

## Impact

- 影響コード:
  - `src/models/contrastive_module.py`
  - `src/models/loss/msc.py`
  - `configs/contrastive/model/msc.yaml`
  - `openspec/specs/training/spec.md`
- 影響範囲: `contrastive/model=msc` を使う contrastive 学習経路。
