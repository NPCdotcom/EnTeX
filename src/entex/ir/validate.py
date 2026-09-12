"""`content` を `schema.json` の型と属性に従って検証する（FR2・FR3）。

方針（plan `ir-validate-and-derive` 案2）: 語彙は 11 型で閉じているので、型ごとの検証関数で
スキーマを辿る。エラーは見つかった分をすべて集めて返し、文言はフィールドの `label` を使った
日本語にする。戻り値の content は NFC 正規化と `default` の補完を済ませた **新しい** dict で、
キーの並びはスキーマの宣言順に揃える。
"""

from __future__ import annotations

import datetime as _dt
import difflib
import re
import unicodedata
from typing import Any

from entex.errors import FieldIssue
from entex.ir.schema import FieldDef, Schema

MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RICH_TEXT_BLOCK_TYPES = ("paragraph", "list")

_TYPE_WORD = {
    "text": "文字列",
    "month": "文字列（YYYY-MM）",
    "date": "文字列（YYYY-MM-DD）",
    "integer": "整数",
    "money": "整数（円）",
    "enum": "文字列（選択肢の値）",
    "boolean": "真偽値（true / false）",
    "object": "オブジェクト（{ ... }）",
    "row_list": "配列（[ ... ]）",
    "list": "配列（[ ... ]）",
    "rich_text": 'オブジェクト（{ "blocks": [ ... ] }）',
}


def validate_content(content: Any, schema: Schema) -> tuple[dict[str, Any], list[FieldIssue]]:
    """検証して `(正規化済み content, 問題の一覧)` を返す。問題が空なら合格。"""
    walker = _Walker(schema)
    if not isinstance(content, dict):
        walker.issue("content", "content はオブジェクト（{ ... }）で入力してください")
        return {}, walker.issues
    normalized = walker.object_like(content, schema.fields, path="", label_prefix="", top=True)
    return normalized, walker.issues


