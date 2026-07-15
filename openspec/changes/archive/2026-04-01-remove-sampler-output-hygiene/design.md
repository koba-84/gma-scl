## Context

この repo の project goal は、同一 commit・同一 Hydra 設定・同一 seed で同じ結果を再現できることである。sampler の system-level validation として重要なのは、`shuffle/gcbs/dpp` 切替、初期化順序、再現性、tokenized refresh path であり、stdout cleanliness はこれらに直接寄与しない。

現在の main spec は `sampler output hygiene` を独立 requirement とし、`tests/test_sampler_output_hygiene.py` で GCBS/DPP の stdout 非出力を確認している。しかしこれはデータ契約・学習挙動・評価プロトコルではなく、実装上の logging hygiene に近い。`src/data/components/dpp.py` でも `FiniteDPP` 初期化時の stdout を `redirect_stdout` で抑止しており、main spec が system-level ではなく implementation detail を縛っている。

## Goals / Non-Goals

**Goals:**

- sampler の main spec を system-level contract に限定する
- output hygiene targeted test を削除する
- DPP sampler 実装から stdout 抑止ロジックを除去する

**Non-Goals:**

- DPP sampler の sampling 挙動変更
- GCBS/DPP/ContrastiveDataModule の functional integration 再設計
- logging policy 全般の新規追加

## Decisions

1. `training` capability から sampler output hygiene requirement を削除する
   本リポジトリの目的に照らして、stdout cleanliness は main spec で守るべき研究システム契約ではない。

2. `tests/test_sampler_output_hygiene.py` は削除する
   この test は system-level regression ではなく implementation hygiene に依存しており、保守価値よりノイズが大きい。

3. `src/data/components/dpp.py` の `redirect_stdout` を削除する
   spec と test を落とした状態で実装だけ抑止を残す理由が薄く、責務を sampler の functional path に絞る。

## Risks / Trade-offs

- [Risk] DPPy の informational stdout が再び log に出る
  → Mitigation: これは system-level contract ではない前提で受容する
- [Risk] 過去 change archive に output hygiene の記述が残る
  → Mitigation: archive は履歴として保持し、main spec だけを現在の project policy とする

## Migration Plan

1. remove-sampler-output-hygiene change の delta spec と tasks を作成する
2. main spec から output hygiene contract を削除する
3. targeted pytest と DPP 実装の stdout 抑止を削除する
4. integration test と pre-commit で functional regressions がないことを確認する

## Open Questions

- なし
