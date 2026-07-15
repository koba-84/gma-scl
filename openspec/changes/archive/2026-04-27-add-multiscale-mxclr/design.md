## Context

t-MXCLR は MXCLR の label semantic initialization と BERTScore_F1 集約を再利用し、score graph を 1 - score の距離へ変換して openTSNE PerplexityBasedNN に渡している。openTSNE の Multiscale は各 perplexity の affinity を計算し、確率分布化したあとスケール間で平均する実装になっているため、同じ precomputed distance matrix から multi-scale 参照分布を構築できる。

## Decisions

1. 新 loss 名は MultiScaleMXCLR、設定名は multi_scale_mxclr とする。

- 理由: loss ファイル命名規約に合わせ、W&B alias は module 名から multi_scale_mxclr として導出できる。

2. MultiScaleMXCLR は MXCLR を継承し、score_graph と semantic initialization を再利用する。

- 理由: ラベル説明文・BERTScore_F1 集約・label stats の契約を重複実装しない。

3. 参照分布は openTSNE.affinity.Multiscale に metric=precomputed, method=exact, symmetrize=True を指定して作る。

- 理由: openTSNE の multi-scale perplexity 実装と同じ正規化済み P を使うため。

4. 学習側分布は z を正規化せず、torch.cdist(z, z, p=2).square() から Gaussian log-kernel を作る。

- 理由: 今回の実験条件では cosine similarity や正規化済み埋込ではなく、非正規化 L2 距離が比較対象である。

5. temperature 系の公開引数は追加しない。

- 理由: MXCLR の instance_temperature と graph_temperature は今回使用せず、temperature scaling は 1 固定として扱う。再現性上も config から調整できないことを明示する。

## Risks

- openTSNE は batch size に対して大きすぎる perplexity を内部で補正する。既存 t-MXCLR と同じく openTSNE の挙動を採用し、loss 側では正値検証だけを行う。
- 参照分布は detach して CPU numpy 経由で構築するため、label graph 側は微分対象外である。これは既存 t-MXCLR と同じ契約である。
