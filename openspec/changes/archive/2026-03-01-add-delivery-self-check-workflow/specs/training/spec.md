## ADDED Requirements

### Requirement: Pre-report delivery self-check

開発者は作業報告の前に自己点検を実行し、OpenSpec 状態・検証結果・commit 情報を確認できる状態を MUST 作る。

#### Scenario: Run delivery self-check script

- **WHEN** 開発者が報告前に `bash scripts/verify_delivery.sh --changes <change> --run "<command>"` を実行する
- **THEN** スクリプトは OpenSpec 完了状態と検証コマンドの成否を表示し、失敗があれば非0で終了する

#### Scenario: Prepare report from checklist

- **WHEN** 開発者が `docs/delivery_self_check.md` のテンプレートに従って報告を作成する
- **THEN** 報告には commit 粒度・実行検証・OpenSpec 状態が含まれる
