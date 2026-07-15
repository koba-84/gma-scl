## Context

本リポジトリは commit/push 粒度や commit message は強制済みだが、branch 運用の強制は不十分である。現状は「protected branch に直接 push しない」方針が agent policy に存在するのみで、命名規約や pre-push 自動ブロックが明確ではない。

## Goals / Non-Goals

**Goals:**

- ブランチ運用ルールを OpenSpec で一意に参照できる状態にする。
- ローカル pre-push ゲートで protected branch 直接 push と不正な branch 名をブロックする。
- 既存の pre-commit 品質ゲート体系へ最小追加で統合する。

**Non-Goals:**

- GitHub サーバー側 ruleset 設定の自動作成・自動更新。
- 既存 branch の一括 rename。
- release 運用プロセスそのものの刷新。

## Decisions

1. 新規 capability `branch-governance-policy` を追加し、branch 運用を独立 spec として管理する。
   - 理由: version-control に寄せすぎると commit/push 規約と混在し、参照性が下がるため。

2. protected branch を `main`, `dev`, `release/*` と定義し、直接 push を禁止する。
   - 理由: 既存 workflow トリガー対象と一致し、現行運用から逸脱しないため。

3. topic branch 命名を `<type>/<topic>` に統一し、`type` を `feat|fix|refactor|docs|test|chore|exp|ops|hotfix` に制限する。
   - 理由: commit type と整合し、目的が分かる履歴を維持できるため。

4. 強制は pre-push hook (`scripts/validate_branch_policy.sh`) で行い、`.pre-commit-config.yaml` に always_run で登録する。
   - 理由: 開発者ローカルで push 前に即時失敗させ、既存ゲート設計に沿えるため。

## Risks / Trade-offs

- [Risk] ローカル hook 未導入環境では強制できない。
  Mitigation: spec に GitHub rulesets / protected branch でのサーバー側統制併用を明記する。

- [Risk] 例外運用（緊急 hotfix）で一時的に制約が厳しすぎる。
  Mitigation: `hotfix/*` を正規 type に含め、緊急対応の正規経路を確保する。

- [Risk] 特殊 push（`HEAD:main`）を current branch 名だけでは検知できない。
  Mitigation: pre-push の stdin から remote ref を検証し、保護ブランチ宛 push を拒否する。
