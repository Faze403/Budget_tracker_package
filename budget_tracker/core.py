"""budget_tracker 패키지의 부모 클래스와 관리자 클래스를 정의"""

from budget_tracker.utils import (
    calculate_category_totals,
    filter_transactions_by_month,
)

from datetime import datetime


class Transaction:
    """단일 수입 또는 지출 거래를 나타낸다."""

    def __init__(self, date, amount, category, description=""):
        """거래 정보를 검증한 뒤 속성으로 저장한다.

        :param date: YYYY-MM-DD 형식의 날짜 문자열
        :param amount: 0보다 큰 거래 금액
        :param category: 거래 카테고리
        :param description: 선택 입력인 거래 설명
        """
        self.date = self._validate_date(date)
        self.amount = self._validate_amount(amount)
        self.category = self._normalize_category(category)
        self.description = self._validate_description(description)

    def _validate_date(self, date):
        """YYYY-MM-DD 형식의 날짜 문자열인지 검사한다."""

        if not isinstance(date, str):
            raise TypeError("date must be a string in YYYY-MM-DD format.")

        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("date must use YYYY-MM-DD format.") from exc

        return parsed_date.strftime("%Y-%m-%d")

    def _validate_amount(self, amount):
        """금액이 숫자이며 0보다 큰 정수 금액인지 검사한다."""

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("amount must be an int or float.")

        if amount <= 0:
            raise ValueError("amount must be greater than 0.")

        if isinstance(amount, float) and not amount.is_integer():
            raise ValueError("amount must be a whole number.")

        return int(amount)

    def _normalize_category(self, category):
        """카테고리 문자열을 검사하고 공백을 정리한다."""

        if not isinstance(category, str):
            raise TypeError("category must be a string.")

        normalized_category = category.strip()
        if not normalized_category:
            raise ValueError("category must not be empty.")

        return normalized_category

    def _validate_description(self, description):
        """설명 문자열을 검사하고 공백을 정리한다."""

        if not isinstance(description, str):
            raise TypeError("description must be a string.")

        return description.strip()

    def to_dict(self):
        """거래 데이터를 딕셔너리로 반환한다.

        :return: 거래 정보를 담은 딕셔너리
        """
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
        }

    def matches_month(self, year_month):
        """거래 날짜가 지정한 달과 일치하는지 확인한다.

        :param year_month: YYYY-MM 형식의 연월 문자열
        :return: 해당 달 거래이면 True, 아니면 False
        """
        if not isinstance(year_month, str):
            raise TypeError("year_month must be a string in YYYY-MM format.")

        try:
            datetime.strptime(year_month, "%Y-%m")
        except ValueError as exc:
            raise ValueError("year_month must use YYYY-MM format.") from exc

        return self.date.startswith(year_month)

    def summary(self):
        """거래 내용을 한 줄 요약 문자열로 반환한다.

        :return: 화면 표시용 요약 문자열
        >>> transaction = Transaction("2026-06-20", 9000, "식비", "점심")
        >>> transaction.summary()
        '2026-06-20 | 식비 | 9000 | 점심'
        """
        parts = [self.date, self.category, str(self.amount)]
        if self.description:
            parts.append(self.description)
        return " | ".join(parts)

    def signed_amount(self):
        """잔액 계산에 사용할 금액을 반환한다.

        :return: 기본 거래 금액
        """
        return self.amount


class BudgetTracker:
    """여러 거래를 저장하고 통계를 계산한다."""

    def __init__(self):
        """비어 있는 거래 목록으로 관리자 객체를 만든다."""
        self.transactions = []

    def add_transaction(self, transaction):
        """거래 객체를 목록에 추가한다.

        :param transaction: 추가할 거래 객체
        :return: 저장한 거래 객체
        """
        required_attrs = (
            "date",
            "amount",
            "category",
            "description",
            "summary",
            "signed_amount",
            "to_dict",
        )
        if not all(hasattr(transaction, attr) for attr in required_attrs):
            raise TypeError("transaction must be a Transaction-like object.")

        self.transactions.append(transaction)
        return transaction

    def add_income(self, date, amount, category, description=""):
        """수입 거래를 만들어 목록에 추가한다.

        :param date: YYYY-MM-DD 형식의 날짜 문자열
        :param amount: 0보다 큰 수입 금액
        :param category: 수입 카테고리
        :param description: 선택 입력인 수입 설명
        :return: 저장한 Income 객체
        """
        from budget_tracker.subclass import Income

        income = Income(date, amount, category, description)
        return self.add_transaction(income)

    def add_expense(self, date, amount, category, description=""):
        """지출 거래를 만들어 목록에 추가한다.

        :param date: YYYY-MM-DD 형식의 날짜 문자열
        :param amount: 0보다 큰 지출 금액
        :param category: 지출 카테고리
        :param description: 선택 입력인 지출 설명
        :return: 저장한 Expense 객체
        """
        from budget_tracker.subclass import Expense

        expense = Expense(date, amount, category, description)
        return self.add_transaction(expense)

    def get_transactions(self):
        """현재 저장된 거래 목록 복사본을 반환한다.

        :return: 거래 객체 목록
        """
        return list(self.transactions)

    def get_transactions_by_month(self, year_month):
        """지정한 달의 거래만 골라 반환한다.

        :param year_month: YYYY-MM 형식의 연월 문자열
        :return: 해당 달의 거래 객체 목록
        """
        return filter_transactions_by_month(self.transactions, year_month)

    def calculate_balance(self, year_month=None):
        """전체 또는 특정 달의 잔액을 계산한다.

        :param year_month: 선택 입력인 YYYY-MM 형식의 연월 문자열
        :return: 잔액 정수
        >>> tracker = BudgetTracker()
        >>> _ = tracker.add_income("2026-06-20", 300000, "용돈", "이번 달 용돈")
        >>> _ = tracker.add_expense("2026-06-21", 10000, "교통", "버스카드 충전")
        >>> tracker.calculate_balance()
        290000
        """
        transactions = self.transactions
        if year_month is not None:
            transactions = self.get_transactions_by_month(year_month)

        return sum(transaction.signed_amount() for transaction in transactions)

    def category_totals(self, year_month=None):
        """전체 또는 특정 달의 카테고리별 금액 합계를 계산한다.

        :param year_month: 선택 입력인 YYYY-MM 형식의 연월 문자열
        :return: 카테고리별 금액 합계 딕셔너리
        """
        transactions = self.transactions
        if year_month is not None:
            transactions = self.get_transactions_by_month(year_month)

        return calculate_category_totals(transactions)

    def monthly_report(self, year_month):
        """지정한 달의 텍스트 리포트를 만든다.

        :param year_month: YYYY-MM 형식의 연월 문자열
        :return: 월간 리포트 문자열
        """
        transactions = self.get_transactions_by_month(year_month)
        balance = self.calculate_balance(year_month)
        category_totals = self.category_totals(year_month)

        lines = [
            f"{year_month} 월간 리포트",
            f"거래 수: {len(transactions)}건",
            f"잔액: {balance}원",
        ]

        if category_totals:
            lines.append("카테고리별 합계:")
            for category, total in sorted(category_totals.items()):
                lines.append(f"- {category}: {total}원")
        else:
            lines.append("카테고리별 합계: 없음")

        if transactions:
            lines.append("거래 내역:")
            for transaction in transactions:
                lines.append(f"- {transaction.summary()}")
        else:
            lines.append("거래 내역: 없음")

        return "\n".join(lines)
