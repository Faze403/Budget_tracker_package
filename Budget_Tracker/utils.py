"""budget_tracker 패키지의 보조 함수를 정의"""


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
