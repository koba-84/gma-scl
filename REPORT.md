# マルチクラス分類における対照学習: 損失関数とサンプリング戦略の相互作用

## Abstract

本稿は、マルチクラス分類タスクにおける対照学習について、損失関数とサンプリング戦略の組合せが性能に与える影響を検証するための研究計画を記述したものである。比較対象は、損失関数として NT-Xent および CACR、サンプリング戦略として default、DPP、GCBS、データセットとして 20NewsGroups および R52 とする。評価は Accuracy を主指標とし、linear evaluation のみを実施する。現時点では実験は未完了であり、本稿では実験設計、評価方針、結果記録形式を明確化する。

## 1. Introduction

対照学習は、表現学習の有効なアプローチとして広く利用されている。一方で、学習挙動は損失関数の選択とサンプル構成方法に依存するため、両者を同時に扱った検証が必要である。本研究の目的は、損失関数の違いに応じて有効なサンプリング戦略が変化するかを、統一的な実験条件下で確認することである。

研究課題は、NT-Xent と CACR の間で高性能となるサンプリング戦略が一致するかである。

## 2. Methods

### 2.1 Loss Function

本研究で用いる損失関数は、通常の Contrastive Learning（NT-Xent）と CACR である。

#### 2.1.1 NT-Xent

バッチサイズを (N) とし、2つのビュー埋め込みを連結した表現を ({z_i}\_{i=1}^{2N}) とする。温度係数を (\\tau)、サンプル (i) の正例インデックスを (p(i)) とすると、NT-Xent は次式で与える。

\[
\\mathcal{L}_{\\mathrm{NTXent}}
=-\\frac{1}{2N}\\sum_{i=1}^{2N}
\\log
\\frac{
\\exp!\\left(\\frac{z_i^\\top z\_{p(i)}}{\\tau}\\right)
}{
\\sum\_{k=1,,k\\neq i}^{2N}
\\exp!\\left(\\frac{z_i^\\top z_k}{\\tau}\\right)
}
\]

分子は正例ペア、分母は自己項を除くミニバッチ全体（正例+負例）である。

#### 2.1.2 CACR（Contrastive Attraction and Contrastive Repulsion）

2ビュー埋め込みを (z^{(1)}, z^{(2)} \\in \\mathbb{R}^{N\\times d}) とする。CACR は Attraction 項と Repulsion 項の和で定義する。

\[
\\mathcal{L}_{\\mathrm{CACR}}=\\mathcal{L}_{CA}+\\mathcal{L}\_{CR}
\]

- Attraction（(\\mathcal{L}_{CA})）:
  \[
  c_i^{(x)}=\\left|z_i^{(x)}-z_i^{(\\bar{x})}\\right|_2^2
  \]
  \[
  \\mathcal{L}_{CA}
  \=
  \\frac{1}{2}\\sum_{x\\in{1,2}}
  \\frac{1}{N}\\sum\_{i=1}^{N}
  \\frac{
  \\exp!\\left(c_i^{(x)}\\tau\_{\\mathrm{pos}}\\right)
  }{
  \\sum\_{v\\neq x}\\exp!\\left(c_i^{(v)}\\tau\_{\\mathrm{pos}}\\right)
  }
  c_i^{(x)}
  \]

- Repulsion（(\\mathcal{L}_{CR}), 対角除外）:
  \[
  c_{ij}=-\\left|z_i^{(1)}-z_j^{(2)}\\right|_2^2 \\quad (i\\neq j)
  \]
  \[
  \\mathcal{L}_{CR}
  \=
  \\frac{1}{N}\\sum\_{i=1}^{N}\\sum\_{j\\neq i}
  \\frac{
  \\exp!\\left(c\_{ij}\\tau\_{\\mathrm{neg}}\\right)
  }{
  \\sum\_{k\\neq i}\\exp!\\left(c\_{ik}\\tau\_{\\mathrm{neg}}\\right)
  }
  c\_{ij}
  \]

### 2.2 Sampling Strategy

本研究では、GCBS と DPP を比較対象とする。以下では、埋め込み行列を (Z=[z_1,\\dots,z_n]^\\top)（各 (z_i) は L2 正規化済み）とする。

#### 2.2.1 GCBS[^gcbs]

