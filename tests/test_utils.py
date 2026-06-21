import pytest

from budget_tracker import (
    Expense,
    Income,
    calculate_category_totals,
    filter_transactions_by_month,
    format_tagged_summary,
)


def test_format_tagged_summary_returns_tagged_string():
    summary_text = "2026-06-20 | 용돈 | 300000 | 이번 달 용돈"

    assert (
        format_tagged_summary(" 수입 ", summary_text)
        == "[수입] 2026-06-20 | 용돈 | 300000 | 이번 달 용돈"
    )


def test_format_tagged_summary_rejects_blank_input():
    with pytest.raises(ValueError):
        format_tagged_summary(" ", "2026-06-20 | 용돈 | 300000 | 이번 달 용돈")

    with pytest.raises(ValueError):
        format_tagged_summary("수입", " ")


def test_filter_transactions_and_calculate_category_totals():
    transactions = [
        Income("2026-06-20", 300000, "용돈", "이번 달 용돈"),
        Expense("2026-06-21", 10000, "교통", "버스카드 충전"),
        Expense("2026-07-03", 5000, "간식", "편의점"),
    ]

    june_transactions = filter_transactions_by_month(transactions, "2026-06")

    assert len(june_transactions) == 2
    assert calculate_category_totals(june_transactions) == {
        "용돈": 300000,
        "교통": -10000,
    }


def test_utils_reject_invalid_input_types():
    with pytest.raises(TypeError):
        filter_transactions_by_month("거래 목록 아님", "2026-06")

    with pytest.raises(ValueError):
        filter_transactions_by_month([], "2026/06")

    with pytest.raises(TypeError):
        calculate_category_totals(["거래 객체 아님"])
