## Why

WoS preprocessing currently emits JSON lines with hierarchical label arrays, while the training pipeline expects the same CSV contract used by AAPD: an `abstract` text column followed by numeric multi-label columns. This prevents WoS outputs from being consumed by the existing datamodules and label-statistics code without ad hoc conversion.

## What Changes

- Update `data/wos/preprocess.py` to write `train.csv`, `dev.csv`, and `test.csv` in the AAPD CSV format.
- Preserve the current WoS document text cleaning, label selection, and split procedure.
- Encode each existing WoS `doc_label` entry as a positive label in the CSV multi-hot vector.

## Impact

- 変更対象: `data/wos/preprocess.py`, WoS preprocessing spec
- 出力影響: WoS preprocessing の主要出力は AAPD 互換 CSV になる
- 再現性影響: split seed と label selection は維持する
