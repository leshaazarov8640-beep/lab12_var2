# Объяснение сложного кода: расчёт штрафов

## Исходный код (из `app/crud.py`)

```python
def calculate_fine(overdue_days, reader_category, daily_fine=0.50):
    fine = overdue_days * daily_fine
    if reader_category == "premium":
        fine *= 0.9
    elif reader_category == "student":
        fine = min(fine, 5.0)
        if fine > 0:
            fine -= 2.0
    return max(fine, 0.0)
```

## Как это работает (простым языком)

Функция рассчитывает размер штрафа за просрочку возврата книги:

1. **Базовая сумма** = количество дней просрочки × 0.50 ₽ (ежедневный тариф)
2. **Для премиум-читателей** — скидка 10% (умножаем на 0.9)
3. **Для студентов** — штраф не больше 5 ₽, и ещё вычитаем 2 ₽ льготы
4. **Финал** — штраф не может быть отрицательным (max с 0.0)

## Предлагаемые улучшения

1. **Вынести магические числа в константы** — DAILY_FINE_RATE, PREMIUM_DISCOUNT, STUDENT_CAP, STUDENT_DISCOUNT
2. **Добавить логирование** — записывать, кому и за что начислен штраф
3. **Параметризовать конфигурацию** — тарифы могут меняться, их стоит вынести в .env или БД
4. **Добавить проверку на отрицательный overdue_days** — если книга возвращена раньше срока, штрафовать не нужно
5. **Типизировать reader_category** — использовать Enum вместо строк ("premium", "student", "standard")

## Улучшенная версия

```python
from enum import Enum
from decimal import Decimal

class ReaderCategory(str, Enum):
    STANDARD = "standard"
    PREMIUM = "premium"
    STUDENT = "student"

DAILY_FINE_RATE = Decimal("0.50")
PREMIUM_DISCOUNT_RATE = Decimal("0.10")
STUDENT_FINE_CAP = Decimal("5.00")
STUDENT_DISCOUNT = Decimal("2.00")

def calculate_fine(
    overdue_days: int,
    reader_category: ReaderCategory,
    daily_fine: Decimal = DAILY_FINE_RATE,
) -> Decimal:
    if overdue_days <= 0:
        return Decimal("0.00")
    fine = Decimal(overdue_days) * daily_fine
    if reader_category == ReaderCategory.PREMIUM:
        fine *= Decimal(1) - PREMIUM_DISCOUNT_RATE
    elif reader_category == ReaderCategory.STUDENT:
        fine = min(fine, STUDENT_FINE_CAP)
        fine = max(fine - STUDENT_DISCOUNT, Decimal("0.00"))
    return max(fine, Decimal("0.00"))
```
