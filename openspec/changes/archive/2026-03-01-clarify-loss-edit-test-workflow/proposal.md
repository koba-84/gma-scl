## Why

現在の training 仕様は新規 Loss 追加時のテスト手順は明確だが、既存 Loss を編集した場合の手順が明示的に分離されておらず、運用判断がぶれやすい。レビューと再現性のため、編集時の最低実施項目と追加実施条件を明文化する。

## What Changes

- 既存 Loss を編集した場合の標準テスト手順を追加する。
- 最低必須手順を「対象 Loss 自己テスト + `tests/test_configs.py`」に固定する。
- 学習・評価・sweep・GPU 実行を、変更影響がある場合の追加手順として明示する。
- OpenSpec change の tasks 記録ルールを、既存 Loss 編集にも適用することを明記する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: 既存 Loss 編集時のテスト手順と記録要件を追加する。

## Impact

- 影響仕様: `openspec/specs/training.md`
- 影響運用: Loss 編集レビュー時の実施基準が統一される
