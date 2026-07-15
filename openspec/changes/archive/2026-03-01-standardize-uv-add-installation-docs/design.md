## Context

現状は uv 前提の実行規約がある一方で、README には pip/conda のインストール手順が残っており、依存追加フローが分岐している。研究用途の再現性要件に照らすと、依存管理の正本と更新手順を固定する必要がある。

## Goals / Non-Goals

**Goals:**

- 依存追加手順を uv add に統一する。
- ドキュメント上の pip/conda インストール手順を削除する。
- 依存定義の正本を pyproject.toml と uv.lock に固定する。

**Non-Goals:**

- 学習ロジックやモデル実装の変更。
- 既存依存バージョンの見直し。
- CI パイプラインの全面改修。

## Decisions

- README の Installation を uv 専用手順へ置換する。

  - 理由: 新規参加者が最初に参照する導線を一本化するため。
  - 代替案: pip/conda 手順を「参考」として残す。
  - 不採用理由: 運用分岐が継続し、再現性の説明責任が弱くなる。

- OpenSpec 文書に「依存追加は uv add を使用」と明記する。

  - 理由: 実装規約と同等の強度で運用を固定するため。
  - 代替案: README のみ更新する。
  - 不採用理由: 仕様上の拘束力が不足する。

- requirements.txt / environment.yaml は運用対象外として扱う。

  - 理由: 依存定義の多重管理を解消するため。
  - 代替案: 3ファイル同期運用を継続する。
  - 不採用理由: 更新漏れリスクが高く、実験再現性を損なう。

## Risks / Trade-offs

- [Risk] README の既存テンプレート節に pip/conda 記述が残存する可能性

  - Mitigation: 文字列検索で pip/conda/install セクションを点検し、uv 導線へ置換する。

- [Risk] 運用対象外ファイルを残すことで混乱が続く可能性

  - Mitigation: OpenSpec project 文書で正本を明示し、README でも明記する。
