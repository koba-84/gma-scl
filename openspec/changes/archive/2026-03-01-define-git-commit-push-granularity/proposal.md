## Why

現在の運用では git commit と push の粒度が明文化されておらず、変更の切り分けとレビュー単位が作業者ごとにぶれています。研究コードとして再現性を担保するため、変更を追跡しやすい commit/push 規約を OpenSpec に固定する必要があります。

## What Changes

- commit 粒度を「単一の論理変更 + その変更単体で説明可能」に統一する。
- push 粒度を「レビュー可能な単位でまとめるが、複数トピックを混在させない」に統一する。
- commit 前の最小検証と、push 前の fast テスト要件を明記する。
- commit メッセージ書式を最小限統一し、再現に必要な情報を含める規約を追加する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- version-control: git commit/push の運用粒度と実行前検証を MUST レベルで標準化する。

## Impact

- 影響コード: openspec/specs/version-control.md
- 影響運用: 変更単位の一貫性が上がり、レビューと原因追跡が容易になる
