## Why

温度パラメータ命名は `temperature` 系へ統一済みのはずだが、MXCLR_PROTO の補助キーに `tau_s_schedule` が残っており、命名ポリシーと実装実態が不一致になっている。設定レビュー時に「どのキーが canonical か」が曖昧になるため、公開設定面を完全に `temperature` 系へ揃える。

## What Changes

- MXCLR_PROTO 由来のスケジュールキーを `tau_s_schedule` から `graph_temperature_schedule` へ改名する。
- W&B alias 導出ロジックで参照する fallback パスを `graph_temperature_schedule.start` に更新する。
- 既存テスト fixture/期待値を新キーへ更新し、`tau` 命名が公開設定面に残らないことを検証する。
- OpenSpec training 要件の該当シナリオを新キーに合わせて更新する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `training`: Contrastive 温度関連キーの canonical naming 要件を MXCLR_PROTO の schedule key まで厳密適用する。

## Impact

- Affected code: `src/utils/wandb_config_aliases.py`
- Affected tests: `tests/test_logging_utils.py`, `tests/test_wandb_config_aliases.py`, `tests/test_backfill_wandb_config.py`
- Affected spec: `openspec/specs/training/spec.md`
- 互換レイヤーは追加せず、旧 `tau_s_schedule` 前提の入力はサポートしない。
