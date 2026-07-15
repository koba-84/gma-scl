## Why

現在のドキュメントには uv 前提の運用と pip/conda 前提の記述が混在しており、依存追加や環境構築の手順が一意に解釈できない。再現性重視の運用に合わせて、依存管理を uv add に統一し、誤った分岐を減らす必要がある。

## What Changes

- README のインストール手順を uv ベースへ統一し、pip/conda 手順を削除する。
- 依存追加手順を uv add（通常依存 / 開発依存）として明示する。
- OpenSpec のプロジェクト文書で、依存定義の正を pyproject.toml + uv.lock に固定し、requirements.txt / environment.yaml を運用対象外として明示する。
- 仕様文書（training capability）に、依存管理の運用ルールを追加する。

## Capabilities

### New Capabilities

- `dependency-management`: uv add による依存追加ルールと依存定義ファイルの正本を定義する。

### Modified Capabilities

- `training`: 実行環境要件に、依存管理手順の統一ルールを追加する。

## Impact

- 影響ドキュメント: README.md, openspec/project.md, openspec/specs/training/spec.md
- 依存追加・更新フロー（開発者運用）に影響する。
- 外部 API / 実装コードへの直接影響はない。
