## Context

本リポジトリは pytest の収集対象を `python_files = ["*.py"]` に設定しており、`test_` 接頭辞の有無で収集可否は変わらない。一方で既存テスト群は `tests/train.py` など接頭辞なし命名が主流で、今回追加された DPP テストのみ接頭辞ありとなっていた。

## Goals / Non-Goals

**Goals:**

- テスト命名を既存運用と一致させる。
- 命名規約を OpenSpec main spec に明記する。

**Non-Goals:**

- pytest 収集設定の変更
- テスト内容や検証ロジックの変更

## Decisions

- Decision 1: `tests/test_dpp_sampler_stdout.py` を `tests/dpp_sampler_stdout.py` にリネームする。
  - Rationale: 既存の接頭辞なし命名へ統一する。
- Decision 2: `dev-quality-tooling` spec に命名規約を追加する。
  - Rationale: 今後の追加テストで揺れを防ぐ。

## Risks / Trade-offs

- [Risk] 将来 `python_files` 収集設定を変更した場合に命名ルールと不整合が再発する可能性
  → Mitigation: 命名規約に「pytest 収集設定と整合させる」前提を明記する。
