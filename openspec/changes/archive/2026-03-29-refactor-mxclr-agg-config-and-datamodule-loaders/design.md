## Context

MXCLR は graph builder の family 差分を Hydra config ではなく Python dict registry で持っており、`agg` の変更が config 解決だけでは完結していません。一方で tokenized datamodule は共通 base に `val_dataloader` / `test_dataloader` があり、subclass に `train_dataloader` だけが残っているため、公開 hook の位置が読みづらくなっています。

## Goals / Non-Goals

**Goals:**
- MXCLR agg 差分を config group に寄せ、Python 側の registry を削除する
- `mxclr.yaml` で agg group を defaults から読む形にする
- datamodule 共通化を維持しながら、各 datamodule が train/val/test loader を同じ module に揃えて持つ

**Non-Goals:**
- MXCLR の数式や supported agg family 自体を変えること
- sampler refresh や tokenized cache contract を変えること
- MCACR の agg config まで同時に group 化すること

## Decisions

### Decision 1: MXCLR agg family は config group から graph builder を注入する

- `configs/contrastive/model/agg/<name>.yaml` を追加し、`loss_fn.agg` と `loss_fn.graph_builder` をその group に持たせる
- `graph_builder` は `_build_mxclr_graph` を target にした partial callable とし、family 差分は config 側で表現する
- `MXCLR` は `graph_builder` callable を受け取り、`score_graph()` で直接呼ぶ
- `MXCLR_GRAPH_BUILDERS` は削除する

### Decision 2: datamodule base は dataloader helper だけを共有する

- base は tokenized setup、label map、shared collate、dataset requirement helper、generic dataloader builder を持つ
- `val_dataloader` / `test_dataloader` は base の公開 API から外す
- `ClassificationDataModule` と `ContrastiveDataModule` はそれぞれ `train_dataloader` / `val_dataloader` / `test_dataloader` を同じ module 内に定義する
- 共通部分は base helper を呼ぶだけにして、挙動差は subclass で明示する

## Risks / Trade-offs

- agg override の CLI 文字列は `contrastive.model.loss_fn.agg=...` から `contrastive/model/agg=...` に寄る
  - 仕様と tests を同時に更新し、config 解決手順を一貫させる
- dataloader 実装を各 module に戻すと見た目の重複は少し増える
  - 共通 DataLoader 組み立ては base helper に残し、公開 hook の所在だけを標準的に揃える
