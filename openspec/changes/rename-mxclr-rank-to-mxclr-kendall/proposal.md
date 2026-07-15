## Why

`mxclr_rank` はすでに ranking 手法として Kendall τ を採用しており、名前と実体が一致していない。実験設定・ログ・比較表で誤解が起きないように、公開名を `mxclr_kendall` へ統一する。

## What Changes

- **BREAKING** `contrastive/model=mxclr_rank` を廃止し、`contrastive/model=mxclr_kendall` に置換する。
- loss 実装の公開クラス/モジュール名を `MXCLRKendall` / `mxclr_kendall.py` に変更する。
- 既存の Kendall 実装ロジックとパラメータ契約（`lambda_rank`, `kendall_k`）は維持する。
- config・pytest・OpenSpec main specs の参照名を `mxclr_kendall` に更新する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: Kendall ranking loss を使う MXCLR 系 loss の公開識別子を `mxclr_rank` から `mxclr_kendall` へ変更する

## Impact

- 影響コード: `src/models/loss/mxclr_rank.py`（rename）, `src/models/loss/__init__.py`, `configs/contrastive/model/*.yaml`, `tests/losses/*`, `tests/test_configs.py`
- 影響仕様: `openspec/specs/training/spec.md`, `openspec/specs/training.md`
- 互換性: 旧識別子 `mxclr_rank` は非対応になる
