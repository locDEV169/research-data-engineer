-- Câu 4: Top 10 khách hàng theo tổng amount SUCCESS,
-- chỉ tính GD mà KH là chủ tài khoản nguồn (source_account_id).
-- Join: transactions → accounts → customers
-- Hiển thị: customer_code, full_name, tong_amount

SELECT
    c.customer_code,
    c.full_name,
    SUM(t.amount) AS tong_amount
FROM transactions AS t
INNER JOIN accounts AS a
    ON a.account_id = t.source_account_id
INNER JOIN customers AS c
    ON c.customer_id = a.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY c.customer_code, c.full_name
ORDER BY tong_amount DESC
LIMIT 10;
