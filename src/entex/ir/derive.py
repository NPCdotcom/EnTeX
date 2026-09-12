"""`schema.json` の `expr` を評価して導出フィールドを埋める（FR4）。

宣言順に評価する。参照先が前方にあることは `entex.ir.schema` がパッケージ読み込み時に
検査済みなので、ここで循環に出会うことはない（出会えば `DerivationError`）。
"""

from __future__ import annotations

from typing import Any

from entex.errors import DerivationError
from entex.ir.schema import Expr, Schema


def apply_derived(content: dict[str, Any], schema: Schema) -> dict[str, Any]:
    """導出値を足した **新しい** dict を返す。キーの並びはスキーマの宣言順。"""
    scope: dict[str, Any] = dict(content)
    for name, fdef in schema.fields.items():
        if not fdef.derived:
            continue
        assert fdef.expr is not None
        scope[name] = evaluate(fdef.expr, scope, owner=name)
    return {name: scope[name] for name in schema.fields if name in scope}


def evaluate(expr: Expr, scope: dict[str, Any], *, owner: str) -> int:
    match expr.op:
        case "count":
            assert expr.count is not None
            return len(_rows(scope, expr.count, owner=owner))
        case "sum":
            assert expr.sum is not None
            list_name, field_name = expr.sum.split(".", 1)
            total = 0
            for row in _rows(scope, list_name, owner=owner):
                if not _matches(row, expr.where):
                    continue
                total += _int(row.get(field_name), owner=owner, what=expr.sum)
            return total
        case "add":
            assert expr.add is not None
            return sum(_arg(a, scope, owner=owner) for a in expr.add)
        case "sub":
            assert expr.sub is not None
            left, right = expr.sub
            return _arg(left, scope, owner=owner) - _arg(right, scope, owner=owner)
    raise DerivationError(f"導出フィールド '{owner}' の式を評価できません。")  # pragma: no cover


def _arg(arg: str | int | Expr, scope: dict[str, Any], *, owner: str) -> int:
    if isinstance(arg, Expr):
        return evaluate(arg, scope, owner=owner)
    if isinstance(arg, bool):  # bool は int の部分型なので先に弾く
        raise DerivationError(f"導出フィールド '{owner}' の式に真偽値は使えません。")
    if isinstance(arg, int):
        return arg
    if arg not in scope:
        raise DerivationError(f"導出フィールド '{owner}' が参照する '{arg}' に値がありません。")
    return _int(scope[arg], owner=owner, what=arg)


def _rows(scope: dict[str, Any], name: str, *, owner: str) -> list[dict[str, Any]]:
    rows = scope.get(name, [])
    if not isinstance(rows, list):
        raise DerivationError(
            f"導出フィールド '{owner}' が参照する '{name}' は行の並びではありません。"
        )
    return rows


def _matches(row: dict[str, Any], where: dict[str, Any] | None) -> bool:
    if not where:
        return True
    return all(row.get(key) == expected for key, expected in where.items())


def _int(value: Any, *, owner: str, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise DerivationError(
            f"導出フィールド '{owner}' が参照する '{what}' は整数ではありません。"
        )
    return value
