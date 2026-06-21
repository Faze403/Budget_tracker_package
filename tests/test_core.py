import pytest

from budget_tracker import BudgetTracker, Expense, Income, Transaction


def test_transaction_stores_valid_data_and_common_methods():
    transaction = Transaction(
        date="2026-06-19",
        amount=9000,
        category=" 식비 ",
        description=" 점심 ",
    )

    assert transaction.date == "2026-06-19"
    assert transaction.amount == 9000
    assert transaction.signed_amount() == 9000
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


def test_budget_tracker_adds_transactions_and_calculates_balance():
    tracker = BudgetTracker()

    income = tracker.add_income("2026-06-20", 300000, "용돈", "이번 달 용돈")
    expense = tracker.add_expense("2026-06-21", 10000, "교통", "버스카드 충전")

    assert isinstance(income, Income)
    assert isinstance(expense, Expense)
    assert tracker.get_transactions() == [income, expense]
    assert tracker.calculate_balance() == 290000
    assert tracker.category_totals() == {"용돈": 300000, "교통": -10000}


def test_budget_tracker_filters_month_and_builds_report():
    tracker = BudgetTracker()
    tracker.add_income("2026-06-20", 300000, "용돈", "이번 달 용돈")
    tracker.add_expense("2026-06-21", 10000, "교통", "버스카드 충전")
    tracker.add_income("2026-07-01", 50000, "용돈", "7월 용돈")

    june_transactions = tracker.get_transactions_by_month("2026-06")
    june_report = tracker.monthly_report("2026-06")

    assert len(june_transactions) == 2
    assert tracker.calculate_balance("2026-06") == 290000
    assert tracker.category_totals("2026-06") == {"용돈": 300000, "교통": -10000}
    assert "2026-06 월간 리포트" in june_report
    assert "거래 수: 2건" in june_report
    assert "잔액: 290000원" in june_report
    assert "- 교통: -10000원" in june_report
    assert "- 용돈: 300000원" in june_report
    assert "[수입] 2026-06-20 | 용돈 | 300000 | 이번 달 용돈" in june_report
    assert "2026-07-01" not in june_report


def test_budget_tracker_rejects_non_transaction_input():
    tracker = BudgetTracker()

    with pytest.raises(TypeError):
        tracker.add_transaction("거래 아님")
