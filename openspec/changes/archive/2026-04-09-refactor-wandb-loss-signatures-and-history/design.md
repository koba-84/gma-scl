## Context

現行実装では W&B 比較列で参照したい alias の導出ルールが暗黙的で、runtime logging と backfill で等価性を仕様として担保しきれていない。また MXCLR/MSC 周辺の loss API は呼び出し側の都合で広い引数を公開しており、未使用引数を受け取って捨てる実装が残っている。さらに tokenized datamodule の `max_length` 既定値が 256 のままで、長文データセット運用の実態とずれている。

同時に、topic branch の履歴が過剰に分割される運用（数百コミット単位の PR）が発生しており、レビュー性と再現調査性を下げている。Git/GitHub の一次資料（gitworkflows の Separate Changes、git-rebase の autosquash、GitHub Docs の small PR 推奨/merge method）に沿って、履歴整形を仕様と自動ゲートに落とし込む。

## Goals / Non-Goals

**Goals:**
- W&B config alias を「何を必ず記録するか」で仕様化し、logging/backfill の導出経路を一致させる。
- loss 引数を実運用入力に縮小し、未使用引数受け取りを廃止する。
- text encoder の max_length を 512 に統一する。
- topic branch の履歴肥大を pre-push で検知し、PR 前に履歴整理を強制する。

**Non-Goals:**
- 既存 run の過去履歴を一括 rewrite すること。
- 新しい loss アルゴリズムの導入。
- CI provider や branch protection 設定の全面刷新。

## Decisions

1. W&B alias 仕様は training capability の MODIFIED Requirement として定義する。
- 理由: 既存 requirement が runtime config logging を扱っているため、同じ能力内で contract を強化するのが自然。
- 代替案: 新 capability を追加する。
- 不採用理由: 既存 requirement と重複し、運用者が参照箇所を分断する。

2. MXCLR の agg 呼び出しは required stats に基づく最小 kwargs へ変更する。
- 理由: agg 側が未使用引数を受ける必要がなくなり、実際に必要な依存統計が明示化される。
- 代替案: 共通シグネチャを維持し `del` で無視する。
- 不採用理由: 実使用契約が曖昧なままになり、実装追加時に過剰引数が温存される。

3. MSC の forward は runtime で使う `prototype` のみを受ける契約に絞る。
- 理由: `ContrastiveLitModule` の標準経路が prototype のみを供給しており、queue/key 経路は現行運用で未使用。
- 代替案: 旧引数を残して deprecate。
- 不採用理由: 本リポジトリ方針として後方互換レイヤーを持たない。

4. commit history 整理は pre-push の branch policy へ統合し、
   (a) upstream 比較で merge commit 禁止
   (b) upstream 比較で commit 数上限を導入
   の2条件で機械検証する。
- 理由: 既存の branch policy hook に責務が近く、運用摩擦が最小。
- 代替案: CI だけで検証する。
- 不採用理由: push 前に防げず、レビュー前に不要履歴が流入する。

## Risks / Trade-offs

- [Risk] 既存のローカル運用で commit 数上限に引っかかる
  -> Mitigation: 環境変数で上限値を調整可能にし、明示 bypass も残す。
- [Risk] loss 引数削減でテスト fixture が壊れる
  -> Mitigation: fixture を実運用経路（train.csv 由来統計）に合わせて更新する。
- [Risk] max_length 512 への変更で tokenized cache サイズが増える
  -> Mitigation: 既存 cache key（max_length 含む）により衝突を避け、必要時のみ再生成する。

## Migration Plan

1. OpenSpec artifacts を作成し、training/version-control の delta spec を確定する。
2. W&B alias と loss 引数を実装・テストで更新する。
3. max_length 512 を config と datamodule 既定値に反映し、設定解決テストを更新する。
4. branch policy hook に history hygiene check を追加する。
5. `uv run pre-commit run -a` と関連 pytest を実行する。
6. main spec へ同期し、PR を作成して CI を通す。

## Open Questions

- なし（commit 数上限は初期値 30 とし、環境変数で調整可能とする）。
