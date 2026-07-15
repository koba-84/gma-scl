## Why

AAPD 以外の Reuters-21578 と UKLEX でも、保存済み classification prediction artifact からラベル頻度帯別の Macro-F1 を再計算できる必要がある。

## What Changes

- `scripts/b.py` を Reuters-21578 用の頻度帯別 Macro-F1 分析スクリプトとして追加する
- `scripts/c.py` を UKLEX 用の頻度帯別 Macro-F1 分析スクリプトとして追加する
- 両スクリプトは train-set label frequency の降順でラベルを並べ、4 つの帯がおおむね 25% ずつになるよう分割し、余りは高頻度側へ寄せる

## Impact

- 既存の AAPD 分析スクリプトの挙動は変更しない
- 追加スクリプトは `tmp/pred/<dataset>/` 配下の保存済み prediction artifact を入力とする
