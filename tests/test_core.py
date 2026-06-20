import pytest

from budget_tracker import Transaction


def test_transaction_stores_valid_data_and_common_methods():
    transaction = Transaction(
        date="2026-06-19",
        amount=9000,
        category=" 식비 ",
        description=" 점심 ",
    )

    assert transaction.date == "2026-06-19"
    assert transaction.amount == 9000.0
    assert transaction.category == "식비"
    assert transaction.description == "점심"
    assert transaction.matches_month("2026-06") is True
    assert transaction.matches_month("2026-07") is False
    assert transaction.to_dict() == {
        "date": "2026-06-19",
        "amount": 9000.0,
        "category": "식비",
        "description": "점심",
    }
    assert transaction.summary() == "2026-06-19 | 식비 | 9000.00 | 점심"


def test_transaction_rejects_invalid_date_and_amount():
    with pytest.raises(ValueError):
        Transaction(date="2026/06/19", amount=9000, category="식비")

    with pytest.raises(TypeError):
        Transaction(date="2026-06-19", amount="9000", category="식비")

    with pytest.raises(ValueError):
        Transaction(date="2026-06-19", amount=0, category="식비")
