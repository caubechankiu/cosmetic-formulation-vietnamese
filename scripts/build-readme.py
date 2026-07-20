#!/usr/bin/env python3
"""Build a single README.md from translated Markdown sections."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
TOC_PATH = ROOT / "translations" / "markdown" / "table-of-contents.md"
DEFAULT_OUTPUT = ROOT / "README.md"

TOC_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
HEADING_RE = re.compile(r"^(#{1,6})(\s+.*)$")
ANCHOR_ID_RE = re.compile(r"[^a-z0-9._-]+")


@dataclass(frozen=True)
class TranslatedSection:
    path: Path
    depth: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a single Markdown README.md by concatenating translated "
            "sections linked from translations/markdown/table-of-contents.md."
        )
    )
    parser.add_argument(
        "--toc",
        type=Path,
        default=TOC_PATH,
        help=f"Path to the translation table of contents. Default: {TOC_PATH}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output Markdown file. Default: {DEFAULT_OUTPUT}",
    )
    return parser.parse_args()


def find_translated_sections(toc_path: Path) -> list[TranslatedSection]:
    toc_dir = toc_path.parent
    translated_sections: list[TranslatedSection] = []
    seen: set[Path] = set()
    columns: dict[str, int] = {}

    for line in toc_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue

        if cells[0] == "Mục":
            columns = {cell.lower(): index for index, cell in enumerate(cells)}
            continue

        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue

        match = TOC_LINK_RE.search(line)
        if not match:
            continue

        item_index = columns.get("mục", 0)
        depth_index = columns.get("depth")
        item = cells[item_index] if item_index < len(cells) else ""
        depth = toc_depth(item)
        if depth_index is not None and depth_index < len(cells):
            depth = parse_depth(cells[depth_index], fallback=depth)

        link_target = match.group(1).strip()
        if is_external_or_anchor(link_target):
            continue

        translated_file = (toc_dir / unquote(urlsplit(link_target).path)).resolve()
        if translated_file in seen:
            continue

        translated_sections.append(
            TranslatedSection(path=translated_file, depth=depth)
        )
        seen.add(translated_file)

    return translated_sections


def parse_depth(value: str, fallback: int) -> int:
    try:
        depth = int(value)
    except ValueError:
        return fallback
    return depth if depth > 0 else fallback


def toc_depth(item: str) -> int:
    if not item:
        return 1
    if item.startswith("Phần"):
        return 1
    if item.startswith("Chương"):
        return 2
    if re.fullmatch(r"\d+(?:\.\d+)*", item):
        return item.count(".") + 2
    return 1


def is_external_or_anchor(target: str) -> bool:
    parts = urlsplit(target)
    return bool(parts.scheme or parts.netloc or target.startswith("#"))


def rewrite_relative_links(markdown: str, source_path: Path, output_path: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        if is_external_or_anchor(target):
            return match.group(0)

        parts = urlsplit(target)
        if not parts.path:
            return match.group(0)

        absolute_target = (source_path.parent / unquote(parts.path)).resolve()
        relative_target = Path(
            relative_path(from_dir=output_path.parent, to_path=absolute_target)
        ).as_posix()
        rewritten = urlunsplit(("", "", relative_target, parts.query, parts.fragment))
        return f"{prefix}{rewritten}{suffix}"

    return MARKDOWN_LINK_RE.sub(replace, markdown)


def build_table_of_contents(toc_path: Path, section_anchors: dict[Path, str]) -> str:
    toc_dir = toc_path.parent
    toc_lines = toc_path.read_text(encoding="utf-8").splitlines()
    output_lines = ["## Mục lục"]

    for line in toc_lines:
        if line.strip() == "# Mục Lục":
            continue

        def replace(match: re.Match[str]) -> str:
            target = match.group(1).strip()
            if is_external_or_anchor(target):
                return match.group(0)

            parts = urlsplit(target)
            if not parts.path:
                return match.group(0)

            translated_file = (toc_dir / unquote(parts.path)).resolve()
            anchor = section_anchors.get(translated_file)
            if not anchor:
                return match.group(0)

            return match.group(0).replace(target, f"#{anchor}", 1)

        output_lines.append(TOC_LINK_RE.sub(replace, line))

    return "\n".join(output_lines).strip()


def anchor_id(path: Path) -> str:
    anchor = ANCHOR_ID_RE.sub("-", path.stem.lower()).strip("-")
    return anchor or "section"


def unique_section_anchors(sections: list[TranslatedSection]) -> dict[Path, str]:
    anchors: dict[Path, str] = {}
    counts: dict[str, int] = {}

    for section in sections:
        base_anchor = anchor_id(section.path)
        count = counts.get(base_anchor, 0)
        counts[base_anchor] = count + 1
        anchors[section.path] = base_anchor if count == 0 else f"{base_anchor}-{count + 1}"

    return anchors


def adjust_heading_depth(markdown: str, target_depth: int) -> str:
    delta = target_depth - 1
    if delta <= 0:
        return markdown

    adjusted_lines: list[str] = []
    in_fenced_code = False

    for line in markdown.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            adjusted_lines.append(line)
            continue

        if in_fenced_code:
            adjusted_lines.append(line)
            continue

        match = HEADING_RE.match(line)
        if not match:
            adjusted_lines.append(line)
            continue

        hashes, title = match.groups()
        adjusted_level = min(len(hashes) + delta, 6)
        adjusted_lines.append(f"{'#' * adjusted_level}{title}")

    return "\n".join(adjusted_lines)


def relative_path(from_dir: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_dir)


def build_readme(toc_path: Path, output_path: Path) -> list[TranslatedSection]:
    toc_path = toc_path.resolve()
    translated_sections = find_translated_sections(toc_path)
    if not translated_sections:
        raise RuntimeError(f"No translated Markdown links found in {toc_path}")

    missing_files = [section.path for section in translated_sections if not section.path.is_file()]
    if missing_files:
        missing = "\n".join(f"- {path}" for path in missing_files)
        raise FileNotFoundError(f"Translated files listed in TOC were not found:\n{missing}")

    section_anchors = unique_section_anchors(translated_sections)
    sections = [
        "# Designing Data-Intensive Applications - Bản dịch tiếng Việt\n\n"
        "<!-- File này được tạo tự động bởi scripts/build-readme.py. -->\n",
        build_table_of_contents(toc_path, section_anchors),
    ]

    for section in translated_sections:
        translated_file = section.path
        content = translated_file.read_text(encoding="utf-8").strip()
        content = adjust_heading_depth(content, section.depth)
        content = rewrite_relative_links(content, translated_file, output_path)
        sections.append(f'<a id="{section_anchors[translated_file]}"></a>\n\n{content}')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n\n---\n\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return translated_sections


def main() -> int:
    args = parse_args()
    toc_path = args.toc if args.toc.is_absolute() else ROOT / args.toc
    output_path = args.output if args.output.is_absolute() else ROOT / args.output

    try:
        translated_sections = build_readme(toc_path, output_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {output_path.relative_to(ROOT)} from {len(translated_sections)} translated files:")
    for section in translated_sections:
        print(f"- depth {section.depth}: {section.path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
