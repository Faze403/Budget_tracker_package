import pytest

from budget_tracker import Expense, Income, Transaction


def test_transaction_stores_valid_data_and_common_methods():
    transaction = Transaction(
        date="2026-06-19",
        amount=9000,
        category=" 식비 ",
        description=" 점심 ",
    )

    assert transaction.date == "2026-06-19"
    assert transaction.amount == 9000
    assert transaction.category == "식비"
    assert transaction.description == "점심"
    assert transaction.matches_month("2026-06") is True
    assert transaction.matches_month("2026-07") is False
    assert transaction.to_dict() == {
        "date": "2026-06-19",
        "amount": 9000,
        "category": "식비",
        "description": "점심",
    }
    assert transaction.summary() == "2026-06-19 | 식비 | 9000 | 점심"


def test_transaction_rejects_invalid_date_and_amount():
    with pytest.raises(ValueError):
        Transaction(date="2026/06/19", amount=9000, category="식비")

    with pytest.raises(TypeError):
        Transaction(date="2026-06-19", amount="9000", category="식비")

    with pytest.raises(ValueError):
        Transaction(date="2026-06-19", amount=0, category="식비")

    with pytest.raises(ValueError):
        Transaction(date="2026-06-19", amount=9000.5, category="식비")


def test_income_uses_parent_validation_and_positive_signed_amount():
    income = Income(
        date="2026-06-20",
        amount=3200000,
        category=" 급여 ",
        description=" 6월 월급 ",
    )

    assert isinstance(income, Transaction)
    assert income.transaction_type() == "수입"
    assert income.signed_amount() == 3200000
    assert income.category == "급여"
    assert income.description == "6월 월급"
    assert income.to_dict() == {
        "date": "2026-06-20",
        "amount": 3200000,
        "category": "급여",
        "description": "6월 월급",
        "type": "수입",
    }
    assert income.summary() == "[수입] 2026-06-20 | 급여 | 3200000 | 6월 월급"


def test_expense_uses_parent_validation_and_negative_signed_amount():
    expense = Expense(
        date="2026-06-21",
        amount=10000,
        category=" 교통 ",
        description=" 버스카드 충전 ",
    )

    assert isinstance(expense, Transaction)
    assert expense.transaction_type() == "지출"
    assert expense.signed_amount() == -10000
    assert expense.category == "교통"
    assert expense.description == "버스카드 충전"
    assert expense.to_dict() == {
        "date": "2026-06-21",
        "amount": 10000,
        "category": "교통",
        "description": "버스카드 충전",
        "type": "지출",
    }
    assert expense.summary() == "[지출] 2026-06-21 | 교통 | 10000 | 버스카드 충전"
