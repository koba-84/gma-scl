## ADDED Requirements

### Requirement: Standard workflow for adding a new contrastive loss

新しい contrastive loss を追加する場合、実装者は MUST OpenSpec change 上で config 追加手順と test 手順を記録し、再現可能な形で検証を完了しなければならない。

#### Scenario: Add loss config

- **WHEN** 開発者が新しい loss 実装を追加する
- **THEN** `configs/contrastive/model/<loss_name>.yaml` を追加し、`loss_fn._target_` が実装クラスを解決できる

#### Scenario: Run mandatory verification steps

- **WHEN** 開発者が loss 追加 change を完了する
- **THEN** 少なくとも loss 自己テストと `tests/test_configs.py` を実行し、結果を change の `tasks.md` に記録する

### Requirement: Ordered verification ladder for loss additions

Loss 追加時の検証は MUST 段階的に実施し、`uv run python src/models/loss/<loss_file>.py` から始めて統合テストおよび GPU 実行へ進める。

#### Scenario: Escalate from unit to integration

- **WHEN** loss 実装を検証する
- **THEN** 自己テスト成功後に pytest 統合（config/train/eval/sweeps）および必要な GPU 実行へ進む
