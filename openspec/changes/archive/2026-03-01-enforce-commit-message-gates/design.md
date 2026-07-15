## Context

現行フローでは pre-commit がコード品質は検証するが、commit message 自体は検証していない。結果として件名形式不一致や本文不足が発生し、履歴品質の維持が人手依存になっている。

## Goals / Non-Goals

**Goals:**

- commit-msg 段で必須フォーマット逸脱を即時検出する。
- pre-push 段で push 対象コミットの再検証を行う。
- エラー理由を具体化し、修正手順を明確化する。

**Non-Goals:**

- Conventional Commits 全体への準拠。
- 既存履歴の自動修復。

## Decisions

- Decision 1: Python スクリプトを単一実装とし、commit-msg と pre-push の両方から再利用する。
  - Rationale: 仕様ロジックの重複を避け、判定差異をなくすため。
- Decision 2: `Feat/Fix/Refactor` は `Why:` と `Validation:` を必須化する。
  - Rationale: 仕様の「挙動変更コミットは根拠と検証を含む」を機械的に担保するため。
- Decision 3: ML 影響ファイル（`src/models`, `src/data`, `configs`）を含む場合は `Reproducibility:` を必須化する。
  - Rationale: 再現性文脈の記録漏れを防ぐため。
- Decision 4: pre-push は upstream 差分コミットを検証し、upstream 未設定時は警告表示のうえ検証をスキップする。
  - Rationale: 初回 push の運用阻害を避けつつ、通常運用の網羅性を確保するため。

## Risks / Trade-offs

- [Risk] 厳格化により一時的にコミット失敗が増える。
  - Mitigation: エラーメッセージに要件と記述例を表示する。
- [Risk] ML 判定パスが将来不足する。
  - Mitigation: 判定対象パスを定数化して追加容易にする。
