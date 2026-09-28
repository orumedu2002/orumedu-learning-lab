#!/usr/bin/env python
"""Fail if a Jekyll post lacks a usable 16:9 thumbnail asset."""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
REQUIRED_FROM = "2026-09-27"
THUMBNAIL_RE = re.compile(r'^thumbnail:\s*["\']?([^"\'\n]+)', re.MULTILINE)
DATE_RE = re.compile(r'^date:\s*(\d{4}-\d{2}-\d{2})', re.MULTILINE)


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as source:
        header = source.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("not a PNG file")
    return struct.unpack(">II", header[16:24])


def asset_path(value: str) -> Path:
    return ROOT / value.lstrip("/")


def main() -> int:
    failures: list[str] = []
    checked = 0

    for post in sorted(POSTS.glob("*.md")):
        text = post.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            failures.append(f"{post.name}: missing YAML front matter")
            continue
        front_matter = text.split("---\n", 2)[1]
        date = DATE_RE.search(front_matter)
        if not date or date.group(1) < REQUIRED_FROM:
            continue
        thumbnail = THUMBNAIL_RE.search(front_matter)
        if not thumbnail:
            failures.append(f"{post.name}: missing thumbnail")
            continue

        thumbnail_value = thumbnail.group(1).strip()
        path = asset_path(thumbnail_value)
        if not path.is_file():
            failures.append(f"{post.name}: thumbnail asset does not exist: {thumbnail_value}")
            continue
        try:
            width, height = png_size(path)
        except ValueError as error:
            failures.append(f"{post.name}: {thumbnail_value}: {error}")
            continue
        if abs(width / height - 16 / 9) > 0.002:
            failures.append(f"{post.name}: {thumbnail_value} is {width}x{height}, not 16:9")
            continue
        checked += 1

    if failures:
        print("Thumbnail verification failed:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print(f"Thumbnail verification passed: {checked} posts dated {REQUIRED_FROM} or later; all assets exist and are 16:9 PNGs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
