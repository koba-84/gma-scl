## Context

現在の tokenized CSV datamodule は両方とも `build_or_load_tokenized_splits` に依存しており、Lightning hook から見ると datamodule が何を準備し何を load するかが外部関数に分散している。`tokenized-datamodule-layout` spec では共通 setup / loader 集約が要求されているため、shared base class へ責務を戻す。

## Goals / Non-Goals

**Goals:**
- Lightning の `prepare_data()` / `setup()` で tokenized cache lifecycle を完結させる
- classification / contrastive が同じ tokenized setup 実装を共有する
- sampler 固有差分は contrastive 側に残す

**Non-Goals:**
- train entrypoint や config key の外部 shape を変えること
- tokenized cache 仕様や metadata contract を変えること

## Decisions

- `TokenizedCSVDataModuleBase` を追加し、batch size per device、prepare/setup、label map、shared collate、val/test dataloader、dataset requirement helper を持たせる
- `hf_tokenized_dataset.py` は `TokenizedTorchDataset` と bundle type を維持しつつ、tokenized cache 操作を private helper 群へ分解する
- classification は num_classes 検証だけを setup 後処理に残し、contrastive は sampler 初期化だけを setup 後処理に残す

## Risks / Trade-offs

- 共通 base へ寄せすぎると subclass の自由度が落ちる → sampler と train_dataloader は subclass 側に残す
- private helper 分解でモジュール間参照が増える → tokenized cache helper は data components 配下に閉じる
