"""
Генерация регулярного выражения для валидации ISBN книги.

ISBN (International Standard Book Number) — международный уникальный номер книги.
Формат: 10 или 13 цифр, допускаются дефисы между группами.
"""

import re

ISBN_PATTERN = r"^(?:\d{9}[\dXx]|\d{13})$"


def validate_isbn(isbn: str) -> bool:
    cleaned = isbn.replace("-", "").replace(" ", "")
    return bool(re.match(ISBN_PATTERN, cleaned))


def main():
    test_cases = {
        "9783161484100": True,
        "0-306-40615-2": True,
        "978-0-306-40615-7": True,
        "3161484100": True,
        "12345": False,
        "97831614841001": False,
        "abcdefghij": False,
        "ISBN-978-0-306-40615-7": False,
    }

    print(f"Pattern: {ISBN_PATTERN}\n")
    for isbn, expected in test_cases.items():
        result = validate_isbn(isbn)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status} {isbn:30s} -> {result} (expected {expected})")


if __name__ == "__main__":
    main()
