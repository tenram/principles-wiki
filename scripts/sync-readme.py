#!/usr/bin/env python3

from __future__ import annotations

import argparse
import difflib
from pathlib import Path
from posixpath import normpath, join as posix_join
from urllib.parse import urlsplit, urlunsplit
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "wiki" / "index.md"
TARGET = REPO_ROOT / "README.md"
LINK_PATTERN = re.compile(r"(!?\[[^\]]*\]\()([^)]*)(\))")


def rewrite_link(href: str) -> str:
    parts = urlsplit(href.strip())
    if parts.scheme or parts.netloc or href.startswith(("/", "#")):
        return href

    path = parts.path
    if not path or path.startswith("wiki/"):
        return href

    rewritten = normpath(posix_join("wiki", path))
    return urlunsplit(("", "", rewritten, parts.query, parts.fragment))


def rewrite_markdown_links(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{rewrite_link(match.group(2))}{match.group(3)}"

    return LINK_PATTERN.sub(replace, text)


def build_readme() -> str:
    return rewrite_markdown_links(SOURCE.read_text(encoding="utf-8"))


def write_readme(content: str) -> None:
    TARGET.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync README.md from wiki/index.md.")
    parser.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    args = parser.parse_args()

    generated = build_readme()
    if not generated.endswith("\n"):
        generated += "\n"

    if args.check:
        current = TARGET.read_text(encoding="utf-8")
        if current == generated:
            return 0
        diff = "".join(
            difflib.unified_diff(
                current.splitlines(True),
                generated.splitlines(True),
                fromfile="README.md",
                tofile="generated README.md",
            )
        )
        sys.stderr.write("README.md is out of date. Run: python3 scripts/sync-readme.py\n")
        sys.stderr.write(diff)
        return 1

    write_readme(generated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
