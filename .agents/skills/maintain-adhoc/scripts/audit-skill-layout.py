#!/usr/bin/env python3
"""Audit .agents/skills layout — canonical (Windows + Unix)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEPRECATED_SKILLS = frozenset(
    {"steward-skill-catalog", "pm-delegation-launch", "hermes-role-execute"}
)
REQUIRED_PM = (
    "pm-turn-start",
    "pm-turn-end",
    "context-guard",
    "memory-reference",
    "memory-reason",
    "memory-flush",
    "memory-record",
    "secretary-brief",
    "secretary-route",
    "role-execute",
    "action-evaluate",
    "memory-critique",
    "lib-memory-io",
    "lib-doc-frontmatter",
    "lib-tdd-cycle",
    "lib-review-vmodel",
)
EXPECTED_SKILL_COUNT = 54
HERMES_OK = re.compile(r"禁止|forbidden|deprecated|撤去|replaces|未使用|No Hermes", re.I)
SKIP_EXT = {".png", ".jpg", ".gif", ".webp", ".pyc"}
PIPELINE_JARGON = re.compile(
    r"\b(P[0-6]\u2014|P[0-6]—|L1 chain step|Use with \w+ after |Every turn end—|Every turn first—)",
    re.I,
)
DEPRECATED_PATHS = (
    "docs/SKILLS_RULES_BY_PHASE.md",
    "rules/cursor-agent-tooling.mdc",
    "skills/_chains/memory-turn.md",
    "skills/_chains/secretary-turn.md",
)
L0_BUDGETS = {
    "secretary-gate.mdc": 25,
    "kit-context-routing.mdc": 15,
    "no-subagents.mdc": 10,
}


def default_skills_root() -> Path:
    script = Path(__file__).resolve()
    return script.parent.parent.parent  # skills/


def kit_root_from_skills(skills: Path) -> Path:
    return skills.parent


def audit(root: Path) -> int:
    issues = 0
    kit = kit_root_from_skills(root)
    skill_mds = sorted(root.glob("*/SKILL.md"))
    print(f"Auditing skills under: {root}")

    for skill_md in skill_mds:
        name = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
        front = m.group(1).strip() if m else ""
        if front != name:
            print(f"NAME_MISMATCH: folder={name} frontmatter name={front}")
            issues += 1

        dm = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        if not dm:
            print(f"MISSING_DESCRIPTION: {name}")
            issues += 1
        else:
            desc = dm.group(1).strip()
            if len(desc) < 40:
                print(f"DESCRIPTION_TOO_SHORT: {name}")
                issues += 1
            if PIPELINE_JARGON.search(desc):
                print(f"DESCRIPTION_PIPELINE_JARGON: {name}")
                issues += 1
            if "Use when" not in desc and "Use at" not in desc and "Use before" not in desc and "Use after" not in desc and "Use for" not in desc and "Use on" not in desc:
                print(f"DESCRIPTION_MISSING_USE_WHEN: {name}")
                issues += 1

        if (skill_md.parent / "STANDARDS.md").is_file():
            print(f"LEGACY_ROOT_FILE: {name}/STANDARDS.md -> move to references/")
            issues += 1

        if (skill_md.parent / "templates").is_dir() and not (skill_md.parent / "assets/templates").is_dir():
            print(f"LEGACY_TEMPLATES: {name}/templates -> move to assets/templates/")
            issues += 1

        if len(text.splitlines()) > 120:
            print(f"SKILL_MD_LONG: {name} ({len(text.splitlines())} lines)")
            issues += 1

        if name in DEPRECATED_SKILLS:
            print(f"DEPRECATED_SKILL_DIR: {name}")
            issues += 1

        if re.search(r"hermes", text, re.I) and not HERMES_OK.search(text):
            print(f"HERMES_MENTION: {name}")
            issues += 1

        support = 0
        for sub in ("references", "assets", "scripts"):
            d = skill_md.parent / sub
            if d.is_dir() and any(
                f for f in d.rglob("*") if f.is_file() and f.suffix.lower() not in SKIP_EXT
            ):
                support += 1
        if support == 0:
            print(f"MISSING_SUPPORT_DIR: {name}")
            issues += 1

        # dead local links to deleted chains
        if "memory-turn.md" in text or "secretary-turn.md" in text:
            print(f"DEAD_CHAIN_LINK: {name}")
            issues += 1

    count = len(skill_mds)
    print(f"Skill count: {count} (expected: {EXPECTED_SKILL_COUNT})")
    if count != EXPECTED_SKILL_COUNT:
        print(f"SKILL_COUNT_MISMATCH: got {count}")
        issues += 1

    for req in REQUIRED_PM:
        if not (root / req / "SKILL.md").is_file():
            print(f"MISSING_PM_SKILL: {req}")
            issues += 1

    if not (root / "_chains" / "pm-turn.md").is_file():
        print("MISSING_PM_TURN_CHAIN")
        issues += 1

    for rel in DEPRECATED_PATHS:
        if (kit / rel).exists():
            print(f"DEPRECATED_FILE_PRESENT: {rel}")
            issues += 1

    rules = kit / "rules"
    for fname, budget in L0_BUDGETS.items():
        path = rules / fname
        if not path.is_file():
            print(f"MISSING_L0_RULE: {fname}")
            issues += 1
            continue
        n = len(path.read_text(encoding="utf-8").splitlines())
        if n > budget:
            print(f"L0_OVER_BUDGET: {fname} {n}/{budget}")
            issues += 1

    if issues == 0:
        print("OK: no layout issues")
    else:
        print(f"Found {issues} issue(s)")
    return issues


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else default_skills_root()
    if not root.is_dir():
        print(f"skills root not found: {root}", file=sys.stderr)
        return 2
    return min(audit(root.resolve()), 255)


if __name__ == "__main__":
    raise SystemExit(main())
