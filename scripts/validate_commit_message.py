#!/usr/bin/env python3
"""Validate commit messages against repository policy."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess  # nosec B404: subprocess is required to invoke git for policy checks
import sys
from dataclasses import dataclass

ALLOWED_TYPES = ("Feat", "Fix", "Refactor", "Docs", "Test", "Chore")
BEHAVIOR_TYPES = ("Feat", "Fix", "Refactor")
ML_PATH_PREFIXES = ("src/models/", "src/data/", "configs/")
SUBJECT_PATTERN = re.compile(r"^(Feat|Fix|Refactor|Docs|Test|Chore):\s+.+$")


@dataclass
class ValidationTarget:
    ref_label: str
    message: str
    changed_files: list[str]


def _run_git(*args: str) -> str:
    git_bin = shutil.which("git")
    if not git_bin:
        raise RuntimeError("git executable not found in PATH")
    result = subprocess.run(
        [git_bin, *args],
        capture_output=True,
        text=True,
        check=False,
    )  # nosec B603: git binary is resolved from PATH and args are fixed git subcommands
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def _has_section(body: str, section: str) -> bool:
    return re.search(rf"(?mi)^{re.escape(section)}:\s*\S+", body) is not None


def _parse_type(subject: str) -> str | None:
    if ":" not in subject:
        return None
    return subject.split(":", 1)[0].strip()


def _is_ml_impact(changed_files: list[str]) -> bool:
    return any(path.startswith(ML_PATH_PREFIXES) for path in changed_files)


def _validate_one(target: ValidationTarget) -> list[str]:
    lines = target.message.strip("\n").splitlines()
    subject = lines[0].strip() if lines else ""
    body = "\n".join(lines[1:]).strip()
    errors: list[str] = []

    if not SUBJECT_PATTERN.match(subject):
        errors.append(
            "件名は '<Type>: <summary>' 形式で、Type は "
            f"{', '.join(ALLOWED_TYPES)} のいずれかにしてください。"
        )
        return errors

    commit_type = _parse_type(subject)
    if commit_type not in ALLOWED_TYPES:
        errors.append(f"未許可の Type です: {commit_type}")
        return errors

    if commit_type in BEHAVIOR_TYPES:
        if not _has_section(body, "Why"):
            errors.append("挙動変更コミットには 'Why:' が必要です。")
        if not _has_section(body, "Validation"):
            errors.append("挙動変更コミットには 'Validation:' が必要です。")

    if _is_ml_impact(target.changed_files) and not _has_section(body, "Reproducibility"):
        errors.append(
            "ML影響ファイルを含むため 'Reproducibility:' が必要です "
            "(例: 設定キー・設定ファイル・データ契約)。"
        )

    return errors


def _validate_commit_message_file(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        message = f.read()

    changed_files = [
        line.strip()
        for line in _run_git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"
        ).splitlines()
        if line.strip()
    ]
    errors = _validate_one(
        ValidationTarget(ref_label="COMMIT_MSG", message=message, changed_files=changed_files)
    )
    if not errors:
        return 0

    print("commit message policy violation (commit-msg stage):", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    print(
        "\n推奨テンプレート:\n"
        "Feat: Short imperative summary\n\n"
        "Why: reason\n"
        "Validation: command/result\n"
        "Reproducibility: config/data context (if ML-impacting)",
        file=sys.stderr,
    )
    return 1


def _collect_push_targets() -> list[ValidationTarget]:
    try:
        upstream = _run_git(
            "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"
        ).strip()
    except RuntimeError:
        print("[commit-message-check] upstream 未設定のため pre-push 検証をスキップします。")
        return []

    rev_range = f"{upstream}..HEAD"
    commits = [
        line.strip()
        for line in _run_git("rev-list", "--reverse", rev_range).splitlines()
        if line.strip()
    ]
    targets: list[ValidationTarget] = []
    for commit in commits:
        message = _run_git("log", "-1", "--pretty=%B", commit)
        changed_files = [
            line.strip()
            for line in _run_git(
                "diff-tree", "--no-commit-id", "--name-only", "-r", commit
            ).splitlines()
            if line.strip()
        ]
        targets.append(
            ValidationTarget(ref_label=commit, message=message, changed_files=changed_files)
        )
    return targets


def _validate_pre_push() -> int:
    targets = _collect_push_targets()
    if not targets:
        return 0

    failures: list[tuple[str, list[str]]] = []
    for target in targets:
        errors = _validate_one(target)
        if errors:
            failures.append((target.ref_label, errors))

    if not failures:
        return 0

    print("commit message policy violation (pre-push stage):", file=sys.stderr)
    for ref, errors in failures:
        print(f"- commit {ref}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("commit-msg", "pre-push"), required=True)
    parser.add_argument("commit_msg_file", nargs="?")
    args = parser.parse_args()

    if args.mode == "commit-msg":
        if not args.commit_msg_file:
            print("commit-msg mode requires commit message file path", file=sys.stderr)
            return 2
        return _validate_commit_message_file(args.commit_msg_file)

    return _validate_pre_push()


if __name__ == "__main__":
    raise SystemExit(main())
