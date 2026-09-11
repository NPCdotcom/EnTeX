#!/usr/bin/env python3
"""Review skill scripts against _SCRIPT_POLICY.md rubric."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[3] / "env" / "python" / "lib"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

from kit_paths import ScriptEntry, find_kit_root, iter_skill_scripts  # noqa: E402

SECRET_PATTERNS = re.compile(
    r"\.env\b|password\s*=|api[_-]?key\s*=|secret\s*=|token\s*=",
    re.I,
)
BASH_ONLY_SKILLS: set[str] = set()  # reserved

def review_file(entry: ScriptEntry, kit: Path) -> list[str]:
    issues: list[str] = []
    text = entry.path.read_text(encoding="utf-8", errors="replace")
    rel = entry.path.relative_to(kit).as_posix()

    if entry.ext == ".py":
        if "argparse" not in text and "def main(" not in text:
            issues.append(f"{rel}: missing argparse or main()")
        if "if __name__" not in text:
            issues.append(f"{rel}: missing if __name__ guard")
    elif entry.ext == ".sh":
        py_twin = entry.path.with_suffix(".py")
        if not py_twin.is_file() and entry.stem != "migrate-hermes-to-cursor-roles":
            issues.append(f"{rel}: shell-only - add .py canonical twin")

    for i, line in enumerate(text.splitlines(), 1):
        if "SECRET_PATTERNS" in line or "re.compile" in line:
            continue
        if SECRET_PATTERNS.search(line):
            issues.append(f"{rel}:{i}: possible secret/env reference - review")
            break

    if entry.skill == "maintain-scripts" and entry.stem == "review":
        issues = [x for x in issues if "secret/env" not in x]

    if len(text.splitlines()) > 250:
        issues.append(f"{rel}: long script ({len(text.splitlines())} lines) - extract to env/python/lib/")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Review skill scripts")
    parser.add_argument("--skill", help="Limit to one skill folder name")
    parser.add_argument("--dry-run", action="store_true", help="Report only (default)")
    args = parser.parse_args()

    kit = find_kit_root(Path(__file__))
    entries = iter_skill_scripts(kit)
    if args.skill:
        entries = [e for e in entries if e.skill == args.skill]

    issues = 0
    print(f"Reviewing {len(entries)} script(s) under {kit}")
    for entry in entries:
        for msg in review_file(entry, kit):
            print(msg)
            issues += 1

    if issues == 0:
        print("OK: review passed")
    else:
        print(f"Found {issues} review issue(s)")
    return min(issues, 255)


if __name__ == "__main__":
    raise SystemExit(main())
