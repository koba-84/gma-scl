# AGENTS

## Project Scope

- multi-label ディレクトリでは Multi-Label Supervised Contrastive Learning を行う。
- 実装・検証・ドキュメント更新は上記テーマに直接関係する範囲を優先すること。

## Implementation Policy

- このリポジトリは研究用途のため、曖昧な実装を行わないこと。
- コード修正時に後方互換性は持たせないこと。旧仕様との互換レイヤーや暫定分岐を追加しないこと。

## Environment

- Python環境はuvで構築しています。

## Test Script

- 実行検証用のシェルスクリプトがあります: scripts/test.sh
- 一時ファイルやテストログはルートの /tmp を使わず、multi-label/tmp 配下に保存すること。

## 実行時の注意

- scripts/test.sh は GPU 実行を前提としているため、サンドボックスではなくローカルマシン上で実行すること。
- GPU 実行が必要な検証は、必ずローカルマシンで実行すること。
- 実行時にはGPUが必要になるのでsandbox環境ではなく、このマシンで実行しろ
- テストは必ずローカルマシンで実行すること。外部サンドボックス環境でのテスト結果は採用しないこと。

## Search

積極的にGithub MCP, Context7 MCPを利用してソースを元に行動しろ。曖昧な可能性で対話を終了するな。

## REPORT.md 編集ルール

- REPORT.md の「実験設定」「再現性」「評価プロトコル」に関する追記・修正時は、NeurIPS Reproducibility Checklist を参照して章構成と記載項目を確認すること。
- 参照先: https://neurips.cc/public/guides/PaperChecklist
- 可能な限り、REPORT.md 側にも該当参照（脚注または参考文献）を残し、後続編集者が辿れる状態にすること。

## OpenSpec (Spec-driven workflow)

このリポジトリは OpenSpec を使用する。

- 実装に入る前に、必ず openspec/project.md と関連する openspec/specs を読むこと。
- 実装に入る前に、必ず openspec/specs/version-control.md と openspec/specs/commit-message-policy/spec.md を確認すること。
- 仕様変更や機能追加は、まず openspec/changes/<change>/ に計画（proposal/spec/design/tasks）を作ってから実装すること。
- OpenSpec の CLI 実行時も必ず uv 仮想環境を使い、uv run openspec ... 形式で実行すること。
- 実装が完了したら、変更内容を main specs（openspec/specs/）へ反映すること。

## OpenSpec タスク完了時のコミット運用

- OpenSpec の tasks.md にある各タスクは、完了ごとに必ず 1 回コミットすること。
- タスク完了の定義は、当該タスクに必要な実装変更と検証完了までを含むこと。
- コミット前に当該タスクに必要な検証を実行し、失敗時はコミットしないこと。
- 1 タスクを複数コミットに分割しないこと。複数タスクを 1 コミットにまとめないこと。
- コミット対象は当該タスクの変更ファイルのみに限定し、無関係な差分を含めないこと。
- コミットメッセージは OpenSpec の commit-message-policy 仕様に準拠すること。
- タスクを完了として報告する場合、対応するコミットハッシュを必ず併記すること。
- 未コミットのタスクが 1 件でもある場合、作業完了として報告してはならない。
- コミット不能な状況が発生した場合は、その時点で停止し、理由と解消に必要な対応を報告すること。

## 文体ルール

- AGENTS.md ではバッククォート記法を使わないこと。
