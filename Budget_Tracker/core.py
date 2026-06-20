"""budget_tracker 패키지의 부모 클래스를 정의"""

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
        """거래 날짜가 지정한 연월과 일치하는지 확인한다.

        :param year_month: YYYY-MM 형식의 연월 문자열
        :return: 해당 월 거래이면 True, 아니면 False
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
