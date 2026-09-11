"""Shared path helpers for agent kit scripts."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SCRIPT_EXTS = (".py", ".ps1", ".sh")
STEM_SKIP = {"__pycache__"}


def find_kit_root(start: Path | None = None) -> Path:
    if start is None:
        start = Path.cwd()
    start = start.resolve()
    candidates = [start, start / ".agents"]
    # From skills/<skill>/scripts/foo.py -> walk up
    for parent in [start, *start.parents]:
        if (parent / "skills").is_dir() and (parent / "env").is_dir():
            return parent
        candidates.append(parent)
    for base in candidates:
        if (base / "skills").is_dir():
            return base.resolve()
    raise SystemExit("kit_paths: kit root not found (expected skills/ directory)")


@dataclass(frozen=True)
class ScriptEntry:
    skill: str
    path: Path
    stem: str
    ext: str

    @property
    def rel(self) -> str:
        return self.path.as_posix()


def iter_skill_scripts(kit: Path) -> list[ScriptEntry]:
    skills_root = kit / "skills"
    entries: list[ScriptEntry] = []
    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.is_dir():
            continue
        skill = skill_dir.name
        for path in sorted(scripts_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SCRIPT_EXTS:
                continue
            if path.stem in STEM_SKIP:
                continue
            entries.append(
                ScriptEntry(
                    skill=skill,
                    path=path,
                    stem=path.stem,
                    ext=path.suffix.lower(),
                )
            )
    return entries


def read_skill_md(kit: Path, skill: str) -> str:
    skill_md = kit / "skills" / skill / "SKILL.md"
    if skill_md.is_file():
        return skill_md.read_text(encoding="utf-8")
    return ""


def skill_mentions_stem(skill_md_text: str, stem: str) -> bool:
    if stem in skill_md_text:
        return True
    return bool(re.search(rf"agents-run\s+[\w-]+\s+{re.escape(stem)}\b", skill_md_text))


def agents_run_resolvable(kit: Path, skill: str, stem: str) -> bool:
    scripts_dir = kit / "skills" / skill / "scripts"
    return any((scripts_dir / f"{stem}{ext}").is_file() for ext in SCRIPT_EXTS)
