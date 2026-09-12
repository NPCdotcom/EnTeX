"""doc-package の `schema.json`（案1 形式）を表す pydantic モデル。

型の語彙とフィールド属性は docs/design/elements/ir-type-vocabulary.md §1・§3、
導出値の `expr` は同 §4 に従う。ここで弾かれるのは **パッケージ作者の誤り** であり、
利用者の入力の誤りは `entex.ir.validate` が扱う。
"""

from __future__ import annotations

import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FieldType = Literal[
    "text",
    "rich_text",
    "month",
    "date",
    "integer",
    "money",
    "enum",
    "boolean",
    "object",
    "row_list",
    "list",
    "document",
]

#: `document` の block の語彙（ir-type-vocabulary.md §2.8）。
#: パッケージは `blocks` 属性でこの部分集合を宣言する
DocumentBlockType = Literal["heading", "paragraph", "list", "quote", "code", "image"]
DOCUMENT_BLOCK_TYPES: tuple[str, ...] = ("heading", "paragraph", "list", "quote", "code", "image")
#: `list` block の入れ子の上限。LaTeX の itemize は 4 段までなので、
#: テンプレートが 1 段包む余地を残す
DOCUMENT_LIST_MAX_DEPTH = 3

SCALAR_TYPES: frozenset[str] = frozenset(
    {"text", "month", "date", "integer", "money", "enum", "boolean"}
)
NUMERIC_TYPES: frozenset[str] = frozenset({"integer", "money"})
LIST_ITEM_TYPES: frozenset[str] = frozenset({"text", "enum", "date", "integer"})
#: `document` でだけ意味を持つ属性。他の型に付いていたらパッケージ作者の誤り
DOCUMENT_ONLY_ATTRS: tuple[str, ...] = (
    "sections",
    "extra_sections",
    "blocks",
    "max_heading_level",
)

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FIELD_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class EnumOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]*$")]
    label: str


class Expr(BaseModel):
    """導出値の式。JSON の構造で書き、`sum` / `count` / `add` / `sub` のちょうど 1 つを持つ。"""

    model_config = ConfigDict(extra="forbid")

    sum: str | None = None
    where: dict[str, str | int | bool] | None = None
    count: str | None = None
    add: list[str | int | Expr] | None = None
    sub: list[str | int | Expr] | None = None

    @model_validator(mode="after")
    def _exactly_one_operator(self) -> Expr:
        ops = [op for op in ("sum", "count", "add", "sub") if getattr(self, op) is not None]
        if len(ops) != 1:
            raise ValueError("expr は sum / count / add / sub のうちちょうど 1 つを持つ")
        if self.where is not None and self.sum is None:
            raise ValueError("where は sum と一緒にだけ使える")
        if self.sum is not None and self.sum.count(".") != 1:
            raise ValueError("sum は '<row_list>.<field>' の形で書く")
        if self.add is not None and len(self.add) < 2:
            raise ValueError("add は 2 つ以上の引数を取る")
        if self.sub is not None and len(self.sub) != 2:
            raise ValueError("sub はちょうど 2 つの引数を取る")
        return self

    @property
    def op(self) -> str:
        for op in ("sum", "count", "add", "sub"):
            if getattr(self, op) is not None:
                return op
        raise AssertionError("unreachable: validated to have one operator")


class SectionDef(BaseModel):
    """`document` の節 1 つの宣言（ir-type-vocabulary.md §3 `sections`）。並びが出力の順序。"""

    model_config = ConfigDict(extra="forbid")

    key: Annotated[str, Field(pattern=FIELD_NAME_RE.pattern)]
    heading: str
    required: bool = True


