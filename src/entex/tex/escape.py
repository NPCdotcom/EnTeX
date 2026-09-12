"""利用者の文字列を TeX 安全な形にする（FR5）。

`escape_text` は文字単位の置換だけを行う純粋関数。`escape_content` はスキーマを辿り、
`text` / `rich_text` の値 **だけ** をエスケープする（数値・日付・enum の値は触らない。
それらの見せ方は doc-package 側の責務。ir-type-vocabulary.md §5）。
"""

from __future__ import annotations

from typing import Any

from entex.ir.schema import FieldDef, Schema

# 1 回の str.translate で同時に置換するので、置換結果の中の `\` や `{}` が再置換されることはない。
TEX_ESCAPES: dict[str, str] = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
    "'": r"\textquotesingle{}",
    '"': r"\textquotedbl{}",
    "`": r"\textasciigrave{}",
    "|": r"\textbar{}",
}

_TRANSLATION = str.maketrans(TEX_ESCAPES)


def escape_text(s: str) -> str:
    """TeX の特殊文字をすべて制御綴りに置き換える。改行は含まない前提（`text` 型の規則）。"""
    return s.translate(_TRANSLATION)


def escape_content(content: dict[str, Any], schema: Schema) -> dict[str, Any]:
    """`content`（導出値込みでよい）の文字列値をエスケープした **新しい** dict を返す。"""
    return _escape_fields(content, schema.fields)


def _escape_fields(value: dict[str, Any], fields: dict[str, FieldDef]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, raw in value.items():
        fdef = fields.get(key)
        out[key] = _escape_value(raw, fdef) if fdef is not None else raw
    return out


def _escape_value(raw: Any, fdef: FieldDef) -> Any:
    t = fdef.type
    if t == "text":
        return escape_text(raw) if isinstance(raw, str) else raw
    if t == "rich_text" and isinstance(raw, dict):
        return {"blocks": [_escape_block(b) for b in raw.get("blocks", [])]}
    if t == "object" and isinstance(raw, dict):
        return _escape_fields(raw, fdef.fields or {})
    if t == "row_list" and isinstance(raw, list):
        return [_escape_fields(row, fdef.fields or {}) for row in raw]
    if t == "list" and isinstance(raw, list) and fdef.items is not None:
        return [_escape_value(item, fdef.items) for item in raw]
    return raw


def _escape_block(block: dict[str, Any]) -> dict[str, Any]:
    if block.get("type") == "paragraph":
        return {"type": "paragraph", "text": escape_text(str(block.get("text", "")))}
    return {"type": "list", "items": [escape_text(str(i)) for i in block.get("items", [])]}
