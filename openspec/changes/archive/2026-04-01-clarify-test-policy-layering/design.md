## Context

現状の repo では、pytest の共通化規約は `openspec/specs/dev-quality-tooling/spec.md` にあり、training 系の integration/test 実行方針は `openspec/specs/training/spec.md` にある。一方で、`tests/test_dpp_sampler_stdout.py` のような sampler 固有 test がなぜ generic sampler integration test に吸収されていないかは明示されていない。

`tests/test_data_integration.py` は `sampler_type=shuffle/gcbs/dpp` の切替と初期化順序を tiny dataset で確認しているが、`tests/test_dpp_sampler_stdout.py` は `src/data/components/dpp.py` 内の `FiniteDPP` 初期化時 stdout 抑止という DPP 専用契約を見ている。ここを spec 上で分けておかないと、「topic 名が同じなら全部 parametrization でまとめるべき」という誤った整理に寄りやすい。

## Goals / Non-Goals

**Goals:**

- test 層ごとの責務を spec に明記し、どこで何を確認するかを読み取れるようにする
- `@pytest.mark.parametrize` を使う条件と、個別 test を残す条件を requirement として明記する
- sampler 固有 test を残す判断基準を training spec で固定する

**Non-Goals:**

- 既存 test suite の全面的な再配置
- sampler 固有 test の一括削除
- 新しい test runner や dependency の導入

## Decisions

1. pytest 一般の layering / parametrization policy は `dev-quality-tooling` に置く
   test style と file/module organization の規約なので、training 固有 spec ではなく dev-quality-tooling capability に置く。

2. sampler 固有 test の許容条件は `training` に置く
   DPP stdout hygiene のような契約は sampler 実装と外部依存の相互作用に依存するため、training capability で「generic sampler integration とは別枠で保持してよい」ことを明記する。

3. DPP stdout hygiene は generic sampler contract へ一般化しない
   現状で stdout 抑止コードを持つのは `src/data/components/dpp.py` のみであり、GCBS には同じ責務が存在しない。したがって「sampler は一般に stdout を出さない」という抽象仕様に上げるより、「sampler 共通の functional integration」と「sampler 固有の compatibility regression」を分ける方が実装実態と一致する。

## Risks / Trade-offs

- [Risk] `dev-quality-tooling` と `training` の両方に test policy が出てきて重複に見える
  → Mitigation: 前者は一般 policy、後者は sampler ドメイン固有例外に限定する
- [Risk] DPP 固有 test を残すことで file 数が増えたままになる
  → Mitigation: 個別 file の存在理由を spec に明記し、無条件な parametrization を避ける判断基準を提供する

## Migration Plan

1. change artifacts に delta spec を追加する
2. main specs に同じ requirement 変更を反映する
3. 今後の test 整理では、この policy を基準に parametrization / fixture 化 / 個別 test 維持を判断する

## Open Questions

- なし
