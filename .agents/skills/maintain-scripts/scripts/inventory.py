#!/usr/bin/env python3
"""Inventory all skill scripts — map to SKILL.md and agents-run."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[3] / "env" / "python" / "lib"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

from kit_paths import (  # noqa: E402
    ScriptEntry,
    agents_run_resolvable,
    find_kit_root,
    iter_skill_scripts,
    read_skill_md,
    skill_mentions_stem,
)


def audit(entries: list[ScriptEntry], kit: Path) -> int:
    issues = 0
    print(f"Kit: {kit}")
    print(f"Scripts found: {len(entries)}")
    print()
    print(f"{'SKILL':<24} {'STEM':<28} {'EXT':<5} {'SKILL.md':<10} {'agents-run'}")
    print("-" * 85)

    by_skill: dict[str, list[ScriptEntry]] = {}
    for e in entries:
        by_skill.setdefault(e.skill, []).append(e)

    for skill in sorted(by_skill):
        md = read_skill_md(kit, skill)
        for e in by_skill[skill]:
            mentioned = skill_mentions_stem(md, e.stem)
            resolvable = agents_run_resolvable(kit, e.skill, e.stem)
            md_flag = "yes" if mentioned else "MISSING"
            ar_flag = "ok" if resolvable else "FAIL"
            if not mentioned:
                print(f"UNDOCUMENTED: {e.skill}/{e.stem}{e.ext} — add to SKILL.md")
                issues += 1
            if not resolvable:
                issues += 1
            print(f"{e.skill:<24} {e.stem:<28} {e.ext:<5} {md_flag:<10} {ar_flag}")

    # hooks (separate from skills)
    hooks = list((kit / "hooks").glob("*.py")) if (kit / "hooks").is_dir() else []
    if hooks:
        print()
        print("Hooks (stdlib-only, not agents-run):")
        for h in sorted(hooks):
            print(f"  hooks/{h.name}")

    print()
    if issues == 0:
        print("OK: inventory clean")
    else:
        print(f"Found {issues} inventory issue(s)")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory skill scripts")
    parser.add_argument(
        "skills_root",
        nargs="?",
        help="Path to skills/ directory (default: auto-detect kit/skills)",
    )
    parser.add_argument("--json", action="store_true", help="Reserved for future use")
    args = parser.parse_args()

    if args.skills_root:
        skills = Path(args.skills_root).resolve()
        kit = skills.parent if skills.name == "skills" else find_kit_root()
    else:
        kit = find_kit_root(Path(__file__))
        skills = kit / "skills"

    if not skills.is_dir():
        print(f"skills root not found: {skills}", file=sys.stderr)
        return 2

    return min(audit(iter_skill_scripts(kit), kit), 255)


if __name__ == "__main__":
    raise SystemExit(main())
