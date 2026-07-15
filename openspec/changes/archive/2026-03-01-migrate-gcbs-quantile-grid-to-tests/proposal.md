## Why

GCBS の quantile 探索が専用ファイルに分離されており、既存の test1 から test4 との対応が分かりにくい。
各データセットと損失設定の探索ファイル内で quantile を管理し、実験設定の見通しを改善する。

## What Changes

- configs/hparams_search/gcbs_quantile_grid.yaml を削除する。
- configs/hparams_search/test1.yaml から test4.yaml で GCBS を固定し、quantile グリッドを追加する。
- quantile 探索で必要な GCBS 固有パラメータ chunk_size を各対象ファイルに明示する。

## Capabilities

### New Capabilities

- `gcbs-quantile-sweep-layout`: hparams_search の各 test 設定で GCBS quantile 探索を直接定義できる。

### Modified Capabilities

- `training`: Hydra の hparams_search 設定運用において、GCBS quantile 探索の定義場所を専用ファイルから test1 から test4 へ変更する。

## Impact

- 影響ファイル: configs/hparams_search/test1.yaml, configs/hparams_search/test2.yaml, configs/hparams_search/test3.yaml, configs/hparams_search/test4.yaml
- 削除ファイル: configs/hparams_search/gcbs_quantile_grid.yaml
- 実験実行時のオーバーライド指定は hparams_search=test1 から test4 に統一される。
