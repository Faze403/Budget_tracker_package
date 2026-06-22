# 실행 결과 요약

## 1. pytest 결과

실행 명령:

```powershell
.venv\Scripts\python.exe -m pytest tests
```

출력:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.13, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\User\Documents\GitHub\Budget_Tracker_Package
collected 13 items

tests\test_core.py .........                                             [ 69%]
tests\test_utils.py ....                                                 [100%]

============================= 13 passed in 0.10s =============================
```

## 2. pycodestyle 결과

실행 명령:

```powershell
.venv\Scripts\python.exe -m pycodestyle budget_tracker tests
```

출력:

```text
(출력 없음: 스타일 경고 없음)
```

## 3. doctest 결과

실행 명령:

```powershell
.venv\Scripts\python.exe -m doctest budget_tracker/core.py budget_tracker/subclass.py budget_tracker/utils.py
```

출력:

```text
(출력 없음: 모든 doctest 통과)
```

## 4. pip install 결과

실행 명령:

```powershell
python.exe -m pip install .
```

출력:

```text
Processing .\.
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Building wheels for collected packages: budget-tracker
  Building wheel for budget-tracker (pyproject.toml) ... done
  Created wheel for budget-tracker: filename=budget_tracker-0.1.0-py3-none-any.whl size=6120 sha256=37d2f435103d6f449a2547109fcafa7aee64f94b261b028d9640c5fdef1833eb
  Stored in directory: C:\Users\User\AppData\Local\Temp\pip-ephem-wheel-cache-10hey0so\wheels\08\91\d9\5f411a202937d7fa11e21ddcb64833fb2da4dd88d3d56d0672
Successfully built budget-tracker
Installing collected packages: budget-tracker
  Attempting uninstall: budget-tracker
    Found existing installation: budget-tracker 0.1.0
    Uninstalling budget-tracker-0.1.0:
      Successfully uninstalled budget-tracker-0.1.0
Successfully installed budget-tracker-0.1.0
```

설치 확인:

```powershell
.venv\Scripts\python.exe -m pip show budget-tracker
```

```text
Name: budget-tracker
Version: 0.1.0
Summary: Track income, expenses, and monthly budget summaries.
Author: PARK SEOJIN
Author-email: cockatoo@kku.ac.kr
```

## 5. 간단 실행 확인

실행 명령:

```powershell
.venv\Scripts\python.exe -c "from budget_tracker import BudgetTracker; tracker=BudgetTracker(); tracker.add_income('2026-06-20',300000,'용돈','이번 달 용돈'); tracker.add_expense('2026-06-21',10000,'교통','버스카드 충전'); print(tracker.calculate_balance())"
```

출력:

```text
290000
```
