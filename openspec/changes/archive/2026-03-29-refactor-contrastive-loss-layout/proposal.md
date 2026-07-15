## Why

contrastive loss 実装ごとに `forward` の責務と private helper の置き方が揺れており、同じ種類の計算でも追い方が変わっています。あわせて各ファイル末尾の自己テスト運用が pytest 中心の現行テスト方針とズレているため、loss 実装構成と検証契約をまとめて整理する必要があります。

## What Changes

- `classification.py` を除く `src/models/loss` の contrastive loss を、`nn.Module` wrapper と module-level `_compute_*` helper の構成へ統一する
- `forward` は入力検証と state 解決に限定し、loss 本体計算は private helper へ寄せる
- `src/models/loss/*.py` の `__main__` 自己テストを削除し、対応する検証を pytest へ移す
- loss 検証の標準経路を pytest に更新し、OpenSpec の training / evaluation 契約を同期する

## Capabilities

### New Capabilities

### Modified Capabilities

- `training`: contrastive loss 実装の内部構成と単体検証契約を pytest ベースへ更新する
- `evaluation`: loss 単体検証の位置づけを自己テストから pytest へ更新する

## Impact

- `src/models/loss/base.py`
- `src/models/loss/ml_supcon.py`
- `src/models/loss/mcacr.py`
- `src/models/loss/mcacr_woneg.py`
- `src/models/loss/msc.py`
- `src/models/loss/mxclr.py`
- `tests/`
- `openspec/specs/training/spec.md`
- `openspec/specs/evaluation/spec.md`
