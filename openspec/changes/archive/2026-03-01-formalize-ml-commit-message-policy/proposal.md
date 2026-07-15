## Why

現在のリポジトリでは commit メッセージの粒度と timing は定義されているが、メッセージ本文に何を残すべきか、特に ML 実験の再現性に必要な情報（設定・検証・影響範囲）の記録要件が不十分である。Git/GitHub/Conventional Commits/OpenSpec のベストプラクティスに基づき、レビューしやすく再現可能な commit メッセージ規約を明文化する必要がある。

## What Changes

- commit メッセージの件名フォーマット（型、命令形、長さ制約）を MUST/SHOULD レベルで定義する。
- 本文の構成を標準化し、変更理由・主要変更点・検証コマンドを記録する要件を追加する。
- ML 変更（モデル・損失・サンプラ・データ・学習設定）の場合に、再現に必要な設定情報を本文へ残す要件を追加する。
- OpenSpec change ID と commit メッセージの対応を推奨し、仕様変更の追跡性を高める。

## Capabilities

### New Capabilities

- commit-message-policy: 再現性を重視する ML プロジェクト向けに、commit message の件名・本文・補助情報の記載規約を定義する。

### Modified Capabilities

- version-control: 既存の commit/push 規約に commit message 規約との接続要件を追加する。

## Impact

- 影響仕様:
  - openspec/specs/version-control.md
  - openspec/specs/commit-message-policy/spec.md（新規）
- 影響運用:
  - commit から再現条件を復元しやすくなり、レビューと差分追跡の品質が向上する。
