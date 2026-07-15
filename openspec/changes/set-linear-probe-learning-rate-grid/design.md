## Context

既存の `configs/hparams_search/contrastive_epoch.yaml` は linear_probe 用 sweep の学習率を単一点で持っており、仕様文書とも不整合がある。
本変更では、contrastive/classification の両ステージで探索候補を明示的に 2 値ずつ定義する。

## Goals / Non-Goals

**Goals:**
- linear_probe の learning rate 探索範囲を `contrastive: 5e-5,1e-4`、`classification: 1e-3,5e-4` に統一する。
- Hydra sweeper 設定と OpenSpec 学習仕様の記述を一致させる。

**Non-Goals:**
- optimizer 種別や weight decay など、learning rate 以外の最適化設定変更。
- train エントリポイントや学習ロジックのコード変更。

## Decisions

- Decision 1: sweep 値は `configs/hparams_search/contrastive_epoch.yaml` にカンマ区切りで定義する。
  - 理由: 既存の Hydra basic sweeper 運用と整合し、追加コードなしで組み合わせ探索できる。
  - 代替案: 別 hparams_search ファイルを新設する案は、設定分散を招くため採用しない。

- Decision 2: main specs (`openspec/specs/training/spec.md` と `openspec/specs/training.md`) へ同一値を同期する。
  - 理由: 実行設定と仕様書の乖離を防ぎ、再現性を担保する。
  - 代替案: 設定ファイルのみ更新する案は、仕様参照時の誤読を招くため採用しない。

## Risks / Trade-offs

- [Risk] sweep 組み合わせ増加で実行時間が増える
  → Mitigation: 候補数は各2値に限定し、既存運用に対して最小限の増分に留める。

- [Risk] 仕様と設定の片側更新による不整合
  → Mitigation: 変更対象を設定ファイルと main specs に限定し、同一コミットで同期する。
