#!/usr/bin/env python3
"""Cursor preCompact hook — set nav.yaml pressure before auto-summarize."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_nav_path() -> Path | None:
    cwd = Path.cwd()
    candidates = [
        cwd / ".agents" / "memory" / "state" / "nav.yaml",
        cwd / ".cursor" / "memory" / "state" / "nav.yaml",  # legacy
        cwd / "memory" / "state" / "nav.yaml",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def patch_section(lines: list[str], section: str, updates: dict[str, str]) -> list[str]:
    in_section = False
    section_indent = 0
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == f"{section}:":
            in_section = True
            section_indent = len(line) - len(line.lstrip())
            out.append(line)
            continue
        if in_section and line and not line[0].isspace():
            in_section = False
        if in_section and stripped and not stripped.startswith("#"):
            indent = line[: len(line) - len(line.lstrip())]
            key = stripped.split(":", 1)[0]
            if key in updates:
                out.append(f"{indent}{key}: {updates[key]}")
                continue
        out.append(line)
    return out


def append_signal(lines: list[str], signal: str) -> list[str]:
    out: list[str] = []
    in_pressure = False
    for line in lines:
        stripped = line.strip()
        if stripped == "pressure:":
            in_pressure = True
            out.append(line)
            continue
        if in_pressure and stripped == "signals: []":
            out.append("  signals:")
            out.append(f'    - "{signal}"')
            in_pressure = False
            continue
        if in_pressure and stripped.startswith("signals:") and stripped != "signals: []":
            out.append(line)
            if stripped == "signals:":
                out.append(f'    - "{signal}"')
            in_pressure = False
            continue
        if in_pressure and line and not line[0].isspace():
            out.append("  signals:")
            out.append(f'    - "{signal}"')
            in_pressure = False
        out.append(line)
    return out


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    nav = find_nav_path()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pct = payload.get("context_usage_percent", payload.get("contextUsagePercent", "?"))
    trigger = payload.get("trigger", "auto")
    signal = f"preCompact:{trigger}:ctx={pct}:{ts}"

    if nav:
        text = nav.read_text(encoding="utf-8")
        lines = text.splitlines()
        lines = patch_section(
            lines,
            "pressure",
            {
                "level": "pre_compact",
                "pre_compact_recommended": "true",
                "reanchor_required": "true",
            },
        )
        lines = append_signal(lines, signal)
        lines = patch_section(lines, "verification", {"chat_vs_file_delta": "pre_compact_pending"})
        nav.write_text("\n".join(lines) + "\n", encoding="utf-8")

        memory_root = nav.parent.parent  # .../memory
        history_dir = memory_root / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        log = history_dir / f"compaction-{ts[:10]}.log"
        with log.open("a", encoding="utf-8") as f:
            f.write(f"{ts} preCompact trigger={trigger} ctx={pct}\n")

        audit_dir = memory_root / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_log = audit_dir / "audit-log.md"
        if not audit_log.is_file():
            audit_log.write_text(
                "# Audit log\n\nAppend-only.\n\n---\n\n",
                encoding="utf-8",
            )
        with audit_log.open("a", encoding="utf-8") as f:
            f.write(
                f"\n## {ts} · preCompact\n\n"
                f"- event: preCompact\n"
                f"- trigger: {trigger}\n"
                f"- context_usage_percent: {pct}\n"
                f"- nav_pressure: pre_compact\n"
                f"- enforcement: hook\n"
            )

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
