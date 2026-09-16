#!/usr/bin/env python3
# ruff: noqa: I001

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import wandb
import yaml  # type: ignore[import-untyped]
from src.utils.wandb_config_aliases import derive_wandb_config_aliases, merge_nested_config

DEFAULT_ENTITY = "koba84-"
DEFAULT_PROJECT = "gma-scl"
FLATTEN_ROOTS = ("contrastive", "classification", "data", "trainer", "callbacks", "extras")
DEFAULT_DOWNLOAD_ROOT = Path("tmp") / "wandb_backfill"


def _get_nested(config: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = config
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _set_nested(config: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    current = config
    for key in path[:-1]:
        nested = current.get(key)
        if not isinstance(nested, dict):
            nested = {}
            current[key] = nested
        current = nested
    current[path[-1]] = value


def _populate_nested_aliases(config: dict[str, Any]) -> None:
    merged = merge_nested_config(config, derive_wandb_config_aliases(config))
    config.clear()
    config.update(merged)


def _inflate_flat_root_keys(config: dict[str, Any]) -> dict[str, Any]:
    inflated = copy.deepcopy(config)

    for key, value in config.items():
        if "." not in key:
            continue
        root, *path = key.split(".")
        if root not in FLATTEN_ROOTS or not path:
            continue
        root_value = inflated.get(root)
        if not isinstance(root_value, dict):
            inflated[root] = {}
        _set_nested(inflated, tuple([root, *path]), copy.deepcopy(value))

    return inflated


def _unwrap_downloaded_config_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _unwrap_downloaded_config_value(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_unwrap_downloaded_config_value(item) for item in value]
    return value


def normalize_downloaded_run_config(config_yaml: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    items = config_yaml.get("_items")
    if isinstance(items, dict):
        items_value = items.get("value")
        if isinstance(items_value, dict):
            for key, value in items_value.items():
                normalized[key] = _unwrap_downloaded_config_value(value)

    for key, wrapped in config_yaml.items():
        if key == "_items":
            continue
        if isinstance(wrapped, dict) and "value" in wrapped:
            value = _unwrap_downloaded_config_value(wrapped["value"])
        else:
            value = _unwrap_downloaded_config_value(wrapped)
        replace_marker = f"__replace_{key}__"
        if value == replace_marker and key in normalized:
            continue
        normalized[key] = value

    return normalized


def merge_backfill_source_config(
    primary_config: dict[str, Any],
    fallback_config: dict[str, Any],
) -> dict[str, Any]:
    merged = _inflate_flat_root_keys(primary_config)
    fallback_inflated = _inflate_flat_root_keys(fallback_config)

    for root in FLATTEN_ROOTS:
        fallback_value = fallback_inflated.get(root)
        current_value = merged.get(root)
        if isinstance(fallback_value, dict) and not isinstance(current_value, dict):
            merged[root] = copy.deepcopy(fallback_value)

    for key, value in fallback_inflated.items():
        if merged.get(key) in (None, ""):
            merged[key] = copy.deepcopy(value)

    return merged


def load_backfill_source_config(
    run: wandb.apis.public.Run,
    *,
    download_root: Path = DEFAULT_DOWNLOAD_ROOT,
) -> dict[str, Any]:
    primary_config = copy.deepcopy(run.config)
    try:
        config_file = run.file("config.yaml")
        download_root.mkdir(parents=True, exist_ok=True)
        downloaded = Path(
            config_file.download(root=str(download_root), replace=True, exist_ok=True).name
        )
        downloaded_config = yaml.safe_load(downloaded.read_text(encoding="utf-8"))
    except Exception:
        return primary_config
    if not isinstance(downloaded_config, dict):
        return primary_config
    return merge_backfill_source_config(
        primary_config,
        normalize_downloaded_run_config(downloaded_config),
    )


def _infer_pretrained_encoder_path(config: dict[str, Any]) -> str | None:
    existing = _get_nested(config, ("classification", "model", "pretrained_encoder_path"))
    if existing:
        return str(existing)

    save_last = _get_nested(config, ("contrastive", "save_last_encoder"))
    default_root_dir = _get_nested(config, ("contrastive", "trainer", "default_root_dir"))
    if save_last is not True or not isinstance(default_root_dir, str) or not default_root_dir:
        return None

    return str(Path(default_root_dir) / "checkpoints" / "contrastive_last.ckpt")


def build_backfill_payload(
    current_config: dict[str, Any],
    source_config: dict[str, Any],
) -> dict[str, Any]:
    working = copy.deepcopy(source_config)
    payload: dict[str, Any] = {}

    _populate_nested_aliases(working)

    inferred_pretrained = _infer_pretrained_encoder_path(working)
    pretrained_path = ("classification", "model", "pretrained_encoder_path")
    if inferred_pretrained is not None and not _get_nested(working, pretrained_path):
        _set_nested(working, pretrained_path, inferred_pretrained)

    for root in FLATTEN_ROOTS:
        root_value = working.get(root)
        current_value = current_config.get(root)
        if isinstance(root_value, dict) and current_value != root_value:
            payload[root] = root_value

    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill missing W&B config aliases.")
    parser.add_argument("run_ids", nargs="+", help="Target W&B run IDs.")
    parser.add_argument("--entity", default=DEFAULT_ENTITY)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Persist updates to W&B. Omit for dry-run.",
    )
    parser.add_argument(
        "--download-root",
        type=Path,
        default=DEFAULT_DOWNLOAD_ROOT,
        help="Directory for downloaded run config files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api = wandb.Api()

    for run_id in args.run_ids:
        run = api.run(f"{args.entity}/{args.project}/{run_id}")
        source_config = load_backfill_source_config(run, download_root=args.download_root)
        payload = build_backfill_payload(run.config, source_config)
        print(f"[{run_id}] {run.name}")
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

        if args.apply and payload:
            run.config.update(payload, allow_val_change=True)
            run.update()
            print(f"[{run_id}] updated {len(payload)} keys")
        elif args.apply:
            print(f"[{run_id}] no update needed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
