## Context

現在の `src/data/components` は sampler や dataset wrapper に加えて shared datamodule base と tokenized cache orchestration まで含んでいる。実装は分かれているが、階層としては datamodule-level concerns が component と同居しており不自然である。

## Goals / Non-Goals

**Goals:**
- `components` には低レベルの reusable data pieces だけを残す
- datamodule base と cache orchestration を `src/data` 直下へ移し、階層から役割が読めるようにする

**Non-Goals:**
- tokenization behavior や datamodule runtime contract を変えること
- config shape や external instantiate path を大きく変えること

## Decisions

- `tokenized_csv_datamodule.py` は `src/data/tokenized_datamodule_base.py` へ移す
- `tokenized_dataset_cache.py` は `src/data/tokenized_dataset_cache.py` へ移す
- classification / contrastive datamodule は新しい直下 module を import する

## Risks / Trade-offs

- import path 変更による参照漏れが起きうる → `rg`, pytest, pre-commit で確認する
