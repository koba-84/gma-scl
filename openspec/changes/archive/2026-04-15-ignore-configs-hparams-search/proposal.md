## Why

configs/hparams_search は実験時の探索条件を一時的に調整するための領域だが、現在は一部ファイルがGit追跡されており、不要な差分やレビュー負荷を生んでいる。追跡を停止し、OpenSpec上でもこの領域の編集を仕様変更に使わないことを明示する必要がある。

## What Changes

- .gitignore に configs/hparams_search/ を追加し、ディレクトリ全体を追跡対象外にする。
- 既存で追跡中の configs/hparams_search 配下ファイルをインデックスから外す。
- OpenSpec の agent-operation-policy に、configs/hparams_search 配下編集は仕様変更を伴わない運用対象であることを追加する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- agent-operation-policy: configs/hparams_search 配下編集の取り扱い（仕様変更禁止）を運用要件として追加する

## Impact

- 影響ファイル:
  - .gitignore
  - configs/hparams_search/*（追跡解除のみ）
- 影響仕様:
  - openspec/specs/agent-operation-policy/spec.md
