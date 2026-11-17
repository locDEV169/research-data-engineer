-- Câu 9 (optional): Mỗi ngày trong 30 ngày gần nhất:
-- số giao dịch + tổng giá trị.
-- Dùng cột nghiệp vụ transaction_time (không dùng created_at/updated_at).

SELECT
    DATE(transaction_time) AS ngay,
    COUNT(*) AS so_giao_dich,
    SUM(amount) AS tong_gia_tri
FROM transactions
WHERE transaction_time >= (CURRENT_TIMESTAMP - INTERVAL '30 days')
GROUP BY DATE(transaction_time)
ORDER BY ngay;