GCBS では、まずコサイン類似度
\[
s\_{ij}=z_i^\\top z_j \\quad (i\\neq j)
\]
を計算し、各 (i) について上位量子点 (q) 以上の類似ペアのみを残して疎グラフを作る。
\[
A\_{ij}=\\mathbf{1}!\\left\[s\_{ij}\\ge \\mathrm{Quantile}_q({s_{ik}}_{k\\neq i})\\right\], \\quad A_{ii}=0
\]
その後、隣接行列 (A) に対して reverse Cuthill-McKee による並べ替え (\\pi) を得て、(\\pi) の順序でサンプルを提示する。これにより近傍関係を保ちながら順序を再構成する。

#### 2.2.2 DPP[^dpp]

DPP では、まず (Z\\in\\mathbb{R}^{n\\times d}) に対して (\\Phi=Z^\\top=[z_1,\\dots,z_n]\\in\\mathbb{R}^{d\\times n}) と定義し、各列 (z_i) をサンプル (i) の埋め込みベクトルとする。ミニバッチサイズを (k) とし、部分集合 (Y\\subset{1,\\dots,n}, |Y|=k) を k-DPP でサンプリングする。確率は
\[
\\Pr(Y)\\propto \\det(L_Y), \\quad L=\\Phi^\\top\\Phi
\]
で与える。 (\\det(L_Y)) が大きいほど多様性の高い集合が選ばれやすい。1エポック内では選択済みサンプルを除外し、残り集合から繰り返しバッチを生成する。

## 3. Experiments

本章では、研究課題「NT-Xent と CACR で有効なサンプリング戦略は一致するか」を、同一の実験条件下で検証する。3.1 でデータセットを示し、3.2 で比較設計と学習条件を定義し、3.3 で結果記録形式を統一して、研究課題に対する比較可能な証拠を整備する。
評価は Accuracy を主指標とする。補助指標は必要に応じて追記する。

### 3.1 データセット

本研究では、ニュース記事分類データセットである 20NewsGroups と、Reuters-21578 由来のトピック分類データセットである R52 を用いる。
R52 は Reuters-21578 から構成された、単一ラベルの52クラス分類用サブセットである。[^r52_extract][^reuters_modapte]
本研究では、テキスト側に追加前処理を行わず、プロジェクト内で train を train/val に再分割して利用する。
データセット統計を表 1 に示す。

表 1: データセット統計

| Dataset      | \|train\| | \|val\| | \|test\| | クラス数 |
| ------------ | --------: | ------: | -------: | -------: |
| 20NewsGroups |      9034 |    2259 |     7528 |       20 |
| R52          |      5225 |    1307 |     2568 |       52 |

### 3.2 実験設定

本研究の評価は2段階で行う。まず、対照学習段階で損失関数 {NT-Xent, CACR} とサンプリング戦略 {default, DPP, GCBS} の全組合せ（2x3）を比較して表現を学習する。次に、学習済みエンコーダを凍結した linear evaluation により、各データセットで下流分類性能を測定する。分類時は対照学習で用いた projection head を破棄し、エンコーダ出力に線形分類層を追加して学習する。

エンコーダは roberta-base[^roberta]（最大長 256）で固定し、対照学習では 2-view augmentation（num_views=2, view_dropout_prob=0.1）を適用する。projection head は 2 層 MLP（in=768, hidden=512, out=128）とする。損失関数は NT-Xent で (\\tau\\in{0.05, 0.1, 0.2}) を探索し、CACR で (\\tau\_{\\mathrm{pos}}=1)とし, (\\tau\_{\\mathrm{neg}}\\in{0.5, 1, 2}) を探索する。最適化は、事前学習では AdamW（lr (\\in{2e!-!5, 5e!-!5})）と warmup + cosine annealing、分類では AdamW と LinearLR を用いる。

学習長は contrastive を 50 epoch、classification を 100 epoch とし、バッチサイズは両段階で 64 に統一する。DPP はエポック内で非復元抽出を行い、GCBS は各 epoch 開始時に埋め込みから順序を再計算する。contrastive 段階では最終 epoch のモデルを用い、分類段階のモデル選択は classification/val/acc を基準とする。数値精度は 32-bit とする。統計報告は各条件 3 seeds の test Accuracy について平均と標準偏差を示す。

表 1-補: 主要ハイパーパラメータ

