"""封筒の検証 → doc-package の解決 → `content` の型検証（FR1–FR3）。

入力は「JSON をパースした後の値」だけを受け取る。ファイルを読む役は CLI（将来は API）が持ち、
ここは IR がどこから来たかを知らない（charter §8）。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

from entex.errors import EnvelopeError, IRValidationError
from entex.ir.schema import SLUG_RE
from entex.ir.validate import validate_content
from entex.packages import DocPackage, PackageNotFoundError, load_package


class Envelope(BaseModel):
    """IR の封筒（ir-type-vocabulary.md §6.1）。`schemas/ir/envelope.schema.json` の正本。"""

    model_config = ConfigDict(
        extra="forbid",
        title="EnTeX IR envelope",
        json_schema_extra={
            "description": "IR がどの文書種のどの版のスキーマに従うかを自己申告する封筒。"
            "content の形は packages/<doc_type>/schema.json が決める。"
        },
    )

    doc_type: Annotated[
        str,
        Field(pattern=SLUG_RE.pattern, description="パッケージのスラッグ。packages/<slug>/ と一致"),
    ]
    schema_version: Annotated[int, Field(ge=1, description="パッケージの schema.json の版")]
    content: dict[str, Any] = Field(description="中身。schema.json の fields に従う")


@dataclass(frozen=True, slots=True)
class ValidatedIR:
    """検証を通った IR。`content` は正規化済み（NFC・default 補完）で導出値はまだ含まない。"""

    doc_type: str
    schema_version: int
    package: DocPackage
    content: dict[str, Any]


def load_and_validate(raw: Any, packages_dir: Path) -> ValidatedIR:
    """封筒 → パッケージ → 中身の順に検証する。

    Raises:
        EnvelopeError: 封筒が不正・不一致（中身は見ない。FR1）
        PackageError: パッケージは存在するが壊れている（作者向け）
        IRValidationError: 中身に 1 件以上の問題（まとめて返す。FR2・FR3）
    """
    doc_type, schema_version, content = _split_envelope(raw)

    try:
        package = load_package(packages_dir, doc_type)
    except PackageNotFoundError as exc:
        raise EnvelopeError(exc.user_message) from exc

    expected = package.schema.schema_version
    if schema_version != expected:
        raise EnvelopeError(
            "文書の版（schema_version）が一致しません"
            f"（期待: {expected}、実際: {schema_version}）。"
        )

    normalized, issues = validate_content(content, package.schema)
    if issues:
        raise IRValidationError(issues)
    return ValidatedIR(
        doc_type=doc_type,
        schema_version=schema_version,
        package=package,
        content=normalized,
    )


def _split_envelope(raw: Any) -> tuple[str, int, Any]:
    if not isinstance(raw, dict):
        raise EnvelopeError(
            '入力はオブジェクト（{ "doc_type": ..., "content": { ... } }）である必要があります。'
        )

    unknown = sorted(set(raw) - set(Envelope.model_fields))
    if unknown:
        raise EnvelopeError(
            "封筒に使えないキーがあります: "
            + ", ".join(unknown)
            + "（使えるのは doc_type / schema_version / content）。"
        )

    doc_type = raw.get("doc_type")
    if not isinstance(doc_type, str) or not doc_type:
        raise EnvelopeError("文書の種類（doc_type）がありません。")
    if not SLUG_RE.match(doc_type):
        raise EnvelopeError(f"文書の種類 '{doc_type}' には対応していません。")

    schema_version = raw.get("schema_version")
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise EnvelopeError("文書の版（schema_version）は整数で指定してください。")

    if "content" not in raw:
        raise EnvelopeError("中身（content）がありません。")
    return doc_type, schema_version, raw["content"]


def envelope_json_schema_text() -> str:
    """`schemas/ir/envelope.schema.json` の中身。pydantic モデルが正本（AGENTS.md 規約）。"""
    import json

    return json.dumps(Envelope.model_json_schema(), ensure_ascii=False, indent=2) + "\n"


if __name__ == "__main__":  # pragma: no cover - 手動再生成用
    target = Path(__file__).resolve().parents[3] / "schemas" / "ir" / "envelope.schema.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(envelope_json_schema_text(), encoding="utf-8")
    print(target)
