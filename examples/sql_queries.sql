-- ============================================================
-- Аналитические SQL-запросы для системы управления библиотекой
-- ============================================================

-- 1. Топ-10 самых читаемых книг (по количеству выдач)
SELECT
    b.id,
    b.title,
    b.author,
    COUNT(c.id) AS checkout_count
FROM books b
LEFT JOIN checkouts c ON c.book_id = b.id
GROUP BY b.id, b.title, b.author
ORDER BY checkout_count DESC
LIMIT 10;

-- 2. Читатели с наибольшим количеством штрафов
SELECT
    r.id,
    r.name,
    r.email,
    COUNT(f.id) AS fine_count,
    SUM(f.amount) AS total_fines,
    SUM(CASE WHEN f.paid = 0 THEN f.amount ELSE 0 END) AS unpaid_fines
FROM readers r
JOIN checkouts c ON c.reader_id = r.id
JOIN fines f ON f.checkout_id = c.id
GROUP BY r.id, r.name, r.email
ORDER BY total_fines DESC
LIMIT 10;

-- 3. Книги, которые сейчас на руках (не возвращены)
SELECT
    b.title,
    b.author,
    r.name AS reader_name,
    c.checkout_date,
    JULIANDAY('now') - JULIANDAY(c.checkout_date) AS days_on_loan
FROM checkouts c
JOIN books b ON b.id = c.book_id
JOIN readers r ON r.id = c.reader_id
WHERE c.status = 'active' AND c.return_date IS NULL
ORDER BY days_on_loan DESC;

-- 4. Статистика по жанрам: среднее время до возврата
SELECT
    b.genre,
    COUNT(c.id) AS total_checkouts,
    AVG(JULIANDAY(c.return_date) - JULIANDAY(c.checkout_date)) AS avg_loan_days,
    MAX(JULIANDAY(c.return_date) - JULIANDAY(c.checkout_date)) AS max_loan_days
FROM checkouts c
JOIN books b ON b.id = c.book_id
WHERE c.return_date IS NOT NULL
GROUP BY b.genre
ORDER BY avg_loan_days DESC;

-- 5. Эффективность сбора штрафов (процент оплаченных)
SELECT
    SUM(CASE WHEN paid = 1 THEN amount ELSE 0 END) / SUM(amount) * 100 AS collection_rate,
    SUM(CASE WHEN paid = 0 THEN amount ELSE 0 END) AS outstanding_amount,
    COUNT(*) AS total_fines
FROM fines;
