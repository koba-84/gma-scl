## Why

直前の MXCLR refactor で graph pipeline は統一できましたが、`_build_graph` と `_distance_to_score` のような薄い wrapper が残りました。どちらも呼び出し先を 1 箇所に隠しているだけで、可読性より indirection を増やしています。

## What Changes

- `src/models/loss/mxclr.py` から不要な薄い wrapper を削除する
- `score_graph` と `_build_mxclr_graph` に処理を寄せ、関数呼び出し段数を減らす
- pytest と main spec は MXCLR の score graph 契約を維持したまま更新する

## Capabilities

### Modified Capabilities

- `training`: MXCLR score graph pipeline で不要な thin wrapper を残さない

## Impact

- `src/models/loss/mxclr.py`
- `openspec/specs/training.md`
- `openspec/specs/training/spec.md`
