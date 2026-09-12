"""FR1–FR3: 封筒・型検証・導出キーの拒否。素材は packages/circle-monthly-report/examples/."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from entex.errors import EnvelopeError, IRValidationError, PackageError
from entex.ir.loader import Envelope, ValidatedIR, load_and_validate
from tests.conftest import EXAMPLES_DIR, REPO_ROOT, load_example

VALID = sorted(p.name for p in (EXAMPLES_DIR / "valid").glob("*.json"))
INVALID = sorted(p.name for p in (EXAMPLES_DIR / "invalid").glob("*.json"))


def _messages(exc: IRValidationError) -> list[str]:
    return [i.message for i in exc.issues]


# --- FR1: 封筒 -------------------------------------------------------------


def test_envelope_mismatch_stops_before_content(packages_dir: Path) -> None:
    raw = load_example("invalid/06-envelope-mismatch.json")
    with pytest.raises(EnvelopeError) as ei:
        load_and_validate(raw, packages_dir)
    msg = ei.value.user_message
    assert "schema_version" in msg and "期待: 1" in msg and "実際: 2" in msg
    # 中身の 6 件（月の形式・日付・学籍番号…）は報告されない
    assert "報告対象月" not in msg and "学籍番号" not in msg


def test_envelope_content_errors_are_reported_once_version_matches(packages_dir: Path) -> None:
    raw = load_example("invalid/06-envelope-mismatch.json")
    raw["schema_version"] = 1
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    msgs = _messages(ei.value)
    assert len(msgs) == 6, msgs
    joined = "\n".join(msgs)
    for needle in ("報告対象月", "提出日", "学籍番号", "活動概要", "会計監査済み", "次月の予定"):
        assert needle in joined


def test_unknown_doc_type_is_an_envelope_error(packages_dir: Path) -> None:
    raw = load_example("valid/01-typical.json")
    raw["doc_type"] = "no-such-doc"
    with pytest.raises(EnvelopeError) as ei:
        load_and_validate(raw, packages_dir)
    assert "no-such-doc" in ei.value.user_message


@pytest.mark.parametrize("bad", ["../circle-monthly-report", "Circle", "a/b", ""])
def test_unsafe_doc_type_never_touches_the_filesystem(packages_dir: Path, bad: str) -> None:
    raw = load_example("valid/01-typical.json")
    raw["doc_type"] = bad
    with pytest.raises(EnvelopeError):
        load_and_validate(raw, packages_dir)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda r: r.pop("doc_type"),
        lambda r: r.pop("schema_version"),
        lambda r: r.pop("content"),
        lambda r: r.__setitem__("schema_version", "1"),
        lambda r: r.__setitem__("schema_version", True),
        lambda r: r.__setitem__("extra", 1),
    ],
)
def test_broken_envelope_shapes(packages_dir: Path, mutate) -> None:
    raw = load_example("valid/01-typical.json")
    mutate(raw)
    with pytest.raises(EnvelopeError):
        load_and_validate(raw, packages_dir)


def test_non_object_input_is_an_envelope_error(packages_dir: Path) -> None:
    with pytest.raises(EnvelopeError):
        load_and_validate(["not", "an", "object"], packages_dir)


# --- FR2: 型検証はまとめて返す -------------------------------------------------


@pytest.mark.parametrize("name", VALID)
def test_all_valid_examples_pass(packages_dir: Path, name: str) -> None:
    ir = load_and_validate(load_example(f"valid/{name}"), packages_dir)
    assert isinstance(ir, ValidatedIR)
    assert ir.package.slug == "circle-monthly-report"
    # 導出フィールドはまだ入っていない
    assert "income_total" not in ir.content


@pytest.mark.parametrize("name", INVALID)
def test_all_invalid_examples_fail(packages_dir: Path, name: str) -> None:
    with pytest.raises((EnvelopeError, IRValidationError)):
        load_and_validate(load_example(f"invalid/{name}"), packages_dir)


def test_two_errors_come_back_in_one_call(packages_dir: Path) -> None:
    raw = load_example("invalid/03-unknown-enum-and-negative-amount.json")
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    msgs = _messages(ei.value)
    assert len(msgs) == 2, msgs
    assert msgs[0] == "会計明細 1行目の区分は 収入 / 支出 のいずれかを選んでください"
    assert msgs[1] == "会計明細 2行目の金額は0以上で入力してください"
    assert ei.value.user_message.startswith("入力に2件の問題があります。")


def test_newline_in_text(packages_dir: Path) -> None:
    raw = load_example("invalid/02-newline-in-text.json")
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    assert _messages(ei.value) == ["団体名は1行で入力してください"]


def test_too_many_rows(packages_dir: Path) -> None:
    raw = load_example("invalid/04-too-many-rows.json")
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    assert _messages(ei.value) == ["活動実績は10行までです"]


def test_null_and_unknown_key(packages_dir: Path) -> None:
    raw = load_example("invalid/05-null-and-unknown-key.json")
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    msgs = _messages(ei.value)
    assert len(msgs) == 3, msgs
    assert "next_month_plans は使えない項目です（next_month_plan の間違い？）" in msgs
    assert "顧問は未入力ならキーごと省いてください（null は使えません）" in msgs
    assert "特記事項・所感は未入力ならキーごと省いてください（null は使えません）" in msgs


def test_messages_use_labels_not_field_names(packages_dir: Path) -> None:
    raw = load_example("valid/01-typical.json")
    raw["content"]["representative"]["student_id"] = "b23-01234"
    raw["content"]["members"]["enrolled"] = "24"
    raw["content"]["audited"] = "false"
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    msgs = _messages(ei.value)
    assert "代表者の学籍番号の形式が正しくありません" in msgs
    assert "会員数の在籍（月末時点）は整数で入力してください" in msgs
    assert "会計監査済みは真偽値（true / false）で入力してください" in msgs
    for m in msgs:
        assert "student_id" not in m and "enrolled" not in m


def test_missing_required_field(packages_dir: Path) -> None:
    raw = load_example("valid/02-minimal.json")
    del raw["content"]["organization"]
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    assert _messages(ei.value) == ["団体名は必須です"]


def test_text_is_nfc_normalized_and_defaults_applied(packages_dir: Path) -> None:
    raw = load_example("valid/02-minimal.json")
    decomposed = "ホ\u309aーカ\u3099ー"  # 半濁点・濁点を結合文字で
    raw["content"]["organization"] = decomposed
    ir = load_and_validate(raw, packages_dir)
    assert ir.content["organization"] == "ポーガー"
    assert ir.content["members"] == {"enrolled": 23, "joined": 0, "left": 0}


def test_max_length_and_pattern(packages_dir: Path) -> None:
    raw = load_example("valid/02-minimal.json")
    raw["content"]["organization"] = "あ" * 41
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    assert _messages(ei.value) == ["団体名は40文字以内で入力してください"]


def test_rich_text_shape_is_checked(packages_dir: Path) -> None:
    raw = load_example("valid/02-minimal.json")
    raw["content"]["summary"] = {
        "blocks": [
            {"type": "paragraph", "text": "ok"},
            {"type": "list", "items": ["a", 1]},
            {"type": "paragraph", "text": "x", "bold": True},
        ],
        "extra": 1,
    }
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    joined = "\n".join(_messages(ei.value))
    assert "活動概要の2番目のブロックの2項目は文字列で入力してください" in joined
    assert "'bold'" in joined and "'extra'" in joined


def test_month_and_date_validity(packages_dir: Path) -> None:
    raw = load_example("valid/02-minimal.json")
    raw["content"]["report_month"] = "2026-13"
    raw["content"]["submitted_on"] = "2026-02-30"
    raw["content"]["activities"] = [
        {"date": "2026/02/01", "category": "regular", "title": "x", "place": "y", "participants": 1}
    ]
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    msgs = _messages(ei.value)
    assert len(msgs) == 3, msgs
    assert msgs[0].startswith("報告対象月は YYYY-MM")
    assert msgs[1].startswith("提出日は YYYY-MM-DD")
    assert msgs[2].startswith("活動実績 1行目の日付は YYYY-MM-DD")


# --- FR3: 導出キーの拒否 -------------------------------------------------------


def test_derived_key_in_input_is_rejected(packages_dir: Path) -> None:
    raw = load_example("invalid/01-derived-key-in-input.json")
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(raw, packages_dir)
    assert _messages(ei.value) == [
        "収入合計は自動計算です。入力から外してください",
        "残高（次月繰越）は自動計算です。入力から外してください",
    ]


# --- パッケージ側の不備 ---------------------------------------------------------


def test_broken_package_schema_is_a_package_error(tmp_path: Path) -> None:
    pkg = tmp_path / "broken-doc"
    pkg.mkdir()
    (pkg / "schema.json").write_text("{not json", encoding="utf-8")
    raw = {"doc_type": "broken-doc", "schema_version": 1, "content": {}}
    with pytest.raises(PackageError) as ei:
        load_and_validate(raw, tmp_path)
    assert "broken-doc" in ei.value.user_message


def test_package_doc_type_must_match_directory(tmp_path: Path) -> None:
    schema = copy.deepcopy(
        json.loads(
            (REPO_ROOT / "packages/circle-monthly-report/schema.json").read_text(encoding="utf-8")
        )
    )
    pkg = tmp_path / "renamed-doc"
    pkg.mkdir()
    (pkg / "schema.json").write_text(json.dumps(schema), encoding="utf-8")
    raw = {"doc_type": "renamed-doc", "schema_version": 1, "content": {}}
    with pytest.raises(PackageError):
        load_and_validate(raw, tmp_path)


# --- schemas/ir との同期 --------------------------------------------------------


def test_envelope_json_schema_is_in_sync_with_pydantic_model() -> None:
    path = REPO_ROOT / "schemas" / "ir" / "envelope.schema.json"
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    assert on_disk == Envelope.model_json_schema(), (
        "schemas/ir/envelope.schema.json が entex.ir.loader.Envelope とずれている。"
        "`python -m entex.ir.loader` で再生成すること"
    )
