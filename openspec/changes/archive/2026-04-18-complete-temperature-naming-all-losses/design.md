## Context

loss/config の公開温度キーは canonical naming へ整理済みだが、全 loss 横断の検証が欠けると旧キー再混入を見逃しやすい。特に Hydra config と Python 実装の引数名ずれは、実験再現性の低下に直結する。

## Goals / Non-Goals

**Goals:**
- 全 contrastive loss について runtime 初期化引数と config key の一致を検証する。
- 旧温度キー混入を単体テストで自動検知する。

**Non-Goals:**
- loss の数式・学習挙動の変更。
- 旧キー互換レイヤーの追加。

## Decisions

- Decision 1: `tests/test_configs.py` に、loss クラスの signature と config key を照合する parametrized test を追加する。
  - Rationale: 実装・設定の両面を同時に検証でき、将来の rename 漏れを早期に検出できる。
- Decision 2: 旧キー禁止判定を同テスト内で明示する。
  - Rationale: canonical naming 破壊を直接検知できるため。

## Risks / Trade-offs

- [Risk] 将来の loss 引数追加時にテスト更新が必要になる。
  - Mitigation: 仕様上必要な追従コストとして受け入れ、変更時に expected key を更新する。

## Migration Plan

1. テストを追加し、対象 pytest を実行する。
2. main training spec を delta へ同期する。
3. OpenSpec task 完了後に archive する。

## Open Questions

- なし
