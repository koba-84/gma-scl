## Context

`temperature` 系への命名統一は進んでいるが、MXCLR_PROTO 用の補助キーとして `tau_s_schedule` が alias 導出経路に残っている。現在の実装では `graph_temperature` が無い場合に `tau_s_schedule.start` へフォールバックするため、公開設定面に旧命名が事実上残存している。

## Goals / Non-Goals

**Goals:**
- MXCLR_PROTO の温度スケジュールキーを `graph_temperature_schedule` へ統一する。
- runtime logging と backfill の alias 導出が同一 canonical key を参照する状態に揃える。
- `training` spec の canonical naming 要件を実装と一致させる。

**Non-Goals:**
- 過去 run の互換変換や移行ユーティリティ追加。
- 数式表記としての τ 記号（論文表記）まで機械的に禁止すること。

## Decisions

- Decision 1: alias fallback key を `tau_s_schedule.start` から `graph_temperature_schedule.start` に変更する。
  - Rationale: 命名規約を runtime 実装にも適用し、公開設定面の一貫性を確保するため。
  - Alternative considered: 旧キーと新キーの両対応。却下理由は互換レイヤーを増やし、canonical key の曖昧性を残すため。
- Decision 2: 関連テスト fixture をすべて新キーへ更新する。
  - Rationale: logging/backfill 双方で同じ導出結果を維持しつつ、旧キー残存を検知できるようにするため。
- Decision 3: `openspec/specs/training/spec.md` の該当シナリオを更新し、旧 `tau_s_schedule` 非依存を明記する。
  - Rationale: 仕様と実装の齟齬を防ぎ、将来の回帰を抑制するため。

## Risks / Trade-offs

- [Risk] 旧キーのみを持つ既存設定入力で graph temperature alias が導出されなくなる。
  - Mitigation: 本変更は後方互換を持たない方針を明示し、仕様にも反映する。
- [Risk] テスト fixture の改名漏れにより CI が不安定化する。
  - Mitigation: tau 残存 grep と対象 pytest を併用して検証する。

## Migration Plan

1. OpenSpec task に沿って実装・テスト・spec 更新を 1 タスクで完了させる。
2. main training spec に delta を同期する。
3. change を archive へ移動し、PR でレビュー可能な形にする。

## Open Questions

- なし
