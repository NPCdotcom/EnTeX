#!/usr/bin/env bash
# Create .cursor/ symlinks to .agents/ for Cursor IDE compatibility.
set -euo pipefail

ROOT="$(cd "${1:-.}" && pwd)"
AGENTS_SUB="$ROOT/.agents"

if [[ -d "$ROOT/skills" ]]; then
  AGENTS_DIR="$ROOT"
else
  AGENTS_DIR="$AGENTS_SUB"
fi

if [[ ! -d "$AGENTS_DIR/skills" ]]; then
  echo "Cannot find .agents kit (skills/ missing)" >&2
  exit 1
fi

CURSOR_DIR="$ROOT/.cursor"
mkdir -p "$CURSOR_DIR"

link_dir() {
  local name="$1"
  local target="$AGENTS_DIR/$name"
  local link="$CURSOR_DIR/$name"
  if [[ ! -d "$target" ]]; then
    echo "Skip $name — missing $target"
    return
  fi
  if [[ -e "$link" ]]; then
    echo "Exists: $link"
    return
  fi
  ln -s "../.agents/$name" "$link" 2>/dev/null || ln -s "$target" "$link"
  echo "Linked: $link -> $target"
}

for d in rules skills hooks; do
  link_dir "$d"
done

if [[ -f "$AGENTS_DIR/hooks.json" ]]; then
  cp "$AGENTS_DIR/hooks.json" "$CURSOR_DIR/hooks.json"
  echo "Copied hooks.json"
fi

echo "Done. See docs/CURSOR_COMPAT.md"
