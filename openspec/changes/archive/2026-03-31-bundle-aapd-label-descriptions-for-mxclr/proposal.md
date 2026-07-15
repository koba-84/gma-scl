# Change Proposal

## Why

MXCLR の既定 config は AAPD の label description file を前提に初期化するが、当該 data 配下ファイルは Git 管理されておらず CI checkout には存在しない。そのため `contrastive/model=mxclr` を compose / instantiate する fast test が継続的に失敗する。既定設定はリポジトリ単体で成立しなければならない。

## What Changes

- MXCLR に AAPD 組み込み label descriptions を追加し、`dataset_name=aapd` かつ `label_description_path` 未指定時の既定初期化で使用する。
- `configs/contrastive/model/mxclr.yaml` の既定 `label_description_path` を外部 data file 非依存へ変更する。
- spec とテストを、既定 instantiate が bundled descriptions で成功する契約へ更新する。

## Impact

- `contrastive/model=mxclr` の既定 compose / instantiate は CI とローカルで同一に成功する。
- 明示的に `label_description_path` を指定した場合は従来どおりその file を優先して読み込む。
