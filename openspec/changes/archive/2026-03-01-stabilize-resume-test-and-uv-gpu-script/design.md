## Context

`src/train.py` は stage の `test=true` 実行後に `best.ckpt` と `last.ckpt` の削除を試行する。したがって、resume テストで checkpoint の存在を固定アサートする場合は、対象 stage で `test=false` を明示する必要がある。

また、contrastive stage は既定で `enable_checkpointing: False` のため、resume の checkpoint 起点としては不適切である。

## Goals / Non-Goals

Goals:

- resume テストを stage 設計と checkpoint 削除仕様に整合させる。
- GPU 実行スクリプトを `uv run` 実行へ統一し、再現性を高める。

Non-Goals:

- 学習ループ本体の挙動変更。
- checkpoint 削除仕様そのものの変更。

## Decisions

1. resume テストは classification stage を対象にする。
   理由: classification は checkpointing が有効で、`ckpt_path` 指定による resume を直接検証できるため。

2. checkpoint ファイル存在アサートを行うテストでは、対象 stage の `test` を無効化する。
   理由: `train.py` の仕様で test 後に ckpt 削除が走るため。

3. GPU 実行スクリプトは `uv run python src/train.py` を用い、`PROJECT_ROOT` 既定値を script 内で補完する。
   理由: 環境依存の差分を避け、仕様の実行契約と一致させるため。

## Risks / Trade-offs

- resume テストの対象を classification に寄せることで、contrastive 側の resume 回帰は別テストで担保が必要になる。
  - Mitigation: contrastive は checkpointing 無効が既定であり、本テストの責務外として仕様に明記する。
