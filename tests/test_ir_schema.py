"""doc-package の schema.json を読む側の検査（想定どおりでないパッケージで落ちること）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from entex.errors import PackageError
from entex.ir.schema import FieldDef, Schema
from entex.packages import load_package
from tests.conftest import PACKAGES_DIR


def _base_schema(**fields: Any) -> dict[str, Any]:
    return {"doc_type": "t-doc", "schema_version": 1, "title": "T", "fields": fields}


def _rows() -> dict[str, Any]:
    return {
        "type": "row_list",
        "label": "明細",
        "fields": {
            "category": {
                "type": "enum",
                "label": "区分",
                "options": [{"value": "a", "label": "A"}, {"value": "b", "label": "B"}],
            },
            "amount": {"type": "money", "label": "金額", "minimum": 0},
        },
    }


def test_real_package_schema_loads() -> None:
    pkg = load_package(PACKAGES_DIR, "circle-monthly-report")
    assert pkg.schema.doc_type == "circle-monthly-report"
    assert pkg.schema.derived_names == [
        "activity_count",
        "participants_total",
        "income_total",
        "expense_total",
        "balance",
    ]
    assert pkg.template_path.name == "template.tex.j2"


def test_forward_reference_in_expr_is_rejected() -> None:
    schema = _base_schema(
        total={"type": "money", "label": "合計", "derived": True, "expr": {"add": ["x", 1]}},
        x={"type": "money", "label": "x"},
    )
    with pytest.raises(ValidationError, match="後方"):
        Schema.model_validate(schema)


def test_self_reference_in_expr_is_rejected() -> None:
    schema = _base_schema(
        total={"type": "money", "label": "合計", "derived": True, "expr": {"add": ["total", 1]}},
    )
    with pytest.raises(ValidationError, match="後方"):
        Schema.model_validate(schema)


def test_sum_target_must_be_numeric_column() -> None:
    schema = _base_schema(
        rows=_rows(),
        t={"type": "money", "label": "t", "derived": True, "expr": {"sum": "rows.category"}},
    )
    with pytest.raises(ValidationError, match="integer / money"):
        Schema.model_validate(schema)


def test_where_key_must_be_a_column() -> None:
    schema = _base_schema(
        rows=_rows(),
        t={
            "type": "money",
            "label": "t",
            "derived": True,
            "expr": {"sum": "rows.amount", "where": {"kind": "a"}},
        },
    )
    with pytest.raises(ValidationError, match="where"):
        Schema.model_validate(schema)


def test_optional_numeric_reference_needs_default() -> None:
    schema = _base_schema(
        x={"type": "integer", "label": "x", "required": False},
        t={"type": "integer", "label": "t", "derived": True, "expr": {"add": ["x", 1]}},
    )
    with pytest.raises(ValidationError, match="default"):
        Schema.model_validate(schema)


@pytest.mark.parametrize(
    "expr",
    [
        {},
        {"sum": "a.b", "count": "a"},
        {"where": {"x": 1}},
        {"sum": "nodot"},
        {"sub": [1]},
        {"add": [1]},
    ],
)
def test_expr_shape(expr: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        FieldDef.model_validate({"type": "money", "label": "t", "derived": True, "expr": expr})


@pytest.mark.parametrize(
    "fdef",
    [
        {"type": "enum", "label": "e"},
        {"type": "object", "label": "o"},
        {"type": "list", "label": "l"},
        {"type": "list", "label": "l", "items": {"type": "money"}},
        {
            "type": "row_list",
            "label": "r",
            "fields": {"o": {"type": "object", "label": "o", "fields": {"x": {"type": "text"}}}},
        },
        {"type": "text", "label": "t", "derived": True},
        {"type": "text", "label": "t", "expr": {"count": "x"}},
        {"type": "text", "label": "t", "minimum": 0},
        {"type": "integer", "label": "i", "max_length": 3},
        {"type": "text", "label": "t", "unknown_attr": 1},
        {"type": "text", "label": "t", "pattern": "("},
    ],
)
def test_field_shape_is_checked(fdef: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        FieldDef.model_validate(fdef)


def test_integer_minimum_defaults_to_zero_and_can_be_removed() -> None:
    assert FieldDef.model_validate({"type": "integer", "label": "i"}).effective_minimum == 0
    assert FieldDef.model_validate({"type": "money", "label": "m"}).effective_minimum is None
    assert (
        FieldDef.model_validate(
            {"type": "integer", "label": "i", "minimum": None}
        ).effective_minimum
        is None
    )
    assert (
        FieldDef.model_validate({"type": "integer", "label": "i", "minimum": 5}).effective_minimum
        == 5
    )


def test_object_depth_is_limited_to_two() -> None:
    too_deep = {
        "type": "object",
        "label": "a",
        "fields": {
            "b": {
                "type": "object",
                "label": "b",
                "fields": {
                    "c": {"type": "object", "label": "c", "fields": {"d": {"type": "text"}}}
                },
            }
        },
    }
    with pytest.raises(ValidationError, match="深さ"):
        FieldDef.model_validate(too_deep)


def test_load_package_reports_schema_problems_in_japanese(tmp_path: Path) -> None:
    pkg = tmp_path / "bad-doc"
    pkg.mkdir()
    schema = {
        "doc_type": "bad-doc",
        "schema_version": 1,
        "title": "x",
        "fields": {"e": {"type": "enum", "label": "E"}},
    }
    (pkg / "schema.json").write_text(json.dumps(schema), encoding="utf-8")
    with pytest.raises(PackageError) as ei:
        load_package(tmp_path, "bad-doc")
    assert "options" in ei.value.user_message
    assert "Value error" not in ei.value.user_message
