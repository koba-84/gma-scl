## Why

温度キー統一の修正後も、全 loss を横断した自動検証が弱く、`tau` / `temp_*` 系の旧キー再混入を早期検知しにくい。実装と config の canonical naming が維持されることをテストで固定し、再発を防ぐ。

## What Changes

- 全 contrastive loss 設定と loss クラス初期化引数を照合する回帰テストを追加する。
- 旧温度キー（`temp`, `tau`, `tau_s`, `temp_attract`, `temp_repulse`）が公開 config key として混入していないことを自動検証する。
- OpenSpec training 仕様に「全サポート loss の canonical temperature key をテストで網羅確認する」シナリオを追加する。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `training`: Contrastive temperature naming 要件に、全 loss 網羅の自動検証シナリオを追加する。

## Impact

- Affected tests: `tests/test_configs.py`
- Affected spec: `openspec/specs/training/spec.md`
- 既存 runtime 挙動の変更はなし（検証強化のみ）。
