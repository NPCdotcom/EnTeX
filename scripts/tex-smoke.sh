#!/bin/sh
# Compile the smoke fixture with LuaLaTeX via latexmk. Exit non-zero if no PDF appears.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SRC="$ROOT/tests/fixtures/smoke.tex"
OUT="${ENTEX_SMOKE_OUT:-$ROOT/out/smoke}"

mkdir -p "$OUT"
latexmk -lualatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$OUT" "$SRC" >"$OUT/latexmk.log" 2>&1 || {
  echo "tex-smoke: FAIL (see $OUT/latexmk.log)" >&2
  tail -n 40 "$OUT/latexmk.log" >&2
  exit 1
}

PDF="$OUT/smoke.pdf"
[ -s "$PDF" ] || { echo "tex-smoke: FAIL — no PDF at $PDF" >&2; exit 1; }
echo "tex-smoke: OK -> $PDF ($(wc -c <"$PDF") bytes)"
