"""利用者の文字列を TeX 安全な形にする（FR5）。

`escape_text` は文字単位の置換だけを行う純粋関数。`escape_content` はスキーマを辿り、
`text` / `rich_text` / `document` の文字列 **だけ** をエスケープする（数値・日付・enum の値は
触らない。それらの見せ方は doc-package 側の責務。ir-type-vocabulary.md §5）。

`document` の例外は 2 つ（§2.8・§5）。`code` block の `text` は書かれたとおりに出すので触らない。
span の `href` は URL として生かす必要があるので `escape_text` ではなく `escape_href` を通す。
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


# URL の意味を変えずに TeX の引数へ置ける形。`%` `#` `&` は URL の区切りなので
# パーセントエンコードすると別の URL になってしまう。hyperref の `\url` / `\href` は引数の中の
# `\%` `\#` `\&` をその文字に戻すので、この 3 つだけは `\` を前置する（LuaLaTeX で確認済み）。
_HREF_BACKSLASHED: dict[str, str] = {"%": r"\%", "#": r"\#", "&": r"\&"}
# それ以外の TeX 特殊文字はパーセントエンコードする。`_` `~` は RFC 3986 の unreserved なので
# `%5F` `%7E` にしても同じ URL を指す。他は URL に生で書けない文字なので、元から不正か、
# 利用者が符号化し忘れた文字である
_HREF_PERCENT_ENCODED: frozenset[str] = frozenset(TEX_ESCAPES) - frozenset(_HREF_BACKSLASHED)


def escape_href(url: str) -> str:
    """span の `href` を TeX の引数に安全に置ける形にする。リンク先の URL は変わらない。"""
    out: list[str] = []
    for ch in url:
        if ch in _HREF_BACKSLASHED:
            out.append(_HREF_BACKSLASHED[ch])
        elif ch in _HREF_PERCENT_ENCODED or ch <= " " or ord(ch) > 0x7E:
            # urllib.parse.quote は `_` `~` を常に素通しするので、バイト列から自前で組む
            out.append("".join(rf"\%{b:02X}" for b in ch.encode("utf-8")))
        else:
            out.append(ch)
    return "".join(out)


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
    if t == "document" and isinstance(raw, dict):
        return _escape_document(raw)
    return raw


def _escape_block(block: dict[str, Any]) -> dict[str, Any]:
    if block.get("type") == "paragraph":
        return {"type": "paragraph", "text": escape_text(str(block.get("text", "")))}
    return {"type": "list", "items": [escape_text(str(i)) for i in block.get("items", [])]}


# --- document -----------------------------------------------------------------


def _escape_document(raw: dict[str, Any]) -> dict[str, Any]:
    sections = {
        key: {"blocks": [_escape_document_block(b) for b in sec.get("blocks", [])]}
        for key, sec in raw.get("sections", {}).items()
    }
    extras = [
        {
            # 臨時の節の見出しは利用者の入力なのでエスケープする（宣言節の見出しはスキーマの値で、
            # renderer が schema_context と同じ扱いで付ける）
            "heading": escape_text(str(sec.get("heading", ""))),
            "blocks": [_escape_document_block(b) for b in sec.get("blocks", [])],
        }
        for sec in raw.get("extra_sections", [])
    ]
    return {"sections": sections, "extra_sections": extras}


def _escape_document_block(block: dict[str, Any]) -> dict[str, Any]:
    btype = block.get("type")
    if btype == "heading":
        return {**block, "text": escape_text(str(block.get("text", "")))}
    if btype in ("paragraph", "quote"):
        return {**block, "spans": _escape_spans(block.get("spans", []))}
    if btype == "list":
        return {**block, "items": _escape_list_items(block.get("items", []))}
    if btype == "image":
        # `src` はファイル名として `\includegraphics` に渡るので `escape_text` は掛けない
        # （`_` を `\_` にすると別のファイルになる）。安全側は検証の `IMAGE_SRC_RE` が
        # 許可文字（英数字と `. _ / -`）に絞ることで守る
        out = dict(block)
        if "alt" in block:
            out["alt"] = escape_text(str(block["alt"]))
        return out
    # code: 書かれたとおりに出す唯一の block。lang は表示に使われ得るので触る
    out = dict(block)
    if "lang" in out:
        out["lang"] = escape_text(str(out["lang"]))
    return out


def _escape_spans(spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for span in spans:
        item = {**span, "text": escape_text(str(span.get("text", "")))}
        if "href" in span:
            item["href"] = escape_href(str(span["href"]))
        out.append(item)
    return out


def _escape_list_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for item in items:
        entry = {**item, "spans": _escape_spans(item.get("spans", []))}
        if "items" in item:
            entry["items"] = _escape_list_items(item["items"])
        out.append(entry)
    return out
