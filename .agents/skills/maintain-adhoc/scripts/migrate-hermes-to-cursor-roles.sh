#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-$HOME/.agents}"
cd "$ROOT"
while IFS= read -r -d '' f; do
  sed -i \
    -e 's/hermes-role-execute/role-execute/g' \
    -e 's/hermes\.kit_maintainer/kit_maintainer/g' \
    -e 's/hermes\.spec_designer/spec_designer/g' \
    -e 's/hermes\.plan_slicer/plan_slicer/g' \
    -e 's/hermes\.builder/builder/g' \
    -e 's/hermes\.hotfixer/hotfixer/g' \
    -e 's/hermes\.reviewer/reviewer/g' \
    -e 's/hermes\.evaluator/evaluator/g' \
    -e 's/hermes\.automator/automator/g' \
    -e 's/hermes\.router/router/g' \
    "$f"
done < <(find . -type f \( -name '*.md' -o -name '*.mdc' -o -name '*.yaml' -o -name '*.yml' -o -name '*.template' -o -name '*.json' \) \
  ! -path './hermes-skill-bundles/*' \
  ! -path './skills/hermes-role-execute/*' \
  ! -path './docs/HERMES_*' -print0)
echo "replace done"
