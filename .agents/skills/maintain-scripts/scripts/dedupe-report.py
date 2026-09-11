#!/usr/bin/env python3
"""Report duplicate script stems and similar Python files (dedupe hints)."""
from __future__ import annotations

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

_LIB = Path(__file__).resolve().parents[3] / "env" / "python" / "lib"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

from kit_paths import find_kit_root, iter_skill_scripts  # noqa: E402


def normalized_hash(path: Path) -> str:
    lines = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    body = "\n".join(lines)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description="Dedupe report for skill scripts")
    parser.add_argument("--min-lines", type=int, default=10, help="Min lines for similarity hash")
    args = parser.parse_args()

    kit = find_kit_root(Path(__file__))
    entries = [e for e in iter_skill_scripts(kit) if e.ext == ".py"]

    by_stem: dict[str, list[str]] = defaultdict(list)
    by_hash: dict[str, list[str]] = defaultdict(list)
    hints = 0

    for e in entries:
        rel = e.path.relative_to(kit).as_posix()
        by_stem[e.stem].append(rel)
        line_count = len(e.path.read_text(encoding="utf-8").splitlines())
        if line_count >= args.min_lines:
            h = normalized_hash(e.path)
            by_hash[h].append(rel)

    print("Duplicate stems (same filename across skills):")
    for stem, paths in sorted(by_stem.items()):
        if len(paths) > 1:
            hints += 1
            print(f"  {stem}:")
            for p in paths:
                print(f"    - {p}")

    print()
    print("Similar bodies (normalized hash match):")
    for h, paths in sorted(by_hash.items(), key=lambda x: -len(x[1])):
        if len(paths) > 1:
            hints += 1
            print(f"  hash {h}:")
            for p in paths:
                print(f"    - {p}")
            print("    -> consider env/python/lib/ extraction")

    print()
    if hints == 0:
        print("OK: no dedupe hints")
    else:
        print(f"Found {hints} dedupe hint(s) — dry-run only; apply via maintain-record")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
