## Context

UK-LEX は `data/uklex/train.csv`, `val.csv`, `test.csv` として CSV が存在し、現在の datamodule が要求する validation split 名は `dev.csv` である。リポジトリには `data/uklex/dev.csv` は存在しないが、config 解決そのものは dataset_name と num_classes の選択に閉じている。

## Decisions

- top-level selector は既存 dataset と同じ `configs/data/<dataset>.yaml` 形式にする
- contrastive data config は default を継承し、`dataset_name: uklex` だけを明示する
- classification data config は既存 config と同じ項目を明示し、`num_classes: 69` を CSV ヘッダ数と `label2id.json` に合わせる
- tokenizer と `max_length` は既存データセットと同じ `roberta-base` / `512` を使う
- `val.csv` から `dev.csv` への変換や DataModule の split 名変更は、この config 追加の範囲外とする

## Validation

- `uv run python src/train.py --cfg job --resolve data=uklex logger=csv trainer=cpu`
- `uv run openspec validate tokenized-datamodule-layout --strict`
