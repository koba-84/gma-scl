## Why

Loss を追加した際の設定追加と検証手順が会話ベースで散在し、実施範囲が人によってぶれています。研究用途の再現性を担保するため、OpenSpec 上で必須手順を明文化する必要があります。

## What Changes

- Loss を新規追加した際の標準作業フロー（実装、config追加、テスト）を training 仕様に追加する。
- config 追加手順として、`configs/contrastive/model/<loss_name>.yaml` の作成要件と `_target_` 設定要件を明記する。
- test 手順として、Loss 自己テストから pytest 統合、GPU 実機確認までの順序とコマンドを明記する。
- 変更実施時に OpenSpec change の tasks に検証実行結果を記録する運用を明記する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `training`: Loss 追加時の config 追加手順と test 手順を MUST レベルで標準化する。

## Impact

- 影響コード: `openspec/specs/training.md`
- 影響運用: Loss 追加時の実施手順が固定され、変更レビュー時に確認可能になる
