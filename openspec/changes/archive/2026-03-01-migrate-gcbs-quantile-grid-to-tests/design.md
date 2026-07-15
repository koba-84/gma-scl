## Context

現状は GCBS quantile 探索を configs/hparams_search/gcbs_quantile_grid.yaml に集約している一方、test1 から test4 は別の探索軸を持っている。
この分離により、モデルとデータセットの組み合わせごとの探索設定を確認する際に複数ファイルを往復する必要がある。

## Goals / Non-Goals

**Goals:**

- test1 から test4 の各ファイルで GCBS quantile 探索を自己完結させる。
- 専用の gcbs_quantile_grid.yaml を廃止し、設定管理を簡潔にする。

**Non-Goals:**

- 学習ロジックや損失実装の変更は行わない。
- quantile 値そのもの（0.99, 0.98, 0.97）の再設計は行わない。

## Decisions

- test1 から test4 で sampler を GCBS 固定にする。
  - 理由: quantile 探索は GCBS 固有のため、default や dpp と同時スイープすると探索意図が曖昧になる。
- quantile と chunk_size を各ファイルに明示する。
  - 理由: 実行時に必要な GCBS パラメータを設定ファイル内で完結させるため。
- 既存のモデル別温度・tau 設定は維持する。
  - 理由: 今回の目的は quantile 探索配置の変更であり、他ハイパーパラメータ探索方針の変更はスコープ外。

## Risks / Trade-offs

- [Risk] sampler の探索軸が減ることで、test2 から test4 で比較していた方式差分の同時比較ができなくなる。
  - Mitigation: sampler 比較が必要な場合は別の hparams_search 設定を新規作成して分離する。
- [Risk] seed 探索と quantile 探索の組み合わせ数が増え、実行時間が伸びる。
  - Mitigation: 必要に応じて seed 数を CLI override で削減する。
