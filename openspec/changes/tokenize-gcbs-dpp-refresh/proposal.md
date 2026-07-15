## Why

GCBS/DPP のエポック更新時は依然として raw text から再エンコードしており、tokenized pipeline 導入後も前処理オーバーヘッドが残っている。サンプラ更新経路も tokenized tensors を直接使う契約へ統一し、更新処理の高速化と入力契約の一貫性を確保する。

## What Changes

- contrastive の sampler 更新経路（GCBS/DPP）を raw text ベースから tokenized tensor ベースへ変更する。
- DataModule に sampler 更新専用の tokenized mini-batch 取得APIを追加する。
- ContrastiveLitModule の埋め込み再計算処理を tokenized batch 入力へ変更する。
- サンプラ更新経路のテストを追加し、raw text 経路に依存しないことを検証する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: GCBS/DPP sampler refresh の埋め込み再計算入力を tokenized tensors に変更する。

## Impact

- 影響コード: `src/data/contrastive_datamodule.py`, `src/models/contrastive_module.py`, `tests/data_integration.py`
- 外部 API 影響: なし（内部契約変更）
- 性能影響: sampler refresh の CPU 前処理オーバーヘッド削減を見込む
