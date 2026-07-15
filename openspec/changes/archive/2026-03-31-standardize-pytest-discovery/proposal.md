## Why

現状の pytest 設定は `python_files = ["*.py"]` で標準 discovery を外しており、tests 配下の支援コードと test module の境界が設定依存になっている。pytest 公式の標準構成へ戻して、ファイル名・marker・support code 配置の責務を一致させる必要がある。

## What Changes

- **BREAKING** pytest discovery を標準の `test_*.py` / `*_test.py` に戻し、`python_files = ["*.py"]` を廃止する。
- tests 配下の収集対象ファイルを標準命名へ統一し、support code は collected test modules と別領域へ移す。
- train/eval/sweeps/data integration 系の marker をファイル境界と一致させ、CI suite の所属を明確化する。
- README、training spec、dev-quality-tooling spec の pytest 実行例と命名規約を新構成へ更新する。

## Capabilities

### New Capabilities

- なし

### Modified Capabilities

- `dev-quality-tooling`: pytest ファイル命名規約を標準 discovery 基準へ変更する。
- `training`: pytest のファイル境界、marker 境界、実行例を標準構成へ更新する。

## Impact

- 影響コード: `pyproject.toml`, `tests/`, `README.md`, `scripts/ci_pytest.sh` に関連する実行例
- 影響仕様: `openspec/specs/dev-quality-tooling/spec.md`, `openspec/specs/training.md`
- 影響 API: `tests.helpers.*` の import path は `tests.support.*` へ変わる
