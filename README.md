# budget_tracker

Python 프로그래밍 기말 프로젝트용 가계부 패키지입니다.

## 프로젝트 개요

`budget_tracker`는 일별 수입과 지출을 기록하고, 월별 거래를 모아 잔액과 카테고리별 금액 합계를 확인할 수 있는 Python 패키지입니다.
모든 금액은 원 단위 정수이며, 수입과 지출을 객체로 나누어 관리합니다.

GitHub 저장소: [https://github.com/Faze403/Budget_Tracker_Package](https://github.com/Faze403/Budget_Tracker_Package)

## 설치 방법

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install .
```

설치 후에는 `from budget_tracker import BudgetTracker` 형태로 바로 불러올 수 있습니다.

## 빠른 시작(quick start)

```python
from budget_tracker import BudgetTracker

tracker = BudgetTracker()
tracker.add_income("2026-06-20", 300000, "용돈", "이번 달 용돈")
tracker.add_expense("2026-06-21", 10000, "교통", "버스카드 충전")

print(tracker.calculate_balance())
print(tracker.category_totals("2026-06"))
print(tracker.monthly_report("2026-06"))
```

예시 결과:

```text
290000
{'용돈': 300000, '교통': -10000}
2026-06 월간 리포트
거래 수: 2건
잔액: 290000원
카테고리별 합계:
- 교통: -10000원
- 용돈: 300000원
거래 내역:
- [수입] 2026-06-20 | 용돈 | 300000 | 이번 달 용돈
- [지출] 2026-06-21 | 교통 | 10000 | 버스카드 충전
```

## 주요 기능 설명

현재 구현된 기능은 아래와 같습니다.

- 수입 거래 추가
- 지출 거래 추가
- 잔액 계산
- 카테고리별 금액 합계 계산
- 특정 달 거래 조회
- 월간 리포트 생성

## 테스트 실행 방법

```powershell
.venv\Scripts\python.exe -m pytest tests
.venv\Scripts\python.exe -m pycodestyle budget_tracker tests
.venv\Scripts\python.exe -m doctest budget_tracker/core.py budget_tracker/subclass.py budget_tracker/utils.py
```

## 작성자 정보

- **작성자**: 박서진 (PARK SEOJIN)
- **학번**: 202620859
- **이메일**: [cockatoo@kku.ac.kr](mailto:cockatoo@kku.ac.kr)
- **GitHub 저장소 URL**: [https://github.com/Faze403/Budget_Tracker_Package](https://github.com/Faze403/Budget_Tracker_Package)
