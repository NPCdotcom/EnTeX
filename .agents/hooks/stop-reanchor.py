#!/usr/bin/env python3
"""Cursor stop hook — Re-anchor followup when nav pre_compact flag set."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def find_nav_path() -> Path | None:
    cwd = Path.cwd()
    for rel in (
        ".agents/memory/state/nav.yaml",
        ".cursor/memory/state/nav.yaml",  # legacy
        "memory/state/nav.yaml",
    ):
        p = cwd / rel
        if p.is_file():
            return p
    return None


def read_scalar(nav_text: str, section: str, key: str) -> str | None:
    in_section = False
    for line in nav_text.splitlines():
        stripped = line.strip()
        if stripped == f"{section}:":
            in_section = True
            continue
        if in_section and line and not line[0].isspace():
            in_section = False
        if in_section and stripped.startswith(f"{key}:"):
            return stripped.split(":", 1)[1].strip()
    return None


REANCHOR_MSG = """Re-anchor ターン（preCompact 検知）— 以下のみ実行してください:
1. memory-reference: nav.yaml + project-state.yaml + active thread/plan のみ（探索・Edit 禁止）
2. nav-brief + chat vs file delta 1行
3. turn-brief（nav 正本）
4. 終端 L2 flush + memory-record（nav pressure クリア）
5. ユーザーへ新チャット推奨を1行"""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("{}")
        return 0

    status = payload.get("status", "completed")
    loop_count = payload.get("loop_count", payload.get("loopCount", 0))

    if status != "completed" or loop_count != 0:
        print("{}")
        return 0

    nav = find_nav_path()
    if not nav:
        print("{}")
        return 0

    text = nav.read_text(encoding="utf-8")
    pre_compact = read_scalar(text, "pressure", "pre_compact_recommended")
    reanchor = read_scalar(text, "pressure", "reanchor_required")

    if pre_compact in ("true", "True", "yes") or reanchor in ("true", "True", "yes"):
        out = json.dumps({"followup_message": REANCHOR_MSG}, ensure_ascii=False)
        sys.stdout.buffer.write(out.encode("utf-8"))
        return 0

    sys.stdout.buffer.write(b"{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
