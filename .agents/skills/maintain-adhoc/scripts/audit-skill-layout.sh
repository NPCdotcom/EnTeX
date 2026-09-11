#!/usr/bin/env bash
# Wrapper — canonical implementation: audit-skill-layout.py (via agents-run or direct).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ROOT="${1:-$KIT/skills}"
PY="${KIT}/env/python/.venv/bin/python"
if [[ ! -x "$PY" ]]; then PY=python3; fi
exec "$PY" "$SCRIPT_DIR/audit-skill-layout.py" "$ROOT"