class FieldDef(BaseModel):
    """フィールド 1 つの宣言。型と、型とは別軸の属性を持つ。"""

    model_config = ConfigDict(extra="forbid")

    type: FieldType
    label: str | None = None
    description: str | None = None
    required: bool = True
    default: str | int | bool | None = None
    derived: bool = False
    expr: Expr | None = None
    minimum: int | None = None
    maximum: int | None = None
    max_length: int | None = None
    min_items: int | None = None
    max_items: int | None = None
    pattern: str | None = None
    items: FieldDef | None = None
    fields: dict[str, FieldDef] | None = None
    options: list[EnumOption] | None = None
    # `document` 専用（§2.8・§3）
    sections: list[SectionDef] | None = None
    extra_sections: Literal["allow", "forbid"] = "forbid"
    blocks: list[DocumentBlockType] | None = None
    max_heading_level: Annotated[int, Field(ge=1)] = 2
    # 値の取り出し元。`data-import` が読むだけで、`src/entex/` は中身を解釈しない（§3）
    source: dict[str, str] | None = None

    @property
    def has_default(self) -> bool:
        return "default" in self.model_fields_set and self.default is not None

    @property
    def section_keys(self) -> list[str]:
        return [s.key for s in self.sections or []]

    @property
    def sections_by_key(self) -> dict[str, SectionDef]:
        return {s.key: s for s in self.sections or []}

    @property
    def effective_minimum(self) -> int | None:
        """`integer` は既定で 0 以上。`"minimum": null` を明示すると外れる。"""
        if "minimum" in self.model_fields_set:
            return self.minimum
        return 0 if self.type == "integer" else None

    @property
    def option_values(self) -> list[str]:
        return [o.value for o in self.options or []]

    @property
    def option_labels(self) -> dict[str, str]:
        return {o.value: o.label for o in self.options or []}

    @model_validator(mode="after")
    def _check_shape(self) -> FieldDef:
        t = self.type
        if t == "enum" and not self.options:
            raise ValueError("enum には options が必要")
        if t != "enum" and self.options is not None:
            raise ValueError("options は enum でだけ使える")
        if t in ("object", "row_list") and not self.fields:
            raise ValueError(f"{t} には fields が必要")
        if t not in ("object", "row_list") and self.fields is not None:
            raise ValueError("fields は object / row_list でだけ使える")
        if t == "list" and self.items is None:
            raise ValueError("list には items が必要")
        if t != "list" and self.items is not None:
            raise ValueError("items は list でだけ使える")
        if t == "list" and self.items is not None and self.items.type not in LIST_ITEM_TYPES:
            raise ValueError("list の要素の型は text / enum / date / integer のいずれか")
        if t == "row_list":
            for name, child in (self.fields or {}).items():
                if child.type not in SCALAR_TYPES:
                    raise ValueError(f"row_list の行 '{name}' はスカラーのみ")
        if t == "object":
            for name, child in (self.fields or {}).items():
                if child.type == "object":
                    for gname, grand in (child.fields or {}).items():
                        if grand.type not in SCALAR_TYPES:
                            raise ValueError(
                                f"object の深さは 2 まで（'{name}.{gname}' が深すぎる）"
                            )
                elif child.type not in SCALAR_TYPES:
                    raise ValueError(f"object の子 '{name}' はスカラーか object のみ")
        for name in list((self.fields or {}).keys()):
            if not FIELD_NAME_RE.match(name):
                raise ValueError(f"フィールド名 '{name}' は英小文字のスネークケースで書く")
        if t == "document":
            self._check_document_shape()
        else:
            for attr in DOCUMENT_ONLY_ATTRS:
                if attr in self.model_fields_set:
                    raise ValueError(f"{attr} は document でだけ使える")
        if self.source is not None and not self.source:
            raise ValueError("source は空にできない（付けないなら省く）")
        if self.derived:
            if self.expr is None:
                raise ValueError("derived: true には expr が必要")
            if t not in NUMERIC_TYPES:
                raise ValueError("導出フィールドの型は integer か money")
        elif self.expr is not None:
            raise ValueError("expr は derived: true のフィールドでだけ使える")
        if self.has_default and t not in SCALAR_TYPES:
            raise ValueError("default はスカラーでだけ使える")
        if self.has_default and self.derived:
            raise ValueError("導出フィールドに default は置けない")
        if self.max_length is not None and t != "text":
            raise ValueError("max_length は text でだけ使える")
        if self.pattern is not None:
            if t != "text":
                raise ValueError("pattern は text でだけ使える")
            try:
                re.compile(self.pattern)
            except re.error as exc:
                raise ValueError(f"pattern が正規表現として不正: {exc}") from exc
        if (self.minimum is not None or self.maximum is not None) and t not in NUMERIC_TYPES:
            raise ValueError("minimum / maximum は integer / money でだけ使える")
        if (self.min_items is not None or self.max_items is not None) and t not in (
            "row_list",
            "list",
        ):
            raise ValueError("min_items / max_items は row_list / list でだけ使える")
        return self

    def _check_document_shape(self) -> None:
        if not self.sections:
            raise ValueError("document には sections が必要")
        if not self.blocks:
            raise ValueError("document には blocks が必要")
        seen: set[str] = set()
        for sec in self.sections:
            if sec.key in seen:
                raise ValueError(f"sections のキー '{sec.key}' が重複している")
            seen.add(sec.key)
        if len(set(self.blocks)) != len(self.blocks):
            raise ValueError("blocks に同じ block が 2 回ある")


