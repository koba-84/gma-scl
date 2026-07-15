## 1. Naming compliance and command sync

- [x] 1.1 tests 配下の命名規約違反ファイルを改名する
  - `tests/test_property_based.py` を `tests/property_based.py` に改名する
  - `tests/test_task_wrapper.py` を `tests/task_wrapper.py` に改名する
  - README と関連 OpenSpec 文書の参照パスを新命名へ更新する

## 2. Next property-based targets (planned)

- [x] 2.1 `src/models/loss/msc.py::_log_softmax_temp` の property test を追加する

  - 温度制約（`temp > 0`）の例外契約を検証する
  - マスク有効列に対して有限値出力を検証する

- [x] 2.2 `src/models/loss/base.py::Base.forward` の property test を追加する

  - shape 契約違反時の例外を検証する
  - `batch_size < 2` の例外契約を検証する

- [x] 2.3 `src/data/components/gcbs.py::compute_gcbs_permutation` の拡張 property test を追加する

  - 異常入力（quantile, chunk_size, ndim）の例外契約を検証する
  - 空入力・単一入力の境界挙動を検証する

## 3. Validation

- [x] 3.1 命名変更と計画反映の整合を検証する
  - `uv run pytest tests/property_based.py -q` を成功させる
  - `uv run pytest tests/task_wrapper.py -q` を成功させる
  - `uv run pre-commit run -a` を成功させる