class _Walker:
    def __init__(self, schema: Schema) -> None:
        self.schema = schema
        self.issues: list[FieldIssue] = []

    def issue(self, path: str, message: str) -> None:
        self.issues.append(FieldIssue(path=path, message=message))

    # -- 複合 -------------------------------------------------------------

    def object_like(
        self,
        value: dict[str, Any],
        fields: dict[str, FieldDef],
        *,
        path: str,
        label_prefix: str,
        top: bool,
    ) -> dict[str, Any]:
        out: dict[str, Any] = {}
        derived_names = set(self.schema.derived_names) if top else set()

        for key in value:
            if key in fields and key not in derived_names:
                continue
            key_path = _join(path, key)
            if key in derived_names:
                label = fields[key].label or key
                self.issue(key_path, f"{label}は自動計算です。入力から外してください")
                continue
            candidates = [n for n in fields if n not in derived_names]
            hint = difflib.get_close_matches(key, candidates, n=1, cutoff=0.6)
            suffix = f"（{hint[0]} の間違い？）" if hint else ""
            self.issue(key_path, f"{key} は使えない項目です{suffix}")

        for name, fdef in fields.items():
            if fdef.derived:
                continue
            label = _compose(label_prefix, fdef.label or name)
            key_path = _join(path, name)
            if name not in value:
                if fdef.required:
                    self.issue(key_path, f"{label}は必須です")
                elif fdef.has_default:
                    out[name] = fdef.default
                continue
            raw = value[name]
            if raw is None:
                if fdef.required:
                    self.issue(key_path, f"{label}は必須です（null は使えません）")
                else:
                    self.issue(
                        key_path, f"{label}は未入力ならキーごと省いてください（null は使えません）"
                    )
                continue
            out[name] = self.value(raw, fdef, path=key_path, label=label)
        return out

    def value(self, raw: Any, fdef: FieldDef, *, path: str, label: str) -> Any:
        t = fdef.type
        if t in ("text", "month", "date", "enum"):
            if not isinstance(raw, str):
                self.type_issue(path, label, fdef)
                return raw
            return getattr(self, f"scalar_{t}")(raw, fdef, path=path, label=label)
        if t in ("integer", "money"):
            if isinstance(raw, bool) or not isinstance(raw, int):
                self.type_issue(path, label, fdef)
                return raw
            return self.scalar_number(raw, fdef, path=path, label=label)
        if t == "boolean":
            if not isinstance(raw, bool):
                self.type_issue(path, label, fdef)
            return raw
        if t == "object":
            if not isinstance(raw, dict):
                self.type_issue(path, label, fdef)
                return raw
            return self.object_like(
                raw, fdef.fields or {}, path=path, label_prefix=label, top=False
            )
        if t == "row_list":
            return self.row_list(raw, fdef, path=path, label=label)
        if t == "list":
            return self.plain_list(raw, fdef, path=path, label=label)
        if t == "rich_text":
            return self.rich_text(raw, fdef, path=path, label=label)
        raise AssertionError(f"unknown type {t}")  # pragma: no cover - schema 側で弾く

    def row_list(self, raw: Any, fdef: FieldDef, *, path: str, label: str) -> Any:
        if not isinstance(raw, list):
            self.type_issue(path, label, fdef)
            return raw
        self.check_count(len(raw), fdef, path=path, label=label, unit="行")
        rows = []
        for i, row in enumerate(raw):
            row_path = f"{path}[{i}]"
            row_label = f"{label} {i + 1}行目"
            if not isinstance(row, dict):
                self.issue(row_path, f"{row_label}はオブジェクト（{{ ... }}）で入力してください")
                rows.append(row)
                continue
            rows.append(
                self.object_like(
                    row, fdef.fields or {}, path=row_path, label_prefix=row_label, top=False
                )
            )
        return rows

    def plain_list(self, raw: Any, fdef: FieldDef, *, path: str, label: str) -> Any:
        if not isinstance(raw, list):
            self.type_issue(path, label, fdef)
            return raw
        self.check_count(len(raw), fdef, path=path, label=label, unit="件")
        item_def = fdef.items
        assert item_def is not None
        items = []
        for i, item in enumerate(raw):
            item_path = f"{path}[{i}]"
            item_label = f"{label}の{i + 1}件目"
            if item is None:
                self.issue(item_path, f"{item_label}が null です。要素を削るか値を入れてください")
                items.append(item)
                continue
            items.append(self.value(item, item_def, path=item_path, label=item_label))
        return items

    def rich_text(self, raw: Any, fdef: FieldDef, *, path: str, label: str) -> Any:
        if not isinstance(raw, dict):
            self.type_issue(path, label, fdef)
            return raw
        for key in raw:
            if key != "blocks":
                self.issue(
                    _join(path, key), f"{label}に使えないキー '{key}' があります（blocks のみ）"
                )
        blocks = raw.get("blocks")
        if not isinstance(blocks, list):
            self.issue(_join(path, "blocks"), f"{label}は blocks の配列で入力してください")
            return raw
        out_blocks = []
        for i, block in enumerate(blocks):
            block_path = f"{path}.blocks[{i}]"
            block_label = f"{label}の{i + 1}番目のブロック"
            out_blocks.append(self.rich_text_block(block, path=block_path, label=block_label))
        return {"blocks": out_blocks}

    def rich_text_block(self, block: Any, *, path: str, label: str) -> Any:
        if not isinstance(block, dict):
            self.issue(path, f"{label}はオブジェクト（{{ ... }}）で入力してください")
            return block
        btype = block.get("type")
        if btype not in RICH_TEXT_BLOCK_TYPES:
            self.issue(
                _join(path, "type"),
                f"{label}の種別は paragraph / list のいずれかです（実際: {btype!r}）",
            )
            return block
        allowed = {"type", "text"} if btype == "paragraph" else {"type", "items"}
        for key in block:
            if key not in allowed:
                self.issue(_join(path, key), f"{label}に使えないキー '{key}' があります")
        if btype == "paragraph":
            text = block.get("text")
            if not isinstance(text, str):
                self.issue(_join(path, "text"), f"{label}の text は文字列で入力してください")
                return block
            return {"type": "paragraph", "text": self.text_value(text, path=path, label=label)}
        items = block.get("items")
        if not isinstance(items, list):
            self.issue(_join(path, "items"), f"{label}の items は配列で入力してください")
            return block
        out_items = []
        for j, item in enumerate(items):
            item_label = f"{label}の{j + 1}項目"
            if not isinstance(item, str):
                self.issue(f"{path}.items[{j}]", f"{item_label}は文字列で入力してください")
                out_items.append(item)
                continue
            out_items.append(self.text_value(item, path=f"{path}.items[{j}]", label=item_label))
        return {"type": "list", "items": out_items}

    # -- スカラー -----------------------------------------------------------

    def scalar_text(self, raw: str, fdef: FieldDef, *, path: str, label: str) -> str:
        value = self.text_value(raw, path=path, label=label)
        if fdef.max_length is not None and len(value) > fdef.max_length:
            self.issue(path, f"{label}は{fdef.max_length}文字以内で入力してください")
        if fdef.pattern is not None and re.search(fdef.pattern, value) is None:
            self.issue(path, f"{label}の形式が正しくありません")
        return value

    def text_value(self, raw: str, *, path: str, label: str) -> str:
        """`text` 共通の規則: 1 行・制御文字なし・NFC 正規化（ir-type-vocabulary.md §2.6）。"""
        if "\n" in raw or "\r" in raw:
            self.issue(path, f"{label}は1行で入力してください")
        elif any(unicodedata.category(ch) == "Cc" for ch in raw):
            self.issue(path, f"{label}に制御文字は使えません")
        return unicodedata.normalize("NFC", raw)

    def scalar_month(self, raw: str, fdef: FieldDef, *, path: str, label: str) -> str:
        if not MONTH_RE.match(raw):
            self.issue(path, f"{label}は YYYY-MM の形式で入力してください（例: 2026-08）")
        return raw

    def scalar_date(self, raw: str, fdef: FieldDef, *, path: str, label: str) -> str:
        ok = bool(DATE_RE.match(raw))
        if ok:
            try:
                _dt.date.fromisoformat(raw)
            except ValueError:
                ok = False
        if not ok:
            self.issue(
                path,
                f"{label}は YYYY-MM-DD の形式の実在する日付で入力してください（例: 2026-08-03）",
            )
        return raw

    def scalar_enum(self, raw: str, fdef: FieldDef, *, path: str, label: str) -> str:
        if raw not in fdef.option_values:
            choices = " / ".join(fdef.option_labels.values())
            self.issue(path, f"{label}は {choices} のいずれかを選んでください")
        return raw

    def scalar_number(self, raw: int, fdef: FieldDef, *, path: str, label: str) -> int:
        minimum = fdef.effective_minimum
        if minimum is not None and raw < minimum:
            self.issue(path, f"{label}は{minimum}以上で入力してください")
        if fdef.maximum is not None and raw > fdef.maximum:
            self.issue(path, f"{label}は{fdef.maximum}以下で入力してください")
        return raw

    # -- 共通 ---------------------------------------------------------------

    def type_issue(self, path: str, label: str, fdef: FieldDef) -> None:
        self.issue(path, f"{label}は{_TYPE_WORD[fdef.type]}で入力してください")

    def check_count(self, n: int, fdef: FieldDef, *, path: str, label: str, unit: str) -> None:
        if fdef.max_items is not None and n > fdef.max_items:
            self.issue(path, f"{label}は{fdef.max_items}{unit}までです")
        if fdef.min_items is not None and n < fdef.min_items:
            self.issue(path, f"{label}は{fdef.min_items}{unit}以上入力してください")


def _join(path: str, key: str) -> str:
    return f"{path}.{key}" if path else key


def _compose(prefix: str, label: str) -> str:
    return f"{prefix}の{label}" if prefix else label
