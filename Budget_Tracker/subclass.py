"""budget_tracker 패키지의 하위 클래스를 정의"""

from budget_tracker.core import Transaction
from budget_tracker.utils import format_tagged_summary


class Income(Transaction):
    """수입 거래를 나타낸다."""

    def __init__(self, date, amount, category, description=""):
        """부모 클래스 검증을 재사용해 수입 거래를 만든다.

        :param date: YYYY-MM-DD 형식의 날짜 문자열
        :param amount: 0보다 큰 수입 금액
        :param category: 수입 카테고리
        :param description: 선택 입력인 수입 설명
        """
        super().__init__(date, amount, category, description)

    def transaction_type(self):
        """거래 종류 문자열을 반환한다.

        :return: 수입 거래를 나타내는 문자열
        """
        return "수입"

    def signed_amount(self):
        """잔액 계산에 사용할 금액을 반환한다.

        :return: 양수 수입 금액
        """
        return self.amount

    def to_dict(self):
        """거래 종류가 포함된 수입 데이터를 반환한다.

        :return: 수입 거래 딕셔너리
        """
        data = super().to_dict()
        data["type"] = self.transaction_type()
        return data

    def summary(self):
        """거래 종류가 포함된 수입 요약 문자열을 반환한다.

        :return: 화면 표시용 수입 요약 문자열
        >>> income = Income("2026-06-20", 300000, "용돈", "이번 달 용돈")
        >>> income.summary()
        '[수입] 2026-06-20 | 용돈 | 300000 | 이번 달 용돈'
        """
        return format_tagged_summary(
            self.transaction_type(),
            super().summary(),
        )


class Expense(Transaction):
    """지출 거래를 나타낸다."""

    def __init__(self, date, amount, category, description=""):
        """부모 클래스 검증을 재사용해 지출 거래를 만든다.

        :param date: YYYY-MM-DD 형식의 날짜 문자열
        :param amount: 0보다 큰 지출 금액
        :param category: 지출 카테고리
        :param description: 선택 입력인 지출 설명
        """
        super().__init__(date, amount, category, description)

    def transaction_type(self):
        """거래 종류 문자열을 반환한다.

        :return: 지출 거래를 나타내는 문자열
        """
        return "지출"

    def signed_amount(self):
        """잔액 계산에 사용할 금액을 반환한다.

        :return: 음수 지출 금액
        """
        return -self.amount

    def to_dict(self):
        """거래 종류가 포함된 지출 데이터를 반환한다.

        :return: 지출 거래 딕셔너리
        """
        data = super().to_dict()
        data["type"] = self.transaction_type()
        return data

    def summary(self):
        """거래 종류가 포함된 지출 요약 문자열을 반환한다.

        :return: 화면 표시용 지출 요약 문자열
        """
        return format_tagged_summary(
            self.transaction_type(),
            super().summary(),
        )
