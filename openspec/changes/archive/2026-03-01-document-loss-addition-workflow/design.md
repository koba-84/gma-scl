## Context

現行仕様には Loss 自己テスト要件とテスト階層はあるが、Loss を追加した時にどの config をどう追加し、どの順でどこまで検証するかが一つの手順としてまとまっていません。このため、実装者ごとに検証粒度が変わりやすい状態です。

## Goals / Non-Goals

**Goals:**

- Loss 追加時の config 追加手順を標準化する。
- Loss 追加時の test 手順を段階的に標準化する。
- OpenSpec change の tasks へ検証結果を残す運用を明確化する。

**Non-Goals:**

- 既存 Loss アルゴリズムの変更。
- pytest の新規テストコード追加そのものを必須化すること。

## Decisions

- `openspec/specs/training.md` に「Loss 追加標準フロー」節を追加する。
- config 手順は `configs/contrastive/model/<loss_name>.yaml` 追加と `_target_` 解決確認を必須化する。
- test 手順は以下の順序を必須化する。
  1. Loss ファイル自己テスト
  2. `tests/test_configs.py` による instantiate 検証
  3. 必要に応じて `tests/test_train.py`, `tests/test_eval.py`, `tests/test_sweeps.py`
  4. GPU 実機 `scripts/test.sh`
- 実行結果は対象 change の `tasks.md` にチェックボックスとして記録する。

## Risks / Trade-offs

- [Risk] 手順が増えて初回作業コストが上がる。
  - Mitigation: 実行順と最小コマンドをテンプレ化して迷いを減らす。
- [Risk] 全統合テストを毎回実行できないケースがある。
  - Mitigation: 実施/未実施を tasks に明示記録し、レビュー時に判断可能にする。
