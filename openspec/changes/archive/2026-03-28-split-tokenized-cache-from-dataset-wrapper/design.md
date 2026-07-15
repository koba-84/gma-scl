## Context

shared base datamodule 導入後も `hf_tokenized_dataset.py` に cache key、metadata、CSV tokenization、cache load が残っており、module 名から期待される dataset wrapper 専用責務と一致していない。

## Goals / Non-Goals

**Goals:**
- dataset wrapper と tokenized cache helper の責務を分離する
- shared base datamodule から見た import 境界を明確にする

**Non-Goals:**
- tokenized cache contract や metadata 形式を変えること
- datamodule の外部 API を変えること

## Decisions

- `hf_tokenized_dataset.py` は dataset wrapper / bundle type のみ残す
- cache helper は `tokenized_dataset_cache.py` に移す
- shared base datamodule は cache module と wrapper module の両方を明示 import する

## Risks / Trade-offs

- module split による import path 変更で参照漏れが起きうる → `rg` と `pre-commit` で全参照を確認する
