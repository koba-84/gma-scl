## Design

`scripts/b.py` と `scripts/c.py` は、`scripts/a.py` と同じ prediction artifact 形式を読む。artifact は `scores` と `targets` を持つ PyTorch payload とし、Macro-F1 は `torchmetrics.classification.MultilabelF1Score` の multilabel F1、`threshold=0.5`、`average="macro"` で計算する。

## Decisions

### Decision 1: Dataset-specific standalone scripts

既存の呼び出し形に合わせ、Reuters-21578 は `scripts/b.py`、UKLEX は `scripts/c.py` として追加する。共通化は行わず、各ファイルの先頭定数で dataset path と prediction path を明示する。

### Decision 2: Frequency bands use 25% label-count splits

各 dataset の train frequency を降順で安定ソートし、rank 順に 4 分割する。ラベル数が 4 で割り切れない場合は高頻度側の帯から 1 ラベルずつ多く割り当てる。これにより各帯は可能な範囲で 25% ずつになり、余りラベルは高頻度評価側へ寄せる。

### Decision 3: Output keeps rank and frequency evidence

各帯の出力には rank range、label 数、train frequency range を含め、どの頻度範囲を集計したかを後から確認できるようにする。
