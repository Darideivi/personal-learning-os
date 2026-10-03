#!/usr/bin/env python3
"""Lint `notes/`: frontmatter fields, enums, dangling topic references, broken links.

Usage: python3 scripts/notes/check_notes.py [notes_dir]   (exit 1 on errors)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import notes_lib  # noqa: E402

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "notes"
problems = notes_lib.check(root)
for level, path, msg in problems:
    print(f"{level.upper():5} {path}: {msg}")
items = notes_lib.parse_inbox(root / "inbox.md")
print(f"\ninbox.md: {len(items)} items parse cleanly")
errors = sum(1 for l, *_ in problems if l == "error")
print(f"{errors} error(s), {len(problems) - errors} warning(s)")
sys.exit(1 if errors else 0)
