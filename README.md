# Лабораторная работа №12: AI-ассистированная разработка

**Студент:** Азаров Алексей Семенович
**Группа:** 221331-01
**Вариант:** 2
**Тема:** Система управления библиотекой
**Сложность:** Средняя

## Описание

REST API для управления библиотечным каталогом книг. Реализовано с использованием FastAPI, SQLAlchemy, Pydantic. Все задания выполнены с применением AI-инструментов (vibe coding).

## Установка и запуск

### Локально

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up --build
```

Приложение будет доступно по адресу http://localhost:8000

## API-эндпоинты

### GET /api/v1/books
Получить список книг (с опциональным поиском).

**Параметры:**
- `skip` (int, optional) — сколько пропустить
- `limit` (int, optional, default=100) — сколько вернуть
- `search` (string, optional) — поиск по названию/автору/ISBN

**Ответ:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Война и мир",
    "author": "Лев Толстой",
    "isbn": "9783161484100",
    "published_year": 1869,
    "genre": "Роман",
    "quantity": 5,
    "available_quantity": 5
  }
]
```

### GET /api/v1/books/{id}
Получить книгу по ID.

**Ответ:** `200 OK` | `404 Not Found`

### POST /api/v1/books
Создать новую книгу.

**Тело запроса:**
```json
{
  "title": "Преступление и наказание",
  "author": "Фёдор Достоевский",
  "isbn": "9783161484108",
  "published_year": 1866,
  "genre": "Роман",
  "quantity": 3,
  "available_quantity": 3
}
```

**Ответ:** `201 Created` | `409 Conflict` (ISBN уже существует) | `422 Unprocessable Entity`

### PUT /api/v1/books/{id}
Обновить книгу (частичное обновление).

**Ответ:** `200 OK` | `404 Not Found`

### DELETE /api/v1/books/{id}
Удалить книгу.

**Ответ:** `204 No Content` | `404 Not Found`

## Переменные окружения (`.env`)

| Переменная | Значение по умолчанию | Описание |
|------------|-----------------------|----------|
| `DATABASE_URL` | `sqlite:///./library.db` | URL подключения к БД |
| `DEBUG` | `True` | Режим отладки |
| `MAX_FILE_SIZE_MB` | `10` | Максимальный размер файла (MB) |

## Задания

| № | Задание | Файл |
|---|---------|------|
| 1 | CRUD-приложение | `app/` |
| 2 | Модульные тесты | `tests/test_books.py` |
| 3 | Рефакторинг плохого кода | `examples/` |
| 4 | Docker-конфигурация | `Dockerfile`, `docker-compose.yml` |
| 5 | Объяснение сложного кода | `docs/code_explanation.md` |
| 6 | Документация | `README.md` |
| 7 | Миграции БД | `migrations/` |
| 8 | Поиск уязвимостей | `docs/security_audit.md` |
| 9 | SQL-запросы | `examples/sql_queries.sql` |
| 10 | Регулярное выражение | `examples/regex_validation.py` |
