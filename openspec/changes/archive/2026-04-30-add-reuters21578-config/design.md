## Context

reuters21578 の CSV は `data/reuters21578/train.csv`, `dev.csv`, `test.csv` として存在し、ヘッダは `abstract` と 90 個のラベル列で構成されている。既存の tokenized datamodule は dataset_name から CSV split を読むため、dataset 固有の Python 実装は不要である。

## Decisions

- top-level selector は既存の `aapd`, `rcv1`, `rcv1_3k` と同じ `configs/data/<dataset>.yaml` 形式にする
- contrastive data config は default を継承し、`dataset_name: reuters21578` だけを明示する
- classification data config は既存 config と同じ項目を明示し、`num_classes: 90` を CSV ヘッダ数に合わせる
- tokenizer と `max_length` は既存データセットと同じ `roberta-base` / `512` を使う

## Validation

- `uv run pytest tests/test_configs.py -k "reuters21578 or classification_data_max_length"`
- `uv run python src/train.py --cfg job --resolve data=reuters21578 logger=csv trainer=cpu`
