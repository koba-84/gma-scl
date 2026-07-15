## Context

現在の `log_hyperparameters()` は `OmegaConf.to_container(object_dict["cfg"])` を既定動作で呼んでいるため、Hydra interpolation が未解決のまま dict 化される。W&B logger はその dict をそのまま config として保存するので、`${trainer.accelerator}` のような参照が UI に残る。

## Goals / Non-Goals

**Goals:**

- W&B に記録される config を解決済み値で保存する
- 既存の hyperparameter logging のキー構造は極力維持する
- unit test で interpolation 解決を固定化する

**Non-Goals:**

- Rich config 出力や Hydra 自体の compose 仕様の変更
- W&B run 名や metric logging 仕様の変更

## Decisions

- Decision 1: `OmegaConf.to_container(..., resolve=True)` で root config を plain dict 化する
  - Rationale: 既存の logging 入口を最小変更で直せる
  - Alternative considered: W&B に送る直前だけ再帰的に補間解決する
  - Rejected because: 実装が冗長になり、OmegaConf の責務を重複する
- Decision 2: test では interpolation を含む最小 config と stub logger を使って、送信 payload に `${` が残らないことを直接確認する
  - Rationale: W&B 実サービスや Lightning 実体に依存せずに挙動を固定できる

## Risks / Trade-offs

- [Risk] resolve 時に一部の遅延参照が即時評価される → Mitigation: hyperparameter logging で参照するのは実行直前に compose 済みの config に限定されており、期待動作と一致する
- [Risk] config 内に未解決参照があると logging 時に例外化する → Mitigation: その場合は run 再現に必要な config 自体が壊れているので、早期に失敗した方がよい
