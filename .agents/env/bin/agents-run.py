#!/usr/bin/env python3
"""Dispatch skill scripts from .agents/env — single entry for agent Shell."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def find_kit_root() -> Path:
    env_bin = Path(__file__).resolve().parent
    candidate = env_bin.parent.parent
    if (candidate / "skills").is_dir():
        return candidate
    for base in (Path.cwd(), Path.cwd() / ".agents"):
        if (base / "skills").is_dir():
            return base.resolve()
    raise SystemExit("agents-run: kit root not found (expected skills/ directory)")


def resolve_python(kit: Path) -> Path:
    for rel in (
        "env/python/.venv/Scripts/python.exe",
        "env/python/.venv/bin/python",
    ):
        exe = kit / rel
        if exe.is_file():
            return exe
    return Path(sys.executable)


def resolve_script(kit: Path, skill: str, stem: str) -> Path | None:
    scripts_dir = kit / "skills" / skill / "scripts"
    for ext in (".py", ".ps1", ".sh"):
        path = scripts_dir / f"{stem}{ext}"
        if path.is_file():
            return path
    return None


def build_command(kit: Path, script: Path, args: list[str]) -> list[str]:
    if script.suffix == ".py":
        return [str(resolve_python(kit)), str(script), *args]
    if script.suffix == ".ps1":
        return [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            *args,
        ]
    return ["bash", str(script), *args]


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print(
            "Usage: agents-run <skill> <script-stem> [args...]\n"
            "Example: agents-run maintain-adhoc audit-skill-layout skills",
            file=sys.stderr,
        )
        return 2

    skill, stem, *args = argv
    kit = find_kit_root()
    script = resolve_script(kit, skill, stem)
    if not script:
        print(f"agents-run: script not found: skills/{skill}/scripts/{stem}.{{py,ps1,sh}}", file=sys.stderr)
        return 1

    cmd = build_command(kit, script, args)
    print(f"agents-run: {' '.join(cmd)}", file=sys.stderr)
    return subprocess.call(cmd, cwd=kit)


if __name__ == "__main__":
    raise SystemExit(main())
