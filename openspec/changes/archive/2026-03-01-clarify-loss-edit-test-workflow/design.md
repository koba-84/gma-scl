## Context

既存仕様にはテスト階層の説明と新規 Loss 追加手順があるが、既存 Loss 編集時の「必須」と「影響時追加」の境界が明確ではない。結果として、変更規模に対して過剰または不足の検証が発生しやすい。

## Goals / Non-Goals

**Goals:**

- 既存 Loss 編集時の最低必須テストを明示する。
- 追加で実施すべき統合テスト条件を明示する。
- tasks 記録ルールを既存 Loss 編集にも適用する。

**Non-Goals:**

- pytest ケース自体の増減。
- Loss アルゴリズムや実装の変更。

## Decisions

1. `openspec/specs/training.md` に「既存 Loss 編集時の標準手順」を新設する。
   理由: 既存の「新規 Loss 追加手順」と混同しないため。

2. 最低必須を 2 点に固定する。

- `uv run python src/models/loss/<loss_file>.py`
- `uv run pytest tests/test_configs.py -q`
  理由: 実装妥当性と Hydra 解決破損を最低限カバーできるため。

3. 追加テストは影響ベースで実施条件を明示する。
   理由: 研究コード運用でコストと安全性のバランスを取るため。

## Risks / Trade-offs

- [Risk] 影響判定が主観的になる。
  Mitigation: tasks.md に「なぜ追加テストが不要か」を理由として残す。
- [Risk] 最低手順だけで済ませる誤用。
  Mitigation: 仕様で「学習経路に影響する変更では train/eval/sweeps を追加実施」と明記する。
