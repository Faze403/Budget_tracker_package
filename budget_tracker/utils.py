"""budget_tracker 패키지의 보조 함수"""

from datetime import datetime


def format_tagged_summary(transaction_type, summary_text):
    """거래 종류가 붙은 요약 문자열을 만든다.

    :param transaction_type: 거래 종류 문자열
    :param summary_text: 기본 요약 문자열
    :return: 거래 종류가 붙은 요약 문자열
    >>> format_tagged_summary("수입", "2026-06-20 | 용돈 | 300000 | 이번 달 용돈")
    '[수입] 2026-06-20 | 용돈 | 300000 | 이번 달 용돈'
    """
    if not isinstance(transaction_type, str):
        raise TypeError("transaction_type must be a string.")

    if not isinstance(summary_text, str):
        raise TypeError("summary_text must be a string.")

    normalized_type = transaction_type.strip()
    normalized_summary = summary_text.strip()

    if not normalized_type:
        raise ValueError("transaction_type must not be empty.")

    if not normalized_summary:
        raise ValueError("summary_text must not be empty.")

    return f"[{normalized_type}] {normalized_summary}"


def filter_transactions_by_month(transactions, year_month):
    """지정한 달에 속하는 거래만 골라 반환한다.

    :param transactions: 거래 객체 목록
    :param year_month: YYYY-MM 형식의 연월 문자열
    :return: 해당 달의 거래 객체 목록
    """
    if not isinstance(transactions, list):
        raise TypeError("transactions must be a list.")

    if not isinstance(year_month, str):
        raise TypeError("year_month must be a string in YYYY-MM format.")

    try:
        datetime.strptime(year_month, "%Y-%m")
    except ValueError as exc:
        raise ValueError("year_month must use YYYY-MM format.") from exc

    return [
        transaction
        for transaction in transactions
        if transaction.matches_month(year_month)
    ]


def calculate_category_totals(transactions):
    """카테고리별 금액 합계를 계산한다.

    :param transactions: 거래 객체 목록
    :return: 카테고리별 금액 합계 딕셔너리
    """
    if not isinstance(transactions, list):
        raise TypeError("transactions must be a list.")

    totals = {}
    for transaction in transactions:
        if not hasattr(transaction, "category") or not hasattr(
            transaction,
            "signed_amount",
        ):
            raise TypeError(
                "transactions must contain transaction-like objects."
            )

        totals[transaction.category] = (
            totals.get(transaction.category, 0) + transaction.signed_amount()
        )

    return totals
