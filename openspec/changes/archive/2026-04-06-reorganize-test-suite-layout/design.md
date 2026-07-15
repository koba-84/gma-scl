## Context

現状の test suite には次の整理不足がある。

- `tests/conftest.py` が Hydra config、synthetic dataset、MXCLR stub、logging stub をすべて持つ。
- `tests/test_contrastive_losses.py` が Base / MulSupCon / MCACR / MSC / MXCLR を同居させている。
- `tests/test_property_based.py` が GCBS / label overlap / MSC helper / Base / MXCLR を同居させている。
- integration test が top-level に並び、train/data/CLI の責務がファイル名だけでは分かりにくい。

既存 spec には layering policy と shared setup reuse はあるが、どの directory に何を置くべきかの運用規約までは明示されていない。

## Goals / Non-Goals

**Goals:**

- fixture を `tests/support/fixtures/` の責務別 module へ分割する。
- loss/property/integration test を責務が分かる directory と file 名へ再配置する。
- 既存 test contract と marker を保ちつつ、失敗箇所がディレクトリ構造から読める状態にする。

**Non-Goals:**

- test assertion の意味変更。
- production code の挙動変更。
- pytest plugin や custom collector の追加。

## Decisions

1. root の `tests/conftest.py` は global pytest setup と fixture module 読み込みだけに縮小する。

- 理由: pytest の root fixture entrypoint は維持しつつ、domain-specific fixture の責務を file system 上で分離できる。

2. shared fixture module は `tests/support/fixtures/{config,datasets,mxclr,logging}.py` に分割する。

- 理由: 現在の fixture 集約点をそのまま責務別に切れる最小変更だから。

3. broad regression/property file は target module 単位へ分割する。

- 理由: `losses/` と `property/` で failure location を即座に読めるようにするため。

4. integration test は `tests/integration/data/` と `tests/integration/train/` に再配置し、train entrypoint と datamodule/data contract を分離する。

- 理由: 実行コストだけでなく、どの multi-component wiring が壊れたかを directory から判別できるようにするため。

## Risks / Trade-offs

- [Risk] file move 後に fixture import や pytest discovery が壊れる。
  Mitigation: `pytest_plugins` で fixture module を明示登録し、対象 pytest 群で回帰確認する。

- [Risk] 分割しすぎて test file が過度に小さくなる。
  Mitigation: target module 単位にとどめ、1 assertion 1 file のような過分割は避ける。
