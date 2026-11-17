-- Câu 6 (optional): Số khách hàng theo từng customer_segment.
-- Sắp xếp giảm dần theo số lượng.

SELECT
    customer_segment,
    COUNT(*) AS so_luong
FROM customers
GROUP BY customer_segment
ORDER BY so_luong DESC;
