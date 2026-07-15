## Why

現在は Loss 実装ごとのテスト方針が OpenSpec に明示されておらず、実装者ごとに検証粒度が揺れている。研究コードとして挙動差分の早期検知を安定化するため、Loss の最小単体テスト要件を仕様として固定する。

## What Changes

- `src/models/loss` 配下の各 Loss 実装に、ファイル末尾で直接実行できる簡易単体テストを必須化する。
- 簡易単体テストの最低要件（有限スカラー出力、主要な入力バリデーション確認）を定義する。
- NPMI など一時ファイルを使う Loss では、`multi-label/tmp` 配下を使い、実行後にクリーンアップする要件を定義する。
- 実装時の検証手順として、対象 Loss ファイルの直接実行による自己テスト成功を確認対象に追加する。

## Capabilities

### New Capabilities

- `loss-self-test-policy`: Loss 実装ファイル内で実行可能な最小自己テストの必須ルールを提供する。

### Modified Capabilities

- `training`: contrastive loss 実装運用に、Loss ごとの自己テスト要件と検証手順を追加する。

## Impact

- 影響コード: `src/models/loss/*.py`, `openspec/specs/training.md`, `tests/*`（必要時）
- 影響運用: Loss の追加・修正時に、ファイル末尾自己テストの実装と実行確認が必須になる。
