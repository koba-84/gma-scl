## Why

現在のプロジェクト識別子が `cacr-gcbs` / `cacr_gcbs` / `lightning-hydra-template` で分散しており、実験ログや配布メタデータの一貫性がない。運用上の名称を `multi-label-supcon` に統一したい。

## What Changes

- Python プロジェクト名を `multi-label-supcon` に変更する。
- logger 設定（wandb/comet/neptune）の project 名を `multi-label-supcon` に統一する。
- OpenSpec main specs のプロジェクト名参照を更新する。

## Capabilities

### Modified Capabilities

- training: wandb プロジェクト名の既定値を `multi-label-supcon` に更新する。
- evaluation: wandb プロジェクト名の既定値を `multi-label-supcon` に更新する。

## Impact

- 影響コード: pyproject.toml, uv.lock, configs/logger/*.yaml, openspec/specs/*.md
- モデル学習アルゴリズム・評価ロジックには影響しない。
