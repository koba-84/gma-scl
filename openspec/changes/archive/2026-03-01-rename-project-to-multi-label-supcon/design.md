## Context

プロジェクト名が複数の識別子で混在しているため、パッケージ名と実験ログの突合せがしづらい。

## Goals / Non-Goals

Goals:

- プロジェクト識別子を `multi-label-supcon` に統一する。
- 既存設定との整合を維持しつつ、最小差分で変更する。

Non-Goals:

- リポジトリディレクトリ名の変更。
- import パスやモジュール構造の変更。

## Decisions

1. Python project 名は `pyproject.toml` と `uv.lock` の仮想パッケージ名を更新する。
2. logger 設定は実際に利用される `wandb` に加え `comet` と `neptune` も同名へ寄せる。
3. OpenSpec の main specs は training / evaluation の該当箇所のみ更新する。

## Risks / Trade-offs

- 既存ダッシュボード（旧プロジェクト名）とはログが分離される。
  - Mitigation: 変更を spec と設定に明示し、以降の実験は新名称で統一する。
