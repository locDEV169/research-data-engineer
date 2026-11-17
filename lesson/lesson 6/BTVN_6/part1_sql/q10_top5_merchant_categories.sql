-- Câu 10 (optional): Top 5 ngành hàng (merchant_category)
-- có tổng giá trị giao dịch SUCCESS lớn nhất.

SELECT
    m.merchant_category,
    SUM(t.amount) AS tong_gia_tri
FROM transactions AS t
INNER JOIN merchants AS m
    ON m.merchant_id = t.merchant_id
WHERE t.status = 'SUCCESS'
GROUP BY m.merchant_category
ORDER BY tong_gia_tri DESC
LIMIT 5;
