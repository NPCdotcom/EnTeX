"""FR4: 導出値の計算。期待値は packages/circle-monthly-report/README.md の正常系表。"""

from __future__ import annotations

from pathlib import Path

import pytest

from entex.errors import DerivationError
from entex.ir.derive import apply_derived, evaluate
from entex.ir.loader import load_and_validate
from entex.ir.schema import Expr
from tests.conftest import load_example

EXPECTED = {
    "01-typical.json": dict(
        activity_count=5,
        participants_total=77,
        income_total=138_000,
        expense_total=131_400,
        balance=19_400,
    ),
    "02-minimal.json": dict(
        activity_count=0, participants_total=0, income_total=0, expense_total=0, balance=5_400
    ),
    "03-deficit.json": dict(
        activity_count=2,
        participants_total=42,
        income_total=54_000,
        expense_total=78_200,
        balance=-4_800,
    ),
    "04-max-rows.json": dict(
        activity_count=10,
        participants_total=217,
        income_total=90_600,
        expense_total=44_800,
        balance=41_000,
    ),
    "05-fiscal-year-start.json": dict(
        activity_count=2,
        participants_total=34,
        income_total=71_500,
        expense_total=8_800,
        balance=62_700,
    ),
}


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_derived_values_match_readme(packages_dir: Path, name: str) -> None:
    ir = load_and_validate(load_example(f"valid/{name}"), packages_dir)
    derived = apply_derived(ir.content, ir.package.schema)
    for key, expected in EXPECTED[name].items():
        assert derived[key] == expected, (name, key)


def test_apply_derived_is_pure_and_schema_ordered(packages_dir: Path) -> None:
    ir = load_and_validate(load_example("valid/01-typical.json"), packages_dir)
    before = dict(ir.content)
    derived = apply_derived(ir.content, ir.package.schema)
    assert ir.content == before
    assert list(derived) == [n for n in ir.package.schema.fields if n in derived]
    # 導出フィールドは宣言位置に入る（activities の直後に activity_count）
    keys = list(derived)
    assert keys.index("activity_count") == keys.index("activities") + 1


def test_where_filters_on_equality() -> None:
    rows = [
        {"category": "income", "amount": 10},
        {"category": "expense", "amount": 3},
        {"category": "income", "amount": 5},
    ]
    scope = {"finance": rows}
    assert evaluate(Expr(sum="finance.amount"), scope, owner="t") == 18
    assert (
        evaluate(Expr(sum="finance.amount", where={"category": "income"}), scope, owner="t") == 15
    )
    assert evaluate(Expr(count="finance"), scope, owner="t") == 3
    assert evaluate(Expr(add=["a", 2, Expr(sub=[10, "a"])]), {"a": 4}, owner="t") == 12


def test_missing_reference_is_a_derivation_error() -> None:
    with pytest.raises(DerivationError):
        evaluate(Expr(add=["missing", 1]), {}, owner="t")
    with pytest.raises(DerivationError):
        evaluate(Expr(sum="rows.amount"), {"rows": [{"amount": "x"}]}, owner="t")