| 区分                     | 項目                                                           | 設定値                                                                               |
| ------------------------ | -------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| モデル                   | Encoder                                                        | roberta-base（最大長 256）                                                           |
| モデル                   | Projection head                                                | 2-layer MLP（in=768, hidden=512, out=128）                                           |
| モデル                   | Classification head                                            | Linear layer（encoder出力→クラス数）                                                 |
| 拡張                     | num_views / view_dropout_prob                                  | 2 / 0.1                                                                              |
| 損失                     | NT-Xent (\\tau)（探索）                                        | {0.05, 0.1, 0.2}                                                                     |
| 損失                     | CACR (\\tau\_{\\mathrm{pos}} / \\tau\_{\\mathrm{neg}})（探索） | {0.5, 1, 2} / {0.5, 1, 2}                                                            |
| 最適化（contrastive）    | Optimizer                                                      | AdamW（lr: {2e-5, 5e-5}, weight_decay=0.01）                                         |
| 最適化（contrastive）    | Scheduler                                                      | warmup + cosine annealing（warmup ratio=0.05, warmup start factor=0.1, eta_min=0.0） |
| 最適化（classification） | Optimizer                                                      | AdamW（lr=1e-3, weight_decay=0.01）                                                  |
| 最適化（classification） | Scheduler                                                      | LinearLR（start_factor=1.0, end_factor=0.1, total_iters=100）                        |
| 学習                     | Epoch / Batch size                                             | contrastive=50, classification=100 / 64                                              |
| 選択・評価               | Model selection / Seeds                                        | contrastive: final epoch, classification: classification/val/acc / 3                 |
| 計算設定                 | Precision                                                      | 32-bit                                                                               |

### 3.3 Results

実験結果は表 2 および表 3 に記録する。各セルは Accuracy±std を表す。

表 2: 20NewsGroups

| Loss \\ Sampler | default | DPP | GCBS |
| --------------- | ------: | --: | ---: |
| NT-Xent         |     TBA | TBA |  TBA |
| CACR            |     TBA | TBA |  TBA |

表 3: R52

| Loss \\ Sampler | default | DPP | GCBS |
| --------------- | ------: | --: | ---: |
| NT-Xent         |     TBA | TBA |  TBA |
| CACR            |     TBA | TBA |  TBA |

## 4. 考察

本章では、損失関数とサンプリング戦略の相互作用、および seed 間の安定性を整理して記述する。

## 5. Conclusion

本章では、実験結果に基づく主要知見と今後の課題を記述する。

## References

\[^r52_extract\]: Yao et al., "Graph Convolutional Networks for Text Classification", 2019. https://arxiv.org/abs/1809.05679
\[^reuters_modapte\]: UCI ML Repo (Reuters-21578), processing notes (ModApte split / LEWISSPLIT / TOPICS). https://archive.ics.uci.edu/dataset/137/reuters+21578+text+categorization+collection
\[^gcbs\]: Sachidananda, V., Yang, Z. & Zhu, C.. (2023). Global Selection of Contrastive Batches via Optimization on Sample Permutations. <i>Proceedings of the 40th International Conference on Machine Learning</i>, in <i>Proceedings of Machine Learning Research</i> 202:29542-29562 Available from https://proceedings.mlr.press/v202/sachidananda23a.html.
\[^dpp\]: Zhang, C., Kjellström, H., & Mandt, S. (2017). Determinantal point processes for mini-batch diversification. Uncertainty in Artificial Intelligence - Proceedings of the 33rd Conference, UAI 2017. Presented at the 33rd Conference on Uncertainty in Artificial Intelligence, UAI 2017, Sydney, Australia, 11 August 2017 through 15 August 2017. Retrieved from https://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-218565
\[^neurips_rc\]: NeurIPS. Reproducibility Checklist. https://neurips.cc/public/guides/PaperChecklist
\[^ml_rc\]: Pineau, J. et al. (2021). Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program). JMLR 22(164):1-20. https://www.jmlr.org/papers/v22/20-303.html
\[^roberta\]: Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., ... & Stoyanov, V. (2019). Roberta: A robustly optimized bert pretraining approach. arXiv preprint arXiv:1907.11692.

01. lr=2e-5, temp=0.05, data=20ng
02. lr=2e-5, temp=0.05, data=r52
03. lr=2e-5, temp=0.10, data=20ng
04. lr=2e-5, temp=0.10, data=r52
05. lr=2e-5, temp=0.20, data=20ng
06. lr=2e-5, temp=0.20, data=r52
07. lr=5e-5, temp=0.05, data=20ng
08. lr=5e-5, temp=0.05, data=r52
09. lr=5e-5, temp=0.10, data=20ng
10. lr=5e-5, temp=0.10, data=r52
11. lr=5e-5, temp=0.20, data=20ng
12. lr=5e-5, temp=0.20, data=r52
