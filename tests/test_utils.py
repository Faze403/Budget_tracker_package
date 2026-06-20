import pytest

from budget_tracker import format_tagged_summary


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
