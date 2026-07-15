## Context

現状の ContrastiveLitModule は loss_fn(z, labels) の二引数契約で loss を呼び出す。tmp/msc.py は prototype を外部入力で受ける設計のため、そのままでは既存学習経路に接続できない。既存の loss 追加運用に合わせ、Hydra で切替可能かつ自己テスト可能な形へ整える。

## Goals / Non-Goals

**Goals:**

- MSC loss を src/models/loss 配下の正式実装として追加する。
- 既存契約 loss_fn(z, labels) で動かせるようにし、外部から prototype を必須にしない。
- configs/contrastive/model/msc.yaml で Hydra から選択可能にする。
- loss ファイル末尾自己テストと tests/configs.py で設定解決を確認する。

**Non-Goals:**

- ContrastiveLitModule の呼び出し契約変更。
- queue/key メモリバンク機構の新規導入。
- 既存 loss のアルゴリズム変更。

## Decisions

1. 実装クラス名は MSC とし、tmp ファイルの LossContrastiveMSC をリポジトリ命名規約へ合わせる。
   理由: 既存クラス名（Base, MulSupCon, MXCLR, MCACR_WONEG）と一貫させるため。
   代替案: LossContrastiveMSC のまま公開。却下理由: 命名規約と設定可読性を損なう。

2. forward は forward(z, labels) を標準経路とし、prototype 未指定時はバッチ内ラベルごとの平均埋め込みから prototype を内部生成する。
   理由: train 側改修なしで利用可能にしつつ、元実装の prototype 前提を満たせる。
   代替案: train から prototype を渡す。却下理由: 学習経路への影響が大きい。

3. tmp 実装の主要計算（or, 温度付き log-softmax, 重み付き項）は維持し、未使用 import・固定 DEVICE・スペルミス関数名などは整理する。
   理由: 由来実装の数式を保ちつつ、このリポジトリで安全に実行できる形にするため。
   代替案: 別 loss で再実装。却下理由: 差分検証が難しくなる。

## Risks / Trade-offs

- [Risk] バッチ内 prototype 近似により、外部 prototype 利用時と損失値が一致しない。
  Mitigation: forward で prototype 引数を任意受け取り可能にして比較実験の余地を残す。
- [Risk] 1 ラベルも持たないサンプルがあると正規化で不安定化する。
  Mitigation: 分母 clamp_min と eps を適用し、ゼロ割りを回避する。
