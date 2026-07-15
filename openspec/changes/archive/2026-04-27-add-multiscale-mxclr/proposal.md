## Why

t-MXCLR は単一 perplexity の t-SNE 参照分布を使えるが、局所構造と大域構造を同時に反映する multi-scale perplexity 条件を比較できない。MXCLR 系の意味グラフを使いつつ、openTSNE の Multiscale と同じ参照分布で contrastive pretraining を実行できる loss が必要である。

## What Changes

- multi-scale MXCLR を新しい contrastive loss として追加する。
- 参照分布は MXCLR の BERTScore_F1 score graph を距離に変換し、openTSNE Multiscale の multi-perplexity affinities で作る。
- 学習側分布は埋込を正規化せず、pairwise squared L2 距離から Gaussian kernel を作る。
- MXCLR 由来の temperature は公開設定に持たせず、temperature scaling は 1 固定として扱う。
- Hydra config と pytest を追加し、設定解決・有限 loss・multi-scale 参照分布・非正規化 L2 Gaussian 挙動を検証する。

## Capabilities

### New Capabilities

- training: contrastive/model=multi_scale_mxclr で multi-scale MXCLR loss を選択できる。

### Modified Capabilities

- training: supported contrastive loss config と W&B loss alias の対象に multi_scale_mxclr を含める。

## Impact

- 影響コード: src/models/loss/multi_scale_mxclr.py, configs/contrastive/model/multi_scale_mxclr.yaml, tests/losses/test_multi_scale_mxclr_loss.py, tests/test_configs.py
- 影響仕様: openspec/specs/training.md, openspec/specs/training/spec.md
- 依存追加なし。既存 openTSNE 依存を使用する。
