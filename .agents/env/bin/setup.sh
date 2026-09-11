#!/usr/bin/env bash
# Create agent env: Python venv + optional Node deps.
set -euo pipefail

KIT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY_DIR="$KIT_ROOT/env/python"
VENV="$PY_DIR/.venv"
REQ="$PY_DIR/requirements.txt"

echo "Kit: $KIT_ROOT"

if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
  echo "Created venv: $VENV"
fi

"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r "$REQ"

NODE_DIR="$KIT_ROOT/env/node"
if command -v npm >/dev/null 2>&1 && [[ -f "$NODE_DIR/package.json" ]]; then
  if python3 -c "import json; d=json.load(open('$NODE_DIR/package.json')); exit(0 if d.get('dependencies') else 1)"; then
    (cd "$NODE_DIR" && npm install)
    echo "Node deps installed"
  else
    echo "Node: no dependencies — skip npm install"
  fi
else
  echo "Node: skipped"
fi

echo "Done. Test: python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills"
