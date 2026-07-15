# Design: clarify-test-layer-policy

## Context

現状の pytest 構成には次のズレがある。

- sampler の切替・再現性・tokenized refresh は [training spec](../../../../specs/training/spec.md) と [test_data_integration.py](../../../../../tests/integration/data/test_data_integration.py) が担っている。
- 一方で旧 test_dpp_sampler_stdout.py は DPP 固有の third-party stdout 抑止を担っており、sampler 共通の output hygiene policy との接続が見えにくかった。
- `parametrize` の原則は [dev-quality-tooling spec](../../../../specs/dev-quality-tooling/spec.md) に一部あるが、「同じ assertion contract のみを束ねる」という境界が明文化されていない。

そのため、ファイル名だけを見ると「sampler なのに DPP だけ別 module なのはなぜか」が分からない。

## Decisions

### Decision 1: sampler output hygiene は repo-owned sampler runtime の共通方針として扱う

- sampler runtime は標準出力へ不要なノイズを出さないことを共通要件にする。
- DPP だけは third-party `FiniteDPP` の stdout 抑止という実装理由を持つため、scenario では DPP 固有経路を明示する。
- test module 名も DPP 固有名ではなく sampler hygiene を表す名前へ変更する。

### Decision 2: pytest の責務分担を層ごとに定義する

- pure function / invariant は property-based test で確認する。
- component 固有契約は targeted pytest module で確認する。
- DataModule・sampler 切替・stage artifact 契約は integration module で確認する。
- slow / gpu は runtime コストが高い train・eval 経路に限定する。

### Decision 3: parametrization は assertion contract が 1 つのときに限る

- `parametrize` は独立 case visibility のために使う。
- ただし sampler 切替統合と DPP stdout hygiene のように、検証契約が違うものは 1 test body にまとめない。
- これにより test module の短さよりも、失敗時の責務の明確さを優先する。

## Risks

- [Risk] sampler hygiene test を広げると setup が重くなる
  - Mitigation: GCBS/DPP の最小 runtime path だけを行い、DataModule 統合は既存 integration test に残す。
- [Risk] policy が training/dev-quality-tooling の両方へ跨って重複する
  - Mitigation: 「何をどこで検証するか」は `training`、「pytest の書き方」は `dev-quality-tooling` に限定する。
