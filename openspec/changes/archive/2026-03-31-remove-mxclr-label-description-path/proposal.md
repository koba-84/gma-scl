# Change Proposal

## Why

MXCLR の semantic 初期化は `label_description_path` を明示パラメータとして持っているが、実際には `dataset_name` と data root が分かれば解決先は一意である。公開 config に不要な path 引数が残ると、dataset と独立に file path を二重管理することになり、設定が冗長で壊れやすい。

## What Changes

- MXCLR から `label_description_path` を削除し、`data_dir/<dataset_name>/label_descriptions.json` を既定解決にする。
- `dataset_name!='aapd'` の固定制約を削除し、任意 dataset で対応する `label_descriptions.json` が存在すれば初期化できるようにする。
- `data/aapd/label_descriptions.json` を Git 管理下へ追加し、既定 AAPD config を CI でも再現可能にする。
- spec とテストを新しい path 解決契約へ更新する。

## Impact

- MXCLR config は `data_dir` と `dataset_name` だけで semantic 初期化先が決まる。
- `<data_dir>/<dataset_name>/label_descriptions.json` が存在しない dataset は、学習開始前に FileNotFoundError で失敗する。
