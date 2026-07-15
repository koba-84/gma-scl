## ADDED Requirements

### Requirement: Training internals must use canonical inline normalization
学習関連モジュールで行方向 L2 正規化を行う箇所は、torch.nn.functional.normalize を直接用いて実装しなければならない。単純な正規化 wrapper を新設または維持してはならない。

#### Scenario: Normalize contrastive embeddings and prototypes inline
- **WHEN** 開発者または coding agent が contrastive module や MXCLR loss の正規化実装を更新する
- **THEN** 行方向 L2 正規化は torch.nn.functional.normalize を直接呼び出して実装される
- **AND** normalize_embeddings や _normalize_prototype のような単純 wrapper は残さない

### Requirement: Classification datamodule must share one dataset requirement helper
classification datamodule の train/val/test 用 TokenizedDataset 存在確認は、split 名を受け取る単一 helper で実装しなければならない。

#### Scenario: Resolve split datasets through one shared helper
- **WHEN** 開発者または coding agent が classification datamodule の dataloader 実装を更新する
- **THEN** train_dataloader、val_dataloader、test_dataloader は共通の dataset requirement helper を使って対象 split を取得する
- **AND** split ごとに同型の _require_data_train、_require_data_val、_require_data_test を個別実装しない
