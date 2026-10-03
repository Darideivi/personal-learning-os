#!/usr/bin/env python3
"""Check that every markdown file in notes/ has valid frontmatter (stdlib only).

Usage: python3 scripts/notes/check_notes.py [notes_dir]
Exit code 0 = all good, 1 = problems found. Templates (_template.md) are skipped.
"""
import re
import sys
from pathlib import Path

REQUIRED = {
    "topic": {"title", "status", "domain"},
    "resource": {"kind", "title", "status"},
    "project": {"title", "status"},
    "journal": {"week"},
}
ALLOWED = {
    ("topic", "status"): {"not-started", "learning", "practicing", "comfortable", "confident"},
    ("resource", "status"): {"to-do", "in-progress", "done"},
    ("project", "status"): {"idea", "active", "paused", "done"},
}
FOLDER_TYPE = {"topics": "topic", "resources": "resource", "projects": "project", "journal": "journal"}


def parse_frontmatter(text: str):
    """Return a dict of top-level `key: value` pairs, or None if there is no block."""
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        line = line.split("  #")[0].rstrip()
        if ":" in line and not line.startswith((" ", "#")):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    return data


def check_file(path: Path, folder: str):
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    if fm is None:
        return ["missing frontmatter block"]
    problems = []
    expected = FOLDER_TYPE[folder]
    if fm.get("type") != expected:
        problems.append(f"type should be '{expected}', got '{fm.get('type', '')}'")
    for key in sorted(REQUIRED[expected]):
        if not fm.get(key):
            problems.append(f"missing '{key}'")
    allowed = ALLOWED.get((expected, "status"))
    if allowed and fm.get("status") and fm["status"] not in allowed:
        problems.append(f"status '{fm['status']}' not in {sorted(allowed)}")
    return problems


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[2] / "notes"
    bad = 0
    count = 0
    for folder in FOLDER_TYPE:
        for path in sorted((root / folder).glob("*.md")):
            if path.name.startswith("_"):
                continue
            count += 1
            for problem in check_file(path, folder):
                bad += 1
                print(f"{path.relative_to(root)}: {problem}")
    print(f"checked {count} files, {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
