# Test organization

通常のpytest suiteは、提案手法の中核契約だけを検証する。現在の収集上限は60ケースで、基準時の150ケースから38ケースへ削減している。

- `tests/losses/`: ラベル埋め込みのみの `MultiDatasetMXCLR` とsemantic graphの契約。
- `tests/integration/data/`: mixed datasetのDataModule、global label offset、tokenized batchの契約。
- `tests/integration/train/`: 高速なentrypoint smokeとstage wiringの契約。
- `tests/test_multi_dataset_*.py`: mixed batch、dataset-local classifier、dataset別macro-F1、prediction artifactの契約。
- `tests/support/fixtures/`: 現行の設定とsynthetic datasetで共有するfixture。
- その他の `tests/test_*.py`: 現行の設定、tokenization、task wrapperなどの最小component contract。

NPMI、IDF、ランキング損失、旧単一データセットMXCLR集約器、alias/backfillの全組合せ、slow/GPU/DDP/resume/sweepは通常suiteの対象外とする。これらの回帰が必要になった場合は、現行手法とは別のOpenSpec changeとして追加する。

同じ入力と同じ期待出力を確認するvariantは `pytest.mark.parametrize` と安定したcase IDで一つのtest bodyにまとめる。例外条件、artifact生成、数学的性質、統合wiringのように失敗診断が異なる契約は分けて保持する。

## Local commands

```bash
uv run pytest --collect-only -q
uv run pytest -q
uv run pytest --durations=0 -q
uv run pytest --cov=src --cov-report=term-missing -q
```

`--collect-only` の結果は60以下でなければならない。この構成はpytest公式の [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) と [parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) の使い分けに基づく。