class Schema(BaseModel):
    """`schema.json` 全体。"""

    model_config = ConfigDict(extra="forbid")

    doc_type: Annotated[str, Field(pattern=SLUG_RE.pattern)]
    schema_version: Annotated[int, Field(ge=1)]
    title: str
    description: str | None = None
    fields: dict[str, FieldDef]

    @property
    def derived_names(self) -> list[str]:
        return [name for name, f in self.fields.items() if f.derived]

    @model_validator(mode="after")
    def _check_fields(self) -> Schema:
        if not self.fields:
            raise ValueError("fields が空")
        declared: dict[str, FieldDef] = {}
        for name, fdef in self.fields.items():
            if not FIELD_NAME_RE.match(name):
                raise ValueError(f"フィールド名 '{name}' は英小文字のスネークケースで書く")
            if fdef.label is None:
                raise ValueError(f"フィールド '{name}' に label が必要")
            if fdef.derived and fdef.expr is not None:
                _check_expr_refs(fdef.expr, declared, owner=name)
            declared[name] = fdef
        return self


def _check_expr_refs(expr: Expr, declared: dict[str, FieldDef], *, owner: str) -> None:
    """`expr` の参照先が「自分より前に宣言された適切な型のフィールド」であることを確かめる。

    宣言順に評価するので、前方参照と循環はここで一緒に弾ける（ir-type-vocabulary.md §4）。
    """

    def numeric_ref(name: str) -> None:
        target = declared.get(name)
        if target is None:
            raise ValueError(
                f"'{owner}' の expr が未宣言または後方のフィールド '{name}' を参照している"
            )
        if target.type not in NUMERIC_TYPES:
            raise ValueError(f"'{owner}' の expr が参照する '{name}' は integer / money ではない")
        if not target.derived and not target.required and not target.has_default:
            raise ValueError(
                f"'{owner}' の expr が参照する '{name}' は任意項目なので default が必要"
            )

    def row_list_ref(name: str) -> FieldDef:
        target = declared.get(name)
        if target is None:
            raise ValueError(
                f"'{owner}' の expr が未宣言または後方のフィールド '{name}' を参照している"
            )
        if target.type != "row_list":
            raise ValueError(f"'{owner}' の expr が参照する '{name}' は row_list ではない")
        return target

    match expr.op:
        case "count":
            assert expr.count is not None
            row_list_ref(expr.count)
        case "sum":
            assert expr.sum is not None
            list_name, field_name = expr.sum.split(".", 1)
            rows = row_list_ref(list_name)
            child = (rows.fields or {}).get(field_name)
            if child is None or child.type not in NUMERIC_TYPES:
                raise ValueError(
                    f"'{owner}' の sum の対象 '{expr.sum}' は row_list の integer / money 列でない"
                )
            for key in expr.where or {}:
                if key not in (rows.fields or {}):
                    raise ValueError(
                        f"'{owner}' の where のキー '{key}' は '{list_name}' の列ではない"
                    )
        case "add" | "sub":
            args: list[Any] = (expr.add if expr.op == "add" else expr.sub) or []
            for arg in args:
                if isinstance(arg, Expr):
                    _check_expr_refs(arg, declared, owner=owner)
                elif isinstance(arg, str):
                    numeric_ref(arg)
