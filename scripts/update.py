#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any

import wandb


def parse_value(raw: str) -> Any:
    """VALUE はまず JSON として解釈し、失敗したら文字列として扱う。 例:

    true -> True 1e-4 -> 0.0001 32 -> 32 "abc" -> "abc" [1,2,3] -> [1, 2, 3] {"a":1} -> {"a": 1}
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def set_nested_key(d: dict, dotted_key: str, value: Any) -> None:
    """foo.bar.baz=1 のような dotted key を dict に反映する。"""
    parts = dotted_key.split(".")
    cur = d
    for key in parts[:-1]:
        if key not in cur or not isinstance(cur[key], dict):
            cur[key] = {}
        cur = cur[key]
    cur[parts[-1]] = value


def main() -> int:
    parser = argparse.ArgumentParser(description="Update config of an existing W&B run.")
    parser.add_argument("--entity", default="koba84-", help="W&B entity/user/team name")
    parser.add_argument("--project", default="gma-scl", help="W&B project name")
    parser.add_argument("--run-id", required=True, help="W&B run ID")
    parser.add_argument(
        "--set",
        dest="sets",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help=("Repeatable. Example: --set lr=1e-4 --set trainer.max_epochs=20 --set use_amp=true"),
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        default=None,
        help="Optional path to JSON file containing updates",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would be updated, do not send",
    )
    args = parser.parse_args()

    updates: dict[str, Any] = {}

    if args.json_path is not None:
        with open(args.json_path, encoding="utf-8") as f:
            loaded = json.load(f)
        if not isinstance(loaded, dict):
            raise ValueError("--json must point to a JSON object")
        updates.update(loaded)

    for item in args.sets:
        if "=" not in item:
            raise ValueError(f"Invalid --set value: {item!r}. Expected KEY=VALUE.")
        key, raw_value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid empty key in --set: {item!r}")
        value = parse_value(raw_value.strip())
        set_nested_key(updates, key, value)

    if not updates:
        print("No updates given. Use --set KEY=VALUE or --json updates.json", file=sys.stderr)
        return 1

    run_path = f"{args.entity}/{args.project}/{args.run_id}"
    print(f"Target run: {run_path}")
    print("Updates:")
    print(json.dumps(updates, indent=2, ensure_ascii=False))

    if args.dry_run:
        return 0

    # 認証は WANDB_API_KEY / wandb.login() / Api(api_key=...) のいずれかでよい
    api = wandb.Api()
    api_run = api.run(run_path)

    # 公式例は api_run.config["bar"] = 32; api_run.update()
    # 複数更新したいので dict を merge してから update() する
    api_run.config.update(updates)
    api_run.update()

    print("Config updated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
