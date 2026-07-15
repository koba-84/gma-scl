#!/usr/bin/env python3
"""Build AAPD label-to-arXiv-taxonomy description mapping."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

AAPD_LABELS: list[str] = [
    "cmp-lg",
    "cond-mat.dis-nn",
    "cond-mat.stat-mech",
    "cs.AI",
    "cs.CC",
    "cs.CE",
    "cs.CG",
    "cs.CL",
    "cs.CR",
    "cs.CV",
    "cs.CY",
    "cs.DB",
    "cs.DC",
    "cs.DL",
    "cs.DM",
    "cs.DS",
    "cs.FL",
    "cs.GT",
    "cs.HC",
    "cs.IR",
    "cs.IT",
    "cs.LG",
    "cs.LO",
    "cs.MA",
    "cs.MM",
    "cs.MS",
    "cs.NA",
    "cs.NE",
    "cs.NI",
    "cs.PF",
    "cs.PL",
    "cs.RO",
    "cs.SC",
    "cs.SE",
    "cs.SI",
    "cs.SY",
    "math.CO",
    "math.IT",
    "math.LO",
    "math.NA",
    "math.NT",
    "math.OC",
    "math.PR",
    "math.ST",
    "nlin.AO",
    "physics.data-an",
    "physics.soc-ph",
    "q-bio.NC",
    "q-bio.QM",
    "quant-ph",
    "stat.AP",
    "stat.ME",
    "stat.ML",
    "stat.TH",
]

LABEL_SOURCE_URL = (
    "https://github.com/laddie132/Transformers-MLTC/"
    "blob/431a741cdf0ed0cffc6327808c96147eaaac8443/datasets/processors.py"
)
CMP_LG_ARCHIVE_URL = "https://arxiv.org/archive/cmp-lg"


def _normalize_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@dataclass
class CategoryEntry:
    label: str
    title: str
    description_lines: list[str]


class ArxivTaxonomyParser(HTMLParser):
    def __init__(self, target_labels: list[str]) -> None:
        super().__init__(convert_charrefs=False)
        self.target_labels = {label.lower() for label in target_labels}
        self.entries: dict[str, CategoryEntry] = {}

        self._ignore_depth = 0
        self._in_h4 = False
        self._h4_parts: list[str] = []
        self._active_label: str | None = None
        self._capture_text = False
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, _) -> None:
        if tag in {"script", "style"}:
            self._ignore_depth += 1
            return
        if self._ignore_depth > 0:
            return
        if tag == "h4":
            self._in_h4 = True
            self._h4_parts = []
            return
        if tag in {"p", "li"} and self._active_label is not None:
            self._capture_text = True
            self._text_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignore_depth > 0:
            self._ignore_depth -= 1
            return
        if self._ignore_depth > 0:
            return

        if tag == "h4" and self._in_h4:
            self._in_h4 = False
            self._set_active_label("".join(self._h4_parts))
            return

        if tag in {"p", "li"} and self._capture_text:
            self._capture_text = False
            line = _normalize_text("".join(self._text_parts))
            if line and self._active_label is not None:
                entry = self.entries[self._active_label]
                if not entry.description_lines or entry.description_lines[-1] != line:
                    entry.description_lines.append(line)

    def handle_data(self, data: str) -> None:
        if self._ignore_depth > 0:
            return
        if self._in_h4:
            self._h4_parts.append(data)
            return
        if self._capture_text:
            self._text_parts.append(data)

    def _set_active_label(self, raw_heading: str) -> None:
        heading = _normalize_text(raw_heading)
        match = re.match(r"^([A-Za-z0-9.-]+)\s*\((.+)\)$", heading)
        if not match:
            self._active_label = None
            return
        label = match.group(1)
        title = match.group(2).strip()
        label_key = label.lower()
        if label_key not in self.target_labels:
            self._active_label = None
            return
        self._active_label = label_key
        if label_key not in self.entries:
            self.entries[label_key] = CategoryEntry(label=label, title=title, description_lines=[])


def _fetch_html(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Only https URLs are allowed: {url}")
    request = Request(
        url=url,
        headers={
            "User-Agent": ("Mozilla/5.0 (compatible; AAPDLabelBuilder/1.0; +https://arxiv.org)")
        },
    )
    with urlopen(request, timeout=30) as response:  # nosec B310: scheme is validated as https above
        return response.read().decode("utf-8", errors="replace")


def _html_to_text_lines(html: str) -> list[str]:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?i)<br\\s*/?>", "\n", text)
    text = re.sub(r"(?i)</(p|div|li|h1|h2|h3|h4|h5|h6|tr|section)>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = unescape(text)
    lines = []
    for line in text.splitlines():
        normalized = re.sub(r"\s+", " ", line).strip()
        if normalized:
            lines.append(normalized)
    return lines


def _extract_cmp_lg_alias() -> CategoryEntry:
    html = _fetch_html(CMP_LG_ARCHIVE_URL)
    lines = _html_to_text_lines(html)
    alias_line_head = "The cmp-lg archive has been subsumed into"
    alias_line_tail = "Computation and Language (cs.CL)."
    parent_line = "Computation and Language (cs.CL) is part of the Computer Science archive."
    collected: list[str] = []
    for idx, line in enumerate(lines):
        if line == alias_line_head:
            collected.append(line)
            if idx + 1 < len(lines):
                collected.append(lines[idx + 1])
            for j in range(idx + 1, min(idx + 6, len(lines))):
                if lines[j] == parent_line:
                    collected.append(lines[j])
                    break
            break
    if not collected:
        raise RuntimeError("Failed to extract cmp-lg alias description from arXiv archive page.")
    return CategoryEntry(
        label="cmp-lg",
        title="Computation and Language",
        description_lines=collected,
    )


def build_mapping(taxonomy_url: str) -> dict:
    html = _fetch_html(taxonomy_url)
    parser = ArxivTaxonomyParser(target_labels=AAPD_LABELS)
    parser.feed(html)
    if "cmp-lg" not in parser.entries:
        parser.entries["cmp-lg"] = _extract_cmp_lg_alias()

    labels_payload = []
    missing = []
    for i, label in enumerate(AAPD_LABELS, start=1):
        key = label.lower()
        entry = parser.entries.get(key)
        if entry is None:
            missing.append(label)
            continue
        labels_payload.append(
            {
                "index": i,
                "label": label,
                "taxonomy_title": entry.title,
                "description": "\n".join(entry.description_lines),
            }
        )

    if missing:
        raise RuntimeError("Failed to extract taxonomy entries for labels: " + ", ".join(missing))

    return {
        "dataset": "AAPD",
        "taxonomy_source_url": taxonomy_url,
        "label_source_url": LABEL_SOURCE_URL,
        "cmp_lg_alias_source_url": CMP_LG_ARCHIVE_URL,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "total_labels": len(labels_payload),
        "labels": labels_payload,
    }


def _write_json_atomic(payload: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        tmp_path.replace(output_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        if output_path.exists():
            output_path.unlink()
        raise


def _write_csv_atomic(payload: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["abbreviation", "full_name", "description"])
            for row in payload["labels"]:
                writer.writerow([row["label"], row["taxonomy_title"], row["description"]])
        tmp_path.replace(output_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        if output_path.exists():
            output_path.unlink()
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build AAPD label mapping from arXiv taxonomy (verbatim extraction)."
    )
    parser.add_argument(
        "--taxonomy-url",
        default="https://arxiv.org/category_taxonomy",
        help="Source URL of arXiv category taxonomy page.",
    )
    parser.add_argument(
        "--output",
        default="data/aapd/arxiv_label_descriptions.csv",
        help="Output CSV path.",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    try:
        payload = build_mapping(args.taxonomy_url)
        if args.format == "csv":
            _write_csv_atomic(payload, output_path)
        else:
            _write_json_atomic(payload, output_path)
    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise
    print(f"Wrote {len(payload['labels'])} labels to {output_path}")


if __name__ == "__main__":
    main()
